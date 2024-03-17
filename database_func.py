import sqlite3

from admin_inf import main_admin_context

db = 'bot_db'


def add_user(user_inf: {}):
    id = user_inf['id']
    name = user_inf['name']
    lang = user_inf['lang']
    tag = user_inf['tag']
    chat_id = user_inf['chat_id']
    context = [id, name, lang, tag, chat_id]
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute('INSERT INTO users (user_id, user_name, user_lang, user_tag, chat_id) VALUES(?, ?, ?, ?, ?)',
                   context)
    database.commit()


def check_user(user_id: int) -> bool:
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchall():
        return False
    else:
        return True


def check_admin(username: str) -> bool:
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'SELECT * FROM admins WHERE tag = ?', (username,))
    if cursor.fetchall():
        return False
    else:
        return True


def add_anecdot(an_context: {}):
    text = an_context['text']
    author = an_context['author']
    type = an_context['type']
    context = [type, text, author]
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute('INSERT INTO anecdot (type, text, author) VALUES(?, ?, ?)', context)
    database.commit()


def add_mem(mem_context: {}):
    picture = mem_context['image_path']
    author = mem_context['author']
    type = mem_context['type']
    context = [type, picture, author]
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute('INSERT INTO mems (type, picture, author) VALUES(?, ?, ?)', context)
    database.commit()


def add_admin(admin_context: {}):
    tag = admin_context['tag']
    time_upd = admin_context['time_upd']
    adding = admin_context['adding']
    context = [tag, time_upd, adding]
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute('INSERT INTO admins (tag, time_upd, adding) VALUES(?, ?, ?)', context)
    database.commit()


def check_admin_first(tag: str):
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'SELECT name FROM admins WHERE tag = ?', (tag,))
    if cursor.fetchall():
        return False
    else:
        return True


def upd_admin_inf(tag, name, id):
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'UPDATE admins SET id = ? , name = ? WHERE tag = ?', (id, name, tag))
    database.commit()


def add_notifications(notif_content: {}):
    text = notif_content['text']
    time = str(notif_content['time'])
    name = notif_content['admin_name']
    tag = notif_content['admin_tag']
    context = [text, time, name, tag]
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute('INSERT INTO notifications (text, time, admin_name, admin_tag) VALUES(?, ?, ?, ?)', context)


def get_chats():
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'SELECT chat_id FROM users')
    return cursor.fetchall()


def get_offer_dates():
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'SELECT time FROM offer')
    return cursor.fetchall()


def get_offers_with_date(date: str):
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'SELECT of_id, theme, time FROM offer WHERE time LIKE ?', (f'{date}%',))
    no_filter_offers = cursor.fetchall()
    offers = {}
    for i in no_filter_offers:
        id = i[0]
        theme = i[1]
        time = i[2][-5:]
        offers[id] = {'id': id, 'theme': theme, 'time': time}
    return offers


def get_offer(id: int):
    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(f'SELECT * FROM offer WHERE of_id = ?', (id,))
    return cursor.fetchall()


def add_offer(offer_context: []):
    theme = offer_context['theme']
    time = str(offer_context['time'])
    name = offer_context['user_name']
    tag = offer_context['user_tag']
    id = offer_context['user_id']

    try:
        photo = offer_context['image_path']
        context = [theme, time, name, tag, id, photo]
        sql = 'INSERT INTO offer (theme, time, user_name, user_tag, user_id, picture) VALUES(?, ?, ?, ?, ?, ?)'
    except KeyError:
        text = offer_context['content']
        context = [theme, time, name, tag, id, text]
        sql = 'INSERT INTO offer (theme, time, user_name, user_tag, user_id, text) VALUES(?, ?, ?, ?, ?, ?)'

    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(sql, context)
    database.commit()


def get_an(sel_type: str, w_id=None, back=False):
    database = sqlite3.connect(db)
    cursor = database.cursor()
    if back:
        sql = 'SELECT * FROM anecdot WHERE type = ? and an_id > ? ORDER BY an_id LIMIT 10'
        cursor.execute(sql, (sel_type, w_id))
        return cursor.fetchall()
    if w_id:
        sql = 'SELECT * FROM anecdot WHERE type = ? and an_id < ? ORDER BY an_id DESC LIMIT 10'
        cursor.execute(sql, (sel_type, w_id))
        return cursor.fetchall()
    sql = 'SELECT * FROM anecdot WHERE type = ? ORDER BY an_id DESC LIMIT 10'
    cursor.execute(sql, (sel_type,))
    return cursor.fetchall()


def check_like(rofl_id: int, rofl_type: str) -> bool:
    database = sqlite3.connect(db)
    cursor = database.cursor()
    if rofl_type == 'an':
        sql = 'SELECT id FROM like WHERE an_id = ?'
    elif rofl_type == 'mem':
        sql = 'SELECT id FROM like WHERE mem_id = ?'
    else:
        raise 'Не правильно введен тип, поддерживаются только "an", "mem"'
    cursor.execute(sql, (rofl_id,))
    if cursor.fetchall():
        return True
    else:
        return False


def add_like(like_context: []):
    user_id = like_context['user_id']
    if like_context['type'] == 'an':
        an_id = like_context['an_id']
        context = [an_id, user_id]
        sql = 'INSERT INTO like (an_id, user_id) VALUES(?, ?)'
    else:
        mem_id = like_context['mem_id']
        context = [mem_id, user_id]
        sql = 'INSERT INTO like (mem_id, user_id) VALUES(?, ?)'

    database = sqlite3.connect(db)
    cursor = database.cursor()
    cursor.execute(sql, context)
    database.commit()


def get_mems(sel_type: str, w_id=None, back=False):
    database = sqlite3.connect(db)
    cursor = database.cursor()
    if back:
        sql = 'SELECT * FROM mems WHERE type = ? and mem_id > ? ORDER BY mem_id LIMIT 10'
        cursor.execute(sql, (sel_type, w_id))
        return cursor.fetchall()
    if w_id:
        sql = 'SELECT * FROM mems WHERE type = ? and mem_id < ? ORDER BY mem_id DESC LIMIT 10'
        cursor.execute(sql, (sel_type, w_id))
        return cursor.fetchall()
    sql = 'SELECT * FROM mems WHERE type = ? ORDER BY mem_id DESC LIMIT 10'
    cursor.execute(sql, (sel_type,))
    return cursor.fetchall()


if __name__ == '__main__':
    # def add_first_admin(user_inf: {}):
    #     id = user_inf['id']
    #     name = user_inf['name']
    #     time_upd = user_inf['time_upd']
    #     tag = user_inf['tag']
    #     context = [id, name, time_upd, tag]
    #     database = sqlite3.connect(db)
    #     cursor = database.cursor()
    #     cursor.execute('INSERT INTO admins (id, name, time_upd, tag) VALUES(?, ?, ?, ?)', context)
    #     database.commit()
    # add_first_admin(main_admin_context)

    pass
