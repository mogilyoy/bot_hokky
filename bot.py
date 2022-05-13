import telebot
import logging
import time
import re
import requests
from random import randint
from PIL import ImageFile
from config import BOT_TOKEN, main_token
import vk_api
# from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(token = BOT_TOKEN)
CHANNEL_NAME = '@hokky_t'

def hokky_bot():
    f = open('hokky.txt', 'r', encoding='UTF-8')  # Открываем файл с хокку
    all_hokky = f.read().split('\n')  # Записываем каждую строчку в отдульный элемент списка
    f.close()

    f = open('names.txt', 'r', encoding='UTF-8')  # То же самое для файла с именами
    all_names = f.read().split('\n')
    f.close()
    j = 0
    print('Power on!')   
    while j < 10000:
        a = randint(0,1)  # генерируем случайное число для вставки н.э или до н.э.
        if a == 1:
            era ='до н.э.'
        else: 
            era = 'н.э'
        i =0 
        name = [1, 2, 3]
        text = [1, 2, 3]
        while i<=2: 
            name[i] = all_names[randint(1, len(all_names)-1)]  # Формируем списки из 3 строчек хокку и 3-х имён
            text[i] = all_hokky[randint(1, len(all_hokky)-1)] 
            i += 1
        message = (f'{text[0]}\n{text[1]}\n{text[2]}\n\n     - {name[0].title()} {name[1].title()} {name[2].title()}, {randint(0, 2022)} г. {era}')
        j += 1
        search = text[randint(0,2)] 
        print(f'Японская живопись {search}')
        picture(message, search)
        time.sleep(randint(28800, 57600))


def picture(message, search):
    # Код для вставки своего хокку в изображение из request_photo

    # im = requests.get(request_photo('японcкая живопись'))  
    # out = open("img.jpg", "wb")
    # out.write(im.content)
    # out.close()
    # image = Image.open('img.jpg')

    # # Создаем объект со шрифтом
    # font = ImageFont.truetype('font.name', size= int(image.width/15))
    # draw_text = ImageDraw.Draw(image)
    # draw_text.text(
    #     (int(image.width/50), int(image.height/4)),
    #     message,
    #     # Добавляем шрифт к изображению
    #     font=font,
    #     fill='#d60000') # Цвет
    url = request_photo(f'Японская живопись {search}')
    bot.send_photo(CHANNEL_NAME, photo = url, caption = message)
    vk_post(url=url, message=message)

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
    data = requests.get(url, stream = True, headers = resume_header).content
    p = ImageFile.Parser()
    p.feed(data)   
    if p.image:
        return p.image.size 
    # (1400, 1536) 
    else: 
        return (0, 0)


def vk_post(url, message):
    vk_session = vk_api.VkApi('login', 'password')
    vk_upload = vk_api.upload.VkUpload(vk_session)
    vk_session.auth()

    vk = vk_session.get_api()

    im = requests.get(url=url)  
    out = open("img.jpg", "wb")
    out.write(im.content)
    out.close()

    with open ('img.jpg', 'rb') as f:
        ph = vk_upload.photo(photos=f, album_id=284394723)
        ph_id = ph[0]['id']


    print(vk.wall.post(message=message, owner_id = '-213199160', attachments= f'photo223988241_{ph_id}', copyright= 'https://t.me/hokky_t'))

hokky_bot()
if __name__ == '__main__':
   bot.polling(none_stop=True, interval=0)
