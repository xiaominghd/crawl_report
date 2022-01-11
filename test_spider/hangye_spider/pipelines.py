# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
"""""""""
在这个文件中主要定义的是处理问题的流程
主要是持久层的东西
如果要调用的话需要在setting.py里去设置pipline的优先级，只有设置了优先级的pipline才会被调用
"""""""""
from itemadapter import ItemAdapter
import pymongo
from hangye_spider.settings import mongodb,port,db_name,collection_name
from hangye_spider.items import MySpiderItem
class MongodbPipeline(object):
    def __init__(self):#初始化需要连接的数据库，集合
        self.Client=pymongo.MongoClient(mongodb,port)
        self.test=self.Client[db_name]
        self.post=self.test[collection_name]
#直接将操作mongodb的过程写死在爬虫运行的过程中里
    def process_item(self,item,spider):
        mongo_sql=MySpiderItem.insert_sql(item)#调用inser_sql方法将爬取得到的数据转化为mongodb中的sql
        self.post.insert(mongo_sql)#插入操作
        return mongo_sql
#在爬虫结束之后，对没有去重的数据进行数据去重
    def close_spider(self,spider):
        print("开始数据去重")
        unsolved_num=len(list(self.post.find({'has_checked':'False'})))#提前找到没有去重的数据，所以在后面的操作中就不用遍历整个数据库，减少了时间复杂度
        for i in range(unsolved_num):
            repeating = self.post.find_one({'has_checked': 'False'})
            repeating['has_checked'] = 'True'#修改标志位
            result = self.post.delete_many({'report_id': repeating['report_id']})#去重
            self.post.insert_one(repeating)
        return True
class HangyeSpiderPipeline:
    def process_item(self, item, spider):
        return item
