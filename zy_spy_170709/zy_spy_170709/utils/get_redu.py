# coding:utf-8

import os
import sys
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


def get_key(key):
	results = red.blpop(key, 1)
	if results:
		result = results[0].strip()
		return result
	else:
		return 0
