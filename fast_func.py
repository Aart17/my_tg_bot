from telebot import types


def send_mess(bot, sender, mess):
    if type(mess) != str:
        mess = str(*mess)
    try:
        bot.send_message(sender.chat.id, mess, parse_mode="html")
    except AttributeError:
        bot.send_message(sender.message.chat.id, mess, parse_mode="html")


def send_mark_mess(bot, msg, mess, markup):
    if type(mess) != str:
        mess = str(*mess)
    try:
        bot.send_message(chat_id=msg.message.chat.id,
                         text=mess, reply_markup=markup, parse_mode='html')
    except AttributeError:
        bot.send_message(chat_id=msg.chat.id,
                         text=mess, reply_markup=markup, parse_mode='html')


def send_photo(bot, msg, mess, markup):
    bot.send_photo(msg.message.chat.id, mess, reply_markup=markup)


def edit_txt_mess(bot, msg, mess, markup=None):
    if type(mess) != str:
        mess = str(*mess)
    if markup:
        try:
            bot.edit_message_text(chat_id=msg.message.chat.id,
                                  message_id=msg.message.id, text=mess, reply_markup=markup)
        except AttributeError:
            bot.edit_message_text(chat_id=msg.chat.id,
                                  message_id=msg.id, text=mess, reply_markup=markup)
    else:
        try:
            bot.edit_message_text(chat_id=msg.message.chat.id,
                                  message_id=msg.message.id, text=mess)
        except AttributeError:
            bot.edit_message_text(chat_id=msg.chat.id,
                                  message_id=msg.id, text=mess)


def edit_photo_mess(bot, msg, mess, markup):
    bot.edit_message_media(chat_id=msg.message.chat.id,
                           message_id=msg.message.id, media=types.InputMediaPhoto(mess), reply_markup=markup)


def send_finish_mess(bot, chat_id):
    bot.send_message(chat_id, 'Поздравляю вы посмотрели все до конца🎉,\nТеперь посмотрите другие категории')
