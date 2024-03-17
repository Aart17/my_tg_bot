import datetime
import re

import telebot
from telebot import types

from fast_func import *
from admin_inf import my_sup_api
from database_func import *
from main_bot import bot as main_bot

bot = telebot.TeleBot(my_sup_api)

an_context = {}
mem_context = {}
admin_context = {}
notif_context = {}
rofl_types = ['Про негров', 'Про евреев', 'Про животных', 'Черный юмор', 'Пошлые', 'Обычный']


def add_an_type(msg):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    mess = 'Выберете тип добавляемого анекдота'
    for i in rofl_types:
        markup.add(i)
    markup.add('Отмена')
    try:
        msg = bot.send_message(msg.message.chat.id, mess, reply_markup=markup)
    except AttributeError:
        msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, add_an_text)


def add_an_text(msg):
    if msg.text in rofl_types:
        an_context[msg.chat.id] = {'type': msg.text}
        mess = 'Введите текст анекдота'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Отмена')
        msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
        bot.register_next_step_handler(msg, add_an_confirm)
    elif msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)
    else:
        mess = 'Не правильно введен тип, выберите его из предложенного списка'
        msg = bot.send_message(msg.chat.id, mess)
        add_an_type(msg)


def add_an_confirm(msg):
    if msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)
    elif msg.text:
        an_context[msg.chat.id]['text'] = msg.text
    else:
        return send_mess(bot, msg, 'Отправьте текст, операция отменена')
    an_context[msg.chat.id]['author'] = msg.from_user.first_name
    mess = f'''
Вы уверены что хотите добавить этот текст в базу данных?
Ваш анекдот выглядит так:
Тип: {an_context[msg.chat.id]['type']}
Создатель: {an_context[msg.chat.id]['author']}
Время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
Текст: {an_context[msg.chat.id]['text']}
'''
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Да', 'Нет')
    msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, add_an_finish)


def add_an_finish(msg):
    if msg.text == 'Да':
        add_anecdot(an_context=an_context[msg.chat.id])
        mess = 'Анекдот успешно добавлен'
    else:
        mess = 'Операция отменена'
    an_context[msg.chat.id].clear()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    send_mark_mess(bot, msg, mess, markup)
    start(msg)


def add_mem_type(msg):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    mess = 'Выберете тип добавляемого мема'
    for i in rofl_types:
        markup.add(i)
    markup.add('Отмена')
    try:
        msg = bot.send_message(msg.message.chat.id, mess, reply_markup=markup)
    except AttributeError:
        msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, add_mem_image)


def add_mem_image(msg):
    if msg.text in rofl_types:
        mem_context[msg.chat.id] = {'type': msg.text}
        mess = 'Отправьте ваш мем'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Отмена')
        msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
        bot.register_next_step_handler(msg, add_mem_confirm)
    elif msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)
    else:
        mess = 'Не правильно введен тип, выберите его из предложенного списка'
        msg = bot.send_message(msg.chat.id, mess)
        add_mem_type(msg)


def add_mem_confirm(msg):
    if msg.text and msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)
    try:
        mem_context[msg.chat.id]['image_id'] = msg.photo[-1].file_id
    except TypeError:

        mess = 'Неправильный тип контента, проверьте что отправили изображение как файл и нажали кнопку "Сжать ' \
               'изображение" '
        bot.send_message(msg.chat.id, mess)
        return

    mem_context[msg.chat.id]['author'] = msg.from_user.first_name
    mess = f'''
Вы уверены что хотите добавить эту информацию в базу данных?
Ваш анекдот выглядит так:
Тип: {mem_context[msg.chat.id]['type']}
Создатель: {mem_context[msg.chat.id]['author']}
Время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
Мем: (Выше)
'''
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Да', 'Нет')
    msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, add_mem_finish)


