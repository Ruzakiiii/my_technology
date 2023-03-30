import telebot
from telebot import types
from data import DataBase

bot = telebot.TeleBot('API_KEY')

lo = ['lll']
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    key = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton(text='Регистрация', callback_data='Регистрация')
    item2 = types.InlineKeyboardButton(text='Авторизация', callback_data='Авторизация')
    key.add(item,item2)
    bot.send_message(user_id, 'Hello', reply_markup=key)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == '1':
        DataBase.UPDATE('users', 'phone', '2622', 'user_id', message.from_user.id)
        # DataBase.CREATE('lol',['num integer NOT NULL', 'name varchar(20) NOT NULL'])
        # DataBase.DROP('lol')

    elif message.text == 'Добавить':
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        user_name = message.from_user.username
        number = message.text
        DataBase.INSERT('users', ['user_id', 'phone', 'first_name', 'user_name'],[f'{user_id}', f'{number}', f'{first_name}', f'{user_name}'])

    elif message.text == '228':
        DataBase.DELETE('users')

    elif message.text == '227':
        user_id = message.from_user.id
        not_all = DataBase.SELECT('*', 'users')
        user_all = [i[0] for i in not_all]

        if user_id not in user_all:
            add_to_bs(message)

        elif user_id in user_all:
            key = types.InlineKeyboardMarkup(row_width=2)
            item = types.InlineKeyboardButton(text='Мои данные', callback_data='Мои данные')
            item2 = types.InlineKeyboardButton(text='Меню', callback_data='Меню')
            key.add(item, item2)
            bot.send_message(user_id, 'Вы уже зарегистрировались', reply_markup=key)


def get_user(message):
    user_id = message.from_user.id
    user_all = DataBase.SELECT('*', 'users','user_id', user_id)

    try:
        us = [i for i in user_all[0]]

        if user_id not in us:
            bot.send_message(user_id, 'Вас нет в базе')
            print(user_all)

    except:
        bot.send_message(user_id, 'Вас нет в базе')

    else:
        print(user_all[0])
        all = ''

        for i in user_all:
            all += f'User_id: {i[0]}\nFirst_name: {i[1]}\nNumber: {i[2]}\nUsername: @{i[3]}\n\n'

        bot.send_message(user_id, all)


def add_to_bs(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Введите пароль для учётной записи')
    bot.register_next_step_handler(message,add_password)


def last(message):
    user_id = message.from_user.id
    not_all = DataBase.SELECT('*', 'users')
    user_all = [i[0] for i in not_all]

    if user_id not in user_all:
        add_to_bs(message)

    elif user_id in user_all:
        key = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton(text='Мои данные', callback_data='Мои данные')
        item2 = types.InlineKeyboardButton(text='Меню', callback_data='Меню')
        key.add(item, item2)
        bot.send_message(user_id, 'Вы уже зарегистрировались', reply_markup=key)


def add_password(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    user_name = message.from_user.username
    number = message.text
    DataBase.INSERT('users', ['user_id', 'phone', 'first_name', 'user_name'], [f'{user_id}', f'{number}', f'{first_name}', f'{user_name}'])
    last(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.message:
        if call.data == 'Мои данные':
            get_user(call)

        elif call.data == 'Меню':
            key = types.InlineKeyboardMarkup(row_width=2)
            item = types.InlineKeyboardButton(text='Назад', callback_data='Назад1')
            item2 = types.InlineKeyboardButton(text='2', callback_data='2')
            key.add(item, item2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text=f'Здравствуй {call.from_user.first_name}\n\nЧто будем делать ?', reply_markup=key)

        elif call.data == 'Регистрация':
            bot.send_message(call.from_user.id, 'Отправь свой номер')
            bot.register_next_step_handler(call.message, last)

        elif call.data == 'Назад1':
            key = types.InlineKeyboardMarkup()
            item = types.InlineKeyboardButton(text='Регистрация', callback_data='Регистрация')
            item2 = types.InlineKeyboardButton(text='Авторизация', callback_data='Авторизация')
            key.add(item, item2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text=f'Hello', reply_markup=key)

        elif call.data == 'Авторизация':
            key = types.InlineKeyboardMarkup()

            for i in lo:
                item3 = types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}')

                key.add(item3)

            item = types.InlineKeyboardButton(text='Регистрация', callback_data='Регистрация')
            item2 = types.InlineKeyboardButton(text='Авторизация', callback_data='Авторизация')
            key.add(item, item2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Напиши название кнопки',reply_markup=key)
            lo.append(call.message.text)


bot.polling(non_stop=True)