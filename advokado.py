import schedule as schedule
import telebot
import configparser
import re
import time
from datetime import datetime, timedelta
import traceback
import threading
from database import DataBase

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


schedule.every().day.at("13:00").do(go_to_arena)
schedule.every().day.at("00:55").do(ping_for_battle)
# schedule.every(1).minutes.do(ping_for_battle)
schedule.every().day.at("16:55").do(ping_for_battle)
schedule.every().day.at("08:55").do(ping_for_battle)


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


# @bot.message_handler(func=all_castle_bigpisi, commands=['add_trigger'])
@bot.message_handler(commands=['add_trigger'])
def add_trigger(message):
    db = DataBase()
    # = message.chat.id
    # chat_title = message.chat.title
    print(message)
    try:
        if message.reply_to_message:
            if len(message.text.lower()[13:]) >= 3:
                # если не существует такой триггер
                if not db.is_trigger(message.text.lower()[13:]):
                    # добавить в бд
                    if message.reply_to_message.sticker:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "sticker",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.photo:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "photo",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.video:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "video",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.voice:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "voice",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.audio:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "audio",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.document:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "document",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.video_note:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "video_note",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    elif message.reply_to_message.text:
                        data = [message.text.lower()[13:], message.reply_to_message.sticker.file_id, "text",
                                message.from_user.id, message.from_user.username, message.chat.id, message.date]
                        db.add_trigger(data)
                    bot.send_message(message.chat.id, "Триггер '" + message.text[13:] + "' добавлен.")
                else:
                    bot.send_message(message.chat.id, "Триггер '" + message.text[13:] + "' уже занесен в базу.")
            else:
                bot.send_message(message.chat.id, "Не задано имя триггера или оно короче 3 символов")
        else:
            bot.send_message(message.chat.id, "Нет реплейнутого сообщения.")
    except:
        print("don't add_trigger.  ~~~" + str(time.strftime("%d.%m.%y %H:%M:%S", time.localtime()))
              + "\n\n" + traceback.format_exc() + "\n\n")

    db.close()


@bot.message_handler(content_types=['sticker'])
def get_info_about_messages(message):
    print(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'fff':
        message_id = 'CAACAgIAAx0CTFQ_NgACA0dfp93ekYPFqN6jywABe5OZ5snMm4QAAtEAAzDUnRH8Uep02BrfOx4E'
        bot.send_sticker(chat_id=message.chat.id, reply_to_message_id=message.message_id, data=message_id)

    # print(message)
    if message.forward_from is not None and message.forward_from.id == cw_ID and re.search("враждебных существ",
                                                                                           message.text.lower()):
        # (datetime.utcfromtimestamp(int(message.forward_date)).strftime('%Y-%m-%d %H:%M:%S'))
        msg_date = datetime.utcfromtimestamp(int(message.forward_date))
        date_now = datetime.now().utcnow()
        add_time = 3 * 60  # * 60
        if re.search("ambush", message.text.lower()):
            add_time = 5 * 60
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
            unpin_message(message)


# '👾Встреча:\n2 x Forbidden Knight lvl.29\n\n🐢[AD]form2t ⚔:135 🛡:127 Lvl: 29\nТвои результаты в бою:\n🔥Exp: 7\n💰Gold: 1\n❤️Hp: -244\n\nТвои удары: 6/7\nАтаки врагов: 5/9\nЛастхит: 2'
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
                              text="<u><b>Killer's Ambush</b></u>\n\n" + fight_user + "\nTime left "
                                   + '{:02}:{:02}'.format(duration // 60, duration % 60),
                              reply_markup=btn_fight, parse_mode='HTML')

    unpin_message(message)


# Великолепный план, Уолтер. Просто охуенный, если я правильно понял. Надёжный, блядь, как швейцарские часы.
def get_user_fight_ambush(message_id):
    db = DataBase()
    users = db.select_user_fight_ambush(message_id)

    fight_user = ''
    for u in users:
        fight_user += u[0] + '\n'

    db.close()
    return fight_user


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
                                      text="<u><b>Killer's Ambush</b></u>\n\n" + fight_user + "\n" + msg.message.text[
                                                                                                     -15:],
                                      reply_markup=get_two_button_fight(msg.data),
                                      parse_mode='HTML')
        db.close()

    except:
        print("don't insert from callback_inline_first.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")


while True:
    try:
        bot.polling(none_stop=True, interval=1)  # , timeout=20)
    except:
        bot.stop_polling()
        time.sleep(5)
        print("Я умер.  ~~~" + str(
            time.strftime("%d.%m.%y %H:%M:%S", time.localtime())) + "\n\n" + traceback.format_exc() + "\n\n")
