from socket import *
import time
import os
import sys

host='192.168.229.134'
port=9000
def main():
    s=socket()
    # try:
    #     if len(sys.argv) < 3:
    #         print("缺少参数,请重新输入")
    #         sys.exit(0)
    #     host = sys.argv[1]
    #     port = sys.argv[2]
    s.connect((host,int(port)))
    # except Exception as e:
    #     print(e)

    while True:
        print('''
                ===========Welcome==========
                -- 1.注册   2.登录    3.退出--
                ============================
                ''')
        func=input("请选择")
        if func=="1":
            s.send(b'reg')
            reg(s)
        elif func=="2":
            s.send(b'login')
            login(s)
        elif func == "3":
            s.send(b"exit")
            sys.exit(0)
        else:
            print("请输入正确的数字")

def reg(s):
    while True:#验证账号
        try:
            username=input("username=")
            if username=="":
                print("用户名不能为空")
                continue
            s.send(username.encode())
            reply=s.recv(1024)
            if reply.decode()=="ok":
                break
            else:
                print("用户名已存在或不合法")
        except Exception as e:
            print(e)
            print("未知错误，请重新输入")

    while True:#验证密码
         try:
            password=input("password=")
            if password=="":
                print("密码不能为空")
                continue
            cpassword=input("check password=")
            if password==cpassword:
                s.send(password.encode())
                if s.recv(1024)==b"ok":
                    print('注册成功')
                break
            else:
                print("两次密码输入不一致")
                continue
         except Exception as e:
                print(e)
                sys.exit(0)



def login(s):
    username = input("username=")
    password = input("password=")
    try:
        s.send('{} {}'.format(username,password).encode())
        data=s.recv(1024)
        if  data==b'ok':
            print("登陆成功")
            print('''
                        ==========查询界面==========
                        1.查词    2.历史记录   3.退出
                        ===========================
                        ''')
            cmd=input("请选择")
            if cmd=="1":
                s.send(b'query')
                edict_query(s,username)
            elif cmd=="2":
                s.send(b'history')
                edict_history(s,username)
            elif cmd=="3":
                return
        else:
            print("账号密码错误,请重新输入")
    except Exception as e:
        print(e)

def edict_query(s,username):
    s.send(username.encode())
    time.sleep(0.5)
    while True:
        word=input("请输入需要查询的单词,退出输入##:")
        if word == "##":
            s.send("##".encode())
            break
        try:
            s.send(word.encode())
            explain=s.recv(1024)
            if explain.decode()=="0":
                print("此单词未查到")
            else:
                print(explain.decode())
        except Exception as e:
            print(e)

def edict_history(s,username):
    s.send(username.encode())
    time.sleep(0.5)
    while True:
        history_data=s.recv(100)
        if  history_data.decode()=="^^":
            break
        else:
            print(history_data.decode())


if __name__ == '__main__':
    main()
