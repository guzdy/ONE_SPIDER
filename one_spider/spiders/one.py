# -*- coding: utf-8 -*-
import scrapy
from one_spider.items import OneItemArticle, OneItemImage, OneItemQuestion
from scrapy.loader import ItemLoader
import html2text


class OneSpider(scrapy.Spider):
    name = 'one'
    start_urls = ['http://wufazhuce.com/']

    def parse(self, response):
        """分析首页，获取最新数据"""
        # image 部分
        img_url_latest = response.xpath('//div[@class="fp-one"]//div[@class="item active"]'
                                        '/a/@href').extract_first()
        print(img_url_latest)
        img_num_latest = int(img_url_latest.split('/')[-1])
        print(img_num_latest)
        for num in range(14, img_num_latest+1):  # 14页开始
            img_url = 'http://wufazhuce.com/one/'+str(num)
            yield response.follow(img_url, callback=self.parse_img)

        # article 部分
        article_url_latest = response.xpath('//div[@class="fp-one-articulo"]//p[@class='
                                            '"one-articulo-titulo"]/a/@href').extract_first()
        print(article_url_latest)
        article_num_latest = int(article_url_latest.split('/')[-1])
        print(article_num_latest)
        for num in range(55, article_num_latest+1):  # 55
            # 实际上顺序是很混乱的
            article_url = 'http://wufazhuce.com/article/'+str(num)
            yield response.follow(article_url, callback=self.parse_article)

        # question 部分
        question_url_latest = response.xpath('//div[@class="fp-one-cuestion"]//p[@class='
                                             '"one-cuestion-titulo"]/a/@href').extract_first()
        print(question_url_latest)
        question_num_latest = int(question_url_latest.split('/')[-1])
        print(question_num_latest)
        for num in range(8, question_num_latest+1):  # 8
            question_url = 'http://wufazhuce.com/question/'+str(num)
            yield response.follow(question_url, callback=self.parse_question)

    def parse_img(self, response):
        print('抓取{}成功，正在抓取数据'.format(response.url))
        loader = ItemLoader(item=OneItemImage(), response=response)
        loader.add_xpath('img_url', '//div[@class="one-imagen"]/img/@src')
        img_num = response.xpath('//title/text()').re('\d+')
        loader.add_value('img_num', img_num)
        description = response.xpath('//div[@class="one-cita"]/text()').extract_first().strip()
        loader.add_value('description', description)
        img_info = response.xpath('string(//div[@class="one-imagen-leyenda"])').extract_first().strip()
        loader.add_value('img_info', img_info)
        date_raw = response.xpath('//div[@class="one-pubdate"]/p/text()').extract()
        loader.add_value('date', date_raw[0]+' '+date_raw[1])
        loader.add_value('url', response.url)
        return loader.load_item()

    def parse_article(self, response):
        print('抓取{}成功，正在抓取数据'.format(response.url))
        loader = ItemLoader(item=OneItemArticle(), response=response)
        loader.add_xpath('description', '//meta[@name="description"]/@content')
        title = response.xpath('string(//title)').extract_first().strip(' - 「ONE · 一个」').strip()
        loader.add_value('title', title)
        author = response.xpath('string(//p[@class="articulo-autor"])').extract_first()\
            .strip().strip('作者/')
        loader.add_value('author', author)
        text_raw = response.xpath('//div[@class="articulo-contenido"]').extract_first()
        loader.add_value('article', html2text.html2text(text_raw))
        loader.add_value('url', response.url)
        return loader.load_item()

    def parse_question(self, response):
        print('抓取{}成功，正在抓取数据'.format(response.url))
        loader = ItemLoader(item=OneItemQuestion(), response=response)
        quest = response.xpath('//h4/text()').extract_first().strip()
        loader.add_value('quest', quest)
        quest_detail = response.xpath('//div[@class="cuestion-contenido"]/text()').extract_first().strip()
        loader.add_value('quest_detail', quest_detail)
        answer_raw = response.xpath('//div[@class="cuestion-contenido"][2]').extract_first()
        loader.add_value('answer', html2text.html2text(answer_raw))
        author = response.xpath('//h4[2]/text()').extract_first().strip()
        if author:
            loader.add_value('author', author)
        loader.add_value('url', response.url)
        return loader.load_item()

