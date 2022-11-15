import telebot
from extensions import APIException, CurrencyConverter
from config import TOKEN
from currencies import keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для определения стоимости валюты введите команду:\n<Название валюты цену которой Вы хотите узнать> \
<В какую валюту Вы хотите конвертировать> <Количество валюты для конвертации>\nВывод списка доступных валют: /values'

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Валюты доступные для конвертации:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Количество параметров больше или меньше допустимого /help')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода данных \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Команда \n{e} не обработана /help')

    else:
        text = str.capitalize(f'Конвертация {amount} {quote} в {base} = {total_base}')
        bot.send_message(message.chat.id, text)

bot.polling()
