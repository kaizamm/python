---
title: python几个常模块
date: 2017.7.26
---

### os
操作系统相关
+ os.path  os.path.isdir
+ os.name
+ os.popen  该方法不但执行命令还返回执行后的信息对象
+ os.curdir
+ os.pardir
+ os.environ
+ os.chdir(dir) 切换目录
+ os.getcwd() 得到当前目录
+ os.getgid/os.getuid/os.getlogin
+ os.system(cmd)  运行cmd命令
+ os.listdir() 列出目录下的文件
+ os.makedirs() 若不存在这个目录则创建,递归
+ os.mkdir()  只创建一层

### sys
系统相关
+ sys.argv 是一个list，包含所有的命令行参数
+ sys.path  是一个list，指明所有modules查找的目录，path[0]是script的目录
+ sys.stdin 标准的输入对象，raw_input() OR input()
+ sys.stdout 标准的输出对象，print
+ sys.stderr 标准的错误输出，用于错误的消息
+ sys.exit(exit_code) 退出程序
+ sys.modules 是一个dictionary，表示系统中所有可用的modules  

### requests
第三方库,安装 pip insstall requests
参考官网http://python-requests.org

#### GET
```
import requests
r = requests.get("https://www.python.org")
r.status_code
> 200

```
#### POST
```
payload = dict(key1='value1',key2='')
r = requests.post('http://httpbin.org/post'，data=payload)
print r.text
>输出结果
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "key1": "value1",
    "key2": "value2"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
    "Content-Length": "23",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.18.1"
  },
  "json": null,
  "origin": "113.57.171.147",
  "url": "http://httpbin.org/post"
}
```
#### PUT
#### DELETE
#### HEAD
#### OPTIONS

### socket
### time
```
cur_time = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
```
