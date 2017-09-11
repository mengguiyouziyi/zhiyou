#!/bin/bash
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv activate env_ana3-4.3.0

U_V1=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
U_V2=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
U_V3=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $3}'`

echo your python version is : $U_V1.$U_V2.$U_V3 >> /data1/spider/menggui/zhiyou/zy_spy_170709/111.out

#cd /data1/spider/menggui/zhiyou/zy_spy_170709/

nohup python /data1/spider/menggui/zhiyou/zy_spy_170709/zy_spy_170709/utils/send.py >>/data1/spider/menggui/zhiyou/zy_spy_170709/zy_spy_170709/utils/send.out 2>&1 &
echo "33333" >> /data1/spider/menggui/zhiyou/zy_spy_170709/111.out

sleep 1m
nohup python /data1/spider/menggui/zhiyou/zy_spy_170709/cmd.py >>/data1/spider/menggui/zhiyou/zy_spy_170709/daily_1.out 2>&1 &
nohup python /data1/spider/menggui/zhiyou/zy_spy_170709/cmd.py >>/data1/spider/menggui/zhiyou/zy_spy_170709/daily_2.out 2>&1 &
