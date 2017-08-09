# -*- coding: GB18030 -*-
import logging, time
import os
# log_path�Ǵ����־��·��
cur_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
# ������������logs�ļ��У����Զ�����һ��
if not os.path.exists(log_path):os.mkdir(log_path)

class Log():
    def __init__(self):
        # �ļ�������
        self.logname = os.path.join(log_path, '%s.log'%time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # ��־�����ʽ
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # ����һ��FileHandler������д������
        fh = logging.FileHandler(self.logname, 'a')  # ׷��ģʽ  �����python2��
        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # �����python3��
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # ����һ��StreamHandler,�������������̨
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # �����д�����Ϊ�˱�����־����ظ�����
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # �رմ򿪵��ļ�
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

if __name__ == "__main__":
   log = Log()
   log.info("---���Կ�ʼ----")
   log.info("��������1,2,3")
   log.warning("----���Խ���----")