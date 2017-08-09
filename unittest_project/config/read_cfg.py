# -*- coding: GB18030 -*-
import os,time
import ConfigParser

curr_path = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(curr_path,"cfg.ini")
conf = ConfigParser.ConfigParser()
conf.read(configPath)

smtp_server = conf.get("email","smtp_server")
sender = conf.get("email","sender")
passwd = conf.get("email","passwd")
receiver = conf.get("email","receiver")
port = conf.get("email","port")