#coding:utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,Text
from sqlalchemy.orm import sessionmaker

Base=declarative_base()

class Qshi(Base):
    __tablename__='qshi'
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    logo=Column(String(255))
    content=Column(Text())
    img=Column(String(255))

    def __int__(self,id,name,logo,content,img):
        self.id=id
        self.name=name
        self.logo=logo
        self.content=content
        self.img=img

    def __repr__(self):
        return '<Qshi %s>'%self.name

    __str__=__repr__

engine=create_engine("mysql+pymysql://root:admin@localhost:3306/qiushi",connect_args={'charset':'utf8'})


# Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session=DBSession()

def initdatabase():
    Base.metadata.create_all(engine)

def dropdatabase():
    Base.metadata.drop_all(engine)

# data1=Qshi(id=1,name='Baymax',logo='static/imgs/111.jpg',content='hhh',img='static/imgs/222.jpg')
# session.add(data1)
# session.commit()
# session.close()