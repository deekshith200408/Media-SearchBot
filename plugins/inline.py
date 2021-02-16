from urllib.parse import quote
from pyrogram import Client, emoji, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument
from utils import get_search_results
from info import MAX_RESULTS, CACHE_TIME, SHARE_BUTTON_TEXT, AUTH_USERS


@Client.on_inline_query(filters.user(AUTH_USERS) if AUTH_USERS else None)
async def answer(bot, query):
    """Show search results for given inline query"""

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(bot.username)
    files, next_offset = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=MAX_RESULTS,
                                                  offset=offset)

    for file in files:
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                file_id=file.file_id,
                caption=file.caption or "",
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results"
        if string:
            switch_pm_text += f" for {string}"

        await query.answer(results=results,
                           cache_time=CACHE_TIME,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
    else:

        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           cache_time=CACHE_TIME,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")


def get_reply_markup(username):
    url = 't.me/share/url?url=t.me/MOVIECLUB_CHAT' + quote(SHARE_BUTTON_TEXT.format(username=username))
    buttons = [[
        InlineKeyboardButton('Search again', switch_inline_query_current_chat=''),
        InlineKeyboardButton('Request Movie', url=url),
        InlineKeyboardButton('Share bot', url=tg://msg?text=Hai%20Friend%20%E2%9D%A4%EF%B8%8F%2C%0AToday%20i%20just%20found%20out%20an%20%20intresting%20%2A%2AMovie%2FSeries%20Searching%20Bot%2A%2A%20With%20Lots%20Of%20Collections.%20%F0%9F%A5%B0.%20%0A%2A%2ABot%20Link%20%3A%2A%2A%20%40MC_MovieBot%20%F0%9F%94%A5),
    ]]
    return InlineKeyboardMarkup(buttons)


def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
