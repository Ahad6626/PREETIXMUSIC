import os
import time
import random
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from ShrutiMusic import app
from ShrutiMusic.misc import _boot_
from ShrutiMusic.plugins.sudo.sudoers import sudoers_list
from ShrutiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import help_pannel_page1, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✨ Constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

START_IMG_URL = os.getenv("START_IMG_URL", "https://files.catbox.moe/t16l3a.jpg")
EFFECT_ID = 5102134856319034135  # Your effect ID

RANDOM_STICKERS = [
    "CAACAgUAAxkBAAEPTt1oufwYNPajFHslWKT6a0WdOWlPuwACNxgAAlnaYFXtKE5Nj9mdqzYE",
    "CAACAgUAAxkBAAEPTt9oufwjhYeBaRrkGKa64KjqdpOkbgACcRgAAmY3YVXwdNH-3INmEDYE",
    "CAACAgUAAxkBAAEPTuFoufwloJgjOdEhsL0G4xGyhnrbKAAC-hUAAlimaVVRIEFcr6KXODYE",
    "CAACAgUAAxkBAAEPT7louuu9E18ko1ZT35AE77RYJQzBlgACghYAAvOpaVVCey_HotkCwDYE"
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 Start Command (Private)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    try:
        await message.react("👀")
    except:
        pass

    # Random sticker
    random_sticker = random.choice(RANDOM_STICKERS)
    try:
        stkr = await message.reply_sticker(
            sticker=random_sticker,
            message_effect_id=EFFECT_ID
        )
        await asyncio.sleep(3)
        await stkr.delete()
    except:
        pass

    await add_served_user(message.from_user.id)

    # Check for start parameters
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name.startswith("help"):
            keyboard = help_pannel_page1(_)
            await message.reply_photo(
                photo=START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                protect_content=True,
                has_spoiler=True,
                reply_markup=keyboard,
            )
            return
        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} checked <b>sudolist</b>.\n\n<b>User ID :</b> <code>{message.from_user.id}</code>\n<b>Username :</b> @{message.from_user.username}",
                )
            return
        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(text=_["S_B_8"], url=link),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_GROUP),
                ]]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail or START_IMG_URL,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} checked <b>track info</b>.\n\n<b>User ID :</b> <code>{message.from_user.id}</code>\n<b>Username :</b> @{message.from_user.username}",
                )
            return

    # Default start panel
    out = private_panel(_)
    UP, CPU, RAM, DISK = await bot_sys_stats()
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
        has_spoiler=True,
        reply_markup=InlineKeyboardMarkup(out),
    )
    if await is_on_off(2):
        await app.send_message(
            chat_id=config.LOG_GROUP_ID,
            text=f"{message.from_user.mention} started the bot.\n\n<b>User ID :</b> <code>{message.from_user.id}</code>\n<b>Username :</b> @{message.from_user.username}",
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 Start Command (Group)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    # Random sticker
    random_sticker = random.choice(RANDOM_STICKERS)
    try:
        await message.reply_sticker(sticker=random_sticker, message_effect_id=EFFECT_ID)
    except:
        pass

    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=START_IMG_URL,
        has_spoiler=True,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    await add_served_chat(message.chat.id)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 👋 Welcome New Chat Members
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                try:
                    await message.react("👀")
                except:
                    pass

                # Random sticker
                try:
                    random_sticker = random.choice(RANDOM_STICKERS)
                    stkr = await message.reply_sticker(sticker=random_sticker, message_effect_id=EFFECT_ID)
                    await asyncio.sleep(3)
                    await stkr.delete()
                except:
                    pass

                out = start_panel(_)
                await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    has_spoiler=True,
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print("WELCOME ERROR:", ex)