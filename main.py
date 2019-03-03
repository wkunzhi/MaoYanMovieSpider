# -*- coding: utf-8 -*-
# __author__ = zok 
# Email = 362416272@qq.com
# Date: 2019/3/3  Python: 3.7
"""
【正则匹配】爬取电影网
"""
from spider.movie import TargetSpider
from config import *

if __name__ == '__main__':
    """start"""
    for i in range(10):
        visit = TargetSpider(URL+'?offset='+str(i*10))
        for item in visit.parse_one_page():
            visit.write_to_file(item)
            visit.save_to_mysql(item)  # 不需要存数据库 就注释掉
