#!/bin/bash
yum update -y
# Python 3.7.10がインストール済み
yum install -y git tmux
su ec2-user -c 'git clone https://github.com/demotomohiro/rcauto.git /home/ec2-user/rcauto'

# https://ffmpeg.org/
# ffmpegはリポジトリにないのでyumでインストールできない。
su ec2-user -c 'wget -P ~ https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz'
su ec2-user -c 'tar xf ~/ffmpeg-release-amd64-static.tar.xz -C ~'
su ec2-user -c 'echo export PATH=~/ffmpeg-5.0.1-amd64-static:\$PATH >> ~/.bashrc'
