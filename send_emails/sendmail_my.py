# -*- coding: utf-8 -*-
# @Time : 8/6/2020 1:47 PM
# @Author : Peter yang
import os, datetime, win32
import win32com.client as win32
recipientsPath  = r'.\Recipients.txt'
HTMLBodyPath    = r'.\emailBody.html'
emailTitlePath  = r'.\emailTitle.txt'

def sendmail():
    total_space_2 = 10
    used_space_2 = 8
    free_space_2 = 2
    percentage_free_space_2 = 80

    now_time = datetime.datetime.now().strftime('%F %T')

    outlook = win32.Dispatch('Outlook.Application')

    mail_item = outlook.CreateItem(0)  # 0: olMailItem

    body_dict = {
        'total_space_2': total_space_2,
        'used_space_2': used_space_2,
        'free_space_2': free_space_2,
        'percentage_2': format(percentage_free_space_2, '.1f'),  # Isilon2
        'now_time': now_time
    }

    for recipient in open(recipientsPath).read().split('\n'):  # Add Recipients from file
        if '#' not in recipient:
            mail_item.Recipients.Add(recipient)

    mail_item.Subject = open(emailTitlePath).read().strip('\n')

    mail_item.BodyFormat = 3
    content = open(HTMLBodyPath).read()
    for key in body_dict:
        content = content.replace('{' + key + '}', str(body_dict[key]))

    mail_item.HTMLBody = content

    mail_item.Send()
    print('successful !')


if __name__ == "__main__":
    try:
        sendmail()
    except KeyboardInterrupt:
        print('Manually Stopped')
        os.system('pause')
