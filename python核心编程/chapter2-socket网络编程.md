---
title: chapter2-socket网络编程
date: 2017.7.19
---
###


### 利用socket通信,python提供两种方法:socket对象及文件类对象
#### socket对象
+ send()
+ sendto()
+ recv()
+ recvfrom()
#### 文件类对象
+ read()
+ write()
+ readline()

### 异常
+ 与一般I/O和通信有关的: socket.error
+ 与查询地址信息有关的socket.gaierror
+ 与其他地址错误有关的socket.herror
+ 与在一个socket上调用settimeout()后，处理超时有关的socket.timeout
在connetct(0)的调用时，如果程序可以解决把主机名转换成IP地址的问题，可能产生两种错误，如果主机名不对则会产生socket.gainerror，如果连接远程主机有问题则会产生socket.error

### 必需的参数
+ port： 描述了端口号，或者定义在/etc/services的名字，这个端口号是服务器应该侦听的，例如 80,http
+ type: 若是tcp，则type是SOCK_STREAM;若是udp，则是dgram
+ protocol: tcp或者是udp
+ invocationtype: 对于tcp服务器，invocationtype应该是nowait;对于udp，如果服务器连接远程机器并为来自不同的机器的信息包请求一个新的进程来处理，那么使用nowait。如果UDP在它的端口上处理所有的信息包，直到它终止，那么应该使用wait。
+ username： username 指定了服务器应该在哪个用户下运行
+ path: path是指服务器的完整路径
+ programname: 表示程序的名字，就像在sys.argv[0]中传递的那样
+ arguments: 这个参数是可选的，如果有，则在服务器的脚本中以sys.argv[1:]显示

>  注意，因为socket在连接时，只能有一个进程来连接，若每每个socket开一个进程，势必则会将内存占满；故需要配置xinetd

### syslog模块
python提供了一个可以作为系统syslog程序接口的syslog模块。在开始记录信息之前，需调用openlog()函数来初始化syslog的接口，
```
openlog(ident[,logopt[,facility]])
```
