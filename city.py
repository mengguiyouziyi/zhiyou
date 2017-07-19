# coding:utf-8

import os
import sys
from os.path import dirname

import pymysql

from get_city import city as citys

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)


def send_key():
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	# mysql = pymysql.Connect(host='localhost', user='root', password='3646287', db='spiders', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	try:
		with mysql.cursor() as cursor:
			sql = """select com_id, com_name from zy_all where city = ''"""
			cursor.execute(sql)
			results = cursor.fetchall()
			for result in results:
				try:
					com_id = result['com_id']
					com_name = result['com_name']
					if not com_name:
						continue
					city_li = [city for city in citys if com_name.find(city) > 0]
					if len(city_li) != 1:
						continue
					city = city_li[0]
					sql1 = """replace into zy_all_city(com_id, com_name, city) VALUES (%s, %s, %s)"""
					cursor.execute(sql1, (com_id, com_name, city))
					mysql.commit()
				except Exception as e:
					print(com_id)
					print(e)
					continue
	finally:
		mysql.close()


if __name__ == '__main__':
	send_key()
