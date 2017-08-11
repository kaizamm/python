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

### MySQLdb
### subprocess
subprocess包主要是执行外部命令和程序
#### subprocess.call()
父进程等待子进程完成，返回退出信息returncode
```
import subprocess
rc = subprocess.call("ls -l",shell=True)
```
shell=True表示这个命令只能通过shell来运行
#### subprocess.Popen()
```
import subprocess
child = subprocess.Popen(["ping","-c","5","www.baidu.com"])
print("parent process")
```
从运行结果看，父进程在开启子进程之后并没有等待child的完成，而是直接运行print
```
import subprocess
child = subprocess.Popen(["ping","-c","5","www.baidu.com"])
child.wait() #加上这句则需等待子进程执行完成，再执行下面语句
print("parent process")
```
##### 子进程的文本的控制
```
import subprocess
child1 = subprocess.Popen(["ls","-l"],stdout=subprocess.PIPE)
#subprocess.PIPE实际为文本流提供一个缓存区，child1的stdout将文本输出到缓存区，随后child2的stdin从该PIPE中将文本取走
child2 = subprocess.Popen(["wc"],stdin=child1.stdout,stdout=subprocess.PIPE)
out = child2.communicate()
#communicate()是Popen对象的一个方法，该方法会阻塞父进程，直到子进程完成
print(out)
```
我们还可以利用communicate()方法来使用PIPE给子进程输入:
```
import subprocess
child = subprocess.Popen(["cat"], stdin=subprocess.PIPE)
child.communicate("vamei")
```

#### 另可以在父进程中对子进程操作，例如上面的child对象
+ child.poll() #检查子进程状态
+ child.kill() #终止子进程
+ child.send_signal() #向子进程发送信号
+ child.terminate() #终止子进程
子进程的PID存储在child.pid


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
### json
python有许多内置或第三方模块可以将JSON字符转换成python字典对象。如下，使用json模块及及其loads函数逐行加载已经下载好的数据文件，json.loads即可将JSON字符转换成Python形式；json.dumps则将Python对象转换为JSON格式：
```
import json
path = '/tmp/test.txt'
records = [json.loads(line) for line in open(path)]
```
### urllib2
```
from urllib2 import urlopen
```
### python内置字符串方法
+ count 返回字符串中出现次数(非重叠)
+ endswith、startswith 如果字符串以某个后缀结尾(以某个前缀开关)，则返回True
+ join 将字符串用作连接其他字符序列的分隔符
+ index 如果在字符串中找到子串，则返回子串第一个字符所在的位置。如果没有找到，则引发ValueError。
+ find 如果在字符串中找到子串，则返回第一个发现的子串中的第一个字符所在的位置。如果没有找到，则返回-1
+ rfind 如果在字符串中找到子串，则返回最后一个发现的子串的第一个字符所在的位置。如果没有找到，则返回-1
+ replace 用另一个字符串替换指定子串
+ strip、rstrip、lstrip 去除空白符(包括换行符)。相当于对各个元素执行x.strip()(以及rstrip、lstrip)。
+ split 通过指定的分隔符将字符串拆分为一组子串
+ lower、upper 分别将字母字符转换为小写或大写
+ ljust、rjust 用空格(或其他字符)填充字符串的空白侧以返回符合最低宽度字符串

### re
re模块的函数可以分为三个大类：模式匹配、替换以及拆分。当然，它们之间是相辅相成的。一个regex描述了需要在文本中定位一个模式，它可以用于许多目的。如下例子：拆分一个字符串，分隔符为数量不定的一组空白符(制表符，空格，换行符等)。描述一个或多个空白 符的regex是\s+:
```
In [42]: import re
In [43]: text = "foo bar\t baz \tqux"
In [44]: re.split('\s+',text)
Out[44]: ['foo', 'bar', 'baz', 'qux']
```
调用re.split('\s+',text)时，正则表达式会先被编译，然后再在text上调用其split方法。你可以用re.compile自己编译regex以得到一个可重用的regex对象:
```
In [50]: regex = re.compile('\s+')
In [51]: regex.split(text)
Out[51]: ['foo', 'bar', 'baz', 'qux']
```
如果只希望得到匹配regex的所有模式，则可以使用findall方法：
```
In [52]: regex.findall(text)
Out[52]: [' ', '\t ', ' \t']
```
> 注意：如果想避免正则表达式中不需要的转义(\)，则可以使用原始字符串字面量如r'C:\x'(也可以编写其等价式'C:\\x')。
如果打算对许多字符串用同一条正则表达式，强烈建议通过re.compile创建regex对象。这样可以节省大量的CPU时间。match和search跟findall功能类似。findall返回的是字符串中所有的匹配项，而search则只返回第一个匹配项。match更加严格，它只匹配字符串的首首部。如下例子：
```
In [53]: text = """Kaiz kaiz@quarkfinance.com
   ....: zkai zkai@google.com
   ....: Rob rob@gmail.com
   ....: Ryan ryan@yahoo.com
   ....: """
In [54]: pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
#re.IGNORECASE的作用是对大小写不敏感，对于regex,匹配对象只能告诉我们模式在原字符串中的起始和结束位置
In [57]: regex = re.compile(pattern,flags=re.IGNORECASE)
#findall返回是一个列表
In [58]: regex.findall(text)
Out[58]: ['kaiz@quarkfinance.com', 'zkai@google.com', 'rob@gmail.com', 'ryan@yahoo.com']
```
search返回的是文本中的第一个电子邮件地址(以特殊的匹配项对象形式返回)
```
In [74]: m = regex.search(text)
In [75]: m
Out[75]: <_sre.SRE_Match at 0x20e2a58>
In [81]: m.group()
Out[81]: 'kaiz@quarkfinance.com'
In [83]: text[m.start():m.end()]
Out[83]: 'kaiz@quarkfinance.com'
```
regex.match则将返回None，因为它只匹配出现在字符串开头的模式：
```
In [84]: m = regex.match(text)
In [89]: print m
None
```
另外还有一个sub方法，它会将匹配到的模式替换为指定字符串，并返回所得到的新字符串：
```
In [90]: print regex.sub('REDACTED',text)
Kaiz REDACTED
zkai REDACTED
Rob REDACTED
Ryan REDACTED
```
假设你不仅想要找出电子邮件地址，还想将各个地址分成3个部分：用户名、域名以及域后缀。要实现此功能，只需将分段的模式的各部分用圆括号包起来即可：
```
In [103]: regex =  re.compile(r'([A-Z0-9._%+-]+)@([a-z0-9.-]+)\.([A-Z]{2,4})', re.IGNORECASE)
In [104]: m = regex.match('kaiz@quarkfinance.com')
#由这种正则表达式所产生的匹配对象，可以通过其groups方法一个由模式各段组成的元组：
In [105]: m.groups()
Out[105]: ('kaiz', 'quarkfinance', 'com')
```
findall则不需要groups()方法，可直接返回一个元组列表：
```
In [106]: regex.findall(text)
Out[106]:
[('kaiz', 'quarkfinance', 'com'),
 ('zkai', 'google', 'com'),
 ('rob', 'gmail', 'com'),
 ('ryan', 'yahoo', 'com')]
```
