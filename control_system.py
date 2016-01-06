#-*-coding:utf-8 -*-
import sys, hashlib, os
import sqlite3 as sqlite
from datetime import datetime
from controlor import isValidUser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui


class MainWindow(QMainWindow):
    def __init__(self, user_id, is_admin, parent=None):
        super(MainWindow, self).__init__(parent)
        self.uid = user_id
        self.is_admin = is_admin
        self.setWindowTitle(u"自主访问控制实验系统")
        self.central_widget = QWidget()
        self.setFixedSize(690, 400)
        self.center()
        database = 'ac.db'
        self.conn = sqlite.connect(database)
        self.placemenu()
    def placemenu(self):

        # subject actions
        subjectNewAction = self.createAction(u"新建主体...", self.subjectNew,
            "Ctrl+N", None, u"创建新的主体")
        subjectManageAction = self.createAction(u"管理主体...", self.subjectManage,
            "Ctrl+M", None, u"管理主体")
        subjectChangePwdAction = self.createAction(u"修改密码...", self.subjectChangePwd,
            None, None, u"修改我的密码")

        # object actions
        objectNewAction = self.createAction(u"新建客体...", self.objectNew,
            None, None, u"创建新的客体")
        objectImportAction = self.createAction(u"导入客体...", self.objectImport,
            None, None, u"从文件系统导入客体")

        # permition actions
        permNewAction = self.createAction(u"新的授权...", self.permNew,
            None, None, u"创建一个新的自主授权")
        permManageAction = self.createAction(u"管理授限...", self.permManage,
            None, None, u"管理自主授权")

        # about actions
        aboutAction = self.createAction(u"关于",
            lambda: QMessageBox.about(self, u"关于", u"作者：wong2.cn"), None, None, "About")
        aboutQtAction = self.createAction(u"关于Qt",
            lambda: QMessageBox.aboutQt(self, u"关于Qt"), None, None, "About Qt")

        # creat menubars
        subjectMenu = self.menuBar().addMenu(u"主体(&S)")
        objectMenu = self.menuBar().addMenu(u"客体(&O)")
        permMenu = self.menuBar().addMenu(u"权限(&P)")
        helpMenu = self.menuBar().addMenu(u"帮助(&H)")

        # add menubars to mainwindow
        self.addActions(subjectMenu, (subjectNewAction,subjectManageAction,subjectChangePwdAction))
        self.addActions(objectMenu, (objectNewAction,objectImportAction))
        self.addActions(permMenu, (permNewAction, permManageAction))
        self.addActions(helpMenu, (aboutQtAction, aboutAction))


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
    def subjectNew(self):
        subj_new_dlg = NewSubjectDialog(self)
        subj_new_dlg.exec_()

    #TODO:acomplish this function
    def subjectManage(self):
        pass
    #TODO:acomplish this function
    def subjectChangePwd(self):
        pass
    def objectNew(self):
        obj_new_dlg = NewObjectDialog(self)
        obj_new_dlg.exec_()
        pass
    #TODO: do this
    def objectImport(self):
        pass
    #TODO: do this
    def permNew(self):
        pass
    #TODO: do this
    def permManage(self):
        pass
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    # TODO: display one file information to file list table
    def showFile(self, name, owner, size, id):
        pass
