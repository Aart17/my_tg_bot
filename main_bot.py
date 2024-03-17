import datetime

import telebot
from telebot import types

from fast_func import *
from admin_inf import *
from database_func import *

bot = telebot.TeleBot(my_api)

anecdots = {}
mems = {}
offer_context = {}
rofl_types = {'Про негров': 'negr',
              'Про евреев': 'evr',
              'Про животных': 'anim',
              'Черный юмор': 'black',
              'Пошлые': 'vulg',
              'Обычный': 'simp', }


def find_k_by_v(dictionary: dict, value):
    for key, val in dictionary.items():
        if val == value:
            return key


def base_markup_btn(callback_type: str, rofl_type: str, likes: int):
    if callback_type == 'Anecdot':
        markup = types.InlineKeyboardMarkup(row_width=3)
        back_btn = types.InlineKeyboardButton('Назад',
                                              callback_data=f'an_{find_k_by_v(rofl_types, rofl_type)}_back')
        like_btn = types.InlineKeyboardButton(f"{likes}❤ Лайк",
                                              callback_data=f'an_like_None')
        next_btn = types.InlineKeyboardButton('Следующий',
                                              callback_data=f'an_{find_k_by_v(rofl_types, rofl_type)}_next')
        markup.add(back_btn, like_btn, next_btn)
        return markup
    elif callback_type == 'Mem':
        markup = types.InlineKeyboardMarkup(row_width=3)
        back_btn = types.InlineKeyboardButton('Назад',
                                              callback_data=f'mem_{find_k_by_v(rofl_types, rofl_type)}_back')
        like_btn = types.InlineKeyboardButton(f"{likes}❤ Лайк",
                                              callback_data=f'mem_like_None')
        next_btn = types.InlineKeyboardButton('Следующий',
                                              callback_data=f'mem_{find_k_by_v(rofl_types, rofl_type)}_next')
        markup.add(back_btn, like_btn, next_btn)
        return markup


def anecdot(msg):
    btns = []
    markup = types.InlineKeyboardMarkup(row_width=3)
    mess = 'Выберете тип анекдота'
    for i in rofl_types:
        btn = types.InlineKeyboardButton(i, callback_data=f'an_{rofl_types[i]}')
        btns.append(btn)
    btns.append(types.InlineKeyboardButton('<-- Назад', callback_data='back'))
    markup.add(btns[0], btns[1], btns[2], btns[3], btns[4], btns[5], btns[6])
    send_mark_mess(bot, msg, mess, markup)


def send_an(msg, action='start'):
    if action == 'start':
        w_id = anecdots[msg.from_user.id]['watch_id']

        for i in anecdots[msg.from_user.id]['anecdots']:
            if w_id == i[0]:
                an = anecdots[msg.from_user.id]['anecdots'][anecdots[msg.from_user.id]['anecdots'].index(i)][1]
                break
        mess = f"{an['text']} \nАвтор: {an['author']} \nТип: {an['an_type']}"
        markup = base_markup_btn('Anecdot', an["an_type"], an['likes'])
        send_mark_mess(bot, msg, mess, markup)

    elif action == 'next':
        w_id = anecdots[msg.from_user.id]['watch_id']
        for i in anecdots[msg.from_user.id]['anecdots']:
            if w_id == i[0]:
                an = anecdots[msg.from_user.id]['anecdots'][anecdots[msg.from_user.id]['anecdots'].index(i)][1]
                break
        mess = f"{an['text']} \nАвтор: {an['author']} \nТип: {an['an_type']}"
        markup = base_markup_btn('Anecdot', an["an_type"], an['likes'])
        edit_txt_mess(bot, msg, mess, markup)

    elif action == 'back':
        w_id = anecdots[msg.from_user.id]['watch_id']
        for i in anecdots[msg.from_user.id]['anecdots']:
            if w_id == i[0]:
                an = anecdots[msg.from_user.id]['anecdots'][anecdots[msg.from_user.id]['anecdots'].index(i)][1]
                break
        mess = f"{an['text']} \nАвтор: {an['author']} \nТип: {an['an_type']}"
        markup = base_markup_btn('Anecdot', an["an_type"], an['likes'])
        edit_txt_mess(bot, msg, mess, markup)


