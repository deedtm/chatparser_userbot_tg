from datetime import timedelta, datetime
from pyrogram.enums import ChatType
from pyrogram.types import Message

def format_chat_type(chat_type: str):
    return (
        "dms"
        if chat_type == ChatType.PRIVATE
        else "groups"
        if chat_type in (ChatType.GROUP, ChatType.SUPERGROUP)
        else "channels"
        if chat_type == ChatType.CHANNEL
        else "bots"
    )

def get_msg_link(message: Message, chat_id: int):
    link = [f"https:/", "t.me"]
    chat_type = message.chat.type
    try:
        username = message.chat.username
    except AttributeError:
        print(message)
        
    if chat_type == ChatType.BOT or username is None:
        return '—'
    elif chat_type in (ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL):
        link.extend(['c', str(chat_id)])
    else:
        link.append(username)
    
    link.append(str(message.id))
    return '/'.join(link)


def get_yes_no(value: bool):
    return "да" if value else "нет"


def format_seconds(seconds: float):
    formatted = datetime(1, 1, 1, 0, 0, 0, 0) + timedelta(seconds=seconds)
    if formatted.hour != 0:
        return formatted.strftime('%#H ч. %#M мин. %#S сек.')
    else:
        if formatted.minute != 0:
            return formatted.strftime('%#M мин. %#S сек.')
        else:
            return formatted.strftime('%#S.%f')[:-3] + ' сек.'
