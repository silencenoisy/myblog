from . import api

from flask import request, abort, jsonify, redirect, url_for, g
from app import db, Config, rd
from app.ErrorCode import ErrorCode
from datetime import datetime

from app.models import Todo, User
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

auth = HTTPTokenAuth(scheme='JWT')


@auth.verify_token
def verify_token(token):
    # Config.SECRET_KEY:内部的私钥，这里写在配置信息里
    s = Serializer(Config.SECRET_KEY)

    user = User.verify_auth_token(token)
    if not user:
        return False
    # 校验通过返回True
    g.user = user
    return True


@auth.error_handler
def error_handler_401():
    return error_json(401, "invalid token")


# @csrf.exempt
@api.route('/login', methods=['POST'])
def login():
    '''
    接受参数并校验参数，返回token
    :return:
    '''
    user = request.form['username']
    password = request.form['password']
    guest = User.query.filter_by(name=user).first()
    # 生成token
    if guest.check_pwd(password):
        z_token = User.create_token(guest.id)

        return jsonify(token=z_token)
    else:
        return error_json(ErrorCode.LOGIN_FAIL, 'error password'),ErrorCode.LOGIN_FAIL


@api.route('/index')
@auth.login_required
def index():
    return 'helllo word'


def error_json(code, msg=""):
    return jsonify({
        'status': code,
        'message': msg,
    })


def error_post_401(msg="Invalid API key"):
    return error_json(400, msg)


def success_json(*, msg="", data=""):
    return jsonify({
        "status": 0,
        "message": msg,
        "data": data,
    })


