from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            KeyboardButton, Message, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove)

from Yukki import BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME, SUDOERS, app, db_mem
from Yukki.Database import (_get_playlists, delete_playlist, get_playlist,
                            get_playlist_names, save_playlist)
from Yukki.Decorators.admins import AdminRightsCheck
from Yukki.Decorators.assistant import AssistantAdd
from Yukki.Decorators.checker import checker, checkerCB
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (add_genre_markup, check_genre_markup, check_markup,
                          delete_playlist_markuup, download_markup,
                          others_markup, play_genre_playlist, playlist_markup,
                          third_playlist_markup)


__MODULE__ = "Playlist"
__HELP__ = """


/playplaylist 
-  يقوم هذا الامر بتشغيل الاغاني المحفوضه في المجموعه  بل تسلسل
.


/playlist 
- تحقق من قائمة التشغيل المحفوظة على الخوادم.


/delmyplaylist
-احذف أي موسيقى محفوظة في قائمة التشغيل الخاصة بك


/delgroupplaylist
- احذف أي موسيقى محفوظة في قائمة التشغيل الخاصة بمجموعتك [يجب ان تكون مشرف فيه المجموعه.]
"""


@app.on_message(filters.command("playplaylist") & filters.group)
@checker
@PermissionCheck
@AssistantAdd
async def play_playlist_cmd(_, message):
    thumb = "Utils/Playlist.jpg"
    await message.delete()
    if not message.reply_to_message:
        if len(message.command) == 2:
            user = message.text.split(None, 2)[1]
            if "@" in user:
                user = user.replace("@", "")
            try:
                user = int(user)
                try:
                    user = await app.get_users(user)
                    userid = user.id
                    third_name = user.first_name
                except:
                    userid = user
                    third_name = "Deleted Account"
            except:
                try:
                    user = await app.get_users(user)
                    userid = user.id
                    third_name = user.first_name
                except Exception as e:
                    return await message.reply_text("المستخدم ليس موجود")
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            buttons = third_playlist_markup(
                user_name, user_id, third_name, userid, "abcd"
            )
            hmo = await message.reply_photo(
                photo=thumb,
                caption=(
                    f"**{MUSIC_BOT_NAME}'ميزة قائمة التشغيل**\nحدد قائمة التشغيل التي تريد تشغيلها!.\n\nيمكنك تشغيل قائمة تشغيل شخص آخر أيضًا:-\n- /playplaylist[معرف الشخص]\n- /playplaylist [ايدي الشخص](if user has deleted acc)\n- /playplaylist [Reply to a User]"
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        else:
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            buttons = playlist_markup(user_name, user_id, "abcd")
            await message.reply_photo(
                photo=thumb,
                caption=(
                    f"**{MUSIC_BOT_NAME}'ميزة قائمة التشغيل**\nحدد قائمة التشغيل التي تريد تشغيلها!.\n\nيمكنك تشغيل قائمة تشغيل شخص آخر أيضًا:-\n- /playplaylist Username]\n- /playplaylist [ايدي الشخص](if user has deleted acc)\n- /playplaylist [Reply to a User]"
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
    else:
        userid = message.reply_to_message.from_user.id
        third_name = message.reply_to_message.from_user.first_name
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        buttons = third_playlist_markup(
            user_name, user_id, third_name, userid, "abcd"
        )
        hmo = await message.reply_photo(
            photo=thumb,
            caption=(
                f"**{MUSIC_BOT_NAME}'ميزة قائمة التشغيل**\nحدد قائمة التشغيل التي تريد تشغيلها!.\n\nيمكنك تشغيل قائمة تشغيل شخص آخر أيضًا:-\n- /playplaylist[معرف الشخص]\n- /playplaylist [ايدي الشخص](إذا قام المستخدم بحذف لجنة التنسيق الإدارية)\n- /playplaylist [Reply to a User]"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return


@app.on_message(filters.command("playlist") & filters.group)
@checker
@PermissionCheck
@AssistantAdd
async def playlist(_, message):
    thumb = "Utils/Playlist.jpg"
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    buttons = check_markup(user_name, user_id, "abcd")
    await message.reply_photo(
        photo=thumb,
        caption=(
            f"**{MUSIC_BOT_NAME}'ميزة قائمة التشغيل**\n\nحدد قائمة التشغيل ، تريد أن تحقق **!**"
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return


options = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "all",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
]

options_Genre = [
    "Rock",
    "Sad",
    "Party",
    "Lofi",
    "Bollywood",
    "Hollywood",
    "Punjabi",
    "Others",
]


@app.on_message(filters.command("delmyplaylist") & filters.group)
async def del_cmd(_, message):
    usage = f"استعمل :\n\n/delmyplaylist [Genre] [الأعداد بين 1-30] (لحذف موسيقى معينة في قائمة التشغيل )\n\nor\n\n/delmyplaylist [Genre] all ( لحذف قائمة التشغيل بأكملها )\n\n**Genres:-**\n{' | '.join(options_Genre)}"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    genre = message.text.split(None, 2)[1].strip()
    count = message.text.split(None, 2)[2].strip()
    if not count:
        return await message.reply_text(usage)
    if count not in options:
        return await message.reply_text(usage)
    if genre not in options_Genre:
        return await message.reply_text(usage)
    if str(count) == "all":
        buttons = delete_playlist_markuup("Personal", genre)
        return await message.reply_text(
            f"تأكيد!!\nأنت متأكد أنك تريد حذف الخاص بك كله {genre} قائمه التشغيل?",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        _playlist = await get_playlist_names(message.from_user.id, genre)
    if not _playlist:
        await message.reply_text(
            f"ليس لديك قائمة تشغيل {MUSIC_BOT_NAME}"
        )
    else:
        titlex = []
        j = 0
        count = int(count)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note, genre)
            if j == count:
                deleted = await delete_playlist(
                    message.from_user.id, note, genre
                )
                if deleted:
                    return await message.reply_text(
                        f"**تم حذف ملف {count} الموسيقى في قائمة التشغيل**"
                    )
                else:
                    return await message.reply_text(
                        f"**No such saved الموسيقى في قائمة التشغيل.**"
                    )
        await message.reply_text("ليس لديك مثل هذا الموسيقى في قائمة التشغيل.")


@app.on_message(filters.command("delgroupplaylist") & filters.group)
@AdminRightsCheck
async def delgroupplaylist(_, message):
    usage = f"استعمل :\n\n/delgroupplaylist [Genre] [الأعداد بين 1-30] ( to delete a particular الموسيقى في قائمة التشغيل )\n\nor\n\n /delgroupplaylist [Genre] all ( to delete whole playlist )\n\n**Genres:-**\n{' | '.join(options_Genre)}"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    genre = message.text.split(None, 2)[1].strip()
    count = message.text.split(None, 2)[2].strip()
    if not count:
        return await message.reply_text(usage)
    if count not in options:
        return await message.reply_text(usage)
    if genre not in options_Genre:
        return await message.reply_text(usage)
    if str(count) == "all":
        buttons = delete_playlist_markuup("Group", genre)
        return await message.reply_text(
            f"تأكيد!!\nأنت متأكد أنك تريد حذف المجموعة بأكملها {genre} قائمه التشغيل?",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        _playlist = await get_playlist_names(message.chat.id, genre)
    if not _playlist:
        await message.reply_text(
            f"ليس لديك قائمة تشغيل {MUSIC_BOT_NAME}'s Server"
        )
    else:
        titlex = []
        j = 0
        count = int(count)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note, genre)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note, genre)
                if deleted:
                    return await message.reply_text(
                        f"**تم حذف ملف {count}الموسيقى في قائمة تشغيل المجموعة**"
                    )
                else:
                    return await message.reply_text(
                        f"**لا توجد مثل هذه الموسيقى المحفوظة في قائمة التشغيل الجماعية.**"
                    )
        await message.reply_text("ليس لديك مثل هذا الموسيقى في قائمة التشغيل.")


@app.on_callback_query(filters.regex(pattern=r"show_genre"))
async def show_genre(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    a, b, c = callback_request.split("|")
    buttons = play_genre_playlist(a, b, "abcd")
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"playlist_check"))
async def playlist_check(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    a, b, c = callback_request.split("|")
    print(b)
    buttons = check_genre_markup(b, "abcd", userid)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"main_playlist"))
async def main_playlist(_, CallbackQuery):
    await CallbackQuery.answer()
    user_id = CallbackQuery.from_user.id
    user_name = CallbackQuery.from_user.first_name
    buttons = playlist_markup(user_name, user_id, "abcd")
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"your_playlist"))
async def your_playlist(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = add_genre_markup(user_id, "Personal", videoid)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"group_playlist"))
async def group_playlist(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = add_genre_markup(user_id, "Group", videoid)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"other"))
async def otherhuvai(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = others_markup(videoid, user_id)
    db_mem[videoid]["check"] = 1
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"goback"))
async def goback(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = others_markup(videoid, user_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        pass
