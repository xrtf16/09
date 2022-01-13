from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app
from Yukki.Database import blacklist_chat, blacklisted_chats, whitelist_chat

__MODULE__ = "Blacklist"
__HELP__ = """


/blacklistedchat 
- تحقق الدردشات المدرجة في القائمة السوداء من Bot.


**Note:**
Only for Sudo Users.


/القائمة السوداء دردشة [CHAT_ID] 
- قم بإدراج أي دردشة في القائمة السوداء من استخدام Music Bot


/قائمة بيضاء [CHAT_ID] 
-أضف إلى القائمة البيضاء أي دردشة في القائمة السوداء من استخدام Music Bot

"""


@app.on_message(filters.command("blacklistchat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**إستعمال:**\n/القائمة السوداء دردشة [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("Chat is already blacklisted.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "تم وضع الدردشة في القائمة السوداء بنجاح"
        )
    await message.reply_text("حدث خطأ ما ، تحقق من السجلات.")


@app.on_message(filters.command("whitelistchat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**إستعمال:**\n/قائمة بيضاء [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("الدردشة مدرجة بالفعل في القائمة البيضاء.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "تمت إضافة الدردشة إلى القائمة البيضاء بنجاح"
        )
    await message.reply_text("حدث خطأ ما ، تحقق من السجلات.")


@app.on_message(filters.command("blacklistedchat"))
async def blacklisted_chats_func(_, message: Message):
    text = "**الدردشات المدرجة في القائمة السوداء:**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("No الدردشات المدرجة في القائمة السوداء")
    else:
        await message.reply_text(text)
