# -*- coding:utf-8 -*-

import sqlite3 as sqlite
import hashlib
def isValidUser(name=None,password=None):
    psw = hashlib.md5(password).hexdigest()
    database = "ac.db"
    try:
        conn = sqlite.connect(database)
    except:
        print('connect to the database failed')

    res = conn.execute("select id,is_admin from subject where name=? and password=?",
        (name, psw)).fetchone()
    conn.close()
    if res == None:
        res = None, None
    return res

class test:
    def test_isValidUser(self):
        user = 'admin'
        password = 'admin'
        assert (isValidUser(user, password) != None)
if __name__ == '__main__':
    onetest = test()
    onetest.test_isValidUser()