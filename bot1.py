# importa l'API de Telegram
import telegram
from telegram.ext import Updater, CommandHandler
import datetime



# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
#def start(update, context):
#    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soc un bot bàsic.")

#def start(update, context):
#    info = '''
#Aquí es pot escriure en MarkDown:
#
#- En *negreta*
#- En _cursiva_
#
#'''
#    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://jutge.org/ico/semafor.png')
#    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('ime.png', 'rb'))
#    context.bot.send_message(chat_id=update.effective_chat.id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)
#    context.bot.send_message(chat_id=update.effective_chat.id, text=" 🎗️ ")

def start(update, context):
    print(update)
    print(context)
    botname = context.bot.username
    username = update.effective_chat.username
    fullname = update.effective_chat.first_name 
    missatge = "Tu ets en %s (%s) i jo soc el %s." % (fullname, username, botname)
    context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)

def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="El meu creador és l'osh.")

def hora(update, context):
    x = datetime.datetime.now()
    context.bot.send_message(chat_id=update.effective_chat.id, text=str(x))

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('info', info))
dispatcher.add_handler(CommandHandler('hora', hora))
# engega el bot
updater.start_polling()
updater.idle()