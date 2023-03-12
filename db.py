from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

user_name = "eduuser"
user_pwd = "1234"
db_host = "127.0.0.1"
db_name = "edudb"

DATABASE = "mysql+pymysql://root:a135792468@localhost:3306/mydatabase?charset=utf8"

ENGINE = create_engine(
    DATABASE,   
    echo = True
)

session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property()
