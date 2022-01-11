import pymongo
from hangye_spider.settings import mongodb,collection_name,db_name,port

class opt_mongo(object):
    def __init__(self):
        self.connect=pymongo.MongoClient(mongodb,port)
        self.test=self.connect[db_name]
        self.post=self.test[collection_name]

#删除数据库中重复的数据
    def drop_duplicate(self):
        unsolved_num=len(list(self.post.find({'has_checked':'False'})))
        for i in range(unsolved_num):
            repeating = self.post.find_one({'has_checked': 'False'})
            repeating['has_checked'] = 'True'
            result = self.post.delete_many({'report_id': repeating['report_id']})
            self.post.insert_one(repeating)
        return True

opt_mongo().drop_duplicate()

