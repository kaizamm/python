#!/usr/bin/env
# _*_coding:UTF-8_*_

__Author__ = "kaiz"

import os,sys,re,requests

def get_appid():
  res = requests.get('http://cmdb.quark.com/api/App/getapplist')
  list_app = res.text.split(",")
  list_app_dst = filter(lambda x:re.search("ApplicationID",x),list_app)
  list_app_dst = map(lambda x:re.search('\d+',x).group(),list_app_dst)
  list_app_dst = map(int,list_app_dst)
  return list_app_dst

def get_info(appid_list):
  import requests,json
  global input_modelname_ 
  resq = ""
  # POST传入的参数
  for appid in appid_list:
    data = {'ApplicationID':appid}
    res = requests.post('http://cmdb.quark.com/api/Host/getapphostlist/api/Host/getmodulehostlist',data=data)
    resq += str(res.text)
  # 将接果转化成列表
  list_raw = re.split('ApplicationID',resq)
  count = 0
  while count < 3:
    #给定的关键字
    input_modelname_ = (count == 0 and len(sys.argv)>1 and sys.argv[1]  or raw_input("\033[1;32;40m请输入要匹配的关键字或IP:\033[0m"))
    #取出符合关键字的列表，筛选对应module
    list_module = filter(lambda x:re.search(input_modelname_,x,re.IGNORECASE),list_raw)
    if list_module: 
      break
    else:
      print "\033[1;31;40m[Info]Nothing Match,%s Times Chance Left,Again...\033[0m" % (3-count)
    count +=1
  else:
    sys.exit("\033[1;31;40m[Error]Nothing Matched For 3 Times!\033[0m")
  #对过滤出来的结果分组，
  list_dst = map(lambda x:re.split(',',x),list_module)
  #过滤特定字段
  list_ = map(lambda y: filter(lambda x:re.search('ApplicationName|ModuleName|SetName|InnerIP|HostName',x),y),list_dst)
  #打印信息
  for item in list_:
    item_ = map(lambda x:x.decode('unicode-escape'),item)
    print "\033[1;31;40mIndex:\033[0m \033[1;5;40m%s\033[0m".center(50,'*') % list_.index(item) ,item_[0],"\033[1;31;40m%s\033[0m" % item_[1],item_[2],item_[3],item_[4]
  i = 0
  while i < 3:
    i +=1
    try:
      input_index = raw_input("\033[1;32;40m若输入闪烁的Index，则直接登陆对应IP主机；若需继续搜索，请输入关键字或IP:\033[0m")
      input_index_ = int(input_index)
    except ValueError,e:
      #若是输入的字符串，则在搜索中的结果中继续搜索
      list_module_ = filter(lambda y: filter(lambda x:re.search(input_index,x,re.IGNORECASE),y),list_)
      for item in list_module_:
        item_ = map(lambda x:x.decode('unicode-escape'),item)
        print "\033[1;31;40mIndex:\033[0m \033[1;5;40m%s\033[0m".center(50,'*') % list_.index(item) ,item_[0],"\033[1;31;40m%s\033[0m" % item_[1],item_[2],item_[3],item_[4]
      print "\033[1;31;40m[Info]你还有%s次搜索机会\033[0m" % (3-i)
      continue
    except Exception,e:
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
    sys.exit("\033[1;31;40m[Info]Just 3 Times, Exit...\033[0m")
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
      passwd = getpass.getpass(prompt='\033[1;32;40m请输入您的Ldap帐户密码:\033[0m')
      ssh.connect(ip,22,user,passwd)
      break
    except paramiko.ssh_exception.AuthenticationException,e:
      print '\033[1;31;40m[INFO]Wrong Ldap Passwd , %s Chance Left\033[0m' % (3-i)
  else:
    sys.exit('\033[1;31;40m[Error]Wrong Passwd 3 Times,Exit!\033[0m')
  os.system('clear')
  print '\033[1;32;40m*** Hi,%s, 欢迎登陆至 %s 若要退出至跳板机请直接按 Ctrl + D ***\033[0m' % (user,ip)
  #channel = ssh.invoke_shell(term='vt100',width=80,height=50,width_pixels=0,height_pixels=0)
  channel = ssh.invoke_shell(term='xterm',width=196)
  #channel = ssh.invoke_shell(term = 'xterm+256color')
  interactive.interactive_shell(channel)
  #关闭连接
  channel.close()
  ssh.close()

if __name__ == "__main__":
  try:
    appid_list =  get_appid()
    ip = get_info(appid_list = appid_list) 
    login(ip)
  except Exception,e:
    sys.exit("\n\033[1;31;40m[Error]Invalid Input,Exit...\033[0m")
