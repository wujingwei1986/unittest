# -*- coding: GB18030 -*-
import os,time
import unittest
import HTMLTestRunner
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

#获取run_main的路径
curr_path = os.path.dirname(os.path.realpath(__file__))

def add_case(caseDirectory="testCase",caseName="test*.py"):
    #添加用例
    case_path = os.path.join(curr_path,caseDirectory)
    #如果用例文件夹不存在，自动创建
    if not os.path.exists(case_path):
        os.mkdir(case_path)
        print ("test case path is %s" %case_path)
    discover = unittest.defaultTestLoader.discover(case_path,pattern=caseName,top_level_dir=None)
    return discover

def run_case(allcase,reportName="reports"):
    #执行所有用例并把报告写入HTML中
    report_path = os.path.join(curr_path,reportName)
    if not os.path.exists(report_path):
        os.mkdir(report_path)
        print ("report path is %s" %report_path)
    now = time.strftime("%Y-%m-%M-%H_%M_%S",time.localtime(time.time()))
    report_abspath = os.path.join(report_path,now + "_result.html")

    with open(report_abspath,'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'自动化测试报告',
        description=u'详细报告:'
        )
        runner.run(allcase)

def get_report_file(report_path):
    #获取最新report文件
    lists = os.listdir(report_path)

    lists.sort(key = lambda filename: os.path.getmtime(os.path.join(report_path,filename)))
    print (u"最新生成的测试报告：" + lists[-1])
    report_file = os.path.join(report_path,lists[-1])
    return report_file

def send_email(sender,passwd,receiver,smtpserver,report_file):
    #发送邮件
    #定义邮件内容
    msg = MIMEMultipart()
    msg['Subject'] = u"自动化测试报告"
    msg['from'] = sender
    msg['to'] = receiver

    #添加附件
    attachment = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')
    attachment["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    attachment["Content-Disposition"] = 'attachment; filename="report.html"'
    msg.attach(attachment)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    #用户密码
    smtp.login(sender,passwd)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()
    print(u"邮件发送成功！")
    '''
    try:
        smtp = smtplib.SMTP_SSL(smtpserver,port)#qq邮箱用SSL
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,port)
    #用户密码
        smtp.login(sender,passwd)
        smtp.sendmail(sender,receiver,msg.as_string())
        smtp.quit()
        print(u"邮件发送成功！")
    '''
if __name__ == '__main__':
    all_case = add_case() #添加用例
    run_case(all_case)
    report_path = os.path.join(curr_path,"reports")
    report_file = get_report_file(report_path)

    from config import read_cfg
    smtp_server = read_cfg.smtp_server
    sender = read_cfg.sender
    passwd = read_cfg.passwd
    receiver = read_cfg.receiver
    port = read_cfg.port

    send_email(sender,passwd,receiver,smtp_server,report_file)
