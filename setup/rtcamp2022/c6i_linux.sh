#!/bin/bash
yum update -y
# Python 3.7.10がインストール済み
yum install -y git tmux
su ec2-user -c 'git clone https://github.com/demotomohiro/rcauto.git /home/ec2-user/rcauto'
