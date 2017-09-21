#!/bin/usr/env python
# -*- coding: UTF-8 -*-
import cx_Oracle
import smtplib
from email.mime.text import MIMEText

itop_id = raw_input("请输入ITOP编号及标题：")

code = raw_input("请输入进件编号：")


def bid(code):
    cxn = cx_Oracle.connect('biddbread/biddbread@172.30.32.159:1521/BIDDB')
    cur = cxn.cursor()
    sql = "Select bid_code,bid_contract_no,bid_app_code,bid_state from quotabid.qb_bid_info a where a.bid_app_code in(%s) and a.bid_state in('BS_WHB')" % code
    cur.execute(sql)
    out_list = cur.fetchall()
    cxn.close()
    #return map(lambda x:map(str,x),out_list)
    return map(lambda x:map(str,x),out_list)
    #return out_list

def send_mail(to_list,sub,content,itop):
    #mailto_list = ['lingwang@quarkfinance.com','zhiyuzhang@quarkfinance.com','shuguangxie@quarkfinance.com','yunzhicui@quarkfinance.com','jinggao@quarkfinance.com','itapplicationsupport@quarkfinance.com','hangzhang@quarkfinance.com']
    mail_port = 25
    mail_host = 'mail.quarkfinance.com'
    mail_user = 'qingpengzhao'
    mail_pass = 'ZQPmdy53542316'
    mail_postfix = 'quarkfinance.com'
    me = itop_id + "未划标告警" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = itop+sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP(mail_host,mail_port)
        s.login(mail_user,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(str(e))
        return False

if __name__ == "__main__" :
    mailto_list = ['itapplicationsupport@quarkfinance.com']
    cnn = bid(code)
    if cnn:
      send_mail(mailto_list,"未划标告警",str(cnn)+'\n请驳回协议，并取消挂标',itop_id)
    else:
      print "None"
    

