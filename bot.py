from random import randint
from PIL import ImageFile
import schedule
import requests
import telebot
import os
import re


bot = telebot.TeleBot(token=os.getenv('BOT_TOKEN'))
CHANNEL_NAME = '@hokky_t'


def hokky_bot():
    f = open('resources/hokky.txt', 'r', encoding='UTF-8')  # Открываем файл с хокку
    all_hokky = f.read().split('\n')  # Записываем каждую строчку в отдульный элемент списка
    f.close()

    f = open('resources/names.txt', 'r', encoding='UTF-8')  # То же самое для файла с именами
    all_names = f.read().split('\n')
    f.close()
    j = 0
    print('Power on!')   
    a = randint(0,1)  # генерируем случайное число для вставки н.э или до н.э.
    if a == 1:
        era ='до н.э.'
    else:
        era = 'н.э'
    i =0
    name = [1, 2, 3]
    text = [1, 2, 3]
    while i <= 2:
        name[i] = all_names[randint(1, len(all_names)-1)]  # Формируем списки из 3 строчек хокку и 3-х имён
        text[i] = all_hokky[randint(1, len(all_hokky)-1)]
        i += 1
    message = (f'{text[0]}\n{text[1]}\n{text[2]}\n\n     - {name[0].title()} {name[1].title()} {name[2].title()}, {randint(0, 2022)} г. {era}')
    j += 1
    search = text[randint(0,2)]
    print(f'Японская живопись {search}')
    send_picture(message, search)


def send_picture(message, search):
    url = request_photo(f'Японская живопись {search}')
    bot.send_photo(CHANNEL_NAME, photo=url, caption=message)


def request_photo(message):
    req = requests.get("https://yandex.ru/images/search?text="+message)
    ph_links = list(filter(lambda x: '.jpg' in x, re.findall('''(?<=["'])[^"']+''', req.text)))
    ph_list = []
    for i in range(1, 10):
        if len(ph_links[i]) > 5:
            if ph_links[i][0:4] == "http":
                size = ph_size(ph_links[i])[0]
                print(size)
                if size > 500:
                    ph_list.append(ph_links[i])
                    print(ph_list)

    return ph_list[randint(0, len(ph_list) - 1)]


def ph_size(url):
    resume_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive", 
    'Range': 'bytes=0-2000000'}  
    data = requests.get(url, stream=True, headers=resume_header).content
    p = ImageFile.Parser()
    p.feed(data)   
    if p.image:
        return p.image.size 
    # (1400, 1536) 
    else: 
        return (0, 0)


schedule.every(8).to(16).hours.do(hokky_bot)

if __name__ == '__main__':
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f'СЛомалось: {e}')

