from pyrogram import Client
from pyrogram.types import Chat
from pyrogram.enums import ChatType


async def get_chats(messages: list[str], client: Client):
    return [found_message.chat async for found_message in client.search_global(query=' '.join(messages))]


def format_chat_type(chat_type: str):
    return 'лс' if chat_type == ChatType.PRIVATE \
        else 'группа' if chat_type == ChatType.GROUP \
        else 'супер-группа' if chat_type == ChatType.SUPERGROUP \
        else 'канал' if chat_type == ChatType.CHANNEL \
        else 'бот'


def get_yes_no(value: bool):
    return 'да' if value \
        else 'нет'


def get_chat_info(chat: Chat):
    base = [f'юзернейм: {'@' + chat.username if chat.username is not None else '—'}',
            f'id: `{chat.id}`',
            f'тип: `{format_chat_type(chat.type)}`',
            f'запрещен: `{get_yes_no(chat.is_restricted)}`',
            f'верификация: `{get_yes_no(chat.is_verified)}`',
            f'скам: `{get_yes_no(chat.is_scam)}`',
            f'фейк: `{get_yes_no(chat.is_fake)}`',
            f'помощь: `{get_yes_no(chat.is_support)}`',
            f'номер датацентра — {chat.dc_id}']
    
    if chat.type == ChatType.CHANNEL:
        base.insert(0, f'название: `{chat.title}`')
        base.insert(9, f'контент защищен: `{get_yes_no(chat.has_protected_content)}`')
        return '\n'.join(base)
    
    elif chat.type == ChatType.PRIVATE:
        base.insert(0, f'имя: `{chat.first_name}` `{chat.last_name if chat.last_name is not None else ''}`')
        return '\n'.join(base)
    
    elif chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
        base.insert(0, f'название: `{chat.title}`')
        base.insert(3, f'создатель: `{get_yes_no(chat.is_creator)}`')
        return '\n'.join(base)
    
    elif chat.type == ChatType.BOT:
        base.insert(0, f'имя: `{chat.first_name}`')
        base.pop(-1)
        return '\n'.join(base)
    