#!/usr/bin/env python
# _*_ coding=utf-8 _*_

import sys,os,re

def buy_goods():
    serial = raw_input("id of buy:")
    serial = int(serial)
    if serial >= len(goods_list):
        sys.exit("invalid serial input")
    num = raw_input("numbers of buy:")
    num = int(num)
    goods_name = goods_list[serial][0]
    if choose_goods.has_key(goods_name):
        choose_goods[goods_name] += num
    else:
        choose_goods[goods_name] = num
    print "you will buy" + str(choose_goods)

def go_on_buy():
    go_on = raw_input("go on buy? Y or N")
    if go_on.upper() == "Y": #继续买,将输入的字母转化为大写
        buy_goods()
        go_on_buy()
    elif go_on.upper() == "N": #不买了，登陆后结账
        login_payoff()
    else:
        print "invalid input,retry" #非法输入重新判断
        go_on_buy()

def login_payoff():
    with open("user_list.txt","r") as f: #把user_list.txt文件读取后转化为列表user_list
        for line in f.readlines():
            line_list = line.strip().split()
            user_list.append(line_list)
    print user_list
    login_flag = False  #False表示未登陆成功，True表示登陆成功
    count = 0  #密码最多可以输入三次，输错三次后锁定
    while(count<3):
        user_name = raw_input("username:")
        user_passwd = raw_input("password:")
        for item in user_list:
            if user_name == item[0] and user_passwd == item[1]:
                login_flag = True  #login_flag为登陆标志
                print login_flag
                break  #当验证难过，跳出for循环
            else:
                login_flag = False
        if login_flag:
            print "*"*12+"login success" +"*"+ user_name+"*"*12
            bill = 0.0
            for i in choose_goods:
                for j in goods_list:
                    if i == j[0]:
                        bill += float(j[2])*choose_goods[i]
            user_list_str = ""  #对应user_list的字符串，即将写入文件user_list.txt
            for i in user_list:
                if  user_name == i[0]:
                    print "*"*12 + "cost" +" "+ str(bill)+ "***"+"remain"+" "+str(float(i[2])-bill)
                    if i[2] >= bill:  #判断余额是否足够
                        i[2] = str(float(i[2]) - bill)  #购物完后从余额里去除消费的金额后写进文件
                        for m in user_list:
                            user_list_str += " ".join(m)+"\n" #变量user_list_str是要写进文件user_list的字符串形式
                            with open("user_list.txt","w+") as f:
                                f.write(user_list_str)
                    else:
                        print u"你的余额不足"
                else:
                    continue
            break  #跳出while循环
        else:
            print "*"*12+"login fail,retry" + "*"+user_name+ "*"*12  #登陆失败可重试三次
            count +=1
    else:
        sys.exit("auth fail 3 tries,exit")

if __name__ == '__main__':  #主程序开始
    #print goods_serial
    goods_list = []
    user_list = []
    choose_goods = {} #购物清单，字典表示，货物：数量(int)
    with open("goods_list.txt","r") as f:
        for line in f.readlines():
            line_list = line.strip().split()
            goods_list.append(line_list)

    print "goods available as follows:"
    for i in goods_list:
        print "*"*12+u"  id:%s  %s  ￥%s/per  " % (goods_list.index(i),i[0],i[1])+"*"*12
    buy_goods()
    go_on_buy()
