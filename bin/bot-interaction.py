from random import randint

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from bin.todo import Todo
from bin.storage import Storage


# TODO handle Storage Exceptions

def get_token():
    with open('../config/token.txt', 'r') as token:
        return token.readlines()[0]


bot = Bot(token=get_token())
dp = Dispatcher(bot)


def get_todo_id():
    return randint(0, 1000)


def get_filename(message: types.Message, end_data: str):
    chat_id = str(message.chat.id)
    cut_end = len(end_data)
    todo_type = str(message.get_command()[3:-cut_end])
    return chat_id + '_' + todo_type + '.td'


@dp.message_handler(commands=['start'])
async def show_welcome(message: types.Message):
    await message.reply("Hi!\nI'm TodoBot!\nPowered by Odea.")


@dp.message_handler(commands=['help'])
async def show_help(message: types.Message):
    await message.reply("todoadd TODO_DESCRIPTION: adds a TODO\ntodolist: displays TODOs\n"
                        "tododone TODO_ID: deletes a TODO")


@dp.message_handler(regexp='[tT]o.+add')
async def save_todo(message: types.Message):
    filename = get_filename(message, "add")
    todo = Todo(get_todo_id(), message.get_args())
    Storage(filename).store_todo(todo)


@dp.message_handler(regexp='[tT]o.+done')
async def todo_done(message: types.Message):
    filename = get_filename(message, "done")
    todo_id = message.get_args()
    Storage(filename).delete_todo(todo_id)


@dp.message_handler(regexp='[tT]o.+list')
async def show_todo(message: types.Message):
    todo_type = str(message.get_command())[3:-4]
    txt = 'TO-' + todo_type.upper() + 's:\n'
    filename = get_filename(message, "list")
    todos = Storage(filename).get_todos()
    for todo in todos:
        txt += str(todo.id) + '. ' + todo.description
    await message.reply(txt)


@dp.message_handler(command=['list', 'List'])
async def show_todo(message: types.Message):
    txt = "Lists:\n"
    txt += Storage.existing_lists(str(message.chat))
    await message.reply(txt)


if __name__ == '__main__':
    executor.start_polling(dp)
