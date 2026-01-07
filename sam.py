import asyncio
import random
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import *

app = Client(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH
)

TAG_RUNNING = False


async def log(text):
    try:
        await app.send_message(LOG_CHAT, text)
    except:
        pass


async def ensure_peer(chat_id):
    try:
        await app.get_chat(chat_id)
        return True
    except:
        return False


@app.on_message(filters.command("tagall") & filters.user(SUDO_USERS))
async def tagall(_, message):
    global TAG_RUNNING

    if TAG_RUNNING:
        return await message.reply("⚠️ Tag already running")

    if not await ensure_peer(TARGET_GROUP):
        return await message.reply(
            "❌ Target GC invalid ya userbot member nahi hai\n"
            "👉 Pehle GC me manually ek msg bhej"
        )

    TAG_RUNNING = True

    # 🔹 FIRST NORMAL MESSAGE
    await app.send_message(
        TARGET_GROUP,
        "🔔 Attention everyone\nPlease check 👇"
    )

    await asyncio.sleep(4)

    await message.reply("✅ TagAll Started (Custom Text Mode)")
    await log(f"▶️ TAGALL STARTED by {message.from_user.id}")

    # ===== TEXT SELECTION LOGIC =====
    custom_text = None

    # 1️⃣ Reply text
    if message.reply_to_message and message.reply_to_message.text:
        custom_text = message.reply_to_message.text.strip()

    # 2️⃣ /tagall ke baad ka text
    elif len(message.command) > 1:
        custom_text = " ".join(message.command[1:]).strip()

    words = TAG_WORDS.copy()

    try:
        async for member in app.get_chat_members(TARGET_GROUP):
            if not TAG_RUNNING:
                break

            user = member.user
            if user.is_bot or user.is_deleted:
                continue

            # 3️⃣ Fallback random word
            text = custom_text if custom_text else random.choice(words)

            try:
                await app.send_message(
                    TARGET_GROUP,
                    f"[{user.first_name}](tg://user?id={user.id}) {text}",
                    disable_web_page_preview=True
                )

                # 🐢 SAFE HUMAN SPEED
                await asyncio.sleep(random.uniform(3.5, 6.0))

            except FloodWait as e:
                await asyncio.sleep(e.value + 5)

            except Exception:
                continue

    finally:
        TAG_RUNNING = False
        await log("⏹️ TAGALL FINISHED")


@app.on_message(filters.command("stop") & filters.user(SUDO_USERS))
async def stop(_, message):
    global TAG_RUNNING

    TAG_RUNNING = False
    await message.reply("🛑 TagAll Stopped")
    await log(f"🛑 TAGALL STOPPED by {message.from_user.id}")


print("🔥 USERBOT RUNNING (CUSTOM TAG MODE)")
app.run()






