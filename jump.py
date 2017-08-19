#!/usr/bin/env
# _*_coding:UTF-8_*_

__Author__ = "kaiz"

import os,sys,re,time

def get_info():
  import requests,json
  #POST传入的参数
  data = {'ApplicationID':2}
  res = requests.post('http://testcmdb.quark.com/api/Host/getapphostlist/api/Host/getmodulehostlist',data=data)
  #将接果转化成列表
  list_raw = re.split('ApplicationID',str(res.text))
  count = 0
  while count < 3:
    count +=1
    #给定的关键字
    input_modelname_ = raw_input("\033[1;32;40m关键字或IP:\033[0m")
    #取出符合关键字的列表，筛选对应module
    list_module = filter(lambda x:re.search(input_modelname_,x),list_raw)
    if list_module: 
      break
    else:
      print "\033[1;31;40m[Info]Nothing Match,%s Times Chance Left,Again...\033[0m" % (3-count)
  else:
    sys.exit("\033[1;31;40m[Error]Nothing Matched For 3 Times!\033[0m")
  #对过滤出来的结果分组，
  list_dst = map(lambda x:re.split(',',x),list_module)
  #过滤特定字段
  list_ = map(lambda y: filter(lambda x:re.search('ApplicationName|ModuleName|SetName|InnerIP|HostName',x),y),list_dst)
  #打印信息
  for item in list_:
    print '****'+ "\033[1;31;40mIndex:\033[0m" + "\033[1;5;40m%s\033[0m" % list_.index(item)+ '****',item
  i = 0
  while i < 3:
    i +=1
    try:
      input_index_ = input("\033[1;32;40mPlease_Choose_Index_Above_To_Login_To_The_IP_Host:\033[0m")
    except NameError,e:
      print "\033[1;31;40m[Info]Wrong Index,%s Times Chance Left,Again...\033[0m" % (3-i)
      continue
    if isinstance(input_index_,(int)):
      if input_index_ < len(list_):
        break
      else:
        print "\033[1;31;40m[Info]Wrong Index,%s Times Chance Left,Again...\033[0m" % (3-i)
    else:
      print "\033[1;31;40m[Info]Wrong Index,%s Times Chance Left,Again...\033[0m" % (3-i)
  else:
    sys.exit("\033[1;31;40m[Error]Wrong Index Input  For 3 Times!\033[0m")
  des = list_[input_index_]
  #过滤出IP 
  m = filter(lambda item: 'InnerIP' in item,des)
  ip_ = m[0].split(':')[1].strip('"')
  print ip_
  return ip_

#登陆
def login(ip):
  import getpass,paramiko,interactive
#  paramiko.util.log_to_file('/tmp/login.log')
  user = getpass.getuser()
  if user == "root": sys.exit("\033[1;31;40m[Erorr]Please Use Your Ldap To Login Nor Root \033[0m")
  print '****'+"\033[1;31;40mHi,%s,Welcome Login To \033[0m" % user  + "\033[1;33;40m%s\033[0m"  % ip + '****'
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  i = 0
  while i < 3: 
    i += 1
    try:
      passwd = getpass.getpass(prompt='\033[1;32;40mPasswd:\033[0m')
      ssh.connect(ip,22,user,passwd)
      break
    except paramiko.ssh_exception.AuthenticationException,e:
      print '\033[1;31;40m[INFO]Wrong Ldap Passwd , %s Chance Left\033[0m' % (3-i)
  else:
    sys.exit('\033[1;31;40m[Error]Wrong Passwd 3 Times,Exit!\033[0m')
  channel = ssh.invoke_shell()
  interactive.interactive_shell(channel)
  #关闭连接
  channel.close()
  ssh.close()

if __name__ == "__main__":
  ip = get_info() 
  login(ip)
