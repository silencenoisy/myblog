from . import home

from flask import render_template, request, session, flash, redirect, url_for, jsonify, Response
from app.models import User, Comment, Collection, Blog, Like, Tag, Video, UserLog
from functools import wraps
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import datetime
import uuid

import os
from .form import PageDownForm

from app.config import Config
from app import db, rd


# 设置session参数
def session_set(user):
    session['id'] = user.id
    session['username'] = user.name
    session['introduce'] = user.introduce
    session['headName'] = user.headName
    session['right'] = user.right  # 权限
    if user.head:
        if not os.path.exists(Config.UPLOAD_FOLDER + "/" + session['headName']):
            load_head(user)
    return True


# 判断是否管理员
def adminUserCheck(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        return user.right == 0
    else:
        return False


# 日志添加
def UserLogAdd(user_id, user_name,orders, aim=None):
    order=select_order(orders)
    if aim:
        order = order+" "+aim
    if order:
        log = UserLog(
            user_id=user_id,
            user_name=user_name,
            order=order,
        )
        db.session.add(log)
        db.session.commit()
        return True
    return False


# 指令处理
def select_order(orders):
    if orders==100:     # 登陆
        return "登陆"
    elif orders==101:   # 创建博客
        return "创建博客"
    elif orders==102:   # 修改博客
        return "修改博客"
    elif orders==103:   # 添加评论
        return "添加评论"
    elif orders==104:   # 添加点赞
        return "添加点赞"
    elif orders==105:   # 添加收藏
        return "添加收藏"
    elif orders==106:   # 删除评论
        return "删除评论"
    elif orders==107:   # 删除点赞
        return "删除点赞"
    elif orders==108:   # 删除收藏
        return "删除收藏"
    elif orders==200:   # 删除用户
        return "删除用户"
    elif orders==201:   # 删除博客
        return "删除博客"
    elif orders==202:   # 添加标签
        return "添加标签"
    elif orders==203:   # 删除标签
        return "删除标签"
    elif orders==204:   # 修改评论
        return "修改评论"
    elif orders==205:   # 修改标签
        return "修改标签"
    else:
        return None



# 加载头像
def load_head(user):
    f = user.head
    if f:
        upload_path = os.path.join(Config.UPLOAD_FOLDER, session['headName'])
        f.save(upload_path)


def load_video(video):
    f = video.video_data
    if f:
        upload_path = os.path.join(Config.UPLOAD_FOLDER_BLOG, video.video_name)
        f.save(upload_path)


def allow_pic(filename):
    if '.' in filename:
        if filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS:
            return True
    return False


def allow_video(filename):
    if '.' in filename:
        if filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS_VIDEO:
            return True
    return False


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'username' not in session:
            session.clear()
            return redirect(url_for('home.index', next=request.url))
        return func(*args, **kwargs)

    return inner


def savaImage(url, path):
    filename = url.split('/')[-1]
    path = path + "\\" + filename
    with open(path, 'rb') as f:
        data = f.read()
        f.close()
    params = {
        "filename": filename,
        "data": data,
    }
    return params


def loadImage(data, filename, defaultDir=Config.UPLOAD_FOLDER_BLOG, defaultImg=Config.DEFAULT_BLOG_LOGO):
    file_dir = defaultDir
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if not data or filename == defaultImg:
        return defaultImg
    f = data
    fname = secure_filename(filename)
    path = file_dir + "/" + filename
    if not os.path.exists(path):
        with open(path, 'wb') as fs:
            fs.write(f)
            fs.close()
    return fname


def getBlogID(url):
    return url.split('/')[-1]


def delBlogByBlog(blog):
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


def DelComment(comt):
    try:
        db.session.delete(comt)
        db.session.commit()
    except:
        print("function delComment raise error")
        return False
    return True


def DelCollection(col):
    try:
        db.session.delete(col)
        db.session.commit()
    except:
        print("function delCollection raise error")
        return False
    return True


def checkUser(user_id):
    if is_int(user_id):
        user_id = int(user_id)
    if session['id'] == user_id:
        return True
    return False


def is_int(str):
    try:
        int(str)
        return True
    except:
        return False



def saveVideos(filename, blog_id, user_id):
    path = os.path.join(Config.UPLOAD_FOLDER_BLOG, filename)
    if not os.path.exists(path):
        return False
    if not Video.query.filter(Video.video_name == filename, Video.blog_id == blog_id).first() and Blog.query.filter(
            Blog.id == blog_id).first() \
            and User.query.filter(User.id == user_id).first():
        with open(path, 'rb') as f:
            data = f.read()
            f.close()
        video = Video(
            video_name=filename,
            video_data=data,
            user_id=user_id,
            blog_id=blog_id,
            uuid=uuid.uuid4().hex,
        )
        db.session.add(video)
        db.session.commit()


    else:
        return False;
    return True

@home.app_errorhandler(404)
def page_not_found(e):
    return render_template('home/404.html'),404


# 登陆确认
@home.route('/checkLogin', methods=['POST'])
def checkLogin():
    user = User.query.filter_by(name=request.form['username']).first()
    jsons = {}
    if user:
        if user.check_pwd(request.form['password']):
            session_set(user)
            UserLogAdd(user.id,user.name,100)
            # jsons['id'] = session['id']
            jsons['isSuccess'] = 0
        else:
            jsons['isSuccess'] = 1002  # 密码错误
            session.clear()
    else:
        jsons['isSuccess'] = 1001  # 用户不存在
        session.clear()
    print(jsons)
    return jsonify(jsons)


# 注册普通用户
@home.route('/registers', methods=['POST'])
def registers():
    jsons = {}
    name, pwd, email = request.form['username'], request.form['password'], request.form['email']

    if User.query.filter_by(name=name).first():
        # 用户名重复
        jsons['isSuccess'] = 1001
        return jsonify(jsons)

    user = User(name=name, pwd=generate_password_hash(pwd), email=email, uuid=uuid.uuid4().hex)
    db.session.add(user)
    db.session.commit()
    # 设置session
    session_set(user)
    jsons['isSuccess'] = 0
    return jsonify(jsons)


# 首页
@home.route('/', methods=['GET', 'POST'])
def index():
    item_num = 20  # 显示博客数
    tag_num = 3  # 显示标签数

    params = {  # 返回的信息
        "blog_data": [],
        "tags": [],
        'noBlogData':False,
    }
    tag_id = request.args.get('tag')
    search_keyword = request.args.get('keyword')
    # 根据需求返回博客类型
    if is_int(tag_id):
        # 根据标签
        tag_id = int(tag_id)
        tag = Tag.query.filter_by(id=tag_id).first()
        if tag:
            blog_data = Blog.query.filter_by(tag=tag_id).limit(item_num)
        else:
            blog_data = Blog.query.order_by(Blog.addtime).limit(item_num)
    elif search_keyword:
        # 根据搜索关键字
        blog_data = Blog.query.filter(Blog.title.like("%" + search_keyword + "%")).limit(item_num)
        if not blog_data.count():
            params['noBlogData'] = True
    else:
        # 无特殊需求或遇到错误参数
        blog_data = Blog.query.order_by(Blog.id).limit(item_num)

    # 标签信息
    tags = Tag.query.filter(Tag.id).limit(tag_num)
    for i in tags:
        temp = {
            "id": i.id,
            "tag": i.tag,
        }
        params['tags'].append(temp)

    # 博客内容信息
    for i in blog_data:
        filename = loadImage(i.head, i.headName)  # 博客封面

        temp = {
            "title": i.title,
            "headName": i.headName,
            'url': filename,
            "blog_id": i.id,
        }
        params['blog_data'].append(temp)
    params['len'] = len(params['blog_data'])  # 实际博客数量

    return render_template('home/home.html', session=session, params=params)


# 用户个人中心
@home.route('/userhome', methods=['GET', 'POST'])
@login_required
def userhome():
    return render_template('home/userhome.html', session=session)


# 登出
@home.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('home.index'))


