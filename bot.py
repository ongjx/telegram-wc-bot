from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import requests
from pprint import pprint
import json

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_country_data_today():
    res = requests.get("https://worldcup.sfg.io/matches").text
    out = json.loads(res)
    newlist = []
    for match in out:
        try:
            away_team = match['away_team_country']
            home_team = match['home_team_country']
            winner = match['winner']
            away_team_score = match['away_team']['goals']
            home_team_score = match['home_team']['goals']
            time = match['time']
            stage_name = match['stage_name']
            try:
                string = stage_name + ": " + home_team + " - " + str(home_team_score) +  " vs " + away_team +  " - " + str(away_team_score) + " Winner:" + winner
                newlist.append(string)
            except:
                string = stage_name + ": " + home_team + " vs " + away_team
        except:
            try:
                string = home_team + " - " + str(home_team_score) +  " vs " + away_team +  " - " + str(away_team_score) + " ( " + time + " )"
                newlist.append(string)
            except:
                break
    if len(newlist) == 0:
        return "There are no matches today"
    return newlist

def get_all_data():
    res = requests.get("https://worldcup.sfg.io/matches/").text
    out = json.loads(res)
# def get_score(for_country):
    # res = requests.get('https://worldcup.sfg.io/teams/results').text
    # out = json.loads(res)

    # for i in out:
    #     country = i["country"]
    #     games_played = i["games_played"]
    #     win = i["wins"]
    #     draw = i["draws"]
    #     loss = i["losses"]
    #     points = i["points"]
    #     code = i["fifa_code"]
        
    #     if code == for_country:
    #         return  win, draw, loss, points

    # return "Country not Found"

def results(bot, update):
    country = update.message.text.replace('/results ', '')
    update.message.reply_text(get_country_data_today())

def start(bot, update):
    update.message.reply_text("Hello and Welcome to Jun Xiang's World Cup Bot!\nTo begin, please type /results")

def inline(bot,update):
    reply_keyboard = [['Today\'s Results','All Semi Final', 'start']]
    update.message.reply_text('Hi pls choose ur choice!',reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard = True))

# updater = Updater('594678115:AAFtvy1lRRpTTuPWc_FCpE0EbQCiCeRRmkI')
updater = Updater('586483991:AAEjR5s0ZtN3yY2NC-rGjQgBNYul35Hc5y4')
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('results', results))
dispatcher.add_handler(CommandHandler('inline', inline))

updater.start_polling()
