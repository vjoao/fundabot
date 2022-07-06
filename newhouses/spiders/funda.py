from urllib import request
from venv import create
import scrapy
import telebot

TOKEN = 'BOT_TOKEN'
CHAT_ID = 'ID'

bot = telebot.TeleBot(TOKEN)

db = open('db.txt', 'a+')
db.seek(0)
seen = db.read().splitlines()

class FundaSpider(scrapy.Spider):
    name = 'funda'
    allowed_domains = ['www.funda.nl']
    start_urls = [
       'https://www.funda.nl/koop/hoofddorp/350000-500000/1-dag/+5km/sorteer-datum-af'
    ]

    def parse(self, response):
        housesSelectorList = response.css('.search-result-main')
        for house in housesSelectorList:
            href = 'https://www.funda.nl{}'.format(house.css('.search-result-media > a')[0].attrib['href'])
            if (href not in seen):
                # save current URL as seen in db
                db.write('{}\n'.format(href))

                # prepare message
                street = house.css('.search-result__header-title::text').get().strip()
                city = house.css('.search-result__header-subtitle::text').get().strip()
                img = house.css('img').attrib['src']
                info = [currentInfo.strip() for currentInfo in house.css('.search-result-info > li::text,span::text').getall()]
                info.pop()
                caption = '{}\n{}, {}\n\n{}'.format(href, street, city, ' '.join(info))
                print(caption)
                #send message
                bot.send_photo(CHAT_ID, img, caption=caption)