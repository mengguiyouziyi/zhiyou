# coding:utf-8
import os
import sys
import pymysql
from rediscluster import StrictRedisCluster
from os.path import dirname

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)
startup_nodes = [{"host": "172.29.237.209", "port": "7000"},
                 {"host": "172.29.237.209", "port": "7001"},
                 {"host": "172.29.237.209", "port": "7002"},
                 {"host": "172.29.237.214", "port": "7003"},
                 {"host": "172.29.237.214", "port": "7004"},
                 {"host": "172.29.237.214", "port": "7005"},
                 {"host": "172.29.237.215", "port": "7006"},
                 {"host": "172.29.237.215", "port": "7007"},
                 {"host": "172.29.237.215", "port": "7008"}]

red = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)


def send_key(key):
	"""
	172.31.215.38
	"""
	mysql = pymysql.connect(host='172.31.215.38', port=3306, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	try:
		with mysql.cursor() as cursor:
			sql = """select com_id, comp_name from gaoxin_qiyemingdan"""
			cursor.execute(sql)
			results = cursor.fetchall()
			values = [str(i['com_id']) + '~' + i['comp_name'].strip() for i in results]
	finally:
		mysql.close()

	if values:
		for i, value in enumerate(values):
			red.rpush(key, value)


if __name__ == '__main__':
	send_key(key='zhiyou_redu')
