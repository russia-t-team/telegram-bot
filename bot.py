import random
import re
from dotenv import load_dotenv
from os import getenv
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import requests, json
import datetime

load_dotenv()

IN_RU_REGEX = 'в россии|в рф|на родине'
RU_REGEX = IN_RU_REGEX + '|челябинск|россия|путин|медведев|москва|царь|рф'
UA_REGEX = 'украин|хохл|хохол|война|донбас'
BE_REGEX = 'батьк|белорус|лукашенк'
MAT_REGEX = r"""(?iu)\b((у|[нз]а|(хитро|не)?вз?[ыьъ]|с[ьъ]|(и|ра)[зс]ъ?|(о[тб]|под)[ьъ]?|(.\B)+?[оаеи])?-?([её]б(?!о[рй])|и[пб][ае][тц]).*?|(н[иеа]|([дп]|верт)о|ра[зс]|з?а|с(ме)?|о(т|дно)?|апч)?-?ху([яйиеёю]|ли(?!ган)).*?|(в[зы]|(три|два|четыре)жды|(н|сук)а)?-?бл(я(?!(х|ш[кн]|мб)[ауеыио]).*?|[еэ][дт]ь?)|(ра[сз]|[зн]а|[со]|вы?|п(ере|р[оие]|од)|и[зс]ъ?|[ао]т)?п[иеё]зд.*?|(за)?п[ие]д[аое]?р(ну.*?|[оа]м|(ас)?(и(ли)?[нщктл]ь?)?|(о(ч[еи])?|ас)?к(ой)|юг)[ауеы]?|манд([ауеыи](л(и[сзщ])?[ауеиы])?|ой|[ао]вошь?(е?к[ауе])?|юк(ов|[ауи])?)|муд([яаио].*?|е?н([ьюия]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[еёо]й))\b"""
WEATHER_REGEX = 'погода'
WEST_REGEX = 'в нато|в сша|в америке|в европе|в португалии|в германии'
REMEMBER_REGEX = 'бот,? запомни,? (?:что |это)?'
FORGET_REGEX = 'бот,? не говори (?:это|так)'

UA_PATTERN = re.compile(UA_REGEX, re.IGNORECASE)
MAT_PATTERN = re.compile(MAT_REGEX, re.IGNORECASE)
RU_PATTERN = re.compile(RU_REGEX, re.IGNORECASE)
IN_RU_PATTERN = re.compile(IN_RU_REGEX, re.IGNORECASE)
BE_PATTERN = re.compile(BE_REGEX, re.IGNORECASE)
WEATHER_PATTERN = re.compile(WEATHER_REGEX, re.IGNORECASE)
WEST_PATTERN = re.compile(WEST_REGEX, re.IGNORECASE)
REMEMBER_PATTERN = re.compile(REMEMBER_REGEX, re.IGNORECASE)
FORGET_PATTERN = re.compile(FORGET_REGEX, re.IGNORECASE)
MAT_STICKERS = ['CAACAgIAAxkBAAEEFWdiJkI9efIFCAKgZn9x0WtczrrnFQACtwUAAiMFDQABLgbfFJj7y2sjBA',
                'CAACAgIAAxkBAAEEG2ViKkK_-u5QX7qF6f3stZ531kARhAACBwIAAodOegRVtS-H6GqSQCME',
                'CAACAgIAAxkBAAEEG2diKkLp3KPX0qT_u7PMSuM9bGbjrQACLgEAAodOegRwb7a9j6GCjyME',
                'CAACAgIAAxkBAAEEG2liKkMGlm_U6iEc6y3Q3QZ65uz-XwACOwwAAkADwEn4aMxS-ZzfZCME',
                'CAACAgIAAxkBAAEEG2tiKkNQFeLY83Kvezjzsa9IIwT7TQACHBkAAtjY4QABeejXDAOqS24jBA']

UA_STICKERS = ['CAACAgIAAxkBAAEECn1iIOkPGHzDqt2Zv8I1g-J5o--RjwACFBYAAma5CEmQib3xor7ODCME',
               'CAACAgQAAxkBAAEELMxiMYMQyzcfMz4D_ke8SctLXoJtWwACKAMAAlGMzwGaedJVCQ_ZOCME']

RU_STICKERS = ['CAACAgIAAxkBAAEEFfliJvBGOTKSpwODa-yvxfEzQk5IVgACkgAD1U_lBYNXm1TVqDz1IwQ']

BE_STICKERS = ['CAACAgIAAxkBAAEEGoBiKcICugQT_6tInDE6wuncSv7KiQACTAADHMJYFxRAZGSh7NSaIwQ']

REMEMBER_REPLY = [
    'всегда это знал',
    'понял принял',
    'это точно',
    'само собой',
    'ну это было очевидно'
]

