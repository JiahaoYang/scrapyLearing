# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
import pickle
from urllib import parse
from scrapy.loader import ItemLoader
from articleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers' \
                       '?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_' \
                       'info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_' \
                       'reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_' \
                       'comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_' \
                       'permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_' \
                       'info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_' \
                       'thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.' \
                       'author.follower_count%2Cbadge%5B%2A%5D.topics&limit={1}&offset={2}&sort_by=default'

    def parse(self, response):
        """
        解析首页的问题url，交给parse_question进一步处理
        """
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        for url in all_urls:
            match_obj = re.match(r'(.*question/(\d+))', url)
            if match_obj:
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        match_obj = re.match(r'(.*question/(\d+))', response.url)
        question_id = 0
        if match_obj:
            question_id = int(match_obj.group(2))
        item_loader.add_css("title", ".QuestionHeader-title::text")
        item_loader.add_css("content", ".QuestionHeader-detail")
        item_loader.add_value("url", response.url)
        item_loader.add_value("id", question_id)
        item_loader.add_css("answer_num", ".List-headerText span::text")
        item_loader.add_css("comment_num", ".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
        item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

        question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 5, 0),
                             headers=self.headers, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json['paging']['is_end']
        next_url = ans_json['paging']['next']

        for answer in ans_json['data']:
            answer_item = ZhihuAnswerItem()
            answer_item['id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['question_id'] = answer['question']['id']
            answer_item['author_id'] = answer['author']['id'] if 'id' in answer['author'] else None
            answer_item['content'] = answer['content'] if 'content' in answer else None
            answer_item['praise_num'] = answer['voteup_count']
            answer_item['comment_num'] = answer['comment_count']
            answer_item['update_time'] = answer['updated_time']
            answer_item['create_time'] = answer['created_time']
            answer_item['crawl_time'] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        """
        爬取前模拟登录
        """
        cookies_pkl = pickle.load(open(
            '/Users/jiahaoyang/programs/python/articleSpider/articleSpider/util/cookie.pkl', 'rb'))
        cookies = {}
        for cookie in cookies_pkl:
            cookies[cookie['name']] = cookie['value']
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, cookies=cookies)




