# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis

class ScrapydemoPipeline(object):
    def process_item(self, item, spider):
        return item


class PoetryPipeline(object):
    def open_spider(self, spider):
        self.f = open('poetries.txt', 'w')
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        self.r = redis.Redis(connection_pool=pool)

    def close_spider(self, spider):
        self.f.close()
        for s in self.r.sdiff("poetry"):
            #返回对象是一个bytes类型需要进行解码
            print(s.decode('UTF-8', 'strict'))


    def process_item(self, item, spider):
        try:
            line = str(dict(item)) + '\n'
            self.f.write(line)
            self.r.sadd("poetry", line)
        except:
            pass
        return item