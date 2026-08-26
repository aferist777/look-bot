# -*- coding: utf-8 -*-
"""Telegram bot: colour analysis + celebrity-style fitting room -> BEST LOOK 4:5."""
import asyncio
import os
import sys
import time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (Message, CallbackQuery, FSInputFile,
                           InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto)
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

from colorist.intents import UPLOAD_MESSAGE
from colorist.pipeline import run_pipeline
from colorist.progress import Progress
from colorist.status import render_status
from colorist.stats import load_estimate
from colorist.catalog import CATALOG, BY_ID

BOT_WORK = os.path.join(ROOT, "bot", "_work")
THUMBS = os.path.join(ROOT, "catalog", "thumbs")
os.makedirs(BOT_WORK, exist_ok=True)

N = len(CATALOG)
USER = {}  # user_id -> {"mode": "analysis"|"style", "look": look_id}

WELCOME = (
    "👋 Welcome! I'm your personal colour analyst and stylist.\n\n"
    "Pick what you'd like:\n"
    "✨ My colour analysis — your natural 12-season breakdown from a selfie.\n"
    "💃 Try a look — try a curated style on your own face."
)

bot = Bot(token=os.environ["TG_BOT_TOKEN"])
dp = Dispatcher()


def menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ My colour analysis", callback_data="mode:analysis")],
        [InlineKeyboardButton(text="💃 Try a look", callback_data="looks:open")],
    ])


def carousel(i: int):
    look = CATALOG[i]
    path = os.path.join(THUMBS, f"{look['id']}.png")
    caption = f"{look['emoji']} {look['name']}\n{look['tagline']}\n\n({i + 1}/{N})"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀", callback_data=f"nav:{(i - 1) % N}"),
         InlineKeyboardButton(text="💃 Try this", callback_data=f"try:{look['id']}"),
         InlineKeyboardButton(text="▶", callback_data=f"nav:{(i + 1) % N}")],
        [InlineKeyboardButton(text="🏠 Menu", callback_data="menu")],
    ])
    return path, caption, kb


@dp.message(CommandStart())
async def on_start(m: Message):
    USER[m.from_user.id] = {"mode": "analysis", "look": None}
    await m.answer(WELCOME, reply_markup=menu_kb())


@dp.callback_query(F.data == "menu")
async def cb_menu(c: CallbackQuery):
    await c.message.answer(WELCOME, reply_markup=menu_kb())
    await c.answer()


@dp.callback_query(F.data == "mode:analysis")
async def cb_analysis(c: CallbackQuery):
    USER[c.from_user.id] = {"mode": "analysis", "look": None}
    await c.message.answer("✨ Colour analysis mode.\n\n" + UPLOAD_MESSAGE)
    await c.answer()


@dp.callback_query(F.data == "looks:open")
async def cb_looks(c: CallbackQuery):
    path, caption, kb = carousel(0)
    await c.message.answer_photo(FSInputFile(path), caption=caption, reply_markup=kb)
    await c.answer()


@dp.callback_query(F.data.startswith("nav:"))
async def cb_nav(c: CallbackQuery):
    i = int(c.data.split(":")[1])
    path, caption, kb = carousel(i)
    await c.message.edit_media(
        InputMediaPhoto(media=FSInputFile(path), caption=caption), reply_markup=kb)
    await c.answer()


@dp.callback_query(F.data.startswith("try:"))
async def cb_try(c: CallbackQuery):
    look_id = c.data.split(":", 1)[1]
    look = BY_ID.get(look_id)
    USER[c.from_user.id] = {"mode": "style", "look": look_id}
    await c.message.answer(
        f"{look['emoji']} Trying on **{look['name']}**.\n\n"
        "Send me a clear, front-facing selfie 📸 and I'll style you in this look.")
    await c.answer()


async def _animate(status: Message, progress: Progress, eta: float):
    tick = 0
    try:
        while True:
            try:
                await status.edit_text(render_status(progress, eta, tick))
            except Exception:
                pass
            tick += 1
            await asyncio.sleep(2.5)
    except asyncio.CancelledError:
        pass


@dp.message(F.photo)
async def on_photo(m: Message):
    stt = USER.get(m.from_user.id, {"mode": "analysis", "look": None})
    look = BY_ID.get(stt["look"]) if stt["mode"] == "style" else None
    intent = (m.caption or "").strip()

    progress = Progress()
    eta = load_estimate()
    status = await m.answer(render_status(progress, eta, 0))
    anim = asyncio.create_task(_animate(status, progress, eta))

    work = os.path.join(BOT_WORK, f"{m.from_user.id}_{int(time.time())}")
    os.makedirs(work, exist_ok=True)
    photo_path = os.path.join(work, "input.jpg")
    try:
        await bot.download(m.photo[-1], destination=photo_path)
        out, analysis = await asyncio.to_thread(
            run_pipeline, photo_path, intent, work, "2K", progress, look)
        if look:
            cap = f"{look['emoji']} {look['name']} — your try-on ✨"
        else:
            cap = f"Your BEST LOOK — {analysis['colortype']} ✨"
            if intent:
                cap += f'\nGoal: "{intent}"'
        anim.cancel()
        await m.answer_photo(FSInputFile(out), caption=cap)
    except Exception as e:
        anim.cancel()
        await m.answer(f"😔 Sorry, something went wrong:\n{type(e).__name__}: {e}")
    finally:
        anim.cancel()
        try:
            await status.delete()
        except Exception:
            pass


@dp.message(F.document)
async def on_document(m: Message):
    await m.answer("Please send the photo as a *photo*, not a file 📸")


@dp.message()
async def on_other(m: Message):
    await m.answer("Send /start to begin, or send me a selfie 📸")


async def main():
    me = await bot.get_me()
    print(f"Bot @{me.username} started. Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
