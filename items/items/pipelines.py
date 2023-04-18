# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class ItemsPipeline:
#     def process_item(self, item, spider):
#         return item

import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class ItemsPipeline(object):
    
    def __init__(self):
        ATLAS_KEY=os.getenv('ATLAS_KEY')
        self.client = MongoClient(ATLAS_KEY)
        db = self.client.imdb
        self.collection = db.movies
       
        
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item

