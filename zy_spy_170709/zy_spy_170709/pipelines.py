# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):
	"""
	本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""

	def __init__(self):
		self.conn = pymysql.connect(host='172.31.215.38', port=3306, user='spider', password='spider', db='spider', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		# self.conn = pymysql.connect(host='localhost', user='root', password='3646287', db='spider', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if spider.name == 'jobui':
			sql = """insert into zy_all(com_id, com_name, heat, short_intro, nature_size, industry, short_name, intro, location, com_url, job_num, jobs, city, com_tab) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE com_name=VALUES(com_name),  heat=VALUES(heat),  short_intro=VALUES(short_intro),  nature_size=VALUES(nature_size),  industry=VALUES(industry),  short_name=VALUES(short_name),  intro=VALUES(intro),  location=VALUES(location),  com_url=VALUES(com_url),  job_num=VALUES(job_num),  jobs=VALUES(jobs),  city=VALUES(city),  com_tab=VALUES(com_tab)"""
			args = (
				item["com_id"], item["com_name"], item["heat"], item["short_intro"], item["nature_size"], item["industry"],
				item["short_name"], item["intro"], item["location"], item["com_url"], item["job_num"], item["jobs"],
				item["city"], item["com_tab"])
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			# print(str(item['com_id']) + ' success')
			print(str(item['com_id']))
		elif spider.name == 'jobui_daily':
			sql = """insert into zy_scan_num(com_id, com_name, heat, crawl_time) VALUES(%s, %s, %s, %s)"""
			args = (item["com_id"], item["com_name"], item["heat"], item["crawl_time"])
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			# print(str(item['com_id']) + ' success')
			# print(str(item['com_id']))
		elif spider.name == 'jobui_redu':
			sql = """insert into zy_redu(com_id, com_name, heat) VALUES(%s, %s, %s)"""
			args = (item["com_id"], item["com_name"], item["job_num"])
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			# print(str(item['com_id']) + ' success')
			# print(str(item['com_id']))
