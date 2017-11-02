# -*- coding: utf-8 -*-
import scrapy
import time
import re
from scrapy import Selector
from scrapy.exceptions import CloseSpider
from zy_spy_170709.items import ZySpy170709Item
from zy_spy_170709.utils.get import get_key


class JobuiSpider(scrapy.Spider):
	name = 'jobui_redu'
	com_url = 'http://www.jobui.com/company/{com_id}/'

	def start_requests(self):
		burl = 'http://www.jobui.com/cmp?area={comp_name}'
		x = 0
		while True:
			com_id_name = get_key('comp_id_name')
			if not com_id_name:
				x += 1
				if x > 5:
					raise CloseSpider('no datas')
				time.sleep(60)
				continue
			lis = com_id_name.split('~')
			# com_id = int(lis[0])
			comp_name = lis[1]
			item = ZySpy170709Item()
			# item['com_id'] = com_id
			item['com_name'] = comp_name
			url = burl.format(comp_name=comp_name)
			yield scrapy.Request(url, meta={'item': item})

	def parse(self, response):
		item = response.meta.get('item')
		if not item:
			return
		if '没有找到和您查询条件相符的公司' in response.text:
			yield item
			return
		select = Selector(text=response.text)
		li_tags = select.xpath('//ul[@class="companyList"]/li[@class="atn-li"]/div[@class="atn-content"]')
		li = li_tags[0]
		comp_name = li.xpath('.//span[@class="fl"]/a[@class="fs18 mr5"]/text()').extract_first()
		if item['com_name'] != comp_name:
			yield item
			return
		com_id = li.xpath('.//span[@class="fl"]/span[@class="admin-companyID"]/text()').extract_first()
		job_num_str = li.xpath('.//div[@class="cmpInfoList"]/a[last()]/text()').extract_first()
		job_num = re.search(r'\d+', job_num_str).group()
		item['com_id'] = com_id
		item['job_num'] = job_num
		yield item
