import telebot
import requests
import json

TOKEN = '6464340735:AAEuSyqcD2i16mrNrpJ1lYNMyf8TzWuDD0A'
bot = telebot.TeleBot(TOKEN)

keys = {
    "биткоин": "BTC",
    "эфириум": "ETH",
    "рубль": "RUR",
}

@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text = "Для работы с ботом введите команды в виде: 'имя валюты', 'в какую вылюту перевести', 'какое количество валюты перевести'"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['text'])
def convert (message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')

r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]})
total_base = json.loads(r.content)[keys[base]]
text = f'Цена {amount} {quote} в {base} - {total_base}'
bot.send_message(message.chat.id, text)

bot.polling()
