模拟博客网站
=============
##目录
1. 项目描述
    * 名称
    * 版本
    * 功能
    * 项目树
    * 依赖
    * 启动
2. 业务介绍
    * 用户界面
    * 用户界面接口
    * 管理员界面
    * 管理员界面接口
    * 其他内容
3. 备注

## 项目描述
+ ### 名称
>+ 模拟博客网站

+ ### 版本
>+ V1.1
>+ 更新时间：2021-4-11

+ ### 功能
+ 用户注册、登陆、个人信息修改
+ 博客预览、上传、编辑
+ 博客浏览、搜索
+ 博客视频上传、视频弹幕发送
+ 后台用户、博客评论等管理

+ ### <span id='treez'>项目树</span>
完整内容在->[list.txt](./list.txt)

```
│  list.txt
│  manage.py
│  README.md
│  requirements.txt
|  uwsgi.ini
|  uwsgi.pid
|  redis.conf
│     
├─logs
|  └─ uwsgi.log 
|
├─app
│  │  config.py
│  │  models.py
|  |  ErrorCode.py
│  │  __init__.py
│  │  
│  ├─admin
│  │  │  form.py
│  │  │  view.py
│  │  │  __init__.py
│  │  │  
│  │  └─static
│  │          
│  ├─home
│  │  │  form.py
│  │  │  view.py
│  │  │  __init__.py
│  │  │  
│  │  └─static
|  |
│  ├─api
│  │  │  form.py
│  │  │  view2.py
│  │  │  __init__.py
│  │  │  
│  │  └─static
│  │ 
│  ├─models
│  ├─static
│  │  ├─css
│  │  ├─images
│  │  ├─js
│  │  └─uploads
│  │      ├─blogs
│  │      └─users
│  │              
│  ├─templates
│  │  ├─admin
│  │  │      adminhome.html
│  │  │      index.html
│  │  │      login.html
│  │  │      order.html
│  │  │      userChange.html
│  │  │      
│  │  ├─home
│  │  │      404.html
│  │  │      blogs.html
│  │  │      colManage.html
│  │  │      commentManage.html
│  │  │      home.html
│  │  │      index.html
│  │  │      movie.html
│  │  │      newBlog.html
│  │  │      userBlog.html
│  │  │      userhome.html
│  │  │      video.html
│  │  │      
│  │  └─ul
│  │         usermenu.html

```

+ ### 依赖([requirements.txt](requirements.txt))

>+ Werkzeug==0.16.0
>+ Flask_SQLAlchemy==2.4.1
>+ PyMySQL==0.9.3
>+ Flask==1.1.1
>+ WTForms==2.2.1
>+ Flask_WTF==0.14.3
>+ Flask_PageDown==0.3.0


+ ### 启动（[manage.py](./manage.py)）
```
python manage.py runserver

```


## 业务介绍

+ ### 用户界面
 
 项目页面  | 描述  | 链接 | 参数
 ---- | ----- | ------  | ------  
 index  | 网站首页 | / |  
 userhome  | 用户个人中心 | /userhome |  
 blogs  | 博客页面 | /blogs/\<int:blog_id\> |   blog_id用于区分博客
 newBlog  | 博客编辑 | /newBlog/\<int:user_id\>/\<int:blog_id\> | user_id区分用户<br>blog_id用于区分博客(0表示创建新博客)
 userBlog  | 个人博客管理列表 | /userBlog |
 commentManage  | 个人评论管理列表 | /commentManage |
 colManage  | 个人收藏管理 | /colManage |
 logout  | 登出 | /logout |

 

