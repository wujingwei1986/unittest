#coding:gb18030
import time,os,sys,requests
import unittest
sys.path.append('../db_fixture')
import test_data

class AddEventTest(unittest.TestCase):
    ''' ��ӷ����� '''

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event/"

    def tearDown(self):
        print(self.result)

    def test_add_event_all_null(self):
        ''' ���в���Ϊ�� '''
        payload = {'eid':'','':'','limit':'','address':"",'start_time':''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_add_event_eid_exist(self):
        ''' id�Ѿ����� '''
        payload = {'eid':1,'name':'һ��4������','limit':2000,'address':"���ڱ���",'start_time':'2017'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id already exists')

    def test_add_event_name_exist(self):
        ''' �����Ѿ����� '''
        payload = {'eid':11,'name':'����Pro������','limit':2000,'address':"���ڱ���",'start_time':'2017'}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event name already exists')

    def test_add_event_data_type_error(self):
        ''' ���ڸ�ʽ���� '''
        payload = {'eid':11,'name':'һ��4�ֻ�������','limit':2000,'address':"���ڱ���",'start_time':'2017'}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('start_time format error.', self.result['message'])

    def test_add_event_success(self):
        ''' ��ӳɹ� '''
        payload = {'eid':11,'name':'һ��4�ֻ�������','limit':2000,'address':"���ڱ���",'start_time':'2017-05-10 12:00:00'}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')


if __name__ == '__main__':
    test_data.init_data() # ��ʼ���ӿڲ�������
    unittest.main()

