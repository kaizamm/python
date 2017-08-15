---
title: chapter4-多线程编程
date: 2017.8.16
---
### 简介
在多线程编程出现之前，计算机程序执行是由单个步骤顺序执行，但如果多个程序之间并没有因果关系，则影响计算机执行效率。
### 线程和进程
#### 进程
计算机程序只是存储在磁盘上的二进制文件，只有把它们加载到内存中并被操作系统调用，才拥有其生命周期。进程则是一个执行程序。每个进程都拥有其自己的地址的空间、内存、数据栈等，因此采用IPC进程间通信的方式共享信息。进程也可以通过 派生fork、spawn新进程来执行其他任务。
#### 线程
线程是在同一个进程下执行的，共享相同的上下文。线程包括开始、执行顺序、结束三部分。它有一个指令针记录当前的上下文。当其他程序运行时，它可以被抢占(中断)、临时挂起(睡眠)--这种做法叫让步(yielding)。
### python的threading模块
python提供多个模块来支持多线程编程，包括thread、threading、Queue等。避免使用thread，而尽可能使用更高级别的threading。下列是其模块对象
+ Thread: 表示一个执行线程的对象
+ Lock
+ Rlock
+ Condition
+ Event
+ Semaphore
+ BoundedSemaphore
+ Timer
+ Barrier
### threading主要替代品包括以下几个
#### subprocess
派生的主要替代方案，可以单纯的执行任务，或者通过标准文件stdin/stdout/stderr进行进程间通信
#### multiprocess
#### concurrent.futures