class NewSubjectDialog(QDialog):
    def __init__(self,parent=None):
        super(NewSubjectDialog, self).__init__(parent)
        self.parent = parent
        self.drawlayout()
        # bind the ok button to save_subject methord
        self.connect(self.ok_button, SIGNAL("clicked()"), self.saveSubj)
        # bind the cancle button to cancel methord
        self.connect(self.cancle_button, SIGNAL("clicked()"), self.reject)
    def saveSubj(self):

        def has_subject(name):
            res = self.parent.conn.execute("select id FROM subject WHERE name = ?"(name,))
            return (res != None)
        name = self.input_name.text()
        password = self.input_pwd.text()
        veri_pwd = self.input_verif_pwd.text()

        # make sure that password == veri_pwd
        if password != veri_pwd:
            QMessageBox.critical(self, u"添加失败", u"两次密码输入不等，请重新输入！")
            self.input_pwd.selectAll()
            self.input_pwd.setFocus()

        elif has_subject(str(name)):
            QMessageBox.critical(self,u"添加失败", u"用户已存在！")
            self.input_name.selectAll()
            self.input_name.setFocus()
        else:
            try:
                self.parent.conn.execute("insert into subject values(?,?,?,?)",
                (None, name, hashlib.md5(password).hexdigest(), False))
            except:
                QMessageBox.critical(self, u"添加失败", u"数据插入异常！")
                self.reject()
            finally:
                QMessageBox.critical(self, u"添加成功!")
            self.accept()

    def drawlayout(self):
        # title
        self.setWindowTitle(u"新建主体")
        # size
        size = 300
        self.setFixedSize(size,size)

        # ok button
        self.ok_button = QPushButton(u"确认")
        # cancle button
        self.cancle_button = QPushButton(u"取消")
        # hbox to store ok and calcle button
        hbox_button = QHBoxLayout()
        hbox_button.addWidget(self.ok_button)
        hbox_button.addWidget(self.cancle_button)
        widget_buttons = QWidget()
        widget_buttons.setLayout(hbox_button)

        # lable :user name
        lable_name = QLabel(u"用户名：")
        # input user name
        self.input_name = QLineEdit()
        # lable :password
        lable_pwd = QLabel(u"密码：")
        # input passwort
        self.input_pwd = QLineEdit()
        self.input_pwd.setEchoMode(QLineEdit.Password)
        # lable : verify password
        lable_verify_pwd = QLabel(u"确认密码:")
        # input password
        self.input_verif_pwd = QLineEdit()
        self.input_verif_pwd.setEchoMode(QLineEdit.Password)

        hbox_name = QHBoxLayout()
        hbox_name.addWidget(lable_name)
        hbox_name.addWidget(self.input_name)
        widget_name = QWidget()
        widget_name.setLayout(hbox_name)

        hbox_pwd = QHBoxLayout()
        hbox_pwd.addWidget(lable_pwd)
        hbox_pwd.addWidget(self.input_pwd)
        widget_pwd = QWidget()
        widget_pwd.setLayout(hbox_pwd)

        hbox_veri = QHBoxLayout()
        hbox_veri.addWidget(lable_verify_pwd)
        hbox_veri.addWidget(self.input_verif_pwd)
        widget_veri = QWidget()
        widget_veri.setLayout(hbox_veri)

        vbox = QVBoxLayout()
        vbox.addWidget(widget_name)
        vbox.addWidget(widget_pwd)
        vbox.addWidget(widget_veri)
        vbox.addWidget(widget_buttons)
        self.setLayout(vbox)

