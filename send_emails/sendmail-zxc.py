import time
import datetime
import psutil
import os
import win32com.client as win32  # 发送邮件
from itertools import repeat

state_path    = r'C:\Users\HZX5SZH\Desktop\sendmail\txt' # txt文件夹地址
# recipientsPath  = r'C:\Users\HZX5SZH\Desktop\sendmail\Recipients.txt'  # 邮件接收方
HTMLBodyPath_create    = r'C:\Users\HZX5SZH\Desktop\sendmail\emailBody_create.html'
HTMLBodyPath_complete    = r'C:\Users\HZX5SZH\Desktop\sendmail\emailBody_complete.html'
# emailTitlePath  = r'C:\Users\HZX5SZH\Desktop\sendmail\emailTitle.txt'

# 按行读取txt文件内容，并生成一个列表
def read_txt(path):
  f = open(path)
  content_list = f.readlines()
  return content_list

# 删除path路径下的文件
def delete_txt(path):
  os.remove(path)

# 发送任务创建成功邮件
def send_create_mail(txt_name):
    txt_path = state_path + '\\' + txt_name
    [Server_Name, Project_name, Folder_Path, Email_Address, Task_Progress] = read_txt(txt_path)

    # 截取字符串
    Server_Name = Server_Name[12:]
    Project_name = Project_name[13:]
    Folder_Path = Folder_Path[12:]
    Email_Address = Email_Address[20:]
    Task_Progress = Task_Progress[14:-1]

    if int(Task_Progress) < 10:
        outlook = win32.Dispatch('Outlook.Application')
        mail_item = outlook.CreateItem(0)  # 0: olMailItem

        # 字典创建
        body_dict = {
            'Server Name': Server_Name,
            'Project Name': Project_name,
            'Folder Path': Folder_Path,
            'Bosch Email Address': Email_Address,
            'Task Progress': Task_Progress
        }

        # for recipient in open(recipientsPath).read().split('\n'):# Add Recipients from file
        #   # print(recipient)
        #   if '#' not in recipient:
        #     mail_item.Recipients.Add(recipient)

        # 邮件接收方地址
        mail_item.To = Email_Address
        # 邮件主题字符串
        mail_subject = "PID:{num}/Project name:{name} Task created successfully".format(num=txt_name[:-4],name=Project_name)
        # mail_item.Subject = open(emailTitlePath).read().strip('\n')

        # 邮件主题
        mail_item.Subject = mail_subject

        mail_item.BodyFormat = 3

        # 利用字典向HTML进行值传递
        content = open(HTMLBodyPath_create).read()
        print(type(content))
        for key in body_dict:
            content = content.replace('{' + key + '}', str(body_dict[key]))
        mail_item.HTMLBody = content
        # 邮件发送
        mail_item.Send()
        print('create successful !')

# 发送任务进程结束邮件
def send_complete_mail(txt_name):
  # start =time.perf_counter()
  # now_time = datetime.datetime.now().strftime('%F %T')
# if __name__ == "__main__":

    txt_path = state_path + '\\' + txt_name

    [Server_Name, Project_name, Folder_Path, Email_Address, Task_Progress] = read_txt(txt_path)
    Server_Name = Server_Name[12:]
    Project_name = Project_name[13:]
    Folder_Path = Folder_Path[12:]
    Email_Address = Email_Address[20:]
    Task_Progress = Task_Progress[14:-2]

    # 当进程等于100%时，邮件发送
    if int(Task_Progress) == 100:
        outlook = win32.Dispatch('Outlook.Application')
        mail_item = outlook.CreateItem(0) # 0: olMailItem

        body_dict = {
            'Server Name': Server_Name,
            'Project Name': Project_name,
            'Folder Path': Folder_Path,
            'Bosch Email Address': Email_Address,
            'Task Progress': Task_Progress
        }
        # for recipient in open(recipientsPath).read().split('\n'):# Add Recipients from file
        #   # print(recipient)
        #   if '#' not in recipient:
        #     mail_item.Recipients.Add(recipient)

        mail_item.To = Email_Address

        mail_subject = "PID:{num}/Project name:{name} Task completed successfully".format(num=txt_name[:-4], name=Project_name)
        # mail_item.Subject = open(emailTitlePath).read().strip('\n')
        mail_item.Subject = mail_subject

        mail_item.BodyFormat = 3

        content = open(HTMLBodyPath_complete).read()
        for key in body_dict:
            content = content.replace('{'+key+'}', str(body_dict[key]))
        mail_item.HTMLBody = content
        mail_item.Send()
        print('complete successful !')
        # delete_txt(state_path)

if __name__ == "__main__":

    count_dict = dict()  # 字典创建
    for _ in repeat(None):
        # 设置字典对任务计数，若为新任务，发送任务创建成功邮件给用户，并计数为1；若为旧任务，则只计数。
        listfile = os.listdir(state_path)
        for i in range(len(listfile)):
            for item in listfile:
                if item in count_dict:
                    count_dict[item] += 1
                else:
                    send_create_mail(item)
                    count_dict[item] = 1
            send_complete_mail(listfile[i])

        time.sleep(30)





