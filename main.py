from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
import keyboard

import logging

storage = MemoryStorage()  # FSM
bot = Bot(token=config.TOKEN)  # create an object of class Bot
dispatch = Dispatcher(bot, storage=storage)  # create an object of class Dispatcher and transfer our bot

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO, filename='log.txt')


# will collect the information about the work of the bot  in the file


@dispatch.message_handler(commands='start')  # decorator (catches the start command)
async def welcome(message: types.Message):  # the async function
    file = open('users.txt', 'r')  # open the file for reading
    set_of_id = set()  # create a variable that refers to empty set
    for line in file:  # cycle
        set_of_id.add(line.strip())  # add the id into the set

    if str(message.chat.id) not in set_of_id:  # condition
        file = open('users.txt', 'a')  # open file to add id
        file.write(str(message.chat.id) + '\n')  # write id in file
        set_of_id.add(message.chat.id)

    await bot.send_message(message.chat.id, f'Hello, *{message.from_user.first_name}, * I\'m working',
                           reply_markup=keyboard.start, parse_mode='Markdown')  # send this message


@dispatch.message_handler(commands='info')  # decorator (catches the info command)
async def cmd_test1(message: types.Message):  # the async function
    await bot.send_message(message.chat.id, "this is a talking bot. You can use these commands : /start, /info, /books",
                           reply_markup=keyboard.start, parse_mode='Markdown')  # send this message


@dispatch.message_handler(commands='books')  # decorator (catches the books command)
async def books_you_can_read(message: types.Message):  # the async function
    file = open('books_links.txt', 'r', encoding='UTF-8')  # open file for reading
    list_of_book_name = []  # the variable that refers to empty list

    for line in file:  # cycle
        list_of_book_name.append(line.strip().split(':')[0] + line.strip().split(':')[-1])
        # add to the end of the list book name and the link

    await bot.send_message(message.chat.id, f"You can read books: {list_of_book_name}",
                           reply_markup=keyboard.start, parse_mode='Markdown')  # send message


@dispatch.message_handler(content_types=['text'])  # decorator (caches special text)
async def get_message(message: types.Message):  # the async function
    if message.text == 'Information':  # condition
        await bot.send_message(message.chat.id, text='Information\nThis bot is created for talking with you')
        # send message
    elif message.text == 'Statistics':  # alternative condition
        file = open('users.txt', 'r')  # open file for reading
        set_of_id = set()
        for line in file:
            set_of_id.add(line.strip())
        await bot.send_message(message.chat.id, f'Statistics\nThis bot talked to {len(set_of_id)} people',
                               reply_markup=keyboard.start, parse_mode='Markdown')  # send message


if __name__ == '__main__':  # condition. if we in this python file
    print('Bot is working')  # print to the console
    executor.start_polling(dispatch, skip_updates=True)
