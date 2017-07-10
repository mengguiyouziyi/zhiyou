# -*- coding: utf-8 -*-
import scrapy
import json
import re
from urllib.parse import urljoin
# from scrapy.exceptions import CloseSpider
from zy_spy_170709.items import ZySpy170709Item
from zy_spy_170709.utils.get import get_id


class JobuiSpider(scrapy.Spider):
	name = 'jobui'
	allowed_domains = ['jobui.com']
	com_url = 'http://www.jobui.com/company/{com_id}/'
	salary_url = 'http://www.jobui.com/company/{com_id}/salary/'
	job_url = 'http://www.jobui.com/company/{com_id}/jobs/'

	def start_requests(self):
		while True:
			com_id = get_id()
			print(com_id)
			# com_id = 14270508
			if not com_id:
				continue
			item = ZySpy170709Item()
			item['com_id'] = com_id
			self.url1 = self.com_url.format(com_id=com_id)
			yield scrapy.Request(self.url1, meta={'item': item, 'dont_redirect': True})

	def parse(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		com_id = item['com_id']
		com_name = response.xpath('//h1[@id="companyH1"]/@data-companyname').extract_first()
		heat = response.xpath('//div[@class="fl ele fs16 gray9 mr10"]/text()').extract_first()
		heat = ''.join(heat.split()) if heat else ''
		short_intro = response.xpath('//p[@class="fs16 gray9 sbox company-short-intro"]/text()').extract_first()
		short_intro = short_intro if short_intro else ''

		text1 = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]//text()').extract()
		if '公司信息：' in text1:
			nature_size = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]/dd[1]/text()').extract_first() #性质及规模
		else:
			nature_size = ''
		industrys = response.xpath('//dd[@class="comInd"]/a/text()').extract() #行业
		industry = ','.join(industrys)
		short_name = response.xpath('//dd[@class="gray3"]/text()').extract_first()
		short_name = short_name if short_name else ''
		intros = response.xpath('//p[@id="textShowMore"]/text()').extract()
		if intros:
			intro = ''.join([i.strip() for i in intros])
		else:
			intro = ''
		text2 = response.xpath('//dl[@class="dlli fs16"]//text()').extract()
		if '公司地址：' in text2:
			location = response.xpath('//dl[@class="dlli fs16"]/dd[1]/text()').extract_first()
			city = response.xpath('//span[@class="company-map"]/a/@data-map-city').extract_first()
		else:
			location = city = ''

		if '公司网站：' in text2:
			com_url = response.xpath('//dl[@class="dlli fs16"]/dd[2]/a/@href').extract_first()
		else:
			com_url = ''
		job_nums = response.xpath('//div[@class="middat cfix"]/a[2]/span/text()').extract_first()
		job_num = job_nums if '///' not in job_nums else ''

		item['com_name'] = com_name
		item['heat'] = heat
		item['short_intro'] = short_intro
		item['nature_size'] = nature_size
		item['industry'] = industry
		item['short_name'] = short_name
		item['intro'] = intro
		item['location'] = location
		item['city'] = city
		item['com_url'] = com_url
		item['job_num'] = job_num

		self.url2 = self.salary_url.format(com_id=com_id)
		yield scrapy.Request(self.url2, meta={'item': item, 'job_nums': job_nums}, callback=self.parse_salary)

	def parse_salary(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		com_id = item['com_id']
		job_nums = response.meta.get('job_nums', '')
		com_tabs = response.xpath('//div[@class="company-tab-box sbox j-tab-box fs14"]/span/a/text()').extract()
		com_tab = ','.join(com_tabs)
		item['com_tab'] = com_tab

		if '///' in job_nums:
			item['jobs'] = ''
			yield item
		else:
			self.url3 = self.job_url.format(com_id=com_id)
			yield scrapy.Request(self.url3, meta={'item': item}, callback=self.parse_job)

	def parse_job(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		job_titles = response.xpath('//ul[@class="col-informlist j-joblist"]/li/h3/a/text()').extract()
		job_urls = response.xpath('//ul[@class="col-informlist j-joblist"]/li/h3/a/@href').extract()
		job_ids = [re.search(r'/job/(\d+)/', job_url).group(1) for job_url in job_urls]

		# 不管有没有下一页，都会进行此步操作
		job_id = response.meta.get('job_ids', [])
		job_title = response.meta.get('job_titles', [])

		job_ids.extend(job_id)
		job_titles.extend(job_title)

		text3 = response.xpath('//p[@class="pager cfix box"]//text()').extract()
		if '上一页' in text3:
			next = response.xpath('//a[@class="pg-updown"][2]/@href').extract_first()
		else:
			next = response.xpath('//a[@class="pg-updown"]/@href').extract_first()

		if next:
			page_nt = urljoin(response.url, next)
			yield scrapy.Request(page_nt, meta={'item': item, 'job_ids': job_ids, 'job_titles': job_titles}, callback=self.parse_job)
		else:
			jobs = dict(zip(job_ids, job_titles))
			item['jobs'] = json.dumps(jobs, ensure_ascii=False)
			yield item
