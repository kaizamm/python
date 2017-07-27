---
title: gitlab搭建.md
date: 2017.07.11
---
### 安装
安装:https://about.gitlab.com/installation/#centos-7


### 配置
sudo gitlab-ctl reconfigure

### 服务
+ nginx
+ gitlab-shell
+ gitlab-workhorse
+ logrotate日志管理
+ postgresql
+ redis
+ sidekiq 队列任务，异步执行
+ unicorn HTTPserver

### 目录
+ /opt/gitlab
+ /etc/gitlab
