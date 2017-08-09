# -*- coding: GB18030 -*-
import os,time
import unittest
import HTMLTestRunner
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

#��ȡrun_main��·��
curr_path = os.path.dirname(os.path.realpath(__file__))

def add_case(caseDirectory="testCase",caseName="test*.py"):
    #�������
    case_path = os.path.join(curr_path,caseDirectory)
    #��������ļ��в����ڣ��Զ�����
    if not os.path.exists(case_path):
        os.mkdir(case_path)
        print ("test case path is %s" %case_path)
    discover = unittest.defaultTestLoader.discover(case_path,pattern=caseName,top_level_dir=None)
    return discover

def run_case(allcase,reportName="reports"):
    #ִ�������������ѱ���д��HTML��
    report_path = os.path.join(curr_path,reportName)
    if not os.path.exists(report_path):
        os.mkdir(report_path)
        print ("report path is %s" %report_path)
    now = time.strftime("%Y-%m-%M-%H_%M_%S",time.localtime(time.time()))
    report_abspath = os.path.join(report_path,now + "_result.html")

    with open(report_abspath,'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'�Զ������Ա���',
        description=u'��ϸ����:'
        )
        runner.run(allcase)

def get_report_file(report_path):
    #��ȡ����report�ļ�
    lists = os.listdir(report_path)

    lists.sort(key = lambda filename: os.path.getmtime(os.path.join(report_path,filename)))
    print (u"�������ɵĲ��Ա��棺" + lists[-1])
    report_file = os.path.join(report_path,lists[-1])
    return report_file

def send_email(sender,passwd,receiver,smtpserver,report_file):
    #�����ʼ�
    #�����ʼ�����
    msg = MIMEMultipart()
    msg['Subject'] = u"�Զ������Ա���"
    msg['from'] = sender
    msg['to'] = receiver

    #��Ӹ���
    attachment = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')
    attachment["Content-Type"] = 'application/octet-stream'
    # �����filename��������д��дʲô���֣��ʼ�����ʾʲô����
    attachment["Content-Disposition"] = 'attachment; filename="report.html"'
    msg.attach(attachment)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    #�û�����
    smtp.login(sender,passwd)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()
    print(u"�ʼ����ͳɹ���")
    '''
    try:
        smtp = smtplib.SMTP_SSL(smtpserver,port)#qq������SSL
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,port)
    #�û�����
        smtp.login(sender,passwd)
        smtp.sendmail(sender,receiver,msg.as_string())
        smtp.quit()
        print(u"�ʼ����ͳɹ���")
    '''
if __name__ == '__main__':
    all_case = add_case() #�������
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
