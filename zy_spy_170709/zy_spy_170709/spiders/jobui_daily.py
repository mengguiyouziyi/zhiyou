# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from zy_spy_170709.items import ZySpy170709Item
from zy_spy_170709.utils.get import get_key
from zy_spy_170709.settings import SQL_DATETIME_FORMAT


class JobuiSpider(scrapy.Spider):
	name = 'jobui_daily'
	allowed_domains = ['jobui.com']
	com_url = 'http://www.jobui.com/company/{com_id}/'

	def start_requests(self):
		while True:
			con_id_name = get_key('con_id_name')
			if not con_id_name:
				continue
			lis = con_id_name.split('~')
			com_id = int(lis[0])
			com_name = lis[1]
			item['com_id'] = com_id
			item['com_name'] = com_name
			item = ZySpy170709Item()
			item['com_id'] = com_id
			item['com_name'] = com_name
			self.url = self.com_url.format(com_id=com_id)
			yield scrapy.Request(self.url, meta={'item': item, 'dont_redirect': True})

	def parse(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		# com_name = response.xpath('//h1[@id="companyH1"]/@data-companyname').extract_first()
		heat = response.xpath('//div[@class="fl ele fs16 gray9 mr10"]/text()').extract_first()
		heat = ''.join(heat.split()) if heat else ''

		item['heat'] = heat
		item['crawl_time'] = datetime.now().strftime(SQL_DATETIME_FORMAT)


