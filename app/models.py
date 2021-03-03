from app import db
from datetime import datetime




class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    introduce = db.Column(db.Text, default="洗白白，吃饱饱")
    headName = db.Column(db.String(255), default='default.png')
    head = db.Column(db.LargeBinary(1048576))
    right = db.Column(db.Integer, default=2)
    uuid = db.Column(db.String(100),unique=True)
    addtime = db.Column(db.DateTime, default=datetime.now())
    # 反向引用
    blogs = db.relationship('app.models.Blog')
    comments = db.relationship('app.models.Comment')
    cols = db.relationship('app.models.Collection')
    likes = db.relationship('app.models.Like')
    logs = db.relationship('app.models.UserLog')

    def __repr__(self):
        return "User:%s %s %s" % (self.name, self.pwd, self.id)

    def check_pwd(self, pwdd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwdd)


class Blog(db.Model):
    __tablename__ = "blog"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    body_html = db.Column(db.Text)
    title = db.Column(db.String(255), nullable=False, unique=True)
    headName = db.Column(db.String(255), default='default_blog.png')
    head = db.Column(db.LargeBinary(1048576))
    uuid = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, default=datetime.now())

    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag = db.Column(db.Integer, db.ForeignKey('tag.id'))
    # 反向引用
    comments = db.relationship('app.models.Comment')
    cols = db.relationship('app.models.Collection')
    likes = db.relationship('app.models.Like')

    def __repr__(self):
        return "Blog:%r %r" % (self.id,self.title)


class Like(db.Model):
    __tablename__ = "like"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    addtime = db.Column(db.DateTime, default=datetime.now())
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    # 反向引用

    def __repr__(self):
        return "Like:%r %r %r" % (self.id,self.user_id,self.blog_id)


class Collection(db.Model):
    __tablename__ = "collection"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    addtime = db.Column(db.DateTime, default=datetime.now())
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    # 反向引用

    def __repr__(self):
        return "Collection:%r %r %r" % (self.id,self.user_id,self.blog_id)


class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    addtime = db.Column(db.DateTime, default=datetime.now())
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    # 反向引用


    def __repr__(self):
        return "Comment:%s" % self.content





class Tag(db.Model):
    __tablename__ = "tag"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, default=datetime.now())
    # 反向引用
    blogs = db.relationship('app.models.Blog')


    def __repr__(self):
        return "Tag: %s" % self.tag




class Video(db.Model):
    __tablename__ = "video"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_name = db.Column(db.String(255))
    # url = db.Column(db.String(255))
    video_data = db.Column(db.LargeBinary(4294967295))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer,db.ForeignKey('blog.id'))
    uuid = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "Video:%r %r %r" % (self.id,self.user_id,self.videoName)


class UserLog(db.Model):
    __tablename__ = "userlog"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(255))
    order = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, default=datetime.now())
    # 反向引用



    def __repr__(self):
        return "UserLog: %s" % self.order




if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    # #
    # import uuid
    # suuid = uuid.uuid4().hex
    # print(suuid)

    # roles = User(id=2, name='cat', pwd='cat', email='cat@qq.com',uuid=suuid)
    # roles2 = User(id=1, name='pig5', pwd='pig5', email='pig5@qq.com')
    # admin = User(id=100000,name='pig',pwd='pig',right=0)
    # tag = Tag(id=1, tag="未分类")
    # tag2 = Tag(id=2, tag="美食")
    # blog = Blog(content="我是一条博客哦哦哦哦哦！",user_id=2,title="我是博客1",tag=1)
    # blog2 = Blog(content="我是一条博客哦哦哦哦哦！", user_id=2, title="我是博客2", tag=1)
    # blog3 = Blog(content="我是一条博客哦哦哦哦哦！", user_id=2, title="我是博客3", tag=1)
    # comment = Comment(id=2, content="我我我我我是一条评论",blog_id=2,user_id=2)
    # like = Like(id=2,user_id=2,blog_id=2)
    # collect = Collection(id=3,user_id=2,blog_id=2)

    # admin = Admin(id=1,name="pig", pwd="pig")
    # db.session.add(roles)
    # db.session.add(roles2)
    # db.session.add(tag)
    # db.session.add(tag2)
    # db.session.add(blog)
    # db.session.add(blog2)
    # db.session.add(blog3)
    # db.session.add(comment)
    # db.session.add(like)
    # db.session.add(collect)

    # db.session.add(admin)
    db.session.commit()

    # blogCheck = Blog.query.filter(Blog.id==2).first()
    # for i in blogCheck.likes:
    #     print(i)
