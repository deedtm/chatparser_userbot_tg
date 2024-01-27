from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from utils import get_yes_no, get_msg_link, format_chat_type
import logging


async def search_messages(keywords: list[str], client: Client):
    return [
        found_message
        async for found_message in client.search_global(query=" ".join(keywords))
    ]


async def message_info_generator(messages: list[Message]):
    for message in messages:
        yield await get_info(message)


async def get_info(message: Message):
    chat = message.chat
    chat_id = abs(chat.id)
    chat_id = str(chat_id)[3:] if chat.type in (ChatType.CHANNEL, ChatType.SUPERGROUP) else chat_id
    info = [
        message.text,
        message.id,
        message.date.strftime('%d.%m.%Y %H:%M:%S'),
        get_msg_link(message, chat_id),
        "@" + chat.username if chat.username is not None else "—",
        chat_id,
        get_yes_no(chat.is_restricted),
        get_yes_no(chat.is_verified),
        get_yes_no(chat.is_scam),
        get_yes_no(chat.is_fake),
        get_yes_no(chat.is_support),
        chat.dc_id,
    ]

    if chat.type == ChatType.CHANNEL:
        info.insert(4, chat.title)
        info.insert(13, get_yes_no(chat.has_protected_content))

    elif chat.type == ChatType.PRIVATE:
        info.insert(4, chat.last_name if chat.last_name else "—")
        info.insert(4, chat.first_name)

    elif chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
        info.insert(4, chat.title)
        info.insert(7, get_yes_no(chat.is_creator))

    elif chat.type == ChatType.BOT:
        info.insert(4, chat.first_name)
        info.pop(-1)
        info.pop(3)

    logging.info(msg=f'Найденная информация в чате {'@' + chat.username if chat.username else chat.id}:')
    print(*info, sep=' | ')

    return format_chat_type(chat.type), info