def add_mem_finish(msg):
    if msg.text == 'Да':
        mess = 'Мем успешно добавлен'
        file_info = bot.get_file(mem_context[msg.chat.id]['image_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        downloaded_path = f'image/admin_{mem_context[msg.chat.id]["author"]}_image_{msg.id}.jpg'

        with open(downloaded_path, 'wb+') as new_file:
            new_file.write(downloaded_file)

        mem_context[msg.chat.id]['image_path'] = downloaded_path
        add_mem(mem_context[msg.chat.id])
    else:
        mess = 'Операция отменена'
    mem_context[msg.chat.id].clear()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    send_mark_mess(bot, msg, mess, markup)
    start(msg)


def add_new_admin(msg):
    mess = 'Введите user_tag пользователя которого хотите добавить'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Отмена')
    try:
        msg = bot.send_message(msg.message.chat.id, mess, reply_markup=markup)
    except AttributeError:
        msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, add_new_admin_confirm)


def add_new_admin_confirm(msg):
    if msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)
    if not msg.text:
        return add_new_admin(msg)
    if msg.text[0] == '@':
        tag = msg.text[1:]
    else:
        tag = msg.text

    admin_context[msg.chat.id] = {'tag': tag}
    admin_context[msg.chat.id]['adding'] = msg.from_user.username
    admin_context[msg.chat.id]['time_upd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    mess = f'''Вы уверены что хотите добавить нового админа? В БД будет добавлена такая информация:
Тег: {admin_context[msg.chat.id]['tag']}
Время: {admin_context[msg.chat.id]['time_upd']}
Добавляющий: @{admin_context[msg.chat.id]['adding']}
'''
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Да', 'Нет')
    msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, add_new_admin_finish)


def add_new_admin_finish(msg):
    if msg.text == 'Да':
        add_admin(admin_context[msg.chat.id])
        mess = 'Новый админ успешно добавлен'
    else:
        mess = 'Операция отменена'
    admin_context[msg.chat.id].clear()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    send_mark_mess(bot, msg, mess, markup)
    start(msg)


def notif_start(msg):
    mess = 'Введите текст для массового оповещения'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Отмена')
    try:
        msg = bot.send_message(msg.message.chat.id, mess, reply_markup=markup)
    except AttributeError:
        msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, notif_confirm)


def notif_confirm(msg):
    if not msg.text:
        send_mess(bot, msg, 'Отправьте только текст')
        return notif_start(msg)
    if msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)
    notif_context[msg.chat.id] = {'text': msg.text}
    notif_context[msg.chat.id]['time'] = {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
    notif_context[msg.chat.id]['admin_name'] = msg.from_user.first_name
    notif_context[msg.chat.id]['admin_tag'] = msg.from_user.first_name
    mess = f'''
Вы уверены что хотите отправить такое оповещение?
Отправленный текст будет выглядеть так:
{notif_context[msg.chat.id]['text']}
Создатель: {notif_context[msg.chat.id]['admin_name']}
    '''
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Да', 'Нет')
    msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, notif_finish)


def notif_finish(msg):
    if msg.text == 'Да':
        mess = 'Оповещение рассылается'
        add_notifications(notif_context[msg.chat.id])
        send_notifications(text=notif_context[msg.chat.id]['text'], name=notif_context[msg.chat.id]['admin_name'])
    else:
        mess = 'Оповещение отменено'
    notif_context[msg.chat.id].clear()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('/start')
    send_mark_mess(bot, msg, mess, markup)
    start(msg)


def send_notifications(text, name):
    chats_id = get_chats()
    mess = f"{text} \nСоздатель: {name}"
    for i in chats_id:
        main_bot.send_message(chat_id=i[0], text=mess)


def check_offer_start(msg):
    mess = 'Выберите дату'
    bad_dates = get_offer_dates()
    dates = []
    for i in bad_dates:
        if i[0][:10] not in dates:
            dates.append(i[0][:10])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in dates:
        markup.add(i)
    markup.add('Отмена')
    try:
        msg = bot.send_message(msg.message.chat.id, mess, reply_markup=markup)
    except AttributeError:
        msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, check_offer_sel_offers, dates)


def check_offer_sel_offers(msg, dates: []):
    if not msg.text:
        send_mess(bot, msg, 'Отправьте только текст')
        return check_offer_start(msg)
    if msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)
    if msg.text not in dates:
        return send_mess(bot, msg, 'Выберете только даты из предложенного списка')
    mess = 'Выберите обращение'
    offers = get_offers_with_date(date=msg.text)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in offers:
        markup.add(f'id:{offers[i]["id"]} Тема: {offers[i]["theme"]} От: {offers[i]["time"]}')
    markup.add('Отмена')
    msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, check_offer_send)


def check_offer_send(msg: types.Message):
    if not msg.text:
        mess = 'Вы не ввели текст'
        send_mess(bot, msg, mess)
        return check_offer_start(msg)
    elif msg.text == 'Отмена':
        mess = 'Операция отменена'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/start')
        send_mark_mess(bot, msg, mess, markup)
        return start(msg)

    id_match = re.search(r'id:(\d+)', msg.text)
    if not id_match:
        return bot.send_message(msg.chat.id, 'Выберите только обращение из списка')
    id = id_match.group(1)
    offer = get_offer(int(id))[0]
    theme = offer[1]
    time = offer[6]
    us_tag = offer[7]
    if offer[3]:
        mess = f'''Тема: {theme}
Время: {time}
Автор: {us_tag}
Контент: Приложен выше
'''
        photo_path = offer[3]  # путь к вашему файлу с изображением
        photo = open(photo_path, 'rb')
        bot.send_photo(msg.chat.id, photo, caption=mess)
        photo.close()
    else:
        mess = f'''Тема: {theme}
Время: {time}
Автор: {us_tag}
Контент {offer[2]}: 
'''
        send_mess(bot, msg, mess)


callback_data_types = {'check_offer': lambda msg: check_offer_start(msg),
                       'add_an': lambda msg: add_an_type(msg),
                       'add_mem': lambda msg: add_mem_type(msg),
                       'add_admin': lambda msg: add_new_admin(msg),
                       'notification': lambda msg: notif_start(msg)}


@bot.message_handler(content_types=["audio", "document", "sticker", "video", "video_note", "voice", "location",
                                    "contact", "new_chat_members", "left_chat_member", "new_chat_title",
                                    "new_chat_photo", "supergroup_chat_created", "group_chat_created",
                                    "delete_chat_photo", "migrate_from_chat_id", "migrate_to_chat_id",
                                    "channel_chat_created", "pinned_message", "web_app_data"])
def idk(sender):
    mess = "Простите я не могу распознать такой тип сообщений"
    send_mess(bot, sender, mess)


@bot.message_handler(commands=['start'])
def start(msg):
    if check_admin(msg.from_user.username):
        mess = 'У вас недостаточно прав для использования бота'
        send_mess(bot, msg, mess)
    else:
        if check_admin_first(msg.from_user.username) is False:
            upd_admin_inf(msg.from_user.username, msg.from_user.first_name, msg.from_user.id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        mess = f"<b>Здравствуйте господин, что вы хотите сделать?</b>"
        btn1 = types.InlineKeyboardButton("Прочитать обратную связь", callback_data='check_offer')
        btn2 = types.InlineKeyboardButton("Добавить анекдот", callback_data='add_an')
        btn3 = types.InlineKeyboardButton("Добавить мем", callback_data='add_mem')
        btn4 = types.InlineKeyboardButton('Добавить админа', callback_data='add_admin')
        btn5 = types.InlineKeyboardButton('Массовое оповещение', callback_data='notification')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        send_mark_mess(bot, msg, mess, markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(msg):
    if msg.message:
        if check_admin(msg.message.from_user.username):
            mess = 'У вас недостаточно прав для использования бота'
            send_mess(bot, msg, mess)
        if msg.data in callback_data_types:
            callback_data_types[msg.data](msg)


async def as_start_supbot():
    await bot.polling(none_stop=True)


def start_supbot():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    start_supbot()