def next_10_an(msg, w_id, an_type):
    ans = get_an(an_type, w_id)
    true_ans = []
    ids = []

    for i in ans:
        item = [i[0], {
            'an_type': i[1],
            'text': i[2],
            'likes': i[3],
            'author': i[4]}]
        ids.append(i[0])
        true_ans.append(item)
        iter_ids = iter(ids)

    try:
        if len(ans) == 0:
            raise StopIteration
        next(iter_ids)
    except StopIteration:
        return send_finish_mess(bot, msg.chat.id)

    anecdots[msg.message.from_user.id] = {'watch_id': true_ans[0][0],
                                          'anecdots': true_ans,
                                          'iter_ids': iter_ids,
                                          'ids': ids, }
    send_an(msg.message, action='next')


def back_10_an(msg, w_id, an_type):
    ans = get_an(an_type, w_id, True)
    ans.reverse()
    true_ans = []
    ids = []

    for i in ans:
        item = [i[0], {
            'an_type': i[1],
            'text': i[2],
            'likes': i[3],
            'author': i[4]}]
        ids.append(i[0])
        true_ans.append(item)
        iter_ids = iter(ids)

    try:
        if len(ans) == 0:
            raise StopIteration
        for i in range(10):
            next(iter_ids)
    except StopIteration:
        return send_finish_mess(bot, msg.message.chat.id)

    anecdots[msg.message.from_user.id] = {'watch_id': true_ans[-1][0],
                                          'anecdots': true_ans,
                                          'iter_ids': iter_ids,
                                          'ids': ids, }
    send_an(msg.message, action='back')


def mem(msg):
    btns = []
    markup = types.InlineKeyboardMarkup(row_width=3)
    mess = 'Выберете тип мема'
    for i in rofl_types:
        btn = types.InlineKeyboardButton(i, callback_data=f'mem_{rofl_types[i]}')
        btns.append(btn)
    btns.append(types.InlineKeyboardButton('<-- Назад', callback_data='back'))
    markup.add(btns[0], btns[1], btns[2], btns[3], btns[4], btns[5], btns[6])
    send_mark_mess(bot, msg, mess, markup)


def send_mem(msg, action='start'):
    if action == 'start':
        w_id = mems[msg.from_user.id]['watch_id']

        for i in mems[msg.from_user.id]['mems']:
            if w_id == i[0]:
                mem = mems[msg.from_user.id]['mems'][mems[msg.from_user.id]['mems'].index(i)][1]
                break
        photo = open(mem['path'], 'rb')
        text_mess = f"Автор: {mem['author']} \nТип: {mem['mem_type']}"
        markup = base_markup_btn('Mem', mem["mem_type"], mem['likes'])
        bot.send_photo(msg.chat.id, photo, text_mess, reply_markup=markup)

    elif action == 'next':
        w_id = mems[msg.from_user.id]['watch_id']
        for i in mems[msg.from_user.id]['mems']:
            if w_id == i[0]:
                mem = mems[msg.from_user.id]['mems'][mems[msg.from_user.id]['mems'].index(i)][1]
                break
        photo = open(mem['path'], 'rb')
        text_mess = f"Автор: {mem['author']} \nТип: {mem['mem_type']}"
        markup = base_markup_btn('Mem', mem["mem_type"], mem['likes'])
        try:
            bot.send_photo(msg.chat.id, photo, text_mess, reply_markup=markup)
        except telebot.apihelper.ApiTelegramException:
            return send_finish_mess(bot, msg.chat.id)

    elif action == 'back':
        w_id = mems[msg.from_user.id]['watch_id']
        for i in mems[msg.from_user.id]['mems']:
            if w_id == i[0]:
                mem = mems[msg.from_user.id]['mems'][mems[msg.from_user.id]['mems'].index(i)][1]
                break
        photo = open(mem['path'], 'rb')
        text_mess = f"Автор: {mem['author']} \nТип: {mem['mem_type']}"
        markup = base_markup_btn('Mem', mem["mem_type"], mem['likes'])
        bot.send_photo(msg.chat.id, photo, text_mess, reply_markup=markup)