FORGET_REPLY = [
    'ладно молчу',
    'сорян больше не буду так',
    'не знаю зачем я это сказал',
    'да я чет попутал',
    'согласен, это слишком'
]

FAIL_REPLY = [
    'чет я не нихуя не понял',
    'заебал, нормально скажи',
    'чо ты несешь?',
    'ну это херня какая-то'
    'чо тебе надо от меня?'
]

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

        current_time = datetime.datetime.fromtimestamp(x["dt"] + x["timezone"]).strftime('%H:%M')

        # print following values
        return x["name"] + ": " + str(y["temp"]) + "°C. ATM " + str(y["pressure"]) + ". HUM " + str(
            y["humidity"]) + "%. Desc: " + str(x["weather"][0]["description"]) + ". Time: " + current_time

    else:
        return city_name + ": Нет данных"


def weather_bot(update: Updater, context: CallbackContext):
    match = re.search("(П|п)огода в ([\w-]+)", update.message.text)
    if match:
        city = match.group(2)
        weather_message = weather(getenv("WEATHER_TOKEN"), city)
    else:
        cities = (
            'Челябинск',
            'Лиссабон',
            'Мюнхен',
            'Дубай'
        )
        weather_message = '\n'.join([weather(getenv("WEATHER_TOKEN"), city) for city in cities])

    update.message.reply_text(weather_message)


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
    match = re.search(IN_RU_PATTERN, update.message.text)
    if match:
        command_counter = random.randint(1, 3)
        if command_counter == 1:
            reply(update, "in_ru_reply", match.group(0))
    else:
        match = re.search(RU_PATTERN, update.message.text)
        if match:
            command_counter = random.randint(1, 3)
            if command_counter == 1:
                reply(update, "ru_reply", match.group(0))
            else:
                sticker = get_sticker(RU_STICKERS, 5)
                if sticker:
                    update.message.reply_sticker(sticker)


def west(update: Updater, context: CallbackContext):
    match = re.search(WEST_PATTERN, update.message.text)
    if match:
        command_counter = random.randint(1, 3)
        if command_counter == 1:
            reply(update, "west_reply", match.group(0))


def reply(update: Updater, file, format):
    reply_file = open(file, encoding="utf8")
    replies = reply_file.readlines()
    reply_file.close()
    update.message.reply_text(random.choice(replies).format(format))


def remember(update: Updater, context: CallbackContext):
    if update.message.reply_to_message is None:
        text = re.sub(REMEMBER_PATTERN, "", update.message.text)
    else:
        text = update.message.reply_to_message.text
    if remember_reply(update, text, IN_RU_PATTERN, "in_ru_reply"):
        return
    if remember_reply(update, text, RU_PATTERN, "ru_reply"):
        return
    if remember_reply(update, text, WEST_PATTERN, "west_reply"):
        return
    update.message.reply_text(random.choice(FAIL_REPLY))


def remember_reply(update: Updater, text, pattern, file):
    match = re.search(pattern, text)
    if match:
        f = open(file, mode='a', encoding="utf8")
        f.write("\n" + text.replace(match.group(0), "{}"))
        f.close()
        update.message.reply_text(random.choice(REMEMBER_REPLY))
    return match


def forget(update: Updater, context: CallbackContext):
    if forget_reply(update, IN_RU_PATTERN, "in_ru_reply"):
        return
    if forget_reply(update, RU_PATTERN, "ru_reply"):
        return
    if forget_reply(update, WEST_PATTERN, "west_reply"):
        return
    update.message.reply_text(random.choice(FAIL_REPLY))


def forget_reply(update: Updater, pattern, file):
    if update.message.reply_to_message is None:
        return False
    match = re.search(pattern, update.message.reply_to_message.text)
    if match:
        f = open(file, mode='r', encoding="utf8")
        replies = f.readlines()
        f.close()
        text = update.message.reply_to_message.text.replace(match.group(0), "{}")
        try:
            replies.remove(text + '\n')
        except ValueError:
            return
        f = open(file, mode='w', encoding="utf8")
        f.writelines(replies)
        f.close()
        update.message.reply_text(random.choice(FORGET_REPLY))
    return match


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


def fake(update: Updater, context: CallbackContext):
    if random.randint(1, 10) == 5:
        update.message.reply_text('фейк?')


def main():
    my_bot = Updater(getenv("TOKEN"))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(REMEMBER_PATTERN), remember), 0)
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(UA_PATTERN), ukraine), 1)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(MAT_PATTERN), mat), 2)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(RU_PATTERN), russia), 3)
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(BE_PATTERN), belorus), 4)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(WEATHER_PATTERN), weather_bot), 5)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.forwarded, fake), 6)
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.user(user_id={855480940}), shklyar), 7)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(WEST_PATTERN), west), 8)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(FORGET_PATTERN), forget), 9)
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()
