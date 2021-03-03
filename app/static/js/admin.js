function MyLoginCheck() {
    var params = {
        "username": $("#adminName").val(),
        'pwd': $("#adminPwd").val(),
    };

    if (isEmpty(params['username'])) {
        layer.msg("用户名不能为空")
        return;
    } else if (isEmpty(params['pwd'])) {
        layer.msg("密码不能为空");
        return;
    }
    $.ajax({
        url: "/admin/loginCheck",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {

            window.location.href = '/admin/';
            layer.msg('修改成功');
        } else if (ret['isSuccess'] == 1) {
            layer.msg('管理员账户不存在');
        } else if (ret['isSuccess'] == 11) {
            layer.msg('密码错误');
        } else {
            layer.msg('修改失败，未知错误');
        }
    })
}

function MyLogout() {

    var params = {
        "logout": true,
    };
    $.ajax({
        url: "/admin/logout",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {

            window.location.href = '/admin/login';
            layer.msg('退出成功');
        } else {
            layer.msg('未知错误');
        }
    })
}

function ManageOrder(order) {
    var params = {
        "order": order,
    };
    $.ajax({
        url: "/admin/orderWork",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.href = '/admin/order/' + ret['url'];
            OrderTagColor(order)
        } else if (ret['isSuccess'] == 12) {
            layer.msg('错误指令');
        } else {
            layer.msg('未知错误');
        }
    })
}

function OrderTagColor(order) {
    var self = document.getElementsByClassName("order_num")[order - 1];
    var p = self.parentNode.children;
    for (e of p) {
        e.classList.remove("active");
    }
    self.classList.add("active");
}

function AdminDeleteUser(user_id) {
    var params = {
        "user_id": user_id,
    };
    $.ajax({
        url: "/admin/deleteUser",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("删除成功！")
        } else {
            layer.msg('未知错误');
        }
    })

}

function AdminDeleteBlog(blog_id) {
    var params = {
        "blog_id": blog_id,
    };
    $.ajax({
        url: "/admin/deleteBlog",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("删除成功！")
        } else if (ret['isSuccess'] == 6) {
            layer.msg("博客不存在！")
        } else {
            layer.msg('未知错误');
        }
    })
}

function AdminDeleteComment(comment_id) {
    var params = {
        "comment_id": comment_id,
    };
    $.ajax({
        url: "/admin/deleteComment",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("删除成功！")
        } else if (ret['isSuccess'] == 8) {
            layer.msg("评论不存在！")
        } else {
            layer.msg('未知错误');
        }
    })
}

function AdminDeleteTag(tag_id) {
    var params = {
        "tag_id": tag_id,
    };
    $.ajax({
        url: "/admin/DeleteTag",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("删除成功！")
        } else if (ret['isSuccess'] == 7) {
            layer.msg("标签不存在！")
        } else if (ret['isSuccess'] == 55) {
            layer.msg("改标签不可删除")
        } else {
            layer.msg('未知错误');
        }
    })
}

function ShowComCreateText(comment_id) {
    var com_id = document.getElementById("com_id");
    com_id.value = comment_id;
    layer.open({
        type: 1,
        title: ["修改标签", 'font-size: large;color: black;'],
        closeBtn: 1,
        move: false,
        shade: 0.7,
        area: ["395px", "325px"],
        scrollbar: false,
        content: $("#changeComBox").html(),
    });

}



function ShowTagCreateText() {
    layer.open({
        type: 1,
        title: ["创建标签", 'font-size: large;color: black;'],
        closeBtn: 1,
        move: false,
        shade: 0.7,
        area: ["395px", "325px"],
        scrollbar: false,
        content: $("#createTagBox").html(),
    });
}

function ShowTagChangeText(id, name) {
    var tag_id = document.getElementById("tag_id");
    tag_id.value = id;
    layer.open({
        type: 1,
        title: ["修改标签", 'font-size: large;color: black;'],
        closeBtn: 1,
        move: false,
        shade: 0.7,
        area: ["395px", "325px"],
        scrollbar: false,
        content: $("#changeTagBox").html(),
    });
}

function CommentChange() {
    var params = {
        "comt_id": document.getElementById("com_id").value,
        "comt_data": $(".InputChangeComBox").eq(1).val(),
    };
    $.ajax({
        url: "/admin/changeComment",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("删除成功！")
        } else if (ret['isSuccess'] == 25) {
            layer.msg("评论不存在！")
        } else {
            layer.msg('未知错误');
        }
    })

}

function TagCreate() {
    var params = {
        "tagName": $(".InputTagName").eq(1).val(),
    };
    var ret = ajaxPost(params,"/admin/newTag");
    if(ret){
        var isSuccess=ret['isSuccess'];
        if (!isSuccess) {
            window.location.reload();
            return true;
        } else if (isSuccess == 56) {
            layer.msg("标签已存在！")
        } else {
            layer.msg('未知错误');
        }
    }

    return false;

}

function TagChange() {
    var params = {
        "id": document.getElementById("tag_id").value,
        "tagName": $(".InputChangedTagName").eq(1).val(),
    };
    if (isEmpty(params['id'])) {
        layer.msg("标签错误");
        return;
    } else if (isEmpty(params['tagName'])) {
        layer.msg("标签名不能为空");
        return;
    }
    $.ajax({
        url: "/admin/changeTagName",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("修改成功！")
        } else if (ret['isSuccess'] == 56) {
            layer.msg("标签已存在！")
        } else {
            layer.msg('未知错误');
        }
    })
}

function AdminChangeUser(user_id){
    var params = {
        "user_id":user_id,
        "username": $(".InputUserName").val(),
        "password": $(".InputPWD1").val(),
        "checkpwd": $(".InputPWD2").val(),
        "url": document.getElementById('user_head_pic').src,
        "introduce": $(".InputITD").val(),
    };
    if(isEmpty(params['user_id'])){
        layer.msg('用户出错')
        return false;
    } else if (isEmpty(params['username'])) {
        layer.msg('用户名不能为空!');
        return false;
    } else if ((!isEmpty(params['password'])) & isEmpty(params['checkpwd'])) {
        layer.msg('重复密码不能为空!');
        return false;
    } else if (params['password'] != params['checkpwd']) {
        layer.msg('密码不一致!');
        return false;
    } else if (isEmpty(params['url'])) {
        layer.msg('用户名不能为空!');
        return false;
    }
    $.ajax({
        url: "/admin/changeUserData",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("修改成功！")
        } else if (ret['isSuccess'] == 20) {
            layer.msg("用户名修改失败！")
        }else if (ret['isSuccess'] == 21) {
            layer.msg("密码修改失败！")
        } else if (ret['isSuccess'] == 22) {
            layer.msg("个人介绍修改失败！")
        }  else if (ret['isSuccess'] == 23) {
            layer.msg("头像修改失败！")
        } else if(ret['isSuccess'] == 6){
            layer.msg('用户不存在')
        }else{
            layer.msg('未知错误'+ret['isSuccess']);
        }
    })
}


function isEmpty(item) {
    if (item == '' || item == undefined || item == null) {
        return true;
    } else return false;
}
