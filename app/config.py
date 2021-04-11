import os
import pymysql
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:00929.@127.0.0.1:3307/myblog'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://myblog:00929.@127.0.0.1:3306/myblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    XD_USER_DIR = "static/uploads/users"
    XD_BLOG_DIR = "static/uploads/blogs"
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), XD_USER_DIR)
    UPLOAD_FOLDER_BLOG = os.path.join(os.path.abspath(os.path.dirname(__file__)), XD_BLOG_DIR)
    # FC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users")
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    ALLOWED_EXTENSIONS_VIDEO = set(['avi', 'mp4', 'mov','mpg','mpeg'])
    DEFAULT_USER_LOGO = "default.png"
    DEFAULT_BLOG_LOGO = "default_blog.png"
    DEGAULT_TAG_ID = 1
    EXPIRES_IN = 3600
    # WTF_CSRF_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    REDIS_HISTORY = "histories"
    HISTORY_MAX_LEN = 10

    SECRET_KEY = 'dog'

