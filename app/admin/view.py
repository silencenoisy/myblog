from . import admin

from flask import render_template, redirect, url_for, session, request, jsonify
from app.models import Blog, User, Collection, Comment, Tag, Like, Video, UserLog
from functools import wraps
from werkzeug.utils import secure_filename
import os

from app.home.view import UserLogAdd
from app.config import Config
from app import db


def session_set(admin):
    try:
        session['id'] = admin.id
        session['username'] = admin.name
        session['introduce'] = admin.introduce
        session['headName'] = admin.headName
        session['right'] = admin.right
        if admin.head:
            if not os.path.exists(Config.UPLOAD_FOLDER + "/" + session['headName']):
                load_head(admin)
        return True
    except:
        return False


def load_head(user):
    f = user.head
    if f:
        upload_path = os.path.join(Config.UPLOAD_FOLDER, session['headName'])
        f.save(upload_path)


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'username' not in session :
            session.clear()
            return redirect(url_for('admin.login', next=request.url))
        elif not User.query.filter(User.name==session['username'],User.id==session['id'],User.right==0).first():
            session.clear()
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)

    return inner


def is_int(str):
    try:
        int(str)
        return True
    except:
        print("the %s is not int" % str)
        return False


def loadImage(data, filename, defaultDir=Config.UPLOAD_FOLDER, defaultImage=Config.DEFAULT_USER_LOGO):
    file_dir = defaultDir
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if not data or filename == defaultImage:
        return defaultImage
    f = data
    fname = secure_filename(filename)
    path = file_dir + "/" + filename
    with open(path, 'wb') as fs:
        fs.write(f)
        fs.close()
    return fname


def isOrder(order):
    if order in range(1, 6):
        return True
    return False


def orderSelect(order):
    if not isOrder(order):
        return False
    data = []
    if order == 1:  # 用户
        data = getUserData()

    elif order == 2:  # 博客
        data = getBlogData()

    elif order == 3:  # 评论
        data = getCommentData()
    elif order == 4:  # 标签
        data = getTagData()
    elif order == 5:  # 日志
        data = getLogData()
    else:
        return False
    return data


def getUserData():
    data = []
    users = User.query.filter(User.right>session['right']).all()

    for i in users:
        temp = {
            "id": i.id,
            "username": i.name,
            "head": i.head,
            "headName": i.headName,
            "introduce": i.introduce,
            "email": i.email
        }
        data.append(temp)
    return data


def getBlogData():
    data = []
    blogs = Blog.query.order_by(Blog.id).all()
    for i in blogs:
        tag = Tag.query.filter(Tag.id == i.tag).first()
        user = User.query.filter(User.id == i.user_id).first()
        author = user.name
        temp = {
            "id": i.id,
            "title": i.title,
            "tag": i.tag,
            "head": i.head,
            "headName": i.headName,
            "tag":tag.tag,
            "author":author,
            "user_id":user.id,
        }
        data.append(temp)
    return data


def getCommentData():
    data = []
    comments = Comment.query.order_by(Comment.id).all()
    for i in comments:
        blog = Blog.query.filter(Blog.id==i.blog_id).first()
        user = User.query.filter(User.id==i.user_id).first()
        temp = {
            "id": i.id,
            "content": i.content,
            "user_id": i.user_id,
            "blog_id": i.blog_id,
            "blog_title":blog.title,
            "user_name":user.name,
        }
        data.append(temp)
    return data


def getTagData():
    data = []
    tags = Tag.query.order_by(Tag.id).all()
    for i in tags:
        temp = {
            "id": i.id,
            "tag": i.tag,
        }
        data.append(temp)
    return data


def getLogData():
    data=[]
    logs = UserLog.query.order_by(UserLog.addtime).all()
    for i in logs:
        temp = {
            "id": i.id,
            "username": i.user_name,
            "operation":i.order,
        }
        data.append(temp)
    return data

