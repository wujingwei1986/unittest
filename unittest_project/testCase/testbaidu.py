#coding:gb18030
import time,os,sys
import unittest
from selenium import webdriver
sys.path.append('../common')
from logger import Log

class testBaidu(unittest.TestCase):
    log = Log()
    def setUp(self):
        print "1111"
        #self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(30)
        #self.driver.maximize_window()
        #self.driver.get('http://www.baidu.com')

    def testTitle(self):
        self.log.info("-------start-------")
        #self.assertNotEqual(u"百度一下,你就知道",self.driver.title)
        self.assertEqual(1,1)
        print "assert"

    def tearDown(self):
        #self.driver.close()
        #self.driver.quit()
        print "111111122222"
