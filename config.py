import os
BASE_DIR=os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY='ALSDJFLSJDLFLS2232L3JLJ'
    SQLALCHEMY_DATABASE_URI='mysql+pymsql://root:myroot123@localhost:3306/flaskblog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    