def deleteUserByUser(user):
    blogs = Blog.query.filter(Blog.user_id == user.id).all()

    for i in blogs:
        deleteBlogByBlog(i)
        # comments = Comment.query.filter(Comment.blog_id == i.id).all()
        # for t in comments:
        #     db.session.delete(t)
        # likes = Like.query.filter(Like.blog_id == i.id).all()
        # for t in likes:
        #     db.session.delete(t)
        # cols = Collection.query.filter(Collection.blog_id == i.id).all()
        # for t in cols:
        #     db.session.delete(t)
        # db.session.commit()

    user_comments = Comment.query.filter(Comment.user_id == user.id).all()
    for t in user_comments:
        db.session.delete(t)
    user_likes = Like.query.filter(Like.user_id == user.id).all()
    for t in user_likes:
        db.session.delete(t)
    user_cols = Collection.query.filter(Collection.user_id == user.id).all()
    for t in user_cols:
        db.session.delete(t)
    db.session.delete(user)
    db.session.commit()
    return True


def deleteBlogByBlog(blog):
    try:
        like = Like.query.filter(Like.blog_id == blog.id).all()
        col = Collection.query.filter(Collection.blog_id == blog.id).all()
        comt = Comment.query.filter(Comment.blog_id == blog.id).all()
        video = Video.query.filter(Video.blog_id == blog.id).all()
        for i in like:
            db.session.delete(i)
        for i in col:
            db.session.delete(i)
        for i in comt:
            db.session.delete(i)
        db.session.commit()
        for i in video:
            db.session.delete(i)
            db.session.commit()
        db.session.delete(blog)
        db.session.commit()
    except:
        print("function 'delBlogByBlog' raise error!")
        return False
    return True


def deleteComByCom(comment):
    try:
        db.session.delete(comment)
        db.session.commit()
        return True
    except:
        print("function 'deleteComByCom' raise error!")
        return False


def deleteComByTag(tag):
    if tag.id == Config.DEGAULT_TAG_ID:
        return False
    try:
        blogs = Blog.query.filter(Blog.tag==tag.id).all()
        for i in blogs:
            i.tag = Config.DEGAULT_TAG_ID
        db.session.delete(tag)
        db.session.commit()
        return True
    except:
        print("function 'deleteComByTag' raise error!")
        return False


def tagExist(tag):
    tag = Tag.query.filter(Tag.tag == tag).first()
    if tag:
        return True
    return False


def createTag(tagName):
    try:
        tag = Tag(tag=tagName)
        db.session.add(tag)
        db.session.commit()
    except:
        print("function 'createTag' raise error!")
        return False
    return True


def changeUserName(user,name):
    if user.name != name and User.query.filter(User.name==name).first():
        return False
    user.name = name
    db.session.commit()
    return True

def changeUserPWD(user,pwd):
    user.pwd = pwd
    db.session.commit()
    return True

def changeUserIntr(user,introduce):
    user.introduce = introduce
    db.session.commit()
    return True

def changeUserHead(user,filename):
    user.headName = filename
    path = Config.UPLOAD_FOLDER + "\\" + filename
    with open(path, 'rb') as f:
        data = f.read()
        f.close()
    user.head = data
    db.session.commit()
    return True

def changeCommentByComment(comment,comt_data):
    comment.content = comt_data
    db.session.commit()
    return True



@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    params={}
    if 'right' in session:
        if session['right']!=0:
            session.clear()
    return render_template('admin/order.html', session=session,params=params)


@admin.route('/orderWork', methods=['POST'])
@login_required
def orderWork():
    jsons = {}
    order = request.form['order']
    if not is_int(order):
        jsons['isSuccess'] = 12  # 未知命令
        return jsonify(jsons)
    order = int(order)
    if not isOrder(order):
        jsons['isSuccess'] = 12
    else:
        jsons['order'] = order
        jsons['url'] = order
    return jsonify(jsons)


@admin.route('/order/<int:order>', methods=['GET', 'POST'])
@login_required
def orderManage(order):
    if not isOrder(order):
        return redirect(url_for('admin.index'))
    params = {}
    data = orderSelect(order)
    params['data'] = data
    params['order'] = order
    params['len'] = len(params['data'])
    if order == 1:
        for i in params['data']:
            i['headUrl'] = loadImage(i['head'], i['headName'])
    elif order == 2:
        for i in params['data']:
            i['headUrl'] = loadImage(i['head'], i['headName'],Config.UPLOAD_FOLDER_BLOG,Config.DEFAULT_BLOG_LOGO)
    return render_template('admin/order.html', session=session, params=params)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html')


