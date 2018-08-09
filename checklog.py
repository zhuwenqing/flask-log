import sys
import os 
import time
import datetime
logpath='/root/GetDayLog/tmp/'
date=time.strftime("%Y%m%d",time.localtime())
path=logpath+'20180801'
# print(os.listdir(path))
# print(date)
# logfile='2018080123-sn.163ar.cn.gz'
# os.system("zcat "+ logfile +" |awk -F' ' '$8 !~ /403|404/ {print $9}' | awk -F'/' '{print $3}' |sort |uniq -c | sort -nr")
dirs=os.listdir(path)
# print(aList)
# print(type(dirs))
dirs.sort()
for logfile in dirs:
    print(logfile)
    os.system("zcat "+ os.path.join(path,logfile) +" |awk -F' ' '$8 !~ /403|404/ {print $9}' | awk -F'/' '{print $3}' |sort |uniq -c | sort -nr")