# 修改密码
@home.route('/changePwd', methods=['POST'])
@login_required
def changePwd():
    user = User.query.filter_by(id=session['id']).first()
    user.pwd = generate_password_hash(request.form['password'])
    db.session.commit()
    return redirect(url_for('home.userhome'))


# 修改个人介绍
@home.route('/changeITD', methods=['POST'])
@login_required
def changeITD():
    user = User.query.filter_by(id=session['id']).first()
    intrduce = request.form['introduce']
    user.introduce = intrduce
    db.session.commit()
    session['introduce'] = intrduce
    return redirect(url_for('home.userhome'))


# 缓存预览的头像
@home.route('/changeHead', methods=['POST'])
@login_required
def changeHead():
    uploads_pic = request.files['images']
    if uploads_pic and allow_pic(uploads_pic.filename):  # 文件不为空and文件格式正确
        filename = secure_filename(uploads_pic.filename)
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        uploads_pic.save(path)

    params = {
        'isSuccess': True,
        'url': Config.XD_USER_DIR + '/' + filename,
    }
    return jsonify(params)


@home.route('/changeLoge', methods=['POST'])
@login_required
def changeLoge():
    uploads_pic = request.files['images']
    if uploads_pic and allow_pic(uploads_pic.filename):
        filename = secure_filename(uploads_pic.filename)
        path = os.path.join(Config.UPLOAD_FOLDER_BLOG, filename)
        uploads_pic.save(path)
    ret = {}
    ret['isSuccess'] = True
    pp = 'uploads/blogs/' + filename
    ret['url'] = url_for('static', filename=pp)
    return jsonify(ret)


