var l_url = window.location.href;

function ajaxPost(data, url) {
    var retData;
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'JSON',
        async:false,
    }).done(function (ret) {
        retData = ret;
    });
    return retData;

}

function ShowLoginText() {
    layer.open({
        type: 1,
        title: ["登录", 'font-size: large;color: black;'],
        closeBtn: 1,
        move: false,
        shade: 0.7,
        area: ["395px", "325px"],
        scrollbar: false,
        content: $("#loginBox").html(),
    });
}


function ShowRegisterText() {

    layer.open({
        type: 1,
        title: ["注册", 'font-size: large;color: black;'],
        closeBtn: 1,
        move: false,
        shade: 0.7,
        area: ["395px", "376px"],
        scrollbar: false,
        content: $("#registerBox").html(),
    });
}

function CloseLoginText() {
    layer.closeAll();
    ShowRegisterText()
}

function HttpPost(url, params) {
    var temp = document.createElement("form");
    temp.action = url;
    temp.method = "post";
    temp.style.display = "none";

    for (var v in params) {
        var opt = document.createElement("textarea");
        opt.name = v;
        opt.value = params[v];
        temp.appendChild(opt);
    }

    document.body.appendChild(temp);
    temp.submit();

    return temp;
}


function LoginCheck() {
    var params = {
        "username": $(".InputUsername").eq(1).val(),
        "password": $(".InputUserPwd").eq(1).val(),
    };

    if (isEmpty(params['username'])) {
        // window.alert(params['username']);
        parent.layer.msg("用户名不能为空");
        return false;
    } else if (isEmpty(params['password'])) {
        parent.layer.msg("密码不能为空");
        return false;
    }
    var ret = ajaxPost(params, "/checkLogin")
    if(!isEmpty(ret)){
        var isSuccess=ret['isSuccess'];
        if(!isSuccess){
            window.location.reload();
            return true;
        }else if(isSuccess==1001) {
            layer.msg('用户不存在');
            return false;
        }else if(isSuccess==1002){
            layer.msg('密码错误');
            return false;
        }else{
            layer.msg('未知错误');
            return false;
        }
    }
}

// 注册表单
function Register() {
    var params = {
        "username": $(".InputUsername2").eq(1).val(),
        "password": $(".InputUserPwd1").eq(1).val(),
        "checkpwd": $(".InputUserPwd2").eq(1).val(),
        "email": $(".InputUserEmail").eq(1).val(),
    };

    if (isEmpty(params['username'])) {
        layer.msg("用户名不能为空");
        return false;
    }else if (params['username'].length<3) {
        layer.msg("用户名必须大于3个字符");
        return false;
    } else if (params['username'].length>25) {
        layer.msg("用户名必须小于25个字符");
        return false;
    } else if (isEmpty(params['password'])) {
        layer.msg("密码不能为空");
        return false;
    } else if (params['password'].length<6) {
        layer.msg("密码不能小于6位");
        return false;
    }else if (params['password'].length>25) {
        layer.msg("密码不能大于25位");
        return false;
    }else if (isEmpty(params['checkpwd'])) {
        layer.msg("密码不能为空");
        return false;
    } else if (isEmpty(params['email'])) {
        layer.msg("邮箱不能为空");
        return false;
    } else if (params['checkpwd'] != params['password']) {
        layer.msg("两次密码不一致")
        return false;
    } else if (!checkEmail(params['email'])) {
        layer.msg("邮箱格式错误")
        return false;
    }

    var ret = ajaxPost(params,'/registers');
    if(ret){
        var isSuccess=ret['isSuccess'];
        if(!isSuccess){
            window.location.reload();
            return true;
        }else if(isSuccess==1001){
            layer.msg('用户名已存在!');
        }else{
            layer.msg('未知错误');
        }
    }
    return false;
}

function checkEmail(email) {
    if (email)
        var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
    if (email === "") return false;
    if (!reg.test(email)) {
        return false;
    }
    return true;
}


function ChangePWD() {
    var params = {
        "password": $(".InputPWD1").val(),
        "checkpwd": $(".InputPWD2").val(),
    };

    if (isEmpty(params['password'])) {
        // window.alert(params['username']);
        window.alert("新密码不能为空");
        return;
    } else if (isEmpty(params['checkpwd'])) {
        window.alert("重复密码不能为空");
        return;
    } else if (params['checkpwd'] != params['password']) {
        window.alert("两次密码不同");
        return;
    }

    HttpPost('changePwd', params);
}


function ChangeITD() {
    var params = {
        "introduce": $(".InputITD").val(),
    };

    if (isEmpty(params['introduce'])) {
        window.location.href = l_url
        return;
    }

    HttpPost('changeITD', params);
}

