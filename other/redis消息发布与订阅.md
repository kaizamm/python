---
title: redis消息发布与订阅
date: 2017.10.26
---
### python 与 redis
+ 安装
```
 pip install redis
 ```
+ redis使用
 ```
 import redis
 r = redis.StrictRedis() # 默认为127.0.0.1，端口2379
 r = redis.StrictRedis(host='127.0.0.1',port=6379,db=0) #显式地指定需要连接的地址
 r.set('foo','bar')  #True
 r.get('foo') #'bar'
 r.sadd('websit','yahoo')  #加入集合
 r.sadd('websit','google')  
 r.smembers('website')  # {'google', 'yahoo'}
 r.hmset('dict',{'name':'Bob'})  #存储字典
 people = r.hgetall('dict')
 print people  #{'name':"Bob"}
 ```
+ 事务和管道
```
pipe = r.pipeline
pipe.set('foo','bar')
pipe.get('foo')
result = pipe.execute()
print result
```

### 实践：web.py及redis实现在线好友

+ 代码

```
#!/usr/bin/env python
# coding:utf-8
import web
import time
import redis

r = redis.StrictRedis()
'''
配置路由规则
'/': 模拟用户的访问
'/online': 查看在线用户
'''
urls = (
'/', 'visit',
'/online', 'online'
)

'''返回当前时间的对应的键名
如28分对应的键名是active.users:28
'''
def time_to_key(current_time):
  return 'active.users:' + time.strftime('%M',time.localtime(current_time))

'''返回最近10分钟的键名
结果是列表类型
'''
def keys_in_last_10_minutes():
  now = time.time()
  result = []
  for i in range(10):
    result.append(time_to_key(now - i*60))
  print result
  return result

class visit:
  '''模拟用户访问
  将用户的User agent作为用户的ID加入到当前时间对应的键中
  '''
  def GET(self):
    user_id = web.ctx.env['HTTP_USER_AGENT']
    current_key = time_to_key(time.time())
    pipe = r.pipeline()
    pipe.sadd(current_key,user_id)
    设置键的生存时间为10分钟
    pipe.expire(current_key, 10*60)
    pipe.execute()

    return 'User:\t' + user_id + '\r\nKey:\t' + current_key + '\n' + "circle:\n\t" + str(r.smembers(current_key))
    #return "circle:" + r.smembers(user_id)

class online:
  '''查看当前在线的用户列表'''
  def GET(self):
    online_users = r.sunion(keys_in_last_10_minutes())
    result = ''
    for user in online_users:
      result += 'User agent:' + user + '\r\n'
    return result

if __name__ == '__main__':
  app = web.application(urls,globals())
  app.run()
```

+ 效果图

![效果图1][效果图1]
[效果图1]: ./redis消息发布与订阅/效果图1.png
