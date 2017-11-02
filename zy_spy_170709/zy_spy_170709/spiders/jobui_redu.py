# -*- coding: utf-8 -*-
import scrapy
import time
import re
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from rediscluster import StrictRedisCluster
from zy_spy_170709.items import ZySpy170709Item

# from zy_spy_170709.utils.get_redu import get_key

startup_nodes = [{"host": "172.29.237.209", "port": "7000"},
                 {"host": "172.29.237.209", "port": "7001"},
                 {"host": "172.29.237.209", "port": "7002"},
                 {"host": "172.29.237.214", "port": "7003"},
                 {"host": "172.29.237.214", "port": "7004"},
                 {"host": "172.29.237.214", "port": "7005"},
                 {"host": "172.29.237.215", "port": "7006"},
                 {"host": "172.29.237.215", "port": "7007"},
                 {"host": "172.29.237.215", "port": "7008"}]
#
red = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)


class JobuiSpider(scrapy.Spider):
	name = 'jobui_redu'

	def start_requests(self):
		burl = 'http://www.jobui.com/cmp?area=%E5%85%A8%E5%9B%BD&keyword={comp_name}'
		x = 0
		while True:
			com_id_name = red.lpop('zhiyou_redu')
			# com_id_name = '11066948~北京数之行科技有限公司'
			print(com_id_name)
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
			item['com_id'] = ''
			item['job_num'] = ''
			url = burl.format(comp_name=comp_name)
			yield scrapy.Request(url, meta={'item': item})

	def parse(self, response):
		item = response.meta.get('item')
		if not item:
			return
		# if '没有找到和您查询条件相符的公司' in response.text:
		# 	return
		select = Selector(text=response.text)
		li_tags = select.xpath('//ul[@class="companyList"]/li[@class="atn-li"]/div[@class="atn-content"]')
		if len(li_tags) < 1:
			yield item
			return
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
