import logging
import os
import parse
from configparser import ConfigParser
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from excel import Excel
import time

from utils import format_seconds

config = ConfigParser()
config.read("config.ini")
api_id = config.get("api", "id")
api_hash = config.get("api", "hash")

excel_file_name = config.get("excel", "file_name")
sheets = config.get("excel", "sheets").split(", ")
columns = [config.get(sheet, "columns").split(", ") for sheet in sheets]

app = Client(
    "my_account",
    api_id=api_id,
    api_hash=api_hash,
    parse_mode=ParseMode.MARKDOWN,
)


@app.on_message(filters.me & filters.regex("\\.find .+"))
async def find_handler(client: Client, msg: Message):
    past = time.time()
    if excel_file_name in os.listdir():
        os.remove(excel_file_name)
    xls = Excel(excel_file_name, sheets, columns)

    keywords = msg.text.split()[1:]
    messages = await parse.search_messages(keywords, client)
    if len(messages) <= 1:
        await msg.edit_text(f"🤖 Ничего не было найдено")
    else:    
        await msg.edit_text(f"🤖 Парсинг был начат\n🕒 **~{format_seconds(len(messages) * 0.3)}**")

        async for chat_type, info in parse.message_info_generator(messages):
            sheet = xls.get_sheet(chat_type)
            xls.write(sheet, info)

        await msg.delete()
        future = time.time()
        await client.send_document(
            "me",
            document="chats.xls",
            caption=f'<pre language="Ключевые слова">{" ".join(keywords)}</pre>\n<i>{len(messages)} сообщ. за {format_seconds(future - past)}\nкаждое сообщение ~{format_seconds((future - past) / len(messages))}</i>',
            parse_mode=ParseMode.HTML,  
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()