@admin.route('/userChange/<int:user_id>',methods=['GET','POST'])
@login_required
def userChange(user_id):
    params = {}
    user = User.query.filter(User.id == user_id).first()
    if user:
        headName = loadImage(user.head,user.headName)
        user_data = {
            'id':user.id,
            'name':user.name,
            'introduce':user.introduce,
            'headUrl':headName,
        }
        params['user'] = user_data
    return render_template('admin/userChange.html',session=session,params=params)


@admin.route('/loginCheck', methods=['POST'])
def loginCheck():
    username = request.form['username']
    pwd = request.form['pwd']
    admin = User.query.filter(User.name == username,User.right==0).first()
    if not admin:
        jsons = {
            'isSuccess': 1,  # 用户不存在
        }
        return jsonify(jsons)
    if not admin.check_pwd(pwd):
        jsons = {
            'isSuccess': 11,  # 密码错误
        }
        return jsonify(jsons)
    if session_set(admin):
        jsons = {
            'isSuccess': 0,
        }
    else:
        jsons = {
            'isSuccess': 999,
        }
    return jsonify(jsons)


@admin.route('/logout', methods=['POST'])
@login_required
def logout():
    order = request.form['logout']
    jsons = {}
    if order:
        session.clear()
        jsons['isSuccess'] = 0
    else:
        jsons['isSuccess'] = 999  # 未知错误
    return jsonify(jsons)


@admin.route('/deleteUser', methods=['POST'])
@login_required
def AdmindeleteUser():
    jsons = {}
    if 'user_id' in request.form:
        user_id = request.form['user_id']
        if is_int(user_id):
            user_id = int(user_id)
            user = User.query.filter(User.id == user_id).first()
            if user and deleteUserByUser(user):
                jsons['isSuccess'] = 0
                UserLogAdd(session['id'],session['username'],200,"用户id:"+str(user_id))
            else:
                jsons['isSuccess'] = 5  # 用户不存在
        else:
            jsons['isSuccess'] = 999
    else:
        jsons['isSuccess'] = 999

    return jsonify(jsons)


@admin.route('/deleteBlog',methods=['POST'])
@login_required
def AdmindeleteBlog():
    jsons = {}
    if 'blog_id' in request.form:
        blog_id = request.form['blog_id']
        if is_int(blog_id):
            blog_id = int(blog_id)
            blog = Blog.query.filter(Blog.id == blog_id).first()
            if blog and deleteBlogByBlog(blog):
                jsons['isSuccess'] = 0
                UserLogAdd(session['id'], session['username'],101, "博客id:" + str(blog_id))
            else:
                jsons['isSuccess'] = 6  # 博客不存在
        else:
            jsons['isSuccess'] = 999
    else:
        jsons['isSuccess'] = 999

    return jsonify(jsons)


@admin.route('/deleteComment',methods=['POST'])
@login_required
def AdmindeleteComment():
    jsons={}
    if 'comment_id' in request.form:
        comment_id = request.form['comment_id']
        if is_int(comment_id):
            comment_id = int(comment_id)
            comment = Comment.query.filter(Comment.id == comment_id).first()

            if comment:
                blog_id = comment.blog_id
                if deleteComByCom(comment):
                    jsons['isSuccess'] = 0
                    UserLogAdd(session['id'],session['username'], 106, "博客id：" + str(blog_id))
            else:
                jsons['isSuccess'] = 8  # 评论不存在
        else:
            jsons['isSuccess'] = 999
    else:
        jsons['isSuccess'] = 999
    return jsonify(jsons)


