# -*- coding: utf-8 -*-
# __author__ = zok 
# Email = 362416272@qq.com
# Date: 2019/3/3  Python: 3.7

"""pip3 install fake-useragent"""

import requests
import re
import json
import pymysql

from fake_useragent import UserAgent


class TargetSpider(object):
    """TargetUrl"""
    ua = UserAgent()

    def __init__(self, url):
        self.url = url

    def get_random_ua(self):
        """get random ua"""
        headers = {
            'User-Agent': self.ua.random,
        }
        return headers

    @property
    def get_one_page(self):
        headers = self.get_random_ua()
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None

    def parse_one_page(self):
        """Re解析 one_page"""
        pattern = re.compile(
            '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
            re.S)  # re.S = 非贪婪模式
        items = re.findall(pattern, self.get_one_page)

        for item in items:  # yield生成器，与return类似，可以自行百度
            yield {
                'index': item[0],
                'image': item[1],
                'title': item[2],
                'actor': item[3].strip()[3:],
                'shooting_time': item[4][5:],
                'score': item[5] + item[6],
            }

    @staticmethod
    def write_to_file(content):
        with open('file/result.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False) + '\n')

    @staticmethod
    def save_to_mysql(content):
        db = pymysql.connect(host="localhost", user="root",
                             password="", db="movie", port=3306)
        cur = db.cursor()
        sql_inset = """INSERT INTO maoyan (movie_index, image, title, actor, shooting_time, score) VALUES ("%s","%s","%s","%s","%s","%s") """ % (
            content['index'], content['image'], content['title'], content['actor'], content['shooting_time'],
            content['score'])
        try:
            cur.execute(sql_inset)
            db.commit()
        except Exception as e:
            print('错误回滚')
            db.rollback()
        finally:
            db.close()
