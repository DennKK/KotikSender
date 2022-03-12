import random
import telebot
from telebot import types

token = ''
bot = telebot.TeleBot(token)

# Open and read file with images url
notShown_img = []
images_url = open("images_url.txt", "r")
while True:
    line = images_url.readline()
    if not line:
        break
    notShown_img.append(line.strip())
images_url.close()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('cat')
    itembtn2 = types.KeyboardButton('/help')
    itembtn3 = types.KeyboardButton('donate')

    markup.add(itembtn1, itembtn2, itembtn3)
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Aloha', reply_markup=markup)

    elif message.text == '/help':
        bot.send_message(message.chat.id, 'Type "cat" or "/start" and you will get random cat image')


@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def send_photo(message):
    if message.text == 'cat':

        # Get random image from list and delete it from the list
        random_img = random.choice(notShown_img)
        notShown_img.remove(random_img)

        bot.send_photo(
            message.chat.id,
            photo=random_img,
            caption='You are welcome! Pictures left: ' + str(len(notShown_img))
        )

    elif message.text == 'donate':
        bot.send_message(
            message.chat.id,
            'Pay me via Trust Wallet: https://link.trustwallet.com/send?coin=0&address=bc1q3cs9mx00a5gp5vrv07j2wcvv0yqz9tv43r0dr8'
        )

    else:
        bot.send_message(message.chat.id, 'Wait.....what? Maybe you should type "cat" or "/start" or "/help"?')


def main():
    try:
        bot.polling(none_stop=True, interval=0)
    except IndexError:
        print('no images')


if __name__ == '__main__':
    main()
