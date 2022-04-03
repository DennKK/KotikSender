import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Open and read file with images url
not_shown_img = []
images_url = open('images_url.txt', 'r')
while True:
    line = images_url.readline()
    if not line:
        break
    not_shown_img.append(line.strip())
images_url.close()


def btn():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Get a cat', callback_data='send_cat'))
    return keyboard


def get_random_img():
    try:
        random_img = random.choice(not_shown_img)
        not_shown_img.remove(random_img)
    except IndexError:
        random_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1TXuZba5hlWGqU8PpVbAKCRCT1fi9O-sgQA&usqp=CAU'
    return random_img


users_id = []
user = {}


def calc_usr_imgs(user_id):
    """Returns the number of images that have not been seen yet by the user"""
    if user_id not in users_id:
        new_key_values_itr = ((user_id, len(not_shown_img)),)
        user.update(new_key_values_itr)
        users_id.append(user_id)
    user[user_id] = user[user_id] - 1
    if user[user_id] == -1:
        user[user_id] = 0
    return user[user_id]


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Type "cat"!')


@dp.message_handler()
async def send_button(message: types.Message):
    if message.text.lower() == 'cat':
        await bot.send_message(chat_id=message.chat.id, text='Press on button and get a cat picture. This bot was made by "@DennKK5"', reply_markup=btn())
    else:
        await message.reply('Type "cat"!')


@dp.callback_query_handler(text_contains='send_cat')
async def send_cat(call: CallbackQuery):
    user_id = call.message.from_user.id
    num = calc_usr_imgs(user_id)
    await bot.send_photo(chat_id=call.message.chat.id, photo=get_random_img(), caption='You are welcome! Pictures left: ' + str(num), reply_markup=btn())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
