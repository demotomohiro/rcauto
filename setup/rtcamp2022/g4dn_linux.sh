#!/bin/bash
yum update -y
# Python 3.7.10がインストール済み
yum install -y git tmux
su ec2-user -c 'git clone https://github.com/demotomohiro/rcauto.git /home/ec2-user/rcauto'

# NVIDIA gaming driversインストール関係
yum install -y gcc10 make
reboot

## ↑はユーザーデータに設定してインスタンス作成時に実行できる。
# 以下は手動で

# インスタンス立ち上げ時にAdvanced details -> IAM instance profileでS3を読めるinstance profileを指定すればaws configureは不要。
# その場合はIAMでS3を読めるRoleを作成する必要がある。
$ aws configure
Default region name [None]: us-east-1
Default output format [None]: json
$ sh rcauto/setup/rtcamp2022/g4dn_linux_install_driver.sh
sudo reboot
$ sh rcauto/setup/rtcamp2022/g4dn_linux_config_driver.sh
