# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZySpy170709Item(scrapy.Item):
	# define the fields for your item here like:
	id = scrapy.Field()
	com_id = scrapy.Field()
	com_name = scrapy.Field()
	heat = scrapy.Field()
	short_intro = scrapy.Field()
	nature_size = scrapy.Field()
	industry = scrapy.Field()
	short_name = scrapy.Field()
	intro = scrapy.Field()
	location = scrapy.Field()
	com_url = scrapy.Field()
	job_num = scrapy.Field()
	jobs = scrapy.Field()
	city = scrapy.Field()
	com_tab = scrapy.Field()
	load_time = scrapy.Field()
