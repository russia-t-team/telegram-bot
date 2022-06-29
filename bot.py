import random
import re
from dotenv import load_dotenv
from os import getenv
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import requests, json

load_dotenv()
RU_REGEX = 'россия|путин|медведев|москва|царь|рф'
UA_REGEX = 'украин|хохл|хохол|война|донбас'
BE_REGEX = 'батьк|белорус|лукашенк'
MAT_REGEX = r"""(?iu)\b((у|[нз]а|(хитро|не)?вз?[ыьъ]|с[ьъ]|(и|ра)[зс]ъ?|(о[тб]|под)[ьъ]?|(.\B)+?[оаеи])?-?([её]б(?!о[рй])|и[пб][ае][тц]).*?|(н[иеа]|([дп]|верт)о|ра[зс]|з?а|с(ме)?|о(т|дно)?|апч)?-?ху([яйиеёю]|ли(?!ган)).*?|(в[зы]|(три|два|четыре)жды|(н|сук)а)?-?бл(я(?!(х|ш[кн]|мб)[ауеыио]).*?|[еэ][дт]ь?)|(ра[сз]|[зн]а|[со]|вы?|п(ере|р[оие]|од)|и[зс]ъ?|[ао]т)?п[иеё]зд.*?|(за)?п[ие]д[аое]?р(ну.*?|[оа]м|(ас)?(и(ли)?[нщктл]ь?)?|(о(ч[еи])?|ас)?к(ой)|юг)[ауеы]?|манд([ауеыи](л(и[сзщ])?[ауеиы])?|ой|[ао]вошь?(е?к[ауе])?|юк(ов|[ауи])?)|муд([яаио].*?|е?н([ьюия]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[еёо]й))\b"""
WEATHER_REGEX = 'погода'

UA_PATTERN = re.compile(UA_REGEX, re.IGNORECASE)
MAT_PATTERN = re.compile(MAT_REGEX, re.IGNORECASE)
RU_PATTERN = re.compile(RU_REGEX, re.IGNORECASE)
BE_PATTERN = re.compile(BE_REGEX, re.IGNORECASE)
WEATHER_PATTERN = re.compile(WEATHER_REGEX, re.IGNORECASE)
MAT_STICKERS = ['CAACAgIAAxkBAAEEFWdiJkI9efIFCAKgZn9x0WtczrrnFQACtwUAAiMFDQABLgbfFJj7y2sjBA',
                'CAACAgIAAxkBAAEEG2ViKkK_-u5QX7qF6f3stZ531kARhAACBwIAAodOegRVtS-H6GqSQCME',
                'CAACAgIAAxkBAAEEG2diKkLp3KPX0qT_u7PMSuM9bGbjrQACLgEAAodOegRwb7a9j6GCjyME',
                'CAACAgIAAxkBAAEEG2liKkMGlm_U6iEc6y3Q3QZ65uz-XwACOwwAAkADwEn4aMxS-ZzfZCME',
                'CAACAgIAAxkBAAEEG2tiKkNQFeLY83Kvezjzsa9IIwT7TQACHBkAAtjY4QABeejXDAOqS24jBA']

UA_STICKERS = ['CAACAgIAAxkBAAEECn1iIOkPGHzDqt2Zv8I1g-J5o--RjwACFBYAAma5CEmQib3xor7ODCME',
               'CAACAgQAAxkBAAEELMxiMYMQyzcfMz4D_ke8SctLXoJtWwACKAMAAlGMzwGaedJVCQ_ZOCME']

RU_STICKERS = ['CAACAgIAAxkBAAEEFfliJvBGOTKSpwODa-yvxfEzQk5IVgACkgAD1U_lBYNXm1TVqDz1IwQ']

BE_STICKERS = ['CAACAgIAAxkBAAEEGoBiKcICugQT_6tInDE6wuncSv7KiQACTAADHMJYFxRAZGSh7NSaIwQ']



def weather(api_key, city_name):


    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&lang=ru&units=metric&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidity = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        return (" Температура = " +
              str(current_temperature) +
              ". Атмосферное давление  = " +
              str(current_pressure) +
              ". Влажность (%) = " +
              str(current_humidity) +
              ". Описание = " +
              str(weather_description))

    else:
        return "Нет данных"


def weather_bot(update: Updater, context: CallbackContext):
    chelyabinsk = weather(getenv("WEATHER_TOKEN"), "Chelyabinsk")
    lissbon = weather(getenv("WEATHER_TOKEN"), "Lisbon")
    munich = weather(getenv("WEATHER_TOKEN"), "Munich")
    update.message.reply_text('Челябинск: {}, Лиссабон: {}, Мюнхен: {}'.format(chelyabinsk, lissbon, munich))


def ukraine(update: Updater, context: CallbackContext):
    sticker = get_sticker(UA_STICKERS, 3)
    update.message.reply_sticker(sticker)


def get_sticker(stickers, max_prob):
    command_counter = random.randint(1, max_prob)
    if command_counter == 1:
        return random.choice(stickers)
    return None


def mat(update: Updater, context: CallbackContext):
    sticker = get_sticker(MAT_STICKERS, 3)
    if sticker:
        update.message.reply_sticker(sticker)


def russia(update: Updater, context: CallbackContext):
    sticker = get_sticker(RU_STICKERS, 3)
    if sticker:
        update.message.reply_sticker(sticker)


def belorus(update: Updater, context: CallbackContext):
    sticker = get_sticker(BE_STICKERS, 3)
    if sticker:
        update.message.reply_sticker(sticker)


def shklyar(update: Updater, context: CallbackContext):
    command_counter = random.randint(1, 20)
    if command_counter == 4:
        update.message.reply_text('ну просто реально достало твое нытье, Леха, ты же мужик, начни делать что-то')
    if command_counter == 9:
        update.message.reply_sticker('CAACAgIAAxkBAAEEPrxiOuYWf-1OBo4nkOY-3NeCk43nzgACCxkAAqSEyUlLrhf62L85wSME')


def main():
    my_bot = Updater(getenv("TOKEN"))
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(UA_PATTERN), ukraine), 0)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(MAT_PATTERN), mat), 0)
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(RU_PATTERN), russia), 0)
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(BE_PATTERN), belorus), 0)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(WEATHER_PATTERN), weather_bot), 0)
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.user(user_id={855480940}), shklyar), 1)
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()
