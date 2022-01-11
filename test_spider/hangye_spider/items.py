# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# -*- coding: utf-8 -*-
import scrapy
import json
from hangye_spider.settings import collection_name

#处理爬虫的信息
class MySpiderItem(scrapy.Item):
    report_id=scrapy.Field()
    #研究报告id,每一篇研究报告的id都是唯一的
    title=scrapy.Field()
    #研究报告的标题
    abstract=scrapy.Field()
    #研究报告的摘要
    organ=scrapy.Field()
    #研究报告的机构
    author=scrapy.Field()
    #研究报告的作者
    publish_time=scrapy.Field()
    #研究报告发布的时间
    rating=scrapy.Field()
    #研究报告对应的评级
    """""""""
    写入对数据库的操作
    但是在这里并不实际的进行数据库的操作
    最后只是返回一个查询语句结果
    """""""""
    def insert_sql(self):#根据爬取的数据设计插入到mangodn的语句
        insert_inform={'report_id':self['report_id'],'title':self['title'],'abstract':self['abstract'],'organ':self['organ']
                       ,'author':self['author'],'publish_time':self['publish_time'],'rating':self['rating'],'has_checked':'False'}
        return insert_inform









