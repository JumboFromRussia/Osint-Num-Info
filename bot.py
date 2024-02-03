from config import bot
from telebot import types
import requests, phonenumbers, telebot, sqlite3
from pyshorteners import Shortener
from fake_useragent import UserAgent

bot = bot
s = Shortener()
usa = UserAgent(browsers=['edge', 'chrome'], os='linux')

def db_search(message):
    try:
        con = sqlite3.connect('num_info.db')
        cur = con.cursor()

        phone = message.text
        phone = phone.lstrip('+')

        cur.execute('SELECT * FROM your_table_name WHERE phone = ?', (phone,))
        row = cur.fetchone()

        result=(
                    "----DataBase--Search--Result----"
                     f"\nTelegramm Id: {row[0]}"
                     f"\nNumber: {row[1]}"
                     f"\nUsename: @{row[2]}"
                     f"\nFirstName: {row[3]}"
                     f"\nLastName: {row[4]}"
                )

        bot.send_message(message.chat.id, result)
    except Exception as e:
        print(e)
        pass
    finally:
        con.close()

@bot.message_handler(commands=['start'])
def start(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('📄 Справка по номеру 📱')
        btn2 = types.KeyboardButton('🌐 IP Info 🎯')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Привет! Выберите опцию:", reply_markup=markup)
    except Exception:
        pass

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '📄 Справка по номеру 📱':
        bot.send_message(message.chat.id, 'Укажите номер(Пример: +79999999999): ')
        bot.register_next_step_handler(message, process_phone)
    elif message.text == '🌐 IP Info 🎯':
        bot.send_message(message.chat.id, 'Введите IP адрес:')
        bot.register_next_step_handler(message, ip_check)

def process_phone(message):
    phone = message.text

    if not phone.startswith('+'):
        phone = '+' + phone

    try:
        ph = phonenumbers.parse(phone)
        valid = phonenumbers.is_valid_number(ph)
    except:
        bot.send_message(message.chat.id, 'Номер не действителен!')

    try:
        if valid:

            getInfo = "https://htmlweb.ru/geo/api.php?json&telcod=" + phone

            try:
                infoPhone = requests.get(getInfo).json()

                print("infoPhone:", infoPhone) 

                if 'error' in infoPhone:
                    error_message = infoPhone.get('error', 'Неизвестная ошибка')
                    bot.send_message(message.chat.id, f'Ошибка при получении информации: {error_message}')
                elif isinstance(infoPhone, dict):
                    country_name = infoPhone.get('country', {}).get('name', 'N/A')
                    region_name = infoPhone.get('region', {}).get('name', 'N/A')
                    okrug_name = infoPhone.get('region', {}).get('okrug', 'N/A')
                    operator_name = infoPhone.get('0', {}).get('oper', 'N/A')
                    location_name = infoPhone.get('country', {}).get('location', 'N/A')

                    message_text = (
                                    f"Номер сотового ---> {phone}\n"
                                    f"Страна ---> {infoPhone['country']['name']}\n"
                                    f"Регион ---> {infoPhone['region']['name']}\n"
                                    f"Округ ---> {infoPhone['region']['okrug']}\n"
                                    f"Оператор ---> {infoPhone['0']['oper']}\n"
                                    f"Часть света ---> {infoPhone['country']['location']}\n"
                                    f"Город ---> {infoPhone['0']['name']}"
                                    )

                    bot.send_message(message.chat.id, message_text)

            except Exception as e:
                print(e)
                pass

            try:
                telegram_url = f"https://t.me/{message.text}"
                short_telegram_url = s.tinyurl.short(telegram_url)
                viber_url = f"https://viber.click/{message.text}"
                short_viber_url = s.tinyurl.short(viber_url)
                whatsapp_url = f"https://wa.me/{message.text}"
                whatsapp_url = s.tinyurl.short(whatsapp_url)
                bot.send_message(message.chat.id, f'Результат поиска:\n\nTelegram: {short_telegram_url}\n\nViber: {short_viber_url}\n\nWhatsapp: {whatsapp_url}')

            except Exception as e:
                print(e)
                pass

            db_search(message)

        else:
            bot.send_message(message.chat.id, 'Номер не действителен!')

    except Exception as e:
        print(e)
        pass
    
def ip_check(message):
    try:
        ip = message.text
        url = f'https://ipinfo.io/{ip}/json'

        proxy = {'http': '50.174.145.10:80'}

        headers = {usa.random}
        response = requests.get(url=url, headers=headers, proxies=proxy)
        result = response.text
        bot.send_message(message.chat.id, result)
    except Exception:
        pass

bot.infinity_polling(none_stop=True)
