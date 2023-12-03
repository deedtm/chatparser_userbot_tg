import utils
from pyrogram import Client
from pyrogram.types import Chat


async def chats_by_messages(messages: list[str], client: Client):
    chats: list[Chat] = await utils.get_chats(messages, client)
    self_id = (await client.get_me()).id
    return set(['' if chat.id == self_id
                else utils.get_chat_info(chat) for chat in chats])
