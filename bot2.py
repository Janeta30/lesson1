import telebot
import datetime

bot = telebot.TeleBot("1664758736:AAGdV4gg4b0A0MrBe2y4lws0KrEMZzzZM3c")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if (message.text).capitalize() == 'Привет':
        bot.reply_to(message, 'Привет, как дела?')
    else:
	    bot.reply_to(message, message.text)

bot.polling()