def get_todo_data(todo):
    data = {
        "id": todo.index,
        "user_id": todo.user_id,
        "title": todo.title,
        "content": todo.content,
        "done": todo.done,
        "addtime": todo.addtime.strftime('%Y-%m-%d %H:%M:%S'),
        "deadline": todo.deadline.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return data


def next_index(user_id):
    todo = Todo.query.filter(Todo.user_id == user_id).order_by(Todo.index.desc()).first()
    if todo:
        return todo.index + 1
    else:
        return 1


def id_check(id, user_id):
    if id is not None:

        id = int(id)
        user_id = int(user_id)
        if not User.query.filter_by(id=user_id).first():
            raise IndexError('%d is not exist' % user_id)
        if Todo.query.filter_by(index=id, user_id=user_id).first():
            raise IndexError('%d is exist' % id)


    else:
        id = next_index(user_id)
    return id


def search_todo(user_id, keyword, page=1, per_page=20):
    return Todo.query.filter(Todo.user_id == user_id, Todo.title.like("%" + keyword + "%")) \
        .paginate(page=page, per_page=per_page, error_out=False)


def get_data(user_id, page=1, per_page=20, is_done=-1):
    if is_done == -1:
        return Todo.query.filter_by(user_id=user_id).order_by(Todo.index).paginate(page=page, per_page=per_page,
                                                                                   error_out=False)
    else:
        return Todo.query.filter_by(user_id=user_id, done=is_done).order_by(Todo.index) \
            .paginate(page=page, per_page=per_page, error_out=False)


def save_history(user_id, query_url, addtime):
    value = {'user': user_id, 'url': query_url, 'addtime': addtime.strftime('%Y-%m-%d %H:%M:%S')}
    value = value.__repr__()

    rd.rpush(Config.REDIS_HISTORY, value)
    if rd.llen(Config.REDIS_HISTORY) > Config.HISTORY_MAX_LEN:
        rd.lpop(Config.REDIS_HISTORY)
    return True


def get_history():
    return rd.lrange(Config.REDIS_HISTORY, 0, rd.llen(Config.REDIS_HISTORY) - 1)


# @csrf.exempt
@api.route('/todo/add', methods=['POST'])
@auth.login_required
def add():
    data = request.form

    title = data.get('title')
    if title is None:
        return error_json(ErrorCode.INVALID_KEY,"need 'title'"),ErrorCode.INVALID_KEY

    id = data.get('index')
    user_id = g.user.id
    try:
        id = id_check(id, user_id)
    except ValueError:
        return error_json(ErrorCode.INVALID_KEY, "Invalid value"),ErrorCode.INVALID_KEY
    except IndexError:
        return error_json(ErrorCode.NOT_FOUND, "order failed"),ErrorCode.NOT_FOUND
    except Exception:
        return error_json(ErrorCode.INVALID_KEY,"unknown error"),ErrorCode.INVALID_KEY

    try:
        todo = Todo(
            index=id,
            user_id=user_id,
            title=data.get('title'),
            content=data.get('content'),
            done=False,
        )
        deadline = data.get('deadline')
        if deadline:
            todo.deadline = deadline
        db.session.add(todo)
        db.session.commit()
    except Exception:
        return error_json(ErrorCode.SQL_ERROR, "ADDFIAL")
    return success_json(data=get_todo_data(todo)), ErrorCode.ADD_SUCCESS


# @csrf.exempt
@api.route('/todo/change/<int:id>/done', methods=['PATCH'])
@auth.login_required
def change_status_done(id):
    try:
        user_id = g.user.id
    except KeyError:
        return error_json(ErrorCode.LOGIN_FAIL, "user exist error"),ErrorCode.LOGIN_FAIL
    todo = Todo.query.filter_by(index=id, user_id=user_id).first()
    if not todo:
        return error_json(ErrorCode.NOT_FOUND, "not found"), ErrorCode.NOT_FOUND
    todo.done = True
    db.session.commit()
    return success_json(data=get_todo_data(todo))


# @csrf.exempt
@api.route('/todo/change/done', methods=['PATCH'])
@auth.login_required
def change_all_status_done():
    try:
        user_id = g.user.id
    except KeyError:
        return error_json(ErrorCode.LOGIN_FAIL, "user exist error"),ErrorCode.LOGIN_FAIL
    todo = Todo.query.filter_by(user_id=user_id,done=False).all()
    for i in todo:
        i.done = True
    db.session.commit()
    count = len(todo)
    # todo_list = [get_todo_data(x) for x in todo]
    return success_json(data={'count':count})


# @csrf.exempt
@api.route('/todo/change/<int:id>/undone', methods=['PATCH'])
@auth.login_required
def change_status_undone(id):
    try:
        user_id = g.user.id
    except KeyError:
        return error_json(ErrorCode.LOGIN_FAIL, "user exist error"),ErrorCode.LOGIN_FAIL
    todo = Todo.query.filter_by(index=id, user_id=user_id).first()
    if not todo:
        return error_json(ErrorCode.NOT_FOUND, "not found"),ErrorCode.NOT_FOUND
    todo.done = False
    db.session.commit()
    return success_json(data=get_todo_data(todo))


# @csrf.exempt
@api.route('/todo/change/undone', methods=['PATCH'])
@auth.login_required
def change_all_status_undone():
    try:
        user_id = g.user.id
    except KeyError:
        return error_json(ErrorCode.LOGIN_FAIL, "user exist error"),ErrorCode.LOGIN_FAIL
    todo = Todo.query.filter_by(user_id=user_id).all()
    for i in todo:
        i.done = False
    db.session.commit()
    count = len(todo)
    return success_json(data={'count':count})


# @csrf.exempt
@api.route('/todo', methods=['GET'])
@auth.login_required
def get_todo():
    user_id = g.user.id
    args = request.args
    page = args.get('page', 1, int)
    per_page = args.get('per_page', 20, int)
    data = get_data(user_id, page, per_page, -1)
    save_history(user_id, request.url, datetime.now())
    return success_json(data=[get_todo_data(x) for x in data.items])


# @csrf.exempt
@api.route('/todo/undone', methods=['GET'])
@auth.login_required
def get_todo_undone():
    user_id = g.user.id
    args = request.args
    page = args.get('page', 1, int)
    per_page = args.get('per_page', 20, int)
    data = get_data(user_id, page, per_page, 0)
    save_history(user_id, request.url, datetime.now())
    return success_json(data=[get_todo_data(x) for x in data.items])


# @csrf.exempt
@api.route('/todo/done', methods=['GET'])
@auth.login_required
def get_todo_done():
    user_id = g.user.id
    args = request.args
    page = args.get('page', 1, int)
    per_page = args.get('per_page', 20, int)
    data = get_data(user_id, page, per_page, 1)
    save_history(user_id, request.url, datetime.now())
    return success_json(data=[get_todo_data(x) for x in data.items])


# @csrf.exempt
@api.route('/todo/<int:id>', methods=['GET'])
@auth.login_required
def get_todo_by_id(id):
    user_id = g.user.id
    todo = Todo.query.filter_by(index=id, user_id=user_id).first()
    if not todo:
        save_history(user_id, request.url, datetime.now())
        return error_json(ErrorCode.NOT_FOUND, "not found"),ErrorCode.NOT_FOUND
    save_history(user_id, request.url, datetime.now())
    return success_json(data=get_todo_data(todo))


# @csrf.exempt
@api.route('/todo/search', methods=['GET'])
@auth.login_required
def get_todo_search():
    user_id = g.user.id
    args = request.args
    page = args.get('page', 1, int)
    per_page = args.get('per_page', 20, int)
    keyword = args.get('keyword')
    if not keyword:
        return error_json(ErrorCode.INVALID_KEY,'no keyword'),ErrorCode.INVALID_KEY

    data = search_todo(user_id, keyword, page, per_page)
    save_history(user_id, request.url, datetime.now())
    return success_json(data=[get_todo_data(x) for x in data.items])


# @csrf.exempt
@api.route('/todo/delete', methods=['DELETE'])
@auth.login_required
def delete_todo():
    user_id = g.user.id
    data = Todo.query.filter_by(user_id=user_id).all()
    count = data.count
    for i in data:
        db.session.delete(i)
    db.session.commit()
    return success_json(data={'count': count})


# @csrf.exempt
@api.route('/todo/delete/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_todo_by_id(id):
    user_id = g.user.id

    data = Todo.query.filter_by(user_id=user_id, index=id).first()
    if not data:
        return error_json(ErrorCode.NOT_FOUND, "not found"), ErrorCode.NOT_FOUND
    db.session.delete(data)
    db.session.commit()
    return success_json()


# @csrf.exempt
@api.route('/todo/delete/done', methods=['DELETE'])
@auth.login_required
def delete_todo_done():
    user_id = g.user.id
    data = Todo.query.filter_by(user_id=user_id, done=True).all()
    count = len(data)
    for i in data:
        db.session.delete(i)
    db.session.commit()
    return success_json(data={'count': count})


# @csrf.exempt
@api.route('/todo/delete/undone', methods=['DELETE'])
@auth.login_required
def delete_todo_undone():
    user_id = g.user.id
    data = Todo.query.filter_by(user_id=user_id, done=False).all()
    count = len(data)
    print(count)
    for i in data:
        db.session.delete(i)
    db.session.commit()
    return success_json(data={'count': count})


# @csrf.exempt
@api.route('/todo/history', methods=['GET'])
# @auth.login_required
def get_history_data():
    return success_json(data={'history': [x for x in get_history()]})
