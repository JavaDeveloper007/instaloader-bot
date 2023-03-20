
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputMediaVideo, MediaGroup, InputFile
from aiogram.dispatcher.filters import Command
import instaloader
import shutil

from pathlib import Path
import re

from Myinstaloader import MyInstaLoader 

# Your bot token obtained from BotFather
BOT_TOKEN = '6036185222:AAHkykI2YGW9ZwdIARY8pdxEbq52LNbNrnQ'

BOT_NAME = "@downloader_mybot"
# Create bot and dispatcher instances
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

loader = MyInstaLoader("test_python08","javohir8558@@")

# Define the MyInstaLoader class

# Define the start command handler
@dp.message_handler(Command("start"))
async def send_welcome(message: types.Message):
    """
    This function sends the welcome message and instructions for using the bot
    """

    instructions = """Botga xush kelibsiz /help"""
    await message.answer(text=instructions)


@dp.message_handler(Command("help"))
async def send_welcome(message: types.Message):
    hlp = f"""
<pre>---Yuklash Tartibi---</pre>
1) instagramdan xoxlagan video yoki rasimga kiring
2) <b>... (3 nuqta)</b> ustiga bosing va <b>ulashish ( поделиться )</b>ning ustiga bosing
3) 🔗havolani nusxalash ( <b>копировать ссылку</b> )
4) 📥havolani {BOT_NAME} -ga tashlang
5) 😉xabarni do'stlaringizga yuboring
"""

    await message.answer(text=hlp,parse_mode="HTML")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_url(message: types.Message):
    url = message.text
    user_id = message.from_user.id



    if "http" in url:
        await message.answer("⏳")

        try:
            await loader.get_shortcode(url=url)
        except AttributeError:
            await bot.delete_message(user_id,message_id=message.message_id+1)
            await message.reply(text="Yuborilgan URL-da xatolik mavjud")
            return

    
        try :
           await loader.download_shortcode(file_path=loader.PATH.parent,folder_name=f"DataMedia\{user_id}")
        except instaloader.exceptions.ConnectionException:
            file_path = Path(fr"{loader.PATH.parent}\{loader.USER}")
            file_path.unlink()
            await loader.download_shortcode(file_path=loader.PATH.parent,folder_name=f"DataMedia\{user_id}")

        if not loader.successfully:
            await bot.delete_message(user_id,message_id=message.message_id+1)
            await message.reply(text="Hechnima topilmadi. Qayta urinib ko'ring")
            return
        
        if loader.post.is_video:
            directory_path = Path(loader.target_path)
            mp4_files = list(directory_path.glob("*.mp4"))

            album = types.MediaGroup()
            for index in range(len(mp4_files)-1):
                album.attach_video(video=InputFile(path_or_bytesio=mp4_files[index]))

            else:
                album.attach_video(video=InputFile(path_or_bytesio=mp4_files[-1]),caption=f"📥 Скачано в {BOT_NAME}")


        else:       #photo
            directory_path = Path(loader.target_path)
            jpg_files = list(directory_path.glob("*.jpg"))

            album = types.MediaGroup()
            for index in range(len(jpg_files)-1):
                album.attach_photo(photo=InputFile(path_or_bytesio=jpg_files[index]))

            else:
                album.attach_photo(photo=InputFile(path_or_bytesio=jpg_files[-1]),caption=f"📥 Скачано в {BOT_NAME}")


        await bot.delete_message(user_id,message_id=message.message_id+1)
        await message.answer_media_group(media=album)
        shutil.rmtree(loader.target_path)



        

if __name__ == '__main__':
    executor.start_polling(dp)