@home.route('/changeHeaded', methods=['POST'])
@login_required
def changeHeaded():
    url = request.form['url']
    filename = url.split('/')[-1]
    user = User.query.filter(User.id == session['id']).first()
    user.headName = filename
    path = Config.UPLOAD_FOLDER + "\\" + filename
    with open(path, 'rb') as f:
        data = f.read()
        f.close()
    user.head = data
    db.session.commit()
    session_set(user)
    return redirect('userhome')


@home.route('/blogs/<int:blog_id>', methods=['GET', 'POST'])
def blogs(blog_id):
    params = {}
    params['blog_id'] = blog_id
    blog = Blog.query.filter(Blog.id == blog_id).first()
    if not blog:
        return redirect(url_for('home.index'))
    params['blog_html'] = blog.body_html
    if 'username' not in session:
        params['isLike'] = False
        params['isCollection'] = False
    else:
        if Like.query.filter(Like.blog_id == blog_id, session['id'] == Like.user_id).first():
            params['isLike'] = True
        else:
            params['isLike'] = False
        if Collection.query.filter(Collection.blog_id == blog_id, session['id'] == Collection.user_id).first():
            params['isCollection'] = True
        else:
            params['isCollection'] = False
    params['like'] = Like.query.filter(Like.blog_id == blog_id).count()
    params['collection'] = Collection.query.filter(Collection.blog_id == blog_id).count()
    params['tag'] = Tag.query.filter(Tag.id == blog.tag).first().tag
    params['title'] = blog.title

    comment_data = Comment.query.filter(Comment.blog_id == blog_id).all()

    params['comments'] = []

    for i in comment_data:
        t = {}
        user = User.query.filter(User.id == i.user_id).first()
        headUrl = loadImage(user.head, user.headName, Config.UPLOAD_FOLDER, Config.DEFAULT_USER_LOGO)
        t['comerHead'] = headUrl
        t['isAuthor'] = (user.id == blog.user_id)
        t['comer'] = user.name
        t['comment'] = i.content
        params['comments'].append(t)

    videos = Video.query.filter(Video.user_id == blog.user_id, Video.blog_id == blog.id).all()
    params['videos'] = []
    for i in videos:
        video_name = loadImage(i.video_data, i.video_name)
        temp = {
            'id': i.id,
            'name': video_name,
        }
        params['videos'].append(temp)
    params['videos_len'] = len(videos)
    return render_template('home/blogs.html', session=session, params=params)


@home.route('/comment_submit', methods=['POST'])
@login_required
def comment_submit():
    comment_content = request.form['comment']
    blog_id = request.form['url'].split('/')[-1]
    try:
        id = int(blog_id)
    except:
        jsons = {"isSuccess": 3}  # 格式错误
        return jsonify(jsons)
    comment = Comment(
        content=comment_content,
        user_id=session['id'],
        blog_id=id,
    )
    db.session.add(comment)
    db.session.commit()
    UserLogAdd(session['id'],session['username'],103,"博客id："+blog_id)
    jsons = {
        "isSuccess": 0,
    }
    return jsonify(jsons)


