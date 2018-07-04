from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from pprint import pprint
import json

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_results(for_country):
    res = requests.get('https://worldcup.sfg.io/teams/results').text
    out = json.loads(res)

    for i in out:
        country = i["country"]
        games_played = i["games_played"]
        win = i["wins"]
        draw = i["draws"]
        loss = i["losses"]

        points = i["points"]
        code = i["fifa_code"]
        
        if code == for_country:
            return  win, draw, loss, points

    return "Country not Found"

def results(bot, update):
    country = update.message.text.replace('/results ', '')

    update.message.reply_text(get_results(country))

def start(bot, update):
    update.message.reply_text("Hello!")

updater = Updater('594678115:AAFtvy1lRRpTTuPWc_FCpE0EbQCiCeRRmkI')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('results', results))

updater.start_polling()
