from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, FSMContext
from config import token
import os,time,requests.logging

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
logging.basicConfig(level = logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет! {message.from_user.full_name}")

@dp.message_handler(commands='start')
async def get_video_info(message: types.Message):
    video_id = message.text.split()[1]
    response = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/aweme/detail/?aweme_id={video_id}')
    if response.status_code == 200:
        video_info = response.json()
        video_title = video_info['title']
        video_author = video_info['author_name']
        video_likes = video_info['like_count']
        video_comments = video_info['comment_count']
        video_views = video_info['view_count']

        await bot.send_message(message.chat.id, f"id: {video_id}\nАвтор: {video_author}\nНазвание:{video_title}\nПросмотры:{video_views}\nЛайки:{video_likes}\nКомментарии:{video_comments}")

    else:
        return None

@dp.message_handler()
async def download_send_video(message:types.Message):
    await message.answer("Скачивание видео...")

executor.start_polling(dp)