@home.route('/newBlog/<int:user_id>/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def newBlog(user_id, blog_id=0):
    if not checkUser(user_id) and not adminUserCheck(session['id']):
        return redirect(url_for("home.index"))

    tags_data = Tag.query.order_by('id').all()
    tag = []
    for i in tags_data:
        temp = {
            'id': i.id,
            'tag_name': i.tag,
        }
        tag.append(temp)

    params = {
        'pagedown': PageDownForm(),
        'tag': tag,
    }
    if blog_id == 0:
        params['order'] = 0  # 创建新博客
    else:
        params['order'] = 1  # 修改博客
        blog_id = int(blog_id)
        user_id = int(user_id)
        blog = Blog.query.filter(Blog.id == blog_id, Blog.user_id == user_id).first()

        if not blog:
            params['order'] = 0

        else:
            if blog.headName != Config.DEFAULT_BLOG_LOGO:
                loadImage(blog.head, blog.headName)
            tag_id = blog.tag
            for i in range(len(params['tag'])):
                if params['tag'][i]['id'] == tag_id:
                    tag_id = i
                    break
            videos = Video.query.filter(Video.blog_id == blog.id).all()
            vData = []
            for i in videos:
                vTemp = {
                    'video_id': i.id,
                    'video_name': i.video_name,
                }
                vData.append(vTemp)
            temp = {
                "id": blog.id,
                "content": blog.content,
                "title": blog.title,
                "headname": blog.headName,
                "tag_id": tag_id,
                'vData': vData,
            }
            params['pagedown'].body.data = blog.content
            params['blog'] = temp

    return render_template('home/newBlog.html', session=session, params=params)


@home.route('/blogSubmit', methods=['POST'])
@login_required
def blogSubmit():
    jsons = {}

    title = request.form['title']
    if Blog.query.filter(Blog.title == title).first():
        jsons['isSuccess'] = 1  # 标题重复
        return jsonify(jsons)
    url = request.form['url']
    content = request.form['content']
    body_html = request.form['body_html']
    tag_id = int(request.form['tag_id'])
    videos = request.form['videos']

    path = Config.UPLOAD_FOLDER_BLOG
    img_params = savaImage(url, path)
    one_blog = Blog(
        content=content,
        title=title,
        headName=img_params['filename'],
        head=img_params['data'],
        user_id=session['id'],
        body_html=body_html,
        tag=tag_id,
        uuid=uuid.uuid4().hex,
    )
    db.session.add(one_blog)
    db.session.commit()
    blog = Blog.query.filter(Blog.title == title).first()
    UserLogAdd(session['id'],session['username'],101,"博客id："+str(blog.id))
    if videos:
        temp = videos.split('\\')
        for i in temp:
            saveVideos(i, blog.id, blog.user_id)

    jsons['blog_id'] = blog.id
    jsons['isSuccess'] = 0
    return jsonify(jsons)


@home.route('/addCol', methods=['POST'])
@login_required
def addCol():
    jsons = {}
    blog_id = getBlogID(request.form['url'])
    if Collection.query.filter(Collection.user_id == session['id'], Collection.blog_id == blog_id).first():
        jsons['isSuccess'] = 9  # 已经收藏
        return jsonify(jsons)
    col_add = Collection(user_id=session['id'], blog_id=blog_id)
    db.session.add(col_add)
    db.session.commit()
    UserLogAdd(session['id'],session['username'],105,"博客id："+str(blog_id))
    jsons['isSuccess'] = 0
    return jsonify(jsons)


@home.route('/addLike', methods=['POST'])
@login_required
def addLike():
    jsons = {}
    blog_id = getBlogID(request.form['url'])
    if Like.query.filter(Like.user_id == session['id'], Like.blog_id == blog_id).first():
        jsons['isSuccess'] = 10  # 已经点赞
        return jsonify(jsons)
    like_add = Like(user_id=session['id'], blog_id=blog_id)
    db.session.add(like_add)
    db.session.commit()
    UserLogAdd(session['id'], session['username'],104, "博客id：" + str(blog_id))
    jsons['isSuccess'] = 0
    return jsonify(jsons)


@home.route('/userBlog', methods=['GET', 'POST'])
@login_required
def userBlog():
    params = {}
    params['blogs'] = []
    data = Blog.query.filter(Blog.user_id == session['id']).all()
    for i in data:
        temp = {
            "title": i.title,
            "id": i.id,
        }
        params['blogs'].append(temp)
    params['len'] = len(data)
    return render_template('home/userBlog.html', session=session, params=params)


@home.route('/delBlog', methods=['POST'])
@login_required
def delBlog():
    jsons = {}
    user_id = request.form['user_id']
    if user_id != str(session['id']):
        jsons['isSuccess'] = 5  # 用户信息错误
        return jsonify(jsons)
    blog_id = request.form['blog_id']

    blog = Blog.query.filter(Blog.id == blog_id).first()
    if not blog:
        jsons['isSuccess'] = 6  # 博客不存在
        return jsonify(jsons)
    if str(blog.user_id) != user_id:
        jsons['isSuccess'] = 5  # 用户信息错误
        return jsonify(jsons)

    if not delBlogByBlog(blog):
        jsons['isSuccess'] = 1
    else:
        jsons['isSuccess'] = 0
    return jsonify(jsons)


@home.route('/changeBlog', methods=['POST'])
@login_required
def changeBlog():
    blog_id = int(getBlogID(request.form['url']))

    blog = Blog.query.filter(Blog.id == blog_id).first()
    if not blog:
        jsons = {
            'isSuccess': 6
        }
        return jsonify(jsons)

    title = request.form['title']
    content = request.form['content']
    body_html = request.form['body_html']
    tag_id = int(request.form['tag_id'])
    url = request.form['headUrl']

    if title != blog.title and Blog.query.filter(Blog.title == title).first():
        jsons = {
            'isSuccess': 1  # 标题重复
        }
        return jsonify(jsons)
    elif not Tag.query.filter(Tag.id == tag_id).first():
        jsons = {
            'isSuccess': 3  # 标签不存在
        }
        return jsonify(jsons)

    if 'videos' in request.form:
        videos = request.form['videos']
        if videos:
            temp = videos.split('\\')
            for i in temp:
                saveVideos(i, blog.id, blog.user_id)

    path = Config.UPLOAD_FOLDER_BLOG
    img_params = savaImage(url, path)

    blog.content = content
    blog.body_html = body_html
    blog.title = title
    blog.headName = img_params['filename']
    blog.head = img_params['data']
    blog.tag = tag_id

    db.session.commit()
    UserLogAdd(session['id'],session['username'], 102, "博客id：" + str(blog.id))
    jsons = {
        'isSuccess': 0,
        'blog_id': blog_id,
    }
    return jsonify(jsons)


@home.route('/commentManage', methods=['GET', 'POST'])
@login_required
def commentManage():
    params = {
        'comments': []
    }
    comments = Comment.query.filter(Comment.user_id == session['id']).all()
    for i in comments:
        blog = Blog.query.filter(Blog.id == i.blog_id).first()
        temp = {
            "content": i.content,
            "blog_id": i.blog_id,
            "blog_name": blog.title,
            "comt_id": i.id,
        }
        params['comments'].append(temp)
    params['comments_len'] = len(comments)
    return render_template('home/commentManage.html', session=session, params=params)


@home.route('/delComment', methods=['POST'])
@login_required
def delComment():
    user_id = int(request.form['user_id'])
    comt_id = int(request.form['comt_id'])
    code = 0
    comment = Comment.query.filter(Comment.id == comt_id).first()
    if user_id != session['id'] or user_id != comment.user_id:
        code = 5
    else:
        blog_id = comment.blog_id
        DelComment(comment)
        UserLogAdd(session['id'], session['username'],106, "博客id：" + str(blog_id))
    jsons = {
        'isSuccess': code,
    }
    return jsonify(jsons)


@home.route('/colManage', methods=['GET', 'POST'])
@login_required
def colManage():
    params = {
        'collections': []
    }
    col = Collection.query.filter(Collection.user_id == session['id']).all()
    for i in col:
        blog = Blog.query.filter(Blog.id == i.blog_id).first()
        temp = {
            "blog_id": i.blog_id,
            "blog_name": blog.title,
            "col_id": i.id,
        }
        params['collections'].append(temp)
    params['col_len'] = len(col)
    return render_template('home/colManage.html', session=session, params=params)


@home.route('/delCol', methods=['POST'])
@login_required
def delCol():
    user_id = int(request.form['user_id'])
    col_id = int(request.form['col_id'])
    code = 0
    col = Collection.query.filter(Collection.id == col_id).first()
    if user_id != session['id'] or user_id != col.user_id:
        code = 5
    else:
        blog_id = col.blog_id
        DelCollection(col)
        UserLogAdd(session['id'],session['username'], 108, "博客id：" + str(blog_id))
    jsons = {
        'isSuccess': code,
    }
    return jsonify(jsons)


@home.route('/test', methods=['GET', 'POST'])
def test():
    jsons = {'s': 0}
    rp = request.form.to_dict()

    if rp['ww'] == '12':
        jsons['ttt'] = 12
        print(12)
    else:
        jsons['ttt'] = 11
        print(11)
    return jsonify(jsons)


@home.route('/video', methods=['GET', 'POST'])
@login_required
def videoTest():
    return render_template('home/video.html', session=session)


@home.route('/videoSubmit', methods=['POST'])
@login_required
def videoSubmit():
    uploads_pic = request.files['video']
    if uploads_pic and allow_video(uploads_pic.filename):
        # if uploads_pic:
        filename = secure_filename(uploads_pic.filename)
        path = os.path.join(Config.UPLOAD_FOLDER_BLOG, filename)
        uploads_pic.save(path)
        ret = {}
        ret['isSuccess'] = 0
        pp = 'uploads/blogs/' + filename
        url = url_for('static', filename=pp)
        ret['url'] = url

    else:
        ret = {
            'isSuccess': 1,
        }
    return jsonify(ret)




@home.route('/videoUpload', methods=['POST'])
@login_required
def videoUpload():
    jsons = {
        'isSuccess': 0,
    }
    uploads_pic = request.files['video']
    if uploads_pic and allow_video(uploads_pic.filename):
        # if uploads_pic:
        filename = secure_filename(uploads_pic.filename)
        path = os.path.join(Config.UPLOAD_FOLDER_BLOG, filename)
        uploads_pic.save(path)
        ret = {}
        ret['isSuccess'] = 0
        pp = 'uploads/blogs/' + filename
        url = url_for('static', filename=pp)
        ret['url'] = url
    return jsonify(jsons)


@home.route('/delVideo', methods=['POST'])
@login_required
def delVideo():
    jsons = {}
    if 'video_id' in request.form:
        video_id = request.form['video_id']
        if is_int(video_id):
            video_id = int(video_id)
            video = Video.query.filter(Video.id == video_id).first()
            if video:
                db.session.delete(video)
                db.session.commit()
                jsons['isSuccess'] = 0
            else:
                jsons['isSuccess'] = 29
    else:
        filename = request.form['filename']
        blog_id = request.form['blog_id']
        if is_int(blog_id):
            blog_id = int(blog_id)
            video = Video.query.filter(Video.video_name == filename, Video.blog_id == blog_id).first()
            if video:
                db.session.delete(video)
                db.session.commit()
            jsons['isSuccess'] = 0
        else:
            jsons['isSuccess'] = 5
    return jsonify(jsons)


@home.route('/movie', methods=['GET', 'POST'])
@login_required
def movie():
    video = Video.query.filter(Video.id == 2).first()
    if video:
        url = loadImage(video.video_data, video.video_name)
    else:
        url = video.video_name
    video_id = video.id
    return render_template('home/movie.html', session=session, v=url, video_id=video_id, mimetype='application/json')


@home.route("/tm/v3/", methods=["GET", "POST"])
def tm():
    import json
    if request.method == "GET":
        # 获取弹幕消息队列
        mid = request.args.get("id")
        key = "movie" + str(mid)
        if rd.llen(key):
            msgs = rd.lrange(key, 0, 2999)
            res = {
                "code": 0,
                "data": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                "code": 1,
                "danmaku": []
            }
        resp = json.dumps(res)
    if request.method == "POST":
        # 添加弹幕
        data = json.loads(request.get_data())
        msg = {
            "__v": 0,
            "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data["type"],
            "ip": request.remote_addr,
            "player": data["id"]
        }
        res = {
            "code": 0,
            "danmaku": msg
        }
        resp = json.dumps(res)
        msg = [data["time"], data["type"], data["color"], data["author"], data["text"]]
        rd.lpush("movie" + str(data["id"]), json.dumps(msg))
    return Response(resp, mimetype="application/json")
