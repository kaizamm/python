#!/usr/bin/env python
# _*_ encoding: UTF-8 _*_
__author__="kaiz"

import os,sys,time

#处理日志
class anaysislog:
    #两个变量，备份目录及目录名，初始化
    def __init__(self,bak_path,log_path,save_days):
        self.bak_path = bak_path
        self.log_path = log_path
        self.save_days = save_days

    #压缩日志文件
    def logrotate(self):
        #开始压缩
        print "[info]start logrotate,wait..."
        #文件压缩信号
        if not os.path.isdir(bak_path): os.makedirs(bak_path)
        logrotate_file_flag1 = os.popen('find %s -mtime +%s -name "*txt" ' % (log_path,save_days)).readlines()
        logrotate_file_flag2 = os.popen('find %s -mtime +%s -name "*log" ' % (log_path,save_days)).readlines()
        logrotate_file_flag3 = os.popen('find %s -mtime +%s -name "*gz" ' % (log_path,save_days)).readlines()
        logrotate_file_flag4 = os.popen('find %s -mtime +%s -name "*bz2" ' % (log_path,save_days)).readlines()
        log_path_ = os.path.dirname(os.path.dirname(log_path))
        logrotate_file_flag5 = os.popen('find %s -name "catalina.out" ' % log_path_).readlines()
        logrotate_file_flag6 = os.popen('find %s -mtime +30 ' % bak_path).readlines()
        #开始移动日志到备份目录
        os.popen('find %s -mtime +%s -name "*txt" -exec mv {} %s \;' % (log_path,save_days,bak_path))
        os.popen('find %s -mtime +%s -name "*log" -exec mv {} %s \;' % (log_path,save_days,bak_path))
        os.popen('find %s -name "*gz" -exec mv {} %s \;' % (log_path,bak_path))
        os.popen('find %s -name "*bz2" -exec mv {} %s \;' % (log_path,bak_path))
        #删除bak_path的一个月以前的压缩文件
        if logrotate_file_flag6:
            os.popen('find %s -mtime +30 -exec rm {} -rf \;' % bak_path)
            print "del files before 30 days under %s" % bak_path
        #将备份目录里的日志压缩打包
        os.popen('find %s  -name "*log" -exec bzip2 {} \;' % bak_path)
        #是否有文件被移动或catalina.out是否被清空
        if logrotate_file_flag1 or logrotate_file_flag2 or logrotate_file_flag3 or logrotate_file_flag4:
            print "[info]logrotate success"
        elif logrotate_file_flag5:
            #清空catalina.out
            with open (logrotate_file_flag5[0].strip(),"r+") as f:
                f.truncate()
            print "[info]just truncate catalina.out"
        else:
            print "[info]logrotate nothing"

#主程序从这开始
if __name__ == "__main__":
    #实例化
    try:
    #源日志目录
        log_path = sys.argv[1]
        #备份目录，取当前时间
        cur_time = time.strftime('%Y-%m-%d-%H:%M')
        bak_path_ = sys.argv[2]
        bak_path = bak_path_+'/'+cur_time
        #在源日志目录保留日志的天数
        save_days = sys.argv[3]
        a = anaysislog(log_path,bak_path_,log_path)
        #压缩
        a.logrotate()
    except Exception,e:
        err = "[error]"+cur_time+str(e)+"\n"
        with open("/tmp/lograte_err.log","a+") as f:
          f.write(err)
        print err
