from random import randint

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from bin.todo import Todo
from bin.storage import Storage

bot = Bot(token='461685553:AAH6nNu05ygR3-kKY4tFZKHAlGga54sYh-s')
dp = Dispatcher(bot)


def get_todo_id():
    return randint(0, 1000)


def get_filename(message: types.Message):
    return str(message.chat.id) + '_' + str(message.from_user.id) + '.td'


@dp.message_handler(commands=['start'])
async def show_welcome(message: types.Message):
    await message.reply("Hi!\nI'm TodoBot!\nPowered by Odea.")


@dp.message_handler(commands=['help'])
async def show_help(message: types.Message):
    await message.reply("todoadd TODO_DESCRIPTION: adds a TODO\ntodolist: displays TODOs\n"
                        "tododone TODO_ID: deletes a TODO")


@dp.message_handler(commands=['todoadd', 'Todoadd'])
async def save_todo(message: types.Message):
    filename = get_filename(message)
    todo = Todo(get_todo_id(), message.get_args())
    Storage(filename).store_todo(todo)


@dp.message_handler(commands=['tododone', 'Tododone'])
async def todo_done(message: types.Message):
    filename = get_filename(message)
    todo_id = message.get_args()
    Storage(filename).delete_todo(todo_id)
    pass


@dp.message_handler(commands=['todolist', 'Todolist'])
async def show_todo(message: types.Message):
    txt = 'TODOs:\n'
    filename = get_filename(message)
    todos = Storage(filename).get_todos()
    for todo in todos:
        txt += str(todo.id) + '. ' + todo.description
    await message.reply(txt)


if __name__ == '__main__':
    executor.start_polling(dp)
