#coding:utf-8

import urllib2
import BeautifulSoup
import re
import pymongo
from microsofttranslator import Translator
from key import config

class Scraper:
    def __init__(self):
        conn = pymongo.Connection()
        self.db = conn.mensa
        self.translator_id = config.Translator.userid
        self.translator_key = config.Translator.key

    def translate(self, query, to):
        translator = Translator(self.translator_id,self.translator_key)
        return translator.translate(query, to)

    def getMenu(self):
        url = "http://www.mensa-kl.de/"
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup.BeautifulSoup(html)

        today =  soup.find('div',{'id':'day1'})
        date_res = today.find('b').renderContents().strip()
        date = date_res.split(', ')[1]

        menu_raw = ""
        menu_name_res = today.findAll('p',{'onclick':re.compile(r'markMeal.*')})
        for name in menu_name_res[0:2]:
            name = name.renderContents()
            search = re.search(r'alt="(.*)" title', name)
            if search:
                name = re.sub(r'<img.*/>', search.group(1), name)
            menu_raw = menu_raw + name + ".-. "

        name_translated = self.translate(unicode(menu_raw, 'utf-8'), "ja")
        menu_name = [name for name in name_translated.split(u'-。')]

        menu_image_res  = today.findAll('img',{'width':'100%'})
        menu_image = [url+image['src'][2::] for image in menu_image_res[0:2]]

        res = {"date":date,
                "menu1":{"name":menu_name[0], "image":menu_image[0]},
                "menu2":{"name":menu_name[1], "image":menu_image[1]}}
        self.db.mensa.menu.save(res)
        return res

if __name__ == "__main__":
    scraper = Scraper()
    print scraper.getMenu()