def next_10_mem(msg, w_id, mem_type):
    mema = get_mems(mem_type, w_id)
    true_mems = []
    ids = []

    for i in mema:
        item = [i[0], {
            'mem_type': i[1],
            'path': i[2],
            'likes': i[3],
            'author': i[4]
        }]
        ids.append(i[0])
        true_mems.append(item)
        iter_ids = iter(ids)

    try:
        if len(mema) == 0:
            raise StopIteration
        next(iter_ids)
    except StopIteration:
        if msg.message:
            return send_finish_mess(bot, msg.message.chat.id)
        else:
            return send_finish_mess(bot, msg.chat.id)

    mems[msg.message.from_user.id] = {'watch_id': true_mems[0][0],
                                      'mems': true_mems,
                                      'iter_ids': iter_ids,
                                      'ids': ids, }
    send_mem(msg.message, action='next')


def back_10_mems(msg, w_id, mem_type):
    mems_10 = get_mems(mem_type, w_id, True)
    mems_10.reverse()
    true_mems = []
    ids = []

    for i in mems_10:
        item = [i[0], {
            'mem_type': i[1],
            'path': i[2],
            'likes': i[3],
            'author': i[4]}]
        ids.append(i[0])
        true_mems.append(item)
        iter_ids = iter(ids)

    try:
        if len(mems_10) == 0:
            raise StopIteration
        for i in range(10):
            next(iter_ids)
    except StopIteration:
        return send_finish_mess(bot, msg.message.chat.id)

    mems[msg.message.from_user.id] = {'watch_id': true_mems[-1][0],
                                      'mems': true_mems,
                                      'iter_ids': iter_ids,
                                      'ids': ids, }
    send_mem(msg.message, action='back')


def offer(msg):
    mess = 'Тема вашего запроса \n' \
           '(Кратко опишите то о чем хотите сообщить)'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Новый мем', 'Новый анекдот', 'Баг или ошибка', 'Предложение по развитию', 'Отмена')
    msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, offer_text)


def offer_text(msg):
    if msg.text:
        theme = msg.text
        if theme == 'Отмена':
            return start(msg)
    else:
        bot.send_message(msg.chat.id, 'Отправьте только текст')
        return offer(msg)
    offer_context[msg.chat.id] = {'theme': theme}
    mess = 'Отправьте свой текст/картинку'
    msg = bot.send_message(msg.chat.id, mess)
    bot.register_next_step_handler(msg, offer_confirm)


