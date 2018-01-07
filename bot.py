import tweepy
import telebot
from telebot import types
import os
import time
from datetime import date

contador = 0
consumer_key = ""
consumer_secret = ""
key = ""
secret = ""
token = ""

auth = tweepy.OAuthHandler(consumer_key,consumer_secret);
auth.set_access_token(key, secret)

api = tweepy.API(auth)
bot = telebot.TeleBot(token)

command_list = ['/joni']


def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        print(m.content_type)
        if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
            cid = m.chat.id # Almacenaremos el ID de la conversación.
            print ("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start
            command_true = False
            for com in command_list:
                if com in m.text:
                    command_true = True
                    break
            if command_true == False :
                try:
                    api.update_status(m.text)
                except Exception:
                    if(len(m.text)>280):
                        bot.reply_to(m,"El mensaje excede " +str(len(m.text)-280)+" caracteres el limite maximo " )
        if m.content_type == 'photo':
            message = m.caption
            print(message)
            file_info = bot.get_file(m.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            path = 'Imagenes'
            d = date.today().isoformat()
            file_path = path + '\\' + d + ".jpg"
            if not os.path.exists(path):
                os.makedirs(path)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            try:
                api.update_with_media(file_path, status = message)
            except Exception:
                bot.reply_to(m, 'No se ha podido enviar la imagen')

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.

@bot.message_handler(commands = ['joni'])
def joni(m):
    global contador
    try:
        api.update_status("@Jonizu juapo (" + str(contador) + ")" )
        contador = contador + 1
    except Exception:
        bot.reply_to(m,'No de pudo mandar mensaje a Jonizu ;(')
        return
    bot.reply_to(m, 'Mensaje enviado')

bot.polling(none_stop=True)
