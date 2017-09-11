#!/bin/bash
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
echo "11111" >> /data1/spider/menggui/zhiyou/zy_spy_170709/111.out
eval "$(pyenv init -)"
pyenv activate env_ana3-4.3.0
cd /data1/spider/menggui/zhiyou/zy_spy_170709/
echo "22222" >> /data1/spider/menggui/zhiyou/zy_spy_170709/111.out
nohup python ./zy_spy_170709/utils/send.py >./zy_spy_170709/utils/send.out 2>&1 &
echo "33333" >> /data1/spider/menggui/zhiyou/zy_spy_170709/111.out
sleep 1m
nohup python ./cmd.py >>./daily_1.out 2>&1 &
nohup python ./cmd.py >>./daily_2.out 2>&1 &