@admin.route('/DeleteTag',methods=['POST'])
@login_required
def AdminDeleteTag():
    jsons={}
    if 'tag_id' in request.form:
        tag_id = request.form['tag_id']
        if is_int(tag_id):
            tag_id = int(tag_id)
            tag = Tag.query.filter(Tag.id == tag_id).first()
            if tag_id == Config.DEGAULT_TAG_ID:
                jsons['isSuccess'] = 55     # 无法删除的标签
            elif tag:
                tag_name = tag.tag
                if deleteComByTag(tag):
                    jsons['isSuccess'] = 0
                UserLogAdd(session['id'],session['username'], 203, "标签名：" + tag_name)
            else:
                jsons['isSuccess'] = 7  # 标签不存在
        else:
            jsons['isSuccess'] = 999
    else:
        jsons['isSuccess'] = 999
    return jsonify(jsons)


@admin.route('/changeComment',methods=['POST'])
@login_required
def changeComment():
    jsons={}
    comt_id = request.form['comt_id']
    comt_data = request.form['comt_data']
    if not is_int(comt_id) or not comt_data:
        jsons['isSuccess'] = 999
        return jsonify(jsons)
    comt_id = int(comt_id)
    comment = Comment.query.filter(Comment.id == comt_id).first()
    if not comment:
        jsons['isSuccess'] = 25     # 评论不存在
        return jsonify(jsons)
    if not changeCommentByComment(comment,comt_data):
        jsons['isSuccess'] = 999
        return jsonify(jsons)
    jsons['isSuccess'] = 0
    UserLogAdd(session['id'], session['username'],204, "评论id：" + str(comment.id))
    return jsonify(jsons)


@admin.route('/newTag',methods=['POST'])
@login_required
def newTag():
    jsons={}
    tag_name = request.form['tagName']
    if tagExist(tag_name):
        jsons['isSuccess'] = 56 # 标签重名
    else:
        if createTag(tag_name):
            jsons['isSuccess'] = 0
            UserLogAdd(session['id'],session['username'],202,"标签名："+tag_name)
        else:
            jsons['isSuccess'] = 999
    return jsonify(jsons)


@admin.route('/changeTagName',methods=['POST'])
@login_required
def changeTagName():
    jsons={}
    tag_id = request.form['id']
    if is_int(tag_id):
        tag_id = int(tag_id)
        tag_name = request.form['tagName']
        tag = Tag.query.filter(Tag.id == tag_id).first()
        if tag:
            if tag.tag != tag_name:
                tag.tag = tag_name
                db.session.commit()
                jsons['isSuccess'] = 0
                UserLogAdd(session['id'],session['username'], 205, "标签名：" + tag_name)
            else:
                jsons['isSuccess'] = 56
        else:
            jsons['isSuccess'] = 55
    return jsonify(jsons)


@admin.route('/changeUserData',methods=['POST'])
@login_required
def changeUser():
    jsons={}
    user_id = request.form['user_id']
    if not is_int(user_id):
        jsons['isSuccess'] = 999
        return jsonify(jsons)

    user_id = int(user_id)
    user = User.query.filter(User.id == user_id).first()
    if not user:
        jsons['isSuccess'] = 6
        return jsonify(jsons)

    if 'userName' in request.form:
        userName = request.form['username']
        if not userName or not changeUserName(user,userName):
            jsons['isSuccess'] = 20 # 用户名修改失败
            return jsonify(jsons)

    if 'password' in request.form and 'checkpwd' in request.form:
        pwd = request.form['password']
        pwd2 = request.form['checkpwd']
        if len(pwd)>1:
            if pwd!=pwd2 or not changeUserPWD(user,pwd):
                jsons['isSuccess'] = 21 # 密码修改失败
                return jsonify(jsons)

    if 'introduce' in request.form:
        introduce = request.form['introduce']
        if introduce:
            if not changeUserIntr(user,introduce):
                jsons['isSuccess'] = 22 # 个人介绍修改失败
                return jsonify(jsons)

    if 'url' in request.form:
        url = request.form['url']
        filename = url.split('/')[-1]
        if not changeUserHead(user,filename):
            jsons['isSuccess'] = 23 # 头像修改失败
            return jsonify(jsons)

    jsons['isSuccess'] = 0

    return jsonify(jsons)

