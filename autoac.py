# -*- coding:utf-8 -*-
import hashlib
import sqlite3 as sqlite

class user:
    def __init__(self, name = None,psw = None):
        self.name = name
        self.psw = hashlib.sha1(psw).hexdigest()

class AccessControlor:
    def __init__(self):
        self.conn = sqlite.connect("ac.db")
        self.READ, self.WRITE, self.DELETE, self.EXECUTE, self.OWN, self.CONTROL = range(6)
    def has_access(self,s_id,o_id,access):
        res = self.con.execute("select id from authorize where subject=? and \
                object=? and access=?", (s_id, o_id, access)).fetchone()
        return (res != None )

    def can_read(self,s_id,o_id):
        return self.has_access(s_id,o_id,self.READ)
    def can_write(self, s_id, o_id):
        return self.has_access(s_id,o_id,self.WRITE)
    def can_execute(self, s_id,o_id):
        return self.has_access(s_id,o_id,self.DELETE)
    def can_delete(self, s_id, o_id):
        return self.has_access(s_id,o_id,self.EXECUTE)
    def can_own(self, s_id, o_id):
        return self.has_access(s_id,o_id,self.OWN)
    def can_control(self, s_id, o_id):
        return self.has_access(s_id,o_id,self.CONTROL)
    def login(self,username, password):
        theuser = user(username, password)
        # if the subject has the user return ture else return false
        res = self.conn.execute("select id,is_admin from subject where name=? and pwd=?",
        (theuser.name,theuser.psw).fetchone())
        return (res != None)









def test():
    long = user("long", "long")
    print long.psw

def main():
    test()

if __name__ == '__main__':
    main()