+ ### 用户界面接口

 链接  | 描述  | 参数 | 返回值
 ---- | ----- | ------  | ------  
 /checkLogin  | 登陆验证 |  用户名：'username'<br>密码：'password' | 状态码：'isSuccess'
 /registers  | 注册验证  | 用户名：'username'<br>密码：'password'<br> 邮箱：'email' | 状态码：'isSuccess'
 /changePwd  | 修改密码 |  新密码：'password' | 状态码：'isSuccess'
 /changeITD  | 修改签名 |  个人介绍：'introduce' | 状态码：'isSuccess'
 /changeHead  | 修改头像预览 |  文件：'images' | 状态码：'isSuccess'<br>预览头像地址：'url'
 /changeHeaded  | 保存修改头像 |  头像地址：'url' | --
 /changeLoge  | 修改博客封面预览 |  文件：'images' | 状态码：'isSuccess'<br>封面地址:'url'
 /blogSubmit  | 博客提交 |  标题：'title'<br>封面地址：'url'<br>博客内容：'content'<br>markdown转译结果：'body_html'<br>标签号：'tag_id'<br>视频：'videos' | 状态码：'isSuccess'<br>博客识别码：'blog_id'
 /addCol  | 添加收藏 |  博客地址：'url' | 状态码：'isSuccess'
 /addLike  | 点赞 |  博客地址：'url' | 状态码：'isSuccess'
 /delBlog  | 删除博客 |  评论博客地址:'url' | 状态码：'isSuccess'
 /changeBlog  | 修改博客 |  同"blogSubmit" | 同"blogSubmit"
 /delComment  | 评论删除 |  用户id：'user_id'<br>评论id:'comt_id' | 状态码：'isSuccess'
 /delCol  | 删除收藏 |  用户id：'user_id'<br>收藏id:'col_id' | 状态码：'isSuccess'
 /videoSubmit  | 视频上传 |  文件：'video' | 状态码：'isSuccess'
 /videoUpload  | 视频加载 |  文件：'video' | 状态码：'isSuccess'
 /delVideo  | 视频删除 |  视频id：'video_id'<br>或<br>视频文件名:'filename'<br>视频对应博客id:'blog_id' | 状态码：'isSuccess'
 /tm/v3/  | 弹幕接口 |  (get)弹幕接口id：'id'<br>(post)添加的弹幕内容:略 | 状态码：'code'<br>弹幕内容：'danmaku'
 /delVideo  | 评论提交 |  评论内容：'comment'，评论地址:'url' | 状态码：'isSuccess'
 
 + ### 管理员界面(路由均需加上'/admin')
 
 项目页面  | 描述  | 链接 | 参数
 ---- | ----- | ------  | ------  
 index  | 后台首页 | / |  
 orderManage  | 后台管理界面 | /order/\<int:order\> |  指令：'order'<br>(1:用户,2:博客,3:评论,4:标签,5:日志)
 login  | 后台登陆界面 | /login | 
 userChange  | 博客编辑 | /userChange/\<int:user_id\>| user_id区分用户

+ ### 管理员界面接口(路由均需加上'/admin')

 链接  | 描述  | 参数 | 返回值 | 备注
 ---- | ----- | ------  | ------  | -----
 /orderWork  | 后台功能页选择 |  指令：'order' | 状态码：'isSuccess'<br>指令：'order'<br>地址:'url' |
 /loginCheck  | 登陆验证  | 用户名：'username'<br>密码：'password' | 状态码：'isSuccess' |
 /logout  | 登出 |  新密码：'password' | 状态码：'isSuccess' |    与用户界面实现方式不同
 /deleteUser  | 删除用户 |  用户id：'user_id' | 状态码：'isSuccess' |
 /AdmindeleteBlog  | 删除博客 |  博客id：'blog_id' | 状态码：'isSuccess' |
 /AdmindeleteComment  | 删除评论 |  评论id：'comment_id' | 状态码：'isSuccess' |
 /AdminDeleteTag  | 删除标签 |  标签id：'tag_id' | 状态码：'isSuccess' |
 /changeComment  | 修改评论 |  评论id：'comt_id'<br>评论内容：'comt_data' | 状态码：'isSuccess' |
 /newTag  | 新建标签 |  标签内容：'tagName' | 状态码：'isSuccess' |
 /changeTagName  | 修改标签 |  标签id：'id'<br>标签内容：'tagName' | 状态码：'isSuccess' |
 /changeUser  | 修改用户信息 |  用户id：'user_id'<br>新密码：'password'<br>确认密码：'checkpwd'<br>个人签名：'introduce'<br>头像地址：'url' | 状态码：'isSuccess' | ***除'user_id'外，其他参数非必要***

 
+ ### 其他内容
>+ app通过Config类存放（[config.py](./app/config.py)）
>+ 数据库模型定义于[models.py](./app/models.py)
>+ 404界面为全局重载，在home路由实现
>+ 用户界面的自定义js（[login.js](./app/static/js/login.js)）
>+ 用户界面的自定义css（[home_index.css](./app/static/css/home_index.css)）
>+ 后台界面的自定义js（[admin.js](./app/static/js/admin.js)）
>+ 后台界面的自定义css（[component.css](./app/static/css/component.css)）


## 备注
>+ 需要mysql数据库及redis数据库
>+ 目前项目安全细节尚未完善


### 2021.4.11更新
>+ 项目部署在阿里云上(公安局审批还没搞)
>+ nginx+uwsgi+flask
>+ 域名：[http://lingshipu.ren](http://lingshipu.ren/)
>+ 新增接口(与原项目仅有用户账户是相关的) 详见[aip文档](https://www.showdoc.com.cn/simuwuding)\(密码:yrdblog\)

#### 作者：鼎



