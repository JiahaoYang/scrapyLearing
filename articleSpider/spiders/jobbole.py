# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.http import Request

from articleSpider.items import ArticleItem
from articleSpider.items import ArticleItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取列表页所有文章url，下载解析
        2. 获取下一页url，下载，调用parse
        """

        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            # yield 将request请求交给scrapy下载，urljoin拼接相对地址，mata将参数传递到parse_detail的response参数中
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url},
                          callback=self.parse_detail)

        next_url = response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        """
        提取文章具体字段
        """

        # article_item = ArticleItem()
        #
        # title = response.css('.entry-header h1::text').extract_first('')
        # create_date = response.css('.entry-meta-hide-on-mobile::text').extract_first('')\
        #     .strip().replace('·', '').strip()
        # praise_nums = response.css('.vote-post-up h10::text').extract_first(0)
        # fav_nums = response.css('.bookmark-btn::text').extract_first('')
        # match_re = re.match(r'.*(\d).*', fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        # else:
        #     fav_nums = 0
        # comment_nums = response.css('a[href="#article-comment"] span::text').extract_first('')
        # match_re = re.match(r'.*(\d).*', comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        # else:
        #     comment_nums = 0
        # content = response.css('div.entry').extract_first('')
        # tags = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tag_list = [tag for tag in tags if not tag.strip().endswith('评论')]
        # tags = ','.join(tag_list)
        # front_image_url = response.meta.get('front_image_url', '')
        #
        # article_item['title'] = title
        # try:
        #     create_date = datetime.datetime.strptime(create_date, '%Y/%m%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['praise_nums'] = praise_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['content'] = content
        # article_item['comment_nums'] = comment_nums
        # article_item['tags'] = tags
        # article_item['front_image_url'] = [front_image_url]
        # article_item['url'] = response.url

        front_image_url = response.meta.get('front_image_url', '')
        item_loader = ArticleItemLoader(item=ArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_css('create_date', '.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('contents', 'div.entry')

        article_item = item_loader.load_item()

        yield article_item
