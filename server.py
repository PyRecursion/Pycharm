from socket import *
import signal
import time
import os
import sys
from dictproject.model import *

addr="192.168.229.134",9000

def main():
    s= socket()
    s.bind(addr)
    s.listen(10)
    # 忽略子进程信号
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        try:
            conn, caddr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt: #  control C触发
            s.close()
            sys.exit("服务器退出")
        except Exception as e:  #产生异常继续运行
            print(e)
            continue

        #创建新进程
        pid=os.fork()
        if pid==0: #新进程执行
            s.close()
            dispatcher(conn)
            sys.exit(0)
        else:      #主进程继续等待客户端
            conn.close()
            continue

def dispatcher(conn):  #任务分发
    while True:
        try:
            data = conn.recv(1024)
            if data==b"reg":
                reg(conn)
            elif data==b"login":
                login(conn)
            elif data==b"query":
                query(conn)
            elif data == b"history":
                history(conn)
            elif data.decode() == b"exit":
                conn.close()
                break
        except Exception as e:
            print(e)

def reg(conn):
    while True:
        try:
            username=conn.recv(1024)
            if  check_username(username):
                conn.send(b"ok")
                break
            else:
                conn.send(b"false")
                continue
        except Exception as e:
            print(e)

    while True:
        try:
            password=conn.recv(1024)
            if user_reg(username.decode(),password.decode()):
                conn.send(b"ok")
                break
        except Exception as e:
            print(e)
            sys.exit(0)

def login(conn):
        try:
            userpw=conn.recv(1024)
            print(userpw.decode())
            u,_,p=userpw.decode().partition(" ")
            if user_login(u,p):
                conn.send(b"ok")
                return
            else:
                conn.send(b"no")
        except Exception as e:
            print(e)


def query(conn):
    try:
        username=conn.recv(100).decode()
        while True:
            try:
                word=conn.recv(100)
                word=word.decode()

                if word=="##":
                    break
                history_add(username, word)
                explain=word_query(word)
                if explain:
                    conn.send(explain.encode())
                else:
                    conn.send("0".encode())
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

def history(conn):
    try:
        username=conn.recv(100).decode()
        history_query=lambda loginname:session.query(History).filter(History.name==loginname)
        for i in history_query(username):
            time.sleep(0.5)
            conn.send(i.history.encode())
        conn.send("^^".encode())
        return
    except Exception as e:
        print(e)








if __name__ == '__main__':
    main()