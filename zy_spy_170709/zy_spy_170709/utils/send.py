# coding:utf-8

import os
import sys
import pymysql
import time
from os.path import dirname

from my_redis import QueueRedis

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)


def send_key(key):
	"""
		本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	# mysql = pymysql.Connect(host='localhost', user='root', password='3646287', db='spiders', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	try:
		with mysql.cursor() as cursor:
			sql = """select com_id, com_name from zy_daily ORDER BY com_id"""
			# print('begain')
			cursor.execute(sql)
			results = cursor.fetchall()
			values = [str(i['com_id']) + '~' + i['com_name'].strip() for i in results]
	finally:
		mysql.close()

	red = QueueRedis()

	if values:
		for i, value in enumerate(values):
			# print(i+1)
			red.send_to_queue(key, value)

		# print('done')


if __name__ == '__main__':
	# while True:
	# 	send_key(key='com_id_name')
	# 	time.sleep(86400)
	send_key(key='com_id_name')
















# """
# 本机 localhost；服务器 a027.hb2.innotree.org
# """
# red = QueueRedis()
# def send_id():
# 	for id in range(1, 14300000):
# 	# for id in range(1, 10000):
# 		red.send_to_queue('ids', id)
# 		print(id)


# if __name__ == '__main__':
# 	send_id()