function ClickInputHead() {
    return $("#InputHead").click();

}

function ClickInputLogo() {
    return $("#InputLogo").click();

}

function upload_head() {
    var animateimg = $(".InputHead").val(); //获取上传的图片名 带//
    var imgarr = animateimg.split('\\'); //分割
    var myimg = imgarr[imgarr.length - 1]; //去掉 // 获取图片名
    var houzui = myimg.lastIndexOf('.'); //获取 . 出现的位置
    var ext = myimg.substring(houzui, myimg.length).toUpperCase();  //切割 . 获取文件后缀

    var file = $('#InputHead').get(0).files[0]; //获取上传的文件
    var fileSize = file.size;           //获取上传的文件大小
    var maxSize = 1048576;              //最大1MB
    if (ext != '.PNG' && ext != '.GIF' && ext != '.JPG' && ext != '.JPEG' && ext != '.BMP') {
        parent.layer.msg('文件类型错误,请上传图片类型');
        return false;
    } else if (parseInt(fileSize) >= parseInt(maxSize)) {
        parent.layer.msg('上传的文件不能超过1MB');
        return false;
    } else {
        var data = new FormData();
        //获取文件内容
        data.append('images', $('#InputHead')[0].files[0]);
        $.ajax({
            url: "/changeHead",
            type: 'POST',
            data: data,
            dataType: 'JSON',
            cache: false,
            processData: false,
            contentType: false
        }).done(function (ret) {
            if (ret['isSuccess']) {
                // $("#show").attr('value',+ ret['f'] +);
                var head_img = document.getElementById('user_head_pic');
                head_img.src = ret['url'];
                layer.msg('上传成功');
            } else {
                layer.msg('上传失败');
            }
        });
        return false;
    }
}

function UploadLogo() {
    var animateimg = $("#InputLogo").val(); //获取上传的图片名 带//
    var imgarr = animateimg.split('\\'); //分割
    var myimg = imgarr[imgarr.length - 1]; //去掉 // 获取图片名
    var houzui = myimg.lastIndexOf('.'); //获取 . 出现的位置
    var ext = myimg.substring(houzui, myimg.length).toUpperCase();  //切割 . 获取文件后缀

    var file = $('#InputLogo').get(0).files[0]; //获取上传的文件
    var fileSize = file.size;           //获取上传的文件大小
    var maxSize = 1048576;              //最大1MB
    if (ext != '.PNG' && ext != '.GIF' && ext != '.JPG' && ext != '.JPEG' && ext != '.BMP') {
        parent.layer.msg('文件类型错误,请上传图片类型');
        return false;
    } else if (parseInt(fileSize) >= parseInt(maxSize)) {
        parent.layer.msg('上传的文件不能超过1MB');
        return false;
    } else {
        var data = new FormData();
        //获取文件内容
        data.append('images', $('#InputLogo')[0].files[0]);
        $.ajax({
            url: "/changeLoge",
            type: 'POST',
            data: data,
            dataType: 'JSON',
            cache: false,
            processData: false,
            contentType: false
        }).done(function (ret) {
            if (ret['isSuccess']) {
                // $("#show").attr('value',+ ret['f'] +);
                var head_img = document.getElementById('Blog_logo');
                head_img.src = ret['url'];
                layer.msg('上传成功');
            } else {
                layer.msg('上传失败');
            }
        });
        return false;
    }
}

function ChangeHead() {
    var params = {
        "url": document.getElementById('user_head_pic').src
    };

    HttpPost('changeHeaded', params);
}


function test() {
    $.ajax({
        url: "/home/test",
        type: "post",
        data: {
            "ww": 12,
            "tt": 13,
        },
        dataType: "json",

        success: function (data) {

            alert(data)
            var name = data['ttt']
            alert(name)
        }
    })
}

function LikeThis() {

    var pic = document.getElementById('like_pic');
    var params = {
        'url': location.href,
    };
    $.ajax({
        url: "/addLike",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            pic.src = "/static/images/bkw.png";


            var c1 = document.getElementById('like_span');
            c1.innerText = parseInt(c1.innerText) + 1
        } else if (ret['isSuccess'] == 10) {
            layer.msg('已点赞');
        } else {
            layer.msg("点赞失败")
        }
    })
}

function ColThis() {
    var pic = document.getElementById('col_pic');
    var params = {
        'url': location.href,
    };
    $.ajax({
        url: "/addCol",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            pic.src = "/static/images/bky.png";
            var c1 = document.getElementById('col_span');
            c1.innerText = parseInt(c1.innerText) + 1

        } else if (ret['isSuccess'] == 9) {
            layer.msg('已收藏');
        } else {
            layer.msg("收藏失败")
        }
    })

}

