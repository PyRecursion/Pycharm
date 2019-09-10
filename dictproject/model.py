from sqlalchemy import Column,Integer,String,Date,Text,Boolean,BigInteger,create_engine
from sqlalchemy import ForeignKey,UniqueConstraint,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from . import config
#实体基类
Base=declarative_base()

#引擎 管理连接池
engine=create_engine(config.DB_PATH, echo=True)

class Userinfo(Base):
    __tablename__='userinfo'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    loginname=Column(String(20),nullable=False,unique=True)
    password=Column(String(32),nullable=False)

    historys=relationship('History')

    def __str__(self):
        return "{},id={},loginname={}".format(self.__tablename__,self.id,self.loginname)
    __repr__=__str__

class Edict(Base):
    __tablename__='edict'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    word=Column(String(128),nullable=False)
    explain=Column(String(255),nullable=False)

class History(Base):
    __tablename__='history'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name=Column(String(255),ForeignKey('userinfo.id'),nullable=False)
    history=Column(Text,nullable=True)

Session=sessionmaker(bind=engine)#创建会话类
session=Session() #创建实例

def addedict():
    edictlst=[]
    try:
        with open("dict.txt") as f:
            for l in f:
                word, _, explain = l.partition(' ')
                explain=explain.strip()
                edict = Edict()
                edict.word=word
                edict.explain=explain
                edictlst.append(edict)
            session.add_all(edictlst)
            session.commit()
    except Exception as e:
        print("***************************")
        print(e)
        session.rollback()

def create_table():
    Base.metadata.create_all(engine)#创建表
def drop_table():
    Base.metadata.drop_all(engine)#删除表


def show(query):
    for i in query:
        return i

def check_username(name):  #验证用户名是否重复
    try:
        queryobject = session.query(Userinfo).filter(Userinfo.loginname==name)
        if show(queryobject):
            return 0 #名字重复
        else:
            return 1 #名字可使用
    except Exception as e:
        print(e)


def user_reg(name,password):  #注册用户
    try:
        user=Userinfo()
        user.loginname=name
        user.password=password
        session.add(user)
        session.commit()
        return 1    #注册成功
    except Exception as e:
        print(e)
        session.rollback()

def user_login(name,password):  #用户登录验证
    try:
        queryobject = session.query(Userinfo).filter(Userinfo.loginname==name)
        queryres=show(queryobject)   #获取查询对象
        if queryres.password==password:
            return 1
        else:
            print("用户名密码错误")
            return
    except Exception as e:
        print(e)


def word_query(word):  #查询单词
    try:
        queryobject = session.query(Edict).filter(Edict.word ==word)
        queryres=show(queryobject)
        return  queryres.explain
    except AttributeError:
        return

def history_add(loginname=None,word=None):  #查询单词自动进数据库
    try:
        history=History()
        history.name=loginname
        history.history=word
        session.add(history)
        session.commit()
    except Exception as e:
        print(e)







