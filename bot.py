import random
import re
from os import getenv

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

load_dotenv()
RU_REGEX = 'россия|путин|медведев|москва|царь|рф'
UA_REGEX = 'украин|хохл|хохол|война|донбас'
BE_REGEX = 'батьк|белорус|лукашенк'
MAT_REGEX = r"""(?iu)\b((у|[нз]а|(хитро|не)?вз?[ыьъ]|с[ьъ]|(и|ра)[зс]ъ?|(о[тб]|под)[ьъ]?|(.\B)+?[оаеи])?-?([её]б(?!о[рй])|и[пб][ае][тц]).*?|(н[иеа]|([дп]|верт)о|ра[зс]|з?а|с(ме)?|о(т|дно)?|апч)?-?ху([яйиеёю]|ли(?!ган)).*?|(в[зы]|(три|два|четыре)жды|(н|сук)а)?-?бл(я(?!(х|ш[кн]|мб)[ауеыио]).*?|[еэ][дт]ь?)|(ра[сз]|[зн]а|[со]|вы?|п(ере|р[оие]|од)|и[зс]ъ?|[ао]т)?п[иеё]зд.*?|(за)?п[ие]д[аое]?р(ну.*?|[оа]м|(ас)?(и(ли)?[нщктл]ь?)?|(о(ч[еи])?|ас)?к(ой)|юг)[ауеы]?|манд([ауеыи](л(и[сзщ])?[ауеиы])?|ой|[ао]вошь?(е?к[ауе])?|юк(ов|[ауи])?)|муд([яаио].*?|е?н([ьюия]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[еёо]й))\b"""
UA_PATTERN = re.compile(UA_REGEX, re.IGNORECASE)
MAT_PATTERN = re.compile(MAT_REGEX, re.IGNORECASE)
RU_PATTERN = re.compile(RU_REGEX, re.IGNORECASE)
BE_PATTERN = re.compile(BE_REGEX, re.IGNORECASE)

MAT_STICKERS = ['CAACAgIAAxkBAAEEFWdiJkI9efIFCAKgZn9x0WtczrrnFQACtwUAAiMFDQABLgbfFJj7y2sjBA',
                'CAACAgIAAxkBAAEEG2ViKkK_-u5QX7qF6f3stZ531kARhAACBwIAAodOegRVtS-H6GqSQCME',
                'CAACAgIAAxkBAAEEG2diKkLp3KPX0qT_u7PMSuM9bGbjrQACLgEAAodOegRwb7a9j6GCjyME',
                'CAACAgIAAxkBAAEEG2liKkMGlm_U6iEc6y3Q3QZ65uz-XwACOwwAAkADwEn4aMxS-ZzfZCME',
                'CAACAgIAAxkBAAEEG2tiKkNQFeLY83Kvezjzsa9IIwT7TQACHBkAAtjY4QABeejXDAOqS24jBA']


def years(update: Updater, context: CallbackContext):
    update.message.reply_sticker('CAACAgIAAxkBAAEECn1iIOkPGHzDqt2Zv8I1g-J5o--RjwACFBYAAma5CEmQib3xor7ODCME')


def mat(update: Updater, context: CallbackContext):
    sticker = random.choice(MAT_STICKERS)
    update.message.reply_sticker(sticker)


def russia(update: Updater, context: CallbackContext):
    update.message.reply_sticker('CAACAgIAAxkBAAEEFfliJvBGOTKSpwODa-yvxfEzQk5IVgACkgAD1U_lBYNXm1TVqDz1IwQ')


def belorus(update: Updater, context: CallbackContext):
    update.message.reply_sticker('CAACAgIAAxkBAAEEGoBiKcICugQT_6tInDE6wuncSv7KiQACTAADHMJYFxRAZGSh7NSaIwQ')

def shklyar(update: Updater, context: CallbackContext):
    command_counter = random.randint(1, 10)
    if command_counter == 9:
        update.message.reply_text(
            'ну просто реально достал твое нытье, Леха, ты же мужик, начни делать что-то')


def main():
    my_bot = Updater(getenv("TOKEN"))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(UA_PATTERN), years), 0)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(MAT_PATTERN), mat), 0)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(RU_PATTERN), russia), 0)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex(BE_PATTERN), belorus), 0)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.user(user_id={855480940}), shklyar), 1)
    my_bot.start_polling()
    my_bot.idle()


main()
