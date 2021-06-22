#!/usr/bin/env python#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import schedule as schedule
import telebot
import configparser
import re
import time
from datetime import datetime, timedelta
import traceback
import threading
from database import DataBase

# import drawer #чекнуть что с этой залупой

config = configparser.ConfigParser()
config.read("config.ini")
# Присваиваем значения внутренним переменным
token = config['Telegram']['token']
ADEPT_ID = int(config['Telegram']['ADEPT_ID'])
cw_ID = int(config['Telegram']['cw_ID'])
bot = telebot.TeleBot(token, True, 4)
last_pinned_msg = None
print('Arbeiten!')


def schedule_pending():
    while True:
        schedule.run_pending()
        time.sleep(1)


thr = threading.Thread(target=schedule_pending)
thr.daemon = False
thr.start()


def go_to_arena():
    print("go_to_arena")
    msg = bot.send_message(ADEPT_ID, 'Время побеждать, гоу на арену')
    bot.pin_chat_message(ADEPT_ID, msg.message_id)


def ping_for_battle():
    try:
        print('try ping_for_battle')
        db = DataBase()
        cur = db.select_data_pin_battle()
        if len(cur) > 0:
            for item in cur:
                bot.send_message(item[1], 'Гоу в битву Adept @' + item[0])
    except:
        print("don't ping_for_battle.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


@bot.message_handler(commands=['start'])
def start_message(message):
    db = DataBase()
    try:
        data = [message.from_user.id, message.from_user.username, message.chat.id]
        db.update_data_user(data)
        db.close()
        bot.send_message(message.chat.id, 'Привет моё сладенькое ADvokADo ' + message.from_user.username)
    except:
        print("don't insert from start_message.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")
        db.close()


@bot.message_handler(commands=['get_me'])
def get_me(message):
    db = DataBase()
    try:
        data = [message.from_user.id, message.chat.id]
        response = db.select_get_me(data)

        if response:
            # exp, gold, stock, hp, lastHit
            result = 'Battle count = ' + str(response[0][0])
            result += '\nExp = ' + str(response[0][1])
            result += '\nGolg = ' + str(response[0][2])
            result += '\nStock = ' + str(response[0][3])
            result += '\nHp = ' + str(response[0][4])
            result += '\nLast Hit = ' + str(response[0][5])
            result += '\nKnockout = ' + str(response[0][6])

            # result = '\n'.join('.'.join(map(str, s)) for s in query)
            bot.send_message(message.chat.id, '<u><b>Summary:</b></u>\n\n' + result, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Ты еще не нюхал пороха, воин ' + message.from_user.username)
        db.close()
    except:
        print("don't get_me.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")
        db.close()


@bot.message_handler(commands=['get_topchik'])
def get_topchik_msg(message):
    get_topchik(False)


def get_topchik(week=True):
    db = DataBase()
    try:
        result = ''
        response = db.select_top_count_battle(0, week)
        if response:
            count = 0
            result += '<u><b>Количество битв с мобами за неделю:</b></u>\n'
            for s in response:
                count += 1
                result += '\n{0}#\t{1} = {2}'.format(str(count), str(s[0]), str(s[1]))

        # response = db.select_top_count_battle(1, week)
        # if response:
        #     result = '<u><b>Самый впрягающийся</b></u>\n{0}\t{1}\n\n'.format(str(response[0][1]), str(response[0][0]))
        #
        # response = db.select_top_last_hit(1, week)
        # if response:
        #     result += '<u><b>Убийца</b></u>\n{0}\t{1}\n\n'.format(str(response[0][1]), str(response[0][0]))
        #
        # response = db.select_top_exp(1, week)
        # if response:
        #     result += '<u><b>Самый опытный</b></u>\n{0}\t{1}\n\n'.format(str(response[0][1]), str(response[0][0]))
        #
        # response = db.select_top_gold(1, week)
        # if response:
        #     result += '<u><b>Самый богатый</b></u>\n{0}\t{1}\n\n'.format(str(response[0][1]), str(response[0][0]))
        #
        # response = db.select_top_stock(1, week)
        # if response:
        #     result += '<u><b>Самый запасливый</b></u>\n{0}\t{1}\n\n'.format(str(response[0][1]), str(response[0][0]))
        #
        # response = db.select_top_hp(1, week)
        # if response:
        #     result += '<u><b>Человек-месиво</b></u>\n{0}\t{1}\n\n'.format(str(response[0][1]), str(response[0][0]))
        #     # result = '\n'.join('.'.join(map(str, s)) for s in query)
        #
        # response = db.select_top_knockout(1, week)
        # if response:
        #     result += '<u><b>Человек-зомби</b></u>\n{0}\t{1}\n\n'.format(str(response[0][1]), str(response[0][0]))
            # result = '\n'.join('.'.join(map(str, s)) for s in query)

        db.close()
        if result != '':
            bot.send_message(ADEPT_ID, result, parse_mode='HTML')
        else:
            bot.send_message(ADEPT_ID, 'Нет еще топчика в этом чатике)')
    except:
        print("don't get_topchik.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")
        db.close()


@bot.message_handler(commands=['get_all'])
def get_all(message):
    db = DataBase()
    try:

        response = db.select_get_all()

        if response:
            result = '\n'.join('\t'.join(map(str, s)) for s in response)
            # drawer.create_image(result)
            bot.send_photo(message.chat.id, photo=open('result.png', 'rb'))
            # result = '\n'.join('.'.join(map(str, s)) for s in query)
            # bot.send_message(message.chat.id, '<u><b>Summary:</b></u>\n\n' + result, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Случилась какая-то херня с get_all')
        db.close()
    except:
        print("don't get_all.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")
        db.close()


@bot.message_handler(content_types=["new_chat_members"])
def add_new_member(message):
    try:
        # user_list = message.new_chat_members
        # print(user_list)
        for user in message.new_chat_members:
            bot.send_message(message.chat.id, "Welcome to Hell, @{0}!".format(user.username))
    except:
        print("don't add_new_member.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


@bot.message_handler(content_types=["pinned_message"])
def save_pinned_message(message):
    try:
        global last_pinned_msg
        last_pinned_msg = message.pinned_message
    except:
        print("don't save_pinned_message.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


@bot.message_handler(content_types=["left_chat_member"])
def kick_member(message):
    try:
        bot.send_message(message.chat.id, "Go Home, {0}!".format(message.left_chat_member.username))
    except:
        print("don't kick_member.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


@bot.message_handler(commands=['ping'])
def start_message(message):
    # print(message.chat.id)
    bot.send_message(message.chat.id, 'Живее всех живых')


@bot.message_handler(commands=['random'])
def get_random(message):
    try:
        random.seed(message.message_id)
        digit = message.text.lower()[7:].strip()
        if digit.isdigit() and int(digit) > 0:
            bot.send_message(message.chat.id, str(random.randint(1, int(digit))),
                             reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, 'Параметр не является числом, либо он меньше 1',
                             reply_to_message_id=message.message_id)
    except:
        print("don't get_random.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")


# @bot.message_handler(func=all_castle_bigpisi, commands=['add_trigger'])
@bot.message_handler(commands=['add_trigger'])
def add_trigger(message):
    try:
        if message.reply_to_message:
            if len(message.text.lower()[13:]) >= 3:  # and is_good_name_for_trigger(message.text.lower()):
                db = DataBase()

                if not db.is_trigger(message.text.lower()[13:], message.chat.id):
                    # добавить в бд
                    if message.reply_to_message.sticker:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "sticker",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.photo:
                        data = [message.text.lower()[13:], message.reply_to_message.photo[0].file_id, "photo",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.video:
                        data = [message.text.lower()[13:], message.reply_to_message.video.file_id, "video",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.voice:
                        data = [message.text.lower()[13:], message.reply_to_message.voice.file_id, "voice",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.audio:
                        data = [message.text.lower()[13:], message.reply_to_message.audio.file_id, "audio",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.document:
                        data = [message.text.lower()[13:], message.reply_to_message.document.file_id, "document",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.video_note:
                        data = [message.text.lower()[13:], message.reply_to_message.video_note.file_id, "video_note",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.text:
                        data = [message.text.lower()[13:], message.reply_to_message.text, "text",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    bot.send_message(message.chat.id, "Триггер '" + message.text[13:] + "' добавлен.")

                else:
                    bot.send_message(message.chat.id, "Триггер '" + message.text[13:] + "' уже занесен в базу.")

                db.close()
            else:
                bot.send_message(message.chat.id, "Неккоректное имя триггера менее 3 символов")
        else:
            bot.send_message(message.chat.id, "Нет реплейнутого сообщения.")
    except:
        db.close()
        print("don't add_trigger.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")


@bot.message_handler(commands=['del_trigger'])
def del_trigger(message):
    try:
        db = DataBase()
        if db.is_trigger(message.text.lower()[13:], message.chat.id):  # если триггер существует
            db.delete_trigger(message.text.lower()[13:], message.chat.id)  # удалить триггер
            bot.send_message(message.chat.id, "Триггер '" + message.text[13:] + "' удалён.")
        else:
            bot.send_message(message.chat.id, "Триггера '" + message.text[13:] + "' не существует.")
        db.close()
    except:
        db.close()
        print("don't del_trigger.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")


# @bot.message_handler(content_types=['sticker'])
# def get_info_about_messages(message):
#    print(message)

# def is_good_name_for_trigger(text):
#   match = re.match('^[а-яА-ЯёЁa-zA-Z0-9]+$', text)
#  return bool(match)

def find_trigger_in_message(message):
    try:
        # if is_good_name_for_trigger(message.text.lower()):
        db = DataBase()
        txt = message.text.lower()
        digit = '1'
        get = False
        sendTo = message.chat.id

        if re.search("дайлс", message.text.lower()):
            sendTo = message.from_user.id

        if re.search("дай", message.text.lower()):
            if txt.split(' ')[-1].isdigit():
                digit = int(txt.split(' ')[-1])
            txt = ' '.join(txt.split(' ')[:-1])
            get = True

        response = db.is_trigger(txt, message.chat.id)

        if response:
            trigger_type = ''.join(response[0][0])
            trigger_value = ''.join(response[0][1])

            if trigger_type == "text" and not get:
                bot.send_message(message.chat.id, trigger_value)
            if trigger_type == "text" and get:
                bot.send_message(sendTo, '<pre>/g_withdraw ' + ' '.join(multiply(trigger_value.split(' '),
                                                                                          int(digit))) + '</pre>',
                                 parse_mode='HTML')
            elif trigger_type == "sticker":
                bot.send_sticker(message.chat.id, trigger_value)
            elif trigger_type == "voice":
                bot.send_voice(message.chat.id, trigger_value)
            elif trigger_type == "audio":
                bot.send_audio(message.chat.id, trigger_value)
            elif trigger_type == "video":
                bot.send_video(message.chat.id, trigger_value)
            elif trigger_type == "document":
                bot.send_document(message.chat.id, trigger_value)
            elif trigger_type == "photo":
                bot.send_photo(message.chat.id, trigger_value)
            elif trigger_type == "video_note":
                bot.send_video_note(message.chat.id, trigger_value)
        elif message.text.lower() == "список триггеров":
            query = db.get_trigger_list(message.chat.id)
            result = '\n'.join('.'.join(map(str, s)) for s in query)
            bot.send_message(message.chat.id, '<u><b>Список тригеров:</b></u>\n' + result, parse_mode='HTML')

        db.close()
    except:
        print("don't find_trigger_in_message.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")


def multiply(arr, ind):
    return [str(int(x) * ind) if i % 2 == 1 else x for i, x in enumerate(arr)]


@bot.message_handler(content_types=['sticker'])
def congratulation_level_up(message):
    if message.sticker.set_name == 'ChatwarsLevels':
        bot.send_message(message.chat.id, text="Грац! Совсем большой стал, @{0}!".format(message.from_user.username,
                                                                                         reply_to_message_id=message.message_id))
    elif message.sticker.set_name == 'ChatwarsLevelsF':
        bot.send_message(message.chat.id, text="Грац! Совсем большая стала, @{0}!".format(message.from_user.username,
                                                                                          reply_to_message_id=message.message_id))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.forward_from is None:
        find_trigger_in_message(message)

    print(message)
    if message.forward_from is not None and message.forward_from.id == cw_ID and re.search("встреча",
                                                                                           message.text.lower()):

        data = [message.message_id, message.forward_date, message.from_user.id, message.from_user.username,
                message.chat.id]
        data.extend(get_about_msg(message.text))
        data.append(message.date)

        db = DataBase()
        response = db.select_data_fight_ambush_result(data)  # 'forward_date': 1605379349

        # if len(response) == 0:
        if not response:
            db.insert_data_fight_ambush_result(data)
        else:
            bot.send_message(message.chat.id, text="Репорт уже занесен в базу",
                             reply_to_message_id=message.message_id)

    if message.forward_from is not None and message.forward_from.id == cw_ID and re.search("враждебных существ",
                                                                                           message.text.lower()):
        # (datetime.utcfromtimestamp(int(message.forward_date)).strftime('%Y-%m-%d %H:%M:%S'))
        msg_date = datetime.utcfromtimestamp(int(message.forward_date))
        date_now = datetime.now().utcnow()
        add_time = 3 * 60  # * 600
        if re.search("ambush", message.text.lower()):
            add_time = 6 * 60
        if msg_date + timedelta(seconds=add_time) > date_now:
            bot.pin_chat_message(message.chat.id, message.message_id)

            ####################################
            text = message.text
            fight = text[text.find('/fight'):len(text)]
            btn_fight = get_two_button_fight(fight)

            delta = msg_date + timedelta(seconds=add_time) - date_now
            msg = bot.send_message(message.chat.id, text="<u><b>Killer's Ambush</b></u>" + "\n\nTime left "
                                                         + '{:02}:{:02}'.format(delta.seconds // 60,
                                                                                delta.seconds % 60),
                                   reply_markup=btn_fight, parse_mode='HTML')

            thread_timer = threading.Thread(target=check_send_messages, args=(delta.seconds, 10, msg, btn_fight))
            thread_timer.daemon = False
            thread_timer.start()

        else:
            bot.pin_chat_message(message.chat.id, message.message_id)
            #unpin_message(message)


# return info from message.text
# [msg.message.message_id, msg.from_user.id,msg.from_user.username, msg.chat.id]
def get_about_msg(txt):
    try:
        exp = re.search('Exp:.*?(\d+)', txt)
        gold = re.search('Gold:.*?(\d+)', txt)
        stock = re.search('Stock:.*?(\d+)', txt)
        hp = re.search('Hp:.*?(-?\d+)', txt)
        last_hit = re.search('Ластхит:.*?(\d+)', txt)
        knockout = re.search('В нокауте:.*?(\d+)', txt)

        print(exp, gold, stock, hp, last_hit)
        exp = int(exp.group(1)) if exp else 0
        gold = int(gold.group(1)) if gold else 0
        stock = int(stock.group(1)) if stock else 0
        hp = int(hp.group(1)) if hp else 0
        last_hit = int(last_hit.group(1)) if last_hit else 0
        knockout = int(knockout.group(1)) if knockout else 0
        return [exp, gold, stock, hp, last_hit, knockout]
    except:
        print("don't get_about_msg.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")


def unpin_message(message):
    try:
        bot.unpin_chat_message(message.chat.id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text="Сообщение устарело")
        # global last_pinned_msg
        # if last_pinned_msg is not None:
        #    bot.pin_chat_message(message.chat.id, last_pinned_msg.message_id)
        #    last_pinned_msg = None
    except:
        print("don't unpin_message  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


def get_two_button_fight(query):
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_1 = telebot.types.InlineKeyboardButton(text="SendToCW", switch_inline_query=query)
    btn_2 = telebot.types.InlineKeyboardButton(text="GoFight", callback_data=query)
    keyboard.add(btn_1, btn_2)
    return keyboard


# это функция отправки сообщений по таймеру
def check_send_messages(duration, dt, message, btn_fight):
    while duration:
        # пауза между проверками, чтобы не загружать процессор
        time.sleep(dt)
        duration -= dt
        if duration < 0:
            duration = 0

        fight_user = get_user_fight_ambush(message.message_id)
        bot.edit_message_text(chat_id=ADEPT_ID, message_id=message.message_id,
                              text="<u><b>Killer's Ambush</b></u>\n\n" + fight_user + "\n\nTime left "
                                   + '{:02}:{:02}'.format(duration // 60, duration % 60),
                              reply_markup=btn_fight, parse_mode='HTML')

    unpin_message(message)


# Великолепный план, Уолтер. Просто охуенный, если я правильно понял. Надёжный, блядь, как швейцарские часы.
def get_user_fight_ambush(message_id):
    try:
        db = DataBase()
        users = db.select_user_fight_ambush(message_id)
        fight_user = '\n'.join('.'.join(map(str, s)) for s in users)
        db.close()
        return fight_user
    except:
        print("don't get_user_fight_ambush.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


@bot.callback_query_handler(func=lambda msg: re.search('fight', msg.data))
def callback_inline_first(msg):
    try:
        db = DataBase()
        data = [msg.from_user.id, msg.message.message_id]
        cur = db.select_data_fight_ambush(data)
        if len(cur) > 0:
            bot.answer_callback_query(msg.id, show_alert=True, text="НЕ тыкай больше")
        else:
            tmp = db.select_count_data_fight_ambush(msg.message.message_id)

            if tmp[0][0] >= 4:
                bot.answer_callback_query(msg.id, show_alert=True, text="В следующий раз доблестный воин")
            else:
                data = [msg.message.message_id, msg.from_user.id, msg.from_user.username, msg.message.chat.id]
                db.insert_data_ambush(data)

                fight_user = get_user_fight_ambush(msg.message.message_id)

                bot.edit_message_text(chat_id=ADEPT_ID, message_id=msg.message.message_id,
                                      text="<u><b>Killer's Ambush</b></u>\n\n" + fight_user + "\n\n" + msg.message.text[
                                                                                                       -15:],
                                      reply_markup=get_two_button_fight(msg.data),
                                      parse_mode='HTML')
        db.close()

    except:
        print("don't insert from callback_inline_first.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


schedule.every().monday.at("12:00").do(get_topchik)
# schedule.every().thursday.at("06:15").do(get_topchik)
schedule.every().day.at("13:00").do(go_to_arena)
schedule.every().day.at("00:55").do(ping_for_battle)
# schedule.every(1).minutes.do(ping_for_battle)
schedule.every().day.at("16:55").do(ping_for_battle)
schedule.every().day.at("08:55").do(ping_for_battle)

while True:
    try:
        bot.polling(none_stop=True, interval=1)  # , timeout=20)
    except:
        bot.stop_polling()
        time.sleep(5)
        print("Бот пал.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")
