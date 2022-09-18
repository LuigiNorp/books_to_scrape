# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# class BookscrapperPipeline:
#     def process_item(self, item, spider):
#         return item

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class CustomImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'image_name': item["image_name"]})
                for x in item.get('image_urls', [])]

    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['image_name']