function CommentThis() {
    var params = {
        "comment": $(".InputIComment").val(),
        "url": location.href
    };

    if (isEmpty(params['comment'])) {
        // window.alert(params['username']);
        window.alert("评论不能为空");
        return;
    }

    $.ajax({
        url: "/comment_submit",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            // $("#show").attr('value',+ ret['f'] +);
            window.location.reload();
            layer.msg('上传成功');
        } else {
            layer.msg('上传失败');
        }
    })

}


function SubmitBlog() {
    var video_name = getInnerVideo();
    var params = {
        "url": document.getElementById('Blog_logo').src,
        'title': $("#blog_title").val(),
        'content': $("#flask-pagedown-body").val(),
        'body_html': $("#flask-pagedown-body-preview").html(),
        'tag_id': $('#select_tag_blog option:selected').val(),
        'videos': video_name,
    };

    if (isEmpty(params['url'])) {
        alert("封面错误");
        return;
    } else if (isEmpty(params['title'])) {
        alert("标题不能为空");
        return;
    } else if (isEmpty(params['content'])) {
        alert("内容不能为空");
        return;
    } else if (isEmpty(params['tag_id'])) {
        alert("标签不能为空");
        return;
    }
    alert('文件上传中，请不要关闭或刷新界面!');
    $.ajax({
        url: "/blogSubmit",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            // $("#show").attr('value',+ ret['f'] +);

            window.location.href = '/blogs/' + ret['blog_id'];
            layer.msg('上传成功');

        } else {
            layer.msg('上传失败');
        }
    });


}

function DelBlog(blog_id, user_id) {
    var params = {
        "blog_id": blog_id,
        "user_id": user_id,
    };

    $.ajax({
        url: "/delBlog",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            window.location.reload();
            layer.msg("删除成功")
        } else if (ret['isSuccess'] == 5) {
            layer.msg('无法删除其他用户的博客');
        } else if (ret['isSuccess'] == 6) {
            layer.msg('博客不存在');
        } else {
            layer.msg("删除失败,未知错误")
        }
    })
}

function getInnerVideo() {
    var videos = document.getElementById('video_upload_table');
    var children = videos.children;
    var video_name = "";
    for (var i = 0; i < children.length; i = i + 2) {
        if (i != 0) {
            video_name = video_name + '\\'
        }
        var child = children[i].firstChild;
        video_name = video_name + child.innerText;
    }
    return video_name;

}

function ChangeBlog() {
    var video_name = getInnerVideo();
    var params = {
        "headUrl": document.getElementById('Blog_logo').src,
        'title': $("#blog_title").val(),
        'content': $("#flask-pagedown-body").val(),
        'body_html': $("#flask-pagedown-body-preview").html(),
        'url': location.href,
        'tag_id': $('#select_tag_blog option:selected').val(),
        'videos': video_name,
    };

    if (isEmpty(params['headUrl'])) {
        alert("封面错误");
        return;
    } else if (isEmpty(params['title'])) {
        alert("标题不能为空");
        return;
    } else if (isEmpty(params['content'])) {
        alert("内容不能为空");
        return;
    }
    alert('文件上传中，请不要刷新或关闭界面！');
    $.ajax({
        url: "/changeBlog",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            // $("#show").attr('value',+ ret['f'] +);
            window.location.href = '/blogs/' + ret['blog_id'];
            layer.msg('修改成功');
        } else if (ret['isSuccess'] == 1) {
            layer.msg('标题重复');
        } else if (ret['isSuccess'] == 6) {
            layer.msg('博客不存在');
        } else if (ret['isSuccess'] == 3) {
            layer.msg('标签不存在');
        } else {
            layer.msg('修改失败，未知错误');
        }
    })
}

function DelComment(user_id, comt_id) {
    var params = {
        "user_id": user_id,
        'comt_id': comt_id,
    };

    if (isEmpty(params['user_id'])) {
        alert("用户错误")
        return;
    } else if (isEmpty(params['comt_id'])) {
        alert("评论错误");
        return;
    }
    $.ajax({
        url: "/delComment",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            // $("#show").attr('value',+ ret['f'] +);
            window.location.reload()
            layer.msg('修改成功');
        } else if (ret['isSuccess'] == 5) {
            layer.msg('用户无权限');
        } else if (ret['isSuccess'] == 6) {
            layer.msg('博客不存在');
        } else {
            layer.msg('修改失败，未知错误');
        }
    })
}

