# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 21:21:07 2020

@author: wez1cgd4,uyw2szh
"""


import time
import datetime
import psutil
import os

import win32com.client as win32

g_Disk_path1    = r'\\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\01_GEN4'
g_Disk_path2    = r'\\abtvdfs2.de.bosch.com\ismdfs\loc\szh\DA\Radar\05_Radar_ER'
recipientsPath  = r'.\Recipients.txt'
timePath        = r'.\SendTime.txt'
HTMLBodyPath    = r'.\emailBody.html'
emailTitlePath  = r'.\emailTitle.txt'

g_setTime       = {}

# g_setTime = { 'morning'    :  {'hour':8,   'min':30},
#               'afternoon'  :  {'hour':13,  'min':30},}
#               # 'demo'       :  {'hour':11,  'min':6},}

def setSendingTime(Path):
  global g_setTime
  tmp = open(Path).read().split('\n')[1:]

  for i in tmp:
    if '#' not in i:
      i = i.split(';')
      g_setTime[i[0]] = { 'hour':int(i[1]),  'min':int(i[2])}
    
def getDiskInfos(diskPath):
  
  disk_info = psutil.disk_usage(diskPath)

  total_space=int(disk_info[0]/1024/1024/1024/1024) #单位换成T,磁盘总空间
  used_space=int(disk_info[1]/1024/1024/1024/1024) #单位换成T，磁盘已用空间
  free_space=int(disk_info[2]/1024/1024/1024/1024) #单位换成T，磁盘剩余空间
  percentage_free_space=100-disk_info[3]           #磁盘剩余空间百分比

  return total_space,used_space,free_space,percentage_free_space

def sendmail():
  # start =time.perf_counter() 
  

  #Isilon1
  # total_space_1,used_space_1,free_space_1,percentage_free_space_1 = getDiskInfos(g_Disk_path1)


  #Isilon2
  total_space_2,used_space_2,free_space_2,percentage_free_space_2 = getDiskInfos(g_Disk_path2)

  # end = time.perf_counter()
  # spend_time=end-start

  # if percentage_free_space_1 < 1 or percentage_free_space_2 < 4:
  if percentage_free_space_2 < 4:
    pass
  else:
    return None

  now_time = datetime.datetime.now().strftime('%F %T')  

  outlook = win32.Dispatch('Outlook.Application')
  
  mail_item = outlook.CreateItem(0) # 0: olMailItem

  #dict
  # body_dict = { 'total_space_1':total_space_1,
  #               'used_space_1' :used_space_1,
  #               'free_space_1' :free_space_1,
  #               'percentage_1' :format(percentage_free_space_1,'.1f'),#Isilon1
  body_dict = {
              'total_space_2':total_space_2,
              'used_space_2' :used_space_2,
              'free_space_2' :free_space_2,
              'percentage_2' :format(percentage_free_space_2,'.1f'),#Isilon2
              'now_time' :now_time
              }


  # mail_item.Recipients.Add('Stephanie.ZHANG@cn.bosch.com')
  # mail_item.Recipients.Add('Shiyun.ZHAO@cn.bosch.com')
  # mail_item.Recipients.Add('Jerry.SUN@cn.bosch.com')
  # mail_item.Recipients.Add('Yura.FU@cn.bosch.com')
  # mail_item.Recipients.Add('external.Shuang.Yu2@cn.bosch.com')
  # mail_item.Recipients.Add('zhongjie.wei@cn.bosch.com')
  # mail_item.Recipients.Add('fixed-term.Yuhao.WU@cn.bosch.com')
  # mail_item.Recipients.Add('Lijuan.Zhu4@cn.bosch.com')

  # print('Sending To ...')
  for recipient in open(recipientsPath).read().split('\n'):# Add Recipients from file
    # print(recipient)
    if '#' not in recipient:
      mail_item.Recipients.Add(recipient)


  mail_item.Subject = open(emailTitlePath).read().strip('\n')

  # text= "Hello all, " \
  #     "The following information is automatically sent out by the python script. "  \
  #     "Usage of Isolon storage space: " \
  #     "Total space is " + str(total_space) +"T, "  \
  #     "used space is " + str(used_space) +"T, " \
  #     "free space is " + str(free_space)+"T, " \
  #     "free space percentage is " + str(format(percentage_free_space,'.1f'))+"%. "\
  #     "The update time of the above information is " +str(now_time) +". For your reference, thanks."  


  mail_item.BodyFormat = 3  
  # mail_item.HTMLBody='''
  # <div style="font-size: 20; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;">
  #   <p>Hello all, </p>
  #   <div style="text-indent: -em; margin-left: 2em;">
  #       <p>The following information is automatically sent out by the python script. </p>

  #       <p>Usage of <font color="red">Isilon2</font> storage space: </p>
  #       <ol>
  #           <li>Total space is {total_space_2} T,</li>
  #           <li>used space is {used_space_2} T,</li>
  #           <li>free space is <font color="red">{free_space_2} T</font>, free space percentage is <font color="red">{percentage_2} %</font>. </li>
  #       </ol>
  #       <p></p>
  #       <p>Usage of <font color="red">Isilon1</font> storage space: </p>
  #       <ol>
  #           <li>Total space is {total_space_1} T,</li>
  #           <li>used space is {used_space_1} T,</li>
  #           <li>free space is <font color="red">{free_space_1} T</font>, free space percentage is <font color="red">{percentage_1} %</font>. </li>
  #       </ol>
        
  #       <p>The update time of the above information is {now_time}. For further details, please refer to <a href='http://szhsimu.apac.bosch.com/'>http://szhsimu.apac.bosch.com/</a>, thanks.</p>
  #   </div>
  #   <p>Best regards,</p>
  #   <p>Wei.Zhongjie, Wu.Yuhao</p>
  # </div>'''.format(**dict)
  content =  open(HTMLBodyPath).read()
  for key in body_dict:
    content = content.replace('{'+key+'}',str(body_dict[key]))


  mail_item.HTMLBody=content
   
  mail_item.Send()
  print('successful !')

def checkTime(setTime):
  time_now = {'hour'  :time.localtime().tm_hour ,
              'min'   :time.localtime().tm_min  ,}
  for s in setTime:
    if (setTime[s]['hour'] == time_now['hour']) and (setTime[s]['min'] == time_now['min']):
      return True

  return False
 
def run():

  while(True):
    start = time.time()
    setSendingTime(timePath)
    # print(checkTime(g_setTime))
    if checkTime(g_setTime):
      sendmail()
      print('last sent time:{}'.format(time.strftime('%Y-%m-%d  %H:%M',time.localtime())))
    end = time.time()

    # it will spend some time to run above code, thus we need to substract time used to avoid sleep time > 60, it might cause program skip the whole minute
    time.sleep(60 - (start-end))

if __name__ == "__main__":
  try:
    run()
  except KeyboardInterrupt:
    print('Manually Stopped')
    os.system('pause')