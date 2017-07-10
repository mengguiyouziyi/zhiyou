# coding:utf-8

import os
import sys
from os.path import dirname

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)

from my_redis import QueueRedis

"""
本机 localhost；服务器 a027.hb2.innotree.org
"""
red = QueueRedis()


def send_id():
	# for id in range(14300000):
	for id in range(1, 1430):
		red.send_to_queue('ids', id)
		print(id)


if __name__ == '__main__':
	send_id()