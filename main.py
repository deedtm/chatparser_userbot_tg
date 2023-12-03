import logging
import parse
from configparser import ConfigParser
from pyrogram import Client, idle, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

config = ConfigParser()
config.read('config.ini')
api_id = config.get('api', 'id')
api_hash = config.get('api', 'hash')

app = Client("my_account", 
             api_id=api_id, 
             api_hash=api_hash, 
             parse_mode=ParseMode.MARKDOWN,
             sleep_threshold=999999)


@app.on_message(filters.me)
async def handler(client: Client, msg: Message):
    if msg.text.startswith('.find'):
        chats = await parse.chats_by_messages(msg.text.split()[1:], client)
        chats_count = len(chats) if all(chats) is None else len(chats) - 1
        if chats_count == 0:
            await msg.edit_text('🤖 Ничего не было найдено')
        else:
            adding = 1 if all(chats) is None else 0
            for num, text in enumerate(chats):
                if text == '':
                    continue
                await client.send_message('me', f'__[{num + adding}/{chats_count}]__\n{text}')
    


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run()
    