function DelCollection(user_id, col_id) {
    var params = {
        "user_id": user_id,
        'col_id': col_id,
    };

    if (isEmpty(params['user_id'])) {
        alert("用户错误")
        return;
    } else if (isEmpty(params['col_id'])) {
        alert("评论错误");
        return;
    }
    $.ajax({
        url: "/delCol",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            // $("#show").attr('value',+ ret['f'] +);
            window.location.reload()
            layer.msg('修改成功');
        } else if (ret['isSuccess'] == 5) {
            layer.msg('用户无权限');
        } else if (ret['isSuccess'] == 6) {
            layer.msg('博客不存在');
        } else {
            layer.msg('修改失败，未知错误');
        }
    })
}

function SearchBlogKeyword() {
    var keyword = $('#InputSearch').val();
    var oUrl = location.href.toString();
    var url = location.href
    var re = eval('/(' + "keyword" + '=)([^&]*)/gi');

    oUrl = oUrl.replace(re, "keyword" + '=' + keyword);
    if (oUrl == url) {
        oUrl = oUrl + "/?keyword=" + keyword
    }
    location.href = oUrl;


}

function isEmpty(item) {
    if (item == '' || item == undefined || item == null) {
        return true;
    } else return false;
}


function MarkDown(data) {
    document.getElementById('blog_inner_text').innerHTML = data;
}

function VideoSubmit(url = 'videoSubmit') {

    var animateimg = $("#upload_video").val(); //获取上传的视频名 带//
    var imgarr = animateimg.split('\\'); //分割
    var myimg = imgarr[imgarr.length - 1]; //去掉 // 获取图片名
    var houzui = myimg.lastIndexOf('.'); //获取 . 出现的位置
    var ext = myimg.substring(houzui, myimg.length).toUpperCase();  //切割 . 获取文件后缀

    var file = $('#upload_video').get(0).files[0]; //获取上传的文件
    var fileSize = file.size;           //获取上传的文件大小
    var maxSize = 1048576 * 1024;              //最大1MB
    if (ext != '.MP4' && ext != '.AVI' && ext != '.MOV' && ext != '.MPG' && ext != '.MPEG') {
        parent.layer.msg('文件类型错误,请上传视频类型');
        return false;
    } else if (parseInt(fileSize) >= parseInt(maxSize)) {
        parent.layer.msg('上传的文件不能超过1MB');
        return false;
    } else {
        var data = new FormData();
        //获取文件内容
        data.append('video', $('#upload_video')[0].files[0]);
        // data.append('blog_id',blog_id);
        alert('文件上传中，请不要刷新或关闭界面！');
        $.ajax({
            url: "/" + url,
            type: 'POST',
            data: data,
            dataType: 'JSON',
            cache: false,
            processData: false,
            contentType: false
        }).done(function (ret) {
            if (!ret['isSuccess']) {
                // $("#show").attr('value',+ ret['f'] +);
                return myimg;
            } else {
                parent.layer.msg('视频上传失败');
                return false;
            }
        });
        return myimg;
    }


}

function UploadVideo() {
    var name = VideoSubmit('videoUpload')
    if (name) {
        var p = document.getElementById('video_upload_table');
        var tr = document.createElement('tr');
        var td1 = document.createElement('td');
        var td2 = document.createElement('td');
        var a = document.createElement('a');
        var url = location.href;
        var mystr = url.lastIndexOf('/');
        var blog_id = url.substring(mystr + 1, url.length);
        a.innerText = '删除';

        a.href = 'javascript:;';
        td1.appendChild(a);

        td2.innerText = name;
        tr.appendChild(td2);
        tr.appendChild(td1);
        tr.classList.add("highLightWord");
        p.appendChild(tr);
        a.onclick = function () {
            DelVideoByFilename(name, blog_id, a)
        };
    } else {
        parent.layer.msg('失败')
    }
}

function DelVideoById(video_id, node) {
    var params = {
        "video_id": video_id,
    };

    if (isEmpty(params['video_id'])) {
        alert("视频错误");
        return false;
    }
    $.ajax({
        url: "/delVideo",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            // $("#show").attr('value',+ ret['f'] +);
            // window.location.reload();
            var par = node.parentElement.parentElement;
            par.remove();
            layer.msg('修改成功');
        } else {
            layer.msg('修改失败，未知错误');
        }
    })
}

function DelVideoByFilename(filename, blog_id, a) {
    var params = {
        "filename": filename,
        'blog_id': blog_id,
    };

    if (isEmpty(params['filename'])) {
        alert("视频错误");
        return false;
    }
    $.ajax({
        url: "/delVideo",
        type: "post",
        data: params,
        dataType: "json",
    }).done(function (ret) {
        if (!ret['isSuccess']) {
            // $("#show").attr('value',+ ret['f'] +);
            // window.location.reload();
            var par = a.parentNode.parentNode;
            par.remove()
            layer.msg('修改成功');
        } else {
            layer.msg('修改失败，未知错误');
        }
    })
}



