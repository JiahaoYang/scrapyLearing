# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from articleSpider.settings import SQL_DATETIME_FORMAT


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y/%m%d').date()
    except Exception:
        create_date = datetime.datetime.now().date()
    return create_date


class ArticleItemLoader(ItemLoader):
    default_input_processor = TakeFirst()


def get_num(value):
    match_re = re.match(r'.*(\d).*', value)
    if match_re:
        num = match_re.group(1)
    else:
        num = 0

    return num


def remove_comment(value):
    if '评论' in value:
        return ''
    return value


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(lambda x: x)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment),
        output_processor=Join(',')
    )
    content = scrapy.Field()


class ZhihuQuestionItem(scrapy.Item):
    id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comment_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_question(id, topics, url, title, content, answer_num, comment_num,
              watch_user_num, click_num, crawl_time
              )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), 
            comment_num=VALUES(comment_num), watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        id = self["id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = get_num("".join(self["answer_num"]))
        comment_num = get_num("".join(self["comment_num"]))
        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0].replace(',', ''))
            click_num = int(self["watch_user_num"][1].replace(',', ''))
        else:
            watch_user_num = int(self["watch_user_num"][0].replace(',', ''))
            click_num = 0
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (id, topics, url, title, content, answer_num, comment_num,
                  watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comment_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_answer(id, url, question_id, author_id, content, praise_num, comment_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comment_num=VALUES(comment_num), 
              praise_num=VALUES(praise_num), update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comment_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params
