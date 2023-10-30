import requests, colorama, random, phonenumbers, random, sys
from pyshorteners import Shortener
from colorama import Fore
from banners import banner1, banner2, banner3

s = Shortener()

f = banner1, banner2, banner3 

rm = random.choice(f)

color1 = Fore.RED
color2 = Fore.MAGENTA
color3 = Fore.CYAN
color4 = Fore.GREEN
color5 = Fore.YELLOW

color = random.choice([color1, color2, color3, color4, color5])

def process_phone():
    global phone
    if language == '1':
        phone = input('Введите номер(Пример: +79999999999) >>> ')
    elif language == '2':
        phone = input('Enter the number(Example: +79999999999) >>> ')
    try:
        ph = phonenumbers.parse(phone)
        valid = phonenumbers.is_valid_number(ph)
    except:
        if language == '1':
            print('Номер не действителен!')
        elif language == '2':
            print('The number is not valid!')

    if valid == True:
        getInfo = "https://htmlweb.ru/geo/api.php?json&telcod=" + phone
        try:
            infoPhone = requests.get(getInfo).json()
            message_text1 = (
                f"Номер сотового ---> {phone}\n"
                f"Страна ---> {infoPhone['country']['name']}\n"
                f"Регион ---> {infoPhone['region']['name']}\n"
                f"Округ ---> {infoPhone['region']['okrug']}\n"
                f"Оператор ---> {infoPhone['0']['oper']}\n"
                f"Часть света ---> {infoPhone['country']['location']}"
                )
            message_text2 = (
                f"Phone number ---> {phone}\n"
                f"Country ---> {infoPhone['country']['name']}\n"
                f"Region ---> {infoPhone['region']['name']}\n"
                f"District ---> {infoPhone['region']['okrug']}\n"
                f"Operator ---> {infoPhone['0']['oper']}\n"
                f"Part of the world ---> {infoPhone['country']['location']}"
                )
            if language == '1':
                print(message_text1)
            elif language == '2':
                print(message_text2)
            
        except:
            if language == '1':
                print("\n[!] - Номер не найден - [!]\n")
            elif language == '2':
                print("\n[!] - Number not found - [!]\n")
            
    else: 
        if language == '1':
            print('Номер не действителен!')
        elif language == '2':
            print('The number is not valid!')

def ip_check():
    if language == '1':
        ip = input('Введите ip адресс >>> ')
    elif language == '2':
        ip = input('Enter the ip address >>> ')
        
    url = f'https://ipinfo.io/{ip}/json'

    proxy = {'http': '50.171.32.230:80'}

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
    response = requests.get(url=url, headers=headers, proxies=proxy)
    result = response.text
    print(result)

def search_telegram():

    original_url = f"https://t.me/{phone}"
    short_url = s.tinyurl.short(original_url)

    if language == '1':
        print(f'\n(Такого пользователя может не существовать. Если он есть то вы его увидите): \n\nTelegramm: {short_url}\n')
    elif language == '2':
        print(f'\n(Such a user may not exist. My alogorhythm is not yet able to verify its presence. If there is one, you will see it): \n\nTelegramm: {short_url}\n')

def menu():
    print(color + rm + Fore.RESET)
    global language
    language = input('Выберите язык/Select a language\n[1] - Русский\n[2] - English\nSelect language number >>> ')
    if language == '1':
        user_input = input('\nФункции: \n\n[1] - Поиск по номеру\n[2] - Пробив по ip\n[3] - Выход\n\nВпишите номер функции >>> ')
        if user_input == '1':
            process_phone()
            search_telegram()
        elif user_input == '2':
            ip_check()
        elif user_input == '3':
            sys.exit()

    elif language == '2':
        user_input = input('Functions: \n\n[1] - Search by number\n[2] - Punching by ip\n[3] - Exit\n\nEnter the function number >>> ')
        if user_input == '1':
            process_phone()
            search_telegram()
        elif user_input == '2':
            ip_check()
        elif user_input == '3':
            sys.exit()
if __name__ == '__main__':
    menu()