def offer_confirm(msg):
    if msg.text:
        offer_context[msg.chat.id]['content'] = msg.text

    elif msg.photo:
        offer_context[msg.chat.id]['content'] = 'Приложен выше'
        offer_context[msg.chat.id]['image_id'] = msg.photo[-1].file_id

    else:
        return idk(msg)

    offer_context[msg.chat.id]['user_name'] = msg.from_user.first_name
    offer_context[msg.chat.id]['user_tag'] = msg.from_user.username
    offer_context[msg.chat.id]['user_id'] = msg.from_user.id
    offer_context[msg.chat.id]['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    mess = f'''Ваше обращение выглядит так:
Тема: {offer_context[msg.chat.id]['theme']}
Контент:{offer_context[msg.chat.id]['content']}
Время: {offer_context[msg.chat.id]['time']}
Автор: {offer_context[msg.chat.id]['user_name']}
Вы уверены что хотите его отправить?'''
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Да', 'Нет')
    msg = bot.send_message(msg.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, offer_finish)


def offer_finish(msg):
    if msg.text == 'Да':
        try:
            file_info = bot.get_file(offer_context[msg.chat.id]['image_id'])
            downloaded_file = bot.download_file(file_info.file_path)
            downloaded_path = f'image/user_{offer_context[msg.chat.id]["user_tag"]}_image_{msg.id}.jpg'

            with open(downloaded_path, 'wb+') as new_file:
                new_file.write(downloaded_file)

            offer_context[msg.chat.id]['image_path'] = downloaded_path
        except KeyError:
            pass

        add_offer(offer_context[msg.chat.id])
        mess = 'Обращение отправлено успешно'

    else:
        mess = 'Операция отменена'
    offer_context[msg.chat.id].clear()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Мем", "Анекдот", "Обратная связь")
    send_mark_mess(bot, msg, mess, markup)


text_command = {'Привет': 'И вам привет',
                'Анекдот': lambda msg: anecdot(msg),
                'Мем': lambda msg: mem(msg),
                'Обратная связь': lambda msg: offer(msg), }

callback_data_types = {}


@bot.message_handler(content_types=["audio", "document", "sticker", "video", "video_note", "voice", "location",
                                    "contact", "new_chat_members", "left_chat_member", "new_chat_title",
                                    "new_chat_photo", "supergroup_chat_created", "group_chat_created",
                                    "delete_chat_photo", "migrate_from_chat_id", "migrate_to_chat_id",
                                    "channel_chat_created", "pinned_message", "web_app_data"])
def idk(msg):
    mess = "Простите я не могу распознать такой тип сообщений"
    send_mess(bot, msg, mess)


@bot.message_handler(commands=['start'])
def start(msg):
    if check_user(msg.from_user.id):
        add_user({'id': msg.from_user.id,
                  'name': msg.from_user.full_name,
                  'lang': msg.from_user.language_code,
                  'tag': msg.from_user.username,
                  'chat_id': msg.chat.id})
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    mess = f"<b>Здравствуйте, выбирайте что вы хотите увидеть</b>"
    btn1 = types.KeyboardButton("Мем")
    btn2 = types.KeyboardButton("Анекдот")
    btn3 = types.KeyboardButton("Обратная связь")
    markup.add(btn1, btn2, btn3)
    send_mark_mess(bot, msg, mess, markup)


@bot.message_handler()
def user_text(msg):
    if msg.text in text_command:
        mess = text_command[msg.text]
        if type(mess) == str:
            send_mess(bot, msg, mess)
        else:
            mess(msg=msg)
    else:
        idk(msg)


@bot.callback_query_handler(func=lambda call: True)
def callback(msg):
    if msg.message:
        if msg.data == 'back':
            return start(msg)
        if msg.data.split('_')[0] == 'an':
            if len(msg.data.split('_')) != 3:  # Выбран тип анекдота
                sel_type = find_k_by_v(rofl_types, msg.data.split('_')[1])
                ans = get_an(sel_type)
                true_ans = []
                ids = []

                for i in ans:
                    item = [i[0], {
                        'an_type': i[1],
                        'text': i[2],
                        'likes': i[3],
                        'author': i[4]}]
                    ids.append(i[0])
                    true_ans.append(item)
                iter_ids = iter(ids)
                next(iter_ids)

                anecdots[msg.message.from_user.id] = {'watch_id': true_ans[0][0],
                                                      'anecdots': true_ans,
                                                      'iter_ids': iter_ids,
                                                      'ids': ids}
                send_an(msg.message)

            elif msg.data.split('_')[1] == 'like':  # Нажатие кнопки лайк
                an_id = anecdots[msg.message.from_user.id]['watch_id']
                rofl_type = 'an'
                if check_like(an_id, rofl_type):
                    pass
                else:
                    like_context = {'type': 'an',
                                    'an_id': an_id,
                                    'user_id': msg.message.from_user.id}
                    add_like(like_context)
                    try:
                        send_an(msg.message, 'next')
                    except telebot.apihelper.ApiTelegramException:
                        pass

            elif len(msg.data.split('_')) == 3 and msg.data.split('_')[2] == 'next':  # Нажатие кнопки Следующий
                try:
                    anecdots[msg.message.from_user.id]['watch_id'] = next(
                        anecdots[msg.message.from_user.id]['iter_ids'])
                    send_an(msg.message, action='next')
                except StopIteration:
                    return next_10_an(msg, anecdots[msg.message.from_user.id]['watch_id'],
                                      anecdots[msg.message.from_user.id]['anecdots'][0][1]['an_type'])

            elif len(msg.data.split('_')) == 3 and msg.data.split('_')[2] == 'back':  # Нажатие кнопки Назад
                ids = anecdots[msg.message.from_user.id]['ids']
                index_w_id = ids.index(anecdots[msg.message.from_user.id]['watch_id'])
                new_w_id = ids[index_w_id - 1]
                if index_w_id == 0:
                    return back_10_an(msg,
                                      anecdots[msg.message.from_user.id]['watch_id'],
                                      anecdots[msg.message.from_user.id]['anecdots'][0][1]['an_type'])
                new_iter_ids = iter(ids)
                for _ in ids:
                    v = next(new_iter_ids)
                    if v == new_w_id:
                        break
                anecdots[msg.message.from_user.id]['watch_id'] = new_w_id
                anecdots[msg.message.from_user.id]['iter_ids'] = new_iter_ids

                send_an(msg.message, action='back')

        elif msg.data.split('_')[0] == 'mem':
            if len(msg.data.split('_')) != 3:  # Выбран тип мема
                sel_type = find_k_by_v(rofl_types, msg.data.split('_')[1])
                mems_10 = get_mems(sel_type)
                true_mems = []
                ids = []

                for i in mems_10:
                    item = [i[0], {
                        'mem_type': i[1],
                        'path': i[2],
                        'likes': i[3],
                        'author': i[4]}]
                    ids.append(i[0])
                    true_mems.append(item)
                iter_ids = iter(ids)
                next(iter_ids)

                mems[msg.message.from_user.id] = {'watch_id': true_mems[0][0],
                                                  'mems': true_mems,
                                                  'iter_ids': iter_ids,
                                                  'ids': ids}
                send_mem(msg.message)
            elif len(msg.data.split('_')) == 3 and msg.data.split('_')[2] == 'next':  # Нажатие кнопки Следующий
                try:
                    mems[msg.message.from_user.id]['watch_id'] = next(
                        mems[msg.message.from_user.id]['iter_ids'])
                    send_mem(msg.message, action='next')
                except StopIteration:
                    return next_10_mem(msg, mems[msg.message.from_user.id]['watch_id'],
                                       mems[msg.message.from_user.id]['mems'][0][1]['mem_type'])

            elif len(msg.data.split('_')) == 3 and msg.data.split('_')[2] == 'back':  # Нажатие кнопки Назад
                ids = mems[msg.message.from_user.id]['ids']
                index_w_id = ids.index(mems[msg.message.from_user.id]['watch_id'])
                new_w_id = ids[index_w_id - 1]
                if index_w_id == 0:
                    return back_10_mems(msg,
                                        mems[msg.message.from_user.id]['watch_id'],
                                        mems[msg.message.from_user.id]['mems'][0][1]['mem_type'])
                new_iter_ids = iter(ids)
                for _ in ids:
                    v = next(new_iter_ids)
                    if v == new_w_id:
                        break
                mems[msg.message.from_user.id]['watch_id'] = new_w_id
                mems[msg.message.from_user.id]['iter_ids'] = new_iter_ids

                send_mem(msg.message, action='back')

            elif msg.data.split('_')[1] == 'like':  # Нажатие кнопки лайк
                mem_id = mems[msg.message.from_user.id]['watch_id']
                rofl_type = 'mem'
                if check_like(mem_id, rofl_type):
                    pass
                else:
                    like_context = {'type': 'mem',
                                    'mem_id': mem_id,
                                    'user_id': msg.message.from_user.id}
                    add_like(like_context)


async def as_start_mainbot():
    await bot.polling(none_stop=True)


def start_mainbot():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    start_mainbot()
