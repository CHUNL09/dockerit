from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DB = {
    'connector': 'mysql+pymysql://root:aircool123@127.0.0.1:3306/dockerit',
     'max_session':5
}

engine = create_engine(DB['connector'], max_overflow=DB['max_session'], echo = False)
SessionCls = sessionmaker(bind=engine)
session= SessionCls()

template_variables = {
    'username':""
}

COOKIE_NAME  = "user_id"