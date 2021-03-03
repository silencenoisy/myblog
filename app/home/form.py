from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm,Form
from wtforms import TextField,validators,SubmitField

class PageDownForm(Form):
    body = PageDownField(
        "博客内容",
        validators=[validators.DataRequired("内容不能为空")],
        render_kw={
            "class":"blog_data_pagedown",
            # "id":"blog_data_pagedowns",
        }
    )
    submit = SubmitField("上传")

    # def __init__(self,data):  # 每次实例化都会从数据库取一次   做带数据库和展示页面数据实时更新
    #     super(PageDownForm, self).__init__()
    #     self.data = data
    #
    #
    # def getText(self):
    #     if "content" in self.data:
    #         return self.data['content']