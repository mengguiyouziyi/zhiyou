#!/bin/bash
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv activate env_ana3-4.3.0
nohup python /data1/spider/menggui/zhiyou/zy_spy_170709/zy_spy_170709/utils/send.py >/data1/spider/menggui/zhiyou/zy_spy_170709/zy_spy_170709/utils/send.out 2>&1 &
sleep 1m
nohup python /data1/spider/menggui/zhiyou/zy_spy_170709/cmd.py >/data1/spider/menggui/zhiyou/zy_spy_170709/daily_1.out 2>&1 &
nohup python /data1/spider/menggui/zhiyou/zy_spy_170709/cmd.py >/data1/spider/menggui/zhiyou/zy_spy_170709/daily_2.out 2>&1 &