class NewObjectDialog(QDialog):

    def __init__(self, parent=None):
        super(NewObjectDialog, self).__init__(parent)
        self.parent = parent
        self.drawlayout()
        self.connect(self.ok_button, SIGNAL("clicked()"), self.saveFile)
        self.connect(self.cancel_button, SIGNAL("clicked()"), self.reject)

    def drawlayout(self):
        self.setWindowTitle(u"编辑新客体")
        self.setFixedSize(400, 300)
        label_title = QLabel(u"文件名:")
        self.input_title = QLineEdit()
        label_content = QLabel(u"内容:")
        self.text_editor = QTextEdit()

        self.ok_button = QPushButton(u"保存")
        self.cancel_button = QPushButton(u"取消")
        hbox = QHBoxLayout()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        h_widget = QWidget()
        h_widget.setLayout(hbox)
        vbox = QVBoxLayout()
        vbox.addWidget(label_title)
        vbox.addWidget(self.input_title)
        vbox.addWidget(label_content)
        vbox.addWidget(self.text_editor)
        vbox.addWidget(h_widget)
        self.setLayout(vbox)
    def saveFile(self):

        title = unicode(self.input_title.text()).strip()
        content = unicode(self.text_editor.toPlainText()).strip()
        # make sure of the object
        if not title:
            QMessageBox.critical(self, u"错误", u"文件名不能为空")
        elif not self.parent.conn.execute("select id from object where name=?", (title,)):
            QMessageBox.critical(self, u"错误", u"文件名%s已存在" % title)
        elif len(content) > 2048:
            QMessageBox.critical(self, u"错误", u"文件内容太长，请勿超过2048字节")
        else:

        # update object table
            self.parent.conn.execute("insert into object values(?,?,?,?,?,?,?)",
                (None, title, content, len(content), self.parent.uid,
                 datetime.now(), datetime.now()))

            o_id = self.parent.conn.execute("select id from object where name=?",
                (title,)).fetchone()[0]
        # update authorize table
            for access in range(6):
                self.parent.conn.execute("insert into authorize values(?,?,?,?,?)",
                    (None, self.parent.uid, access, o_id, 0))

        # commit change
            self.parent.conn.commit()
            self.accept()
            QMessageBox.information(self, u"成功", u"客体%s创建成功！" % title)

        # update the fileinfo

        #     self.parent.showFile(title, self.parent.getUserNameById(self.parent.uid),
        #         len(content), o_id)


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle(u"自主访问控制实验")
        self.setFixedSize(270, 220)

        label_intro = QLabel(u"<h2>登录到系统</h2>")
        label_intro.setContentsMargins(0, 0, 0, 20)
        label_name = QLabel(u"用户名：")
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText(u"在此输入用户名")
        label_pwd = QLabel(u"密码：")
        self.input_pwd = QLineEdit()
        self.input_pwd.setPlaceholderText(u"在此输入密码")
        self.input_pwd.setEchoMode(QLineEdit.Password)
        self.input_pwd.setContentsMargins(0, 0, 0, 30)
        button_ok = QPushButton(u"登录")
        button_ok.setFixedHeight(30)
        self.connect(button_ok, SIGNAL("clicked()"), self.doLogin)

        vbox = QVBoxLayout()
        vbox.addWidget(label_intro)
        vbox.addWidget(label_name)
        vbox.addWidget(self.input_name)
        vbox.addWidget(label_pwd)
        vbox.addWidget(self.input_pwd)
        vbox.addWidget(button_ok)
        self.setLayout(vbox)

    def doLogin(self):
        name = self.input_name.text()
        password = self.input_pwd.text()
        id, is_admin = isValidUser(str(name), str(password))
        if id:
            self.done(id*10+is_admin)
        else:
            QMessageBox.critical(self, u"登录错误", u"用户名或密码错误,请重新输入！")
            self.input_name.selectAll()
            self.input_name.setFocus()

def main():
    app = QApplication(sys.argv)
    login_dlg = LoginDialog()
    id_admin = login_dlg.exec_()
    id = id_admin // 10
    is_admin = id_admin % 10
    #id = 2
    #is_admin = 0
    if id:
        win = MainWindow(id, is_admin)
        win.show()
    else:
        QTimer.singleShot(0, app.quit)
    app.exec_()

class test:
    def testMainWindow(self):
        app = QApplication(sys.argv)
        win = MainWindow(1,1)
        win.show()
        app.exec_()
    def testmain(self):
        main()
    def testNewObjectDialog(self):
        app = QApplication(sys.argv)
        newobjectdialog = NewObjectDialog()
        newobjectdialog.exec_()
        app.exec_()
    def testNewSubjectDialog(self):
        app = QApplication(sys.argv)
        new_subj_dlg = NewSubjectDialog()
        new_subj_dlg.exec_()
        app.exec_()

if __name__ == '__main__':
    oneTest = test()
    # oneTest.testMainWindow()
    # oneTest.testmain()
    # oneTest.testNewObjectDialog()
    oneTest.testNewSubjectDialog()