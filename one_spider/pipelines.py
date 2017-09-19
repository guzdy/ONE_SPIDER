# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from pymongo import MongoClient
import scrapy
import os

from one_spider.items import OneItemQuestion, OneItemArticle, OneItemImage
from one_spider.settings import IMAGES_STORE


class ImageDownloadPipeline(ImagesPipeline):
    """图片名按默认hash密文下载，如果有title， 重命名"""
    def get_media_requests(self, item, info):
        if isinstance(item, OneItemImage):
            img_url = item['img_url'][0]
            yield scrapy.Request(img_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        else:
            oldname = os.path.join(IMAGES_STORE,image_paths[0])
            newname = os.path.join(IMAGES_STORE, 'full', item['img_num'][0] + '.jpg')
            os.rename(oldname, newname)
        return item


class ImageInfoPipeline(object):
    def open_spider(self, spider):
        self.file = open('img.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, OneItemImage):
            for key in item.keys():

                if item[key]:
                        line = key + ':' + item[key][0] + '\n\n'
                        self.file.write(line)
            self.file.write('\n\n\n\n')

        return item


class ArticlePipeline(object):
    def open_spider(self, spider):
        self.file = open('one.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, OneItemArticle):
            for key in item.keys():

                if item[key]:
                        line = item[key][0] + '\n\n'
                        self.file.write(line)
            self.file.write('\n\n\n\n')

        return item


class QuestionPipeline(object):
    def open_spider(self, spider):
        self.file = open('one_question.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, OneItemQuestion):
            for key in item.keys():

                if item[key]:
                    line = item[key][0] + '\n\n'
                    self.file.write(line)
            self.file.write('\n\n\n\n\n')

        return item


class MongoPipeline(object):
    def __init__(self):
        db = MongoClient().one
        self.coll_image = db.image
        self.coll_question = db.question
        self.coll_article = db.article

    def process_item(self, item, spider):
        mongo_item = {}
        # 把 item里被 list 嵌套的 value 解开
        for key, value in item.items():
            mongo_item[key] = value[0]
        if isinstance(item, OneItemQuestion):
            self.coll_question.insert_one(mongo_item)
        elif isinstance(item, OneItemImage):
            self.coll_image.insert_one(mongo_item)
        elif isinstance(item, OneItemArticle):
            self.coll_article.insert_one(mongo_item)

        return item
