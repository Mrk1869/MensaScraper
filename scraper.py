# coding:utf-8

import urllib2
import BeautifulSoup
import re
import key
import requests
from xml.etree import ElementTree
from auth import AzureAuthClient
from pymongo import MongoClient


class Scraper:
    def __init__(self):
        conn = MongoClient()
        self.db = conn.mensa

    def translate(self, query, to):
        auth_client = AzureAuthClient(key.Translator.key)
        auth_token = auth_client.get_access_token()
        bearer_token = 'Bearer '.encode('utf-8') + auth_token
        headers = {"Authorization ": bearer_token}
        url = ("http://api.microsofttranslator.com/v2/Http.svc/Translate?" +
               "text={}&to={}".format(query, to))
        data = requests.get(url, headers=headers)
        return ElementTree.fromstring(data.text.encode('utf-8')).text

    def getMenu(self):
        url = "http://www.mensa-kl.de/"
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup.BeautifulSoup(html)

        today = soup.find('div', {'id': 'day1'})
        date_res = today.find('b').renderContents().strip()
        date = date_res.split(', ')[1]

        menu_raw = ""
        menu_name_res = today.findAll('p', {'onclick': re.compile(r'markMeal.*')})
        for name in menu_name_res[0:2]:
            name = name.renderContents()
            search = re.search(r'alt="(.*)" title', name)
            if search:
                name = re.sub(r'<img.*/>', search.group(1), name)
            menu_raw = menu_raw + name + ".-. "

        name_translated = self.translate(menu_raw, "ja")
        menu_name = [name for name in name_translated.split(u'-。')]

        menu_image_res = today.findAll('img', {'width': '100%'})
        menu_image = [url+image['src'][2::] for image in menu_image_res[0:2]]

        self.db.mensa.menu.remove({"date": date})
        res = {"date": date,
               "menu1": {"name": menu_name[0], "image": menu_image[0]},
               "menu2": {"name": menu_name[1], "image": menu_image[1]}}
        self.db.mensa.menu.save(res)
        return res


if __name__ == "__main__":
    scraper = Scraper()
    print(scraper.getMenu())
