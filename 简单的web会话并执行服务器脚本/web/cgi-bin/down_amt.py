#!/usr/local/python3.6/bin/python3.6
# -*- coding: UTF-8 -*-



def get_data(mail):
  import cgi,sys
  form = cgi.FieldStorage()
  try:
    itop_id = form['itop'].value
    code = form['code'].value
  except Exception:
    #print('Error,itop及进件单号不能为空') 
    reshtml = '''Content-Type: text/html\n
  <!doctype html>
  <html lang="en">
   <head>
    <meta charset="UTF-8">
    <meta name="Author" content="kaiz">
    <meta name="Keywords" content="quark">
    <meta name="Description" content="down_amt">
    <title>down_amat</title>
   </head>
   <BODY><H2>ERROR</H2>
   itop编号及进件单号为空<P> 
    <li><a href="http://172.30.30.5:8000/"> 返回</a></li><br>
  </html>
  ''' 
    print(reshtml)
    sys.exit('1')
  reshtml = '''Content-Type: text/html\n
  <!doctype html>
  <html lang="en">
   <head>
    <meta charset="UTF-8">
    <meta name="Author" content="kaiz">
    <meta name="Keywords" content="quark">
    <meta name="Description" content="down_amt">
    <title>down_amt</title>
   </head>
   <BODY><H3>SUCCESS</H2>
   <B>Hi,您的itop编号为:%s</B><P> 
   <B> Hi,您的进件单号为:%s</B><P>
   <B>降额脚本已为您处理，并已将邮件发至 %s </B> <p>
    <li><a href="http://172.30.30.5:8000/"> 返回</a></li><br>
  </html>
  ''' % (itop_id,code,mail)
  print(reshtml) 
  return(code,itop_id)

def app_sql(code):
    app_code = code
    sql1 = "DELETE FROM qcreditadm.app_queue_log WHERE app_id IN (SELECT id FROM app.app_main WHERE app_code in(%s)) AND status_order > '140';" %(app_code,) + "\r\r"
    sql2_1 = "UPDATE app.app_queue SET is_reset = 'Y',app_status = 'FAPPRDISPED',thd_deal_status = '',thd_app_code = '',status_phase='PHASE_APPR',do_action='sysRTDisp',is_final='N',status_order=140 WHERE app_code IN (%s);" %(app_code,) + "\r\r"
    sql2_2 = "UPDATE app.app_main SET app_status='FAPPRDISPED' where app_code in(%s);" %(app_code,) + "\r\r"
    sql2_3 = "UPDATE app.app_dcout SET dcout_is_final='N', dcout_final_decision = '' WHERE app_id  IN (SELECT id FROM app.app_main WHERE app_code IN (%s));" %(app_code,) + "\r\r"
    sql2_4 = "UPDATE app.app_dcin SET dcin_decision_code = '', dcin_action = 'sysRTDisp', dcin_manual_Decision = '' WHERE app_id  IN (SELECT id FROM app.app_main WHERE app_code IN (%s));" %(app_code,) + "\r\r"
    sql3 = "DELETE FROM app.qc_bd_changes_his WHERE main_app_code IN (%s);" %(app_code,) + "\r"
    app_content = "--qcreditadm用户执行--\n" + "--等待终审-删除log--\n" + sql1 + "--app用户执行--\n" + "--等待终审-无指定--\n" + sql2_1 + sql2_2 + sql2_3 + sql2_4 + "--删除同步历史--\n" + sql3
    return app_content

def quotabid_sql(code):
    bid_app_code = code
    sql1 = "DELETE FROM quotabid.qb_bid_info WHERE bid_app_code IN (%s);\n" %(bid_app_code,) + "\r"
    sql2 = "DELETE FROM quotabid.qb_bid_detail_info WHERE bid_code IN (SELECT bid_code FROM quotabid.qb_bid_info WHERE bid_app_code IN (%s));" %(bid_app_code,) + "\r\r"
    sql3 = "DELETE FROM quotabid.qb_bid_config WHERE bid_app_code in(%s);" %(bid_app_code,) + "\r"
    quotabid_content = "--quotabid用户执行--\n" + "--删除标的数据，重新审核！--\n" + sql2 + sql1 + sql3
    return quotabid_content

def send_mail(to_list,sub,content,itop_id):
    mail_port = 25
    mail_host = 'mail.quarkfinance.com'
    mail_user = 'qingpengzhao'
    mail_pass = 'ZQPmdy53542316'
    mail_postfix = 'quarkfinance.com'
    import smtplib
    from email.mime.text import MIMEText
    me = " 降额申请 " + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = itop_id + sub
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
 #mailto_list = ['kaiz@quarkfinance.com','qingpengzhao@quarkfinance.com']
 #mailto_list = ['kaiz@quarkfinance.com']
 mailto_list = ['lingwang@quarkfinance.com','zhiyuzhang@quarkfinance.com','shuguangxie@quarkfinance.com','yunzhicui@quarkfinance.com','jinggao@quarkfinance.com','itapplicationsupport@quarkfinance.com','hangzhang@quarkfinance.com']
 data = get_data(mailto_list)
 send_mail(mailto_list,"降额申请-审核",app_sql(data[0]),data[1])
 send_mail(mailto_list,"降额申请-标的",quotabid_sql(data[0]),data[1])

