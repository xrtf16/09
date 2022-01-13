import random

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import ASSISTANT_PREFIX, SUDOERS, app, random_assistant
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details

__MODULE__ = "Assistant"
__HELP__ = f"""


/checkassistant
- تحقق من المساعد المخصص للدردشة الخاصة بك


**Note:**
-فقط للمطورين

{ASSISTANT_PREFIX[0]}block [ الرد على رسالة المستخدم] 
- يحظر المستخدم من حساب المساعد.

{ASSISTANT_PREFIX[0]}unblock [ الرد على رسالة المستخدم] 
- يفتح المستخدم من حساب المساعد.

{ASSISTANT_PREFIX[0]}approve [ الرد على رسالة المستخدم] 
- يوافق على مستخدم DM.

{ASSISTANT_PREFIX[0]}disapprove [ الرد على رسالة المستخدم] 
- Disيوافق على مستخدم .

{ASSISTANT_PREFIX[0]}pfp [ الرد على الصورة] 
- تغييرات حساب مساعد PFP.

{ASSISTANT_PREFIX[0]}bio [نص السيرة الذاتية] 
- يغير السيرة الذاتية لحساب المساعد.

/changeassistant [ASS NUMBER]
- تغيير المساعد المخصص previoius إلى المساعد الجديد.

/setassistant [رقم  الحساب مساعد]
- قم بتعيين حساب مساعد للدردشة. 
"""


ass_num_list = ["1", "2", "3", "4", "5"]


@app.on_message(filters.command("changeassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"** طريقه استعمالي :**\n/changeassistant + رقم الحساب\n\nاختر منهم\n{' | '.join(ass_num_list)}"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    num = message.text.split(None, 1)[1].strip()
    if num not in ass_num_list:
        return await message.reply_text(usage)
    ass_num = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "لم يتم العثور على مساعد محفوظ مسبقًا.\n\nيمكنك ضبط المساعد عبر /setassistant"
        )
    else:
        ass = _assistant["saveassistant"]
    assis = {
        "saveassistant": ass_num,
    }
    await save_assistant(message.chat.id, "assistant", assis)
    await message.reply_text(
        f"**المساعد المتغير**\n\nالمساعد المتغير حساب من **{ass}** إلى رقم المساعد **{ass_num}**"
    )


ass_num_list2 = ["1", "2", "3", "4", "5", "عشوائي"]


@app.on_message(filters.command("setassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"** طريقه استعمالي :**\n/setassistant [رقم  الحساب مساعد]\n\nاختر منهم\n{' | '.join(ass_num_list2)}\n\nاختر  الحساب مساعد للمجموعه"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    query = message.text.split(None, 1)[1].strip()
    if query not in ass_num_list2:
        return await message.reply_text(usage)
    if str(query) == "عشوائي":
        ran_ass = random.choice(random_assistant)
    else:
        ran_ass = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        await message.reply_text(
            f"**__تم تخصيص برنامج  Music Bot __**\n\nمساعد لا. **{ran_ass}**"
        )
        assis = {
            "saveassistant": ran_ass,
        }
        await save_assistant(message.chat.id, "assistant", assis)
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"رقم الحساب الموجود حاليآ هوه {ass} موجود.\n\nيمكنك تغيير المساعد عبر ارسال الامر /changeassistant"
        )


@app.on_message(filters.command("checkassistant") & filters.group)
async def check_ass(_, message: Message):
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "لم يتم العثور على مساعد محفوظ مسبقًا.\n\nيمكنك ضبط المساعد عبر /play"
        )
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"تم العثور على المساعد المحفوظ مسبقًا\n\nرقم مساعد {ass} "
        )
