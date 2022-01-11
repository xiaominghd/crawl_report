# -*- coding: utf-8 -*-
import time
import logging
import json
from selenium import webdriver
import scrapy
import datetime
from hangye_spider.items import MySpiderItem
class HangyeSpider(scrapy.Spider):
    name = 'report'  # 定义一个爬虫，就是爬虫的名字，由于一个项目里只有一个爬虫，所以在一个项目中的name是一个唯一值
    allowed_domains = ['gw.datayes.com']
    start_urls = ['http://gw.datayes.com/']  # 爬虫开始启动的地方,这个感觉就像是那个在抓到的包里的一些信息

    dt = datetime.datetime.now().strftime('%Y-%m-%d')
    today = dt.replace('-', '')

    base_url = 'https://gw.datayes.com/rrp_adventure/web/search?'
    headers = {
        "Origin": "https://robo.datayes.com",
        "Referer": "https://robo.datayes.com/v2/fastreport/industry?subType=%E4%B8%8D%E9%99%90&induName=%E4%B8%8D%E9%99%90",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }
    """""""""
    爬虫爬取的并不是原始的那个前端网页，而是一个纯json的网页？
    """""""""
    url = "https://gw.datayes.com/rrp_adventure/web/search?pageNow={0}&authorId=&isOptional=false&orgName=&reportType=INDUSTRY&secCodeList=&reportSubType=&industry=&ratingType=&pubTimeStart={1}&pubTimeEnd={1}&type=EXTERNAL_REPORT&pageSize=40&sortOrder=desc&query=&minPageCount=&maxPageCount="
    def start_requests(self):
        cookie=self.get_cookies()
        for page in range(1, 5):
            yield scrapy.Request(
                self.url.format(page, self.today),#这个是实例化url，但是后面有几页是没有的，不知道什么原因
                headers=self.headers,
                cookies=cookie,
                meta={"page": page, "cookie": cookie}
            )

    def parse(self, response):
        time.sleep(10)
        page = response.meta.get('page')
        logging.info('正在抓取第{0}页'.format(page))
        status = response.status
        logging.info(status)
        result = response.text
        result = json.loads(result)
        message=result['message']
        if message != 'success':
            logging.info('message为：{0},请求失败！'.format(message))
            return
        data_all=result['data']['list']#返回的是一个dict类型的list
        for info in data_all:
            item=MySpiderItem()
            meta_data=info['data']
            item['report_id']=meta_data['id']
            item['title']=meta_data['title']
            item['abstract']=meta_data['abstractText']
            item['organ']=meta_data['orgName']
            item['author']=meta_data['author']
            item['publish_time']=meta_data['publishTime']
            item['rating']=meta_data['ratingContent']
            #实例化返回爬虫的结果
            yield item

    def get_cookies(self):
        # Firefox无头浏览器模式
        from selenium.webdriver.firefox.options import Options
        firefox_options = Options()
        firefox_options.set_headless()
        driver = webdriver.Firefox(firefox_options=firefox_options)
        url = 'https://robo.datayes.com/v2/fastreport/industry?subType=%E4%B8%8D%E9%99%90&induName=%E4%B8%8D%E9%99%90'
        driver.get(url)
        # 获取cookie列表
        cookie_list = driver.get_cookies()
        # 格式化打印cookie
        cookie_dict = {}
        for cookie in cookie_list:
            cookie_dict[cookie['name']] = cookie['value']
        driver.quit()
        return cookie_dict