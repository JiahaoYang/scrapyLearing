# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import codecs
import json
import pymysql


class JsonWithEncodingPipline(object):

    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 同步插入mysql
class MysqlPipline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root',
                                    password='yjh961024', db='spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole(title, url, create_date)
            values (%s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date']))
        self.conn.commit()


# 异步插入数据库
class MysqlTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item)

    def handle_error(self, failure, item):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
        pass


class ArticleImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_file_path = ''
        if 'front_image_url' in item:
            for ok, value in results:
                image_file_path = value['path']
        item['front_image_path'] = image_file_path
        return item
