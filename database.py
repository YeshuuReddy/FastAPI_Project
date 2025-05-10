from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL='mysql+mysqldb://root:root@localhost:3306/ubi_bms'

engine=create_engine(DB_URL)

SessionLocal= sessionmaker (autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL='mysql+mysqldb://root:root@localhost:3306/ubi_bms'

engine=create_engine(DB_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()

"""
