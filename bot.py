from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import requests
from pprint import pprint
import json

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def get_score(for_country):
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
    update.message.reply_text(get_score(country))
    update.message.reply_text(get_country_data(country))
def start(bot, update):
    update.message.reply_text("Hello!")

def inline(bot,update):
    reply_keyboard = [['results','start']]
    update.message.reply_text('Hi pls choose ur choice!',reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard = True))
    
def get_country_data(country_name):
    res = requests.get("https://worldcup.sfg.io/matches/country?fifa_code=" + country_name).text
    out = json.loads(res)
    newlist = []
    for i in out:
        away_team = i['away_team']
        away_team_events = i['away_team_events']
        home_team = i['home_team']    
        home_team_events = i['home_team_events']
        winner = i['winner']

        newlist.append([i['away_team'], i['away_team_events'],
         i['home_team'], i['home_team_events'], i['winner']])
    return newlist    

updater = Updater('594678115:AAFtvy1lRRpTTuPWc_FCpE0EbQCiCeRRmkI')
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('results', results))
dispatcher.add_handler(CommandHandler('inline', inline))

updater.start_polling()
