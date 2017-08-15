# -*- coding: GB18030 -*-
#wujingwei
import requests,string,time,os,json
import MySQLdb as mysql

class db_MySQL(object):
    #����mysql�ķ�����connect('ip','user','password','dbname')
    def __init__(self,ip,user,password,dbname):
        self.ip = ip
        self.user = user
        self.passwd = password
        self.dbname = dbname
        self.connection = self.db_connect()
    def db_connect(self):
        try:
            dbcon = mysql.connect(host = self.ip, user = self.user, passwd = self.passwd, db = self.dbname, charset='utf8')
            return dbcon
        except:
            print u"����ʧ��"
            pass
    def db_Query(self,name,table,vin_param):
        sql = "select " + name + " from " + table + " where vin = " + "\'" + vin_param +  "\'"
        print "MySQL���ʽΪ��%s"%sql
        cursor = self.connection.cursor()
        cursor.execute(sql)
        query_result = cursor.fetchone()
        #�ص��α�
        cursor.close()
        #self.conn.close()
        return query_result

    # clear table data
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    # insert sql statement
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key   = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        #print(real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)

        self.connection.commit()

    # close database
    def close(self):
        self.connection.close()

    # init data
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':

    db = db_MySQL()
    table_name = "sign_event"
    data = {'id':1,'name':'����','`limit`':2000,'status':1,'address':'������չ����','start_time':'2016-08-20 00:25:42'}
    table_name2 = "sign_guest"
    data2 = {'realname':'alen','phone':12312341234,'email':'alen@mail.com','sign':0,'event_id':1}

    db.clear(table_name)
    db.insert(table_name, data)
    db.close()
