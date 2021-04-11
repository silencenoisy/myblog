import requests
from datetime import datetime

post_data = {
    # 'id':"sss",
    'title':"555",
    'content':'内容',
    # 'index':1,
    # 'user_id':4,
    # 'done':0,
    # 'addtime':"2021-03-21 11:32:50",
    'deadline':"2021-04-10 11:32:56",
    # 'csrf_token':"IjE1YThjYTI2MTY3NjA1ZDUwZGZjZWMxMDkyMjNhOWY5ZGIyNTc0YzQi.YF8xFA.i5COq3cCGRrqGT_fTZvtJi3F4BA",
}

# print(bool(False))

# response = requests.post('http://127.0.0.1:5000/api/todo/add',post_data)
# response = requests.delete('http://127.0.0.1:5000/api/todo/delete?id=9')
# params = {
#     'num': 1,
#     'size':20,
#     'type':2,
    # 'key':'title',
    # 'value':'标',
# }
patch_data={
    'user_id':4,
}

headers={
    'Authorization':"JWT eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxNjkxMDU0NiwiZXhwIjoxNjE2OTE0MTQ2fQ.eyJpZCI6MTAwMDEwfQ.SD2YTu"
                    "NEtawtedye1Q6dOj3agabfoqh3CR10BGORF4xGY-SLe5ezdaK8br7seXW-LcJgott1vGPeTG3whNQ1jg",

}
post_data2={
    'username':'qqq',
    'password':'qqqqqq'
}
# url = 'http://47.99.169.188'
url = 'http://127.0.0.1:5000'
# response = requests.get(url+'/api/todo/4?page=1&per_page=2',headers=headers)
# response = requests.get(url+'/api/todo/undone?page=1&per_page=2',headers=headers)
# response = requests.get(url+'/api/todo/done?page=1&per_page=2',headers=headers)
# response = requests.get(url+'/api/todo?page=1&per_page=2',headers=headers)
# response = requests.patch(url+'/api/todo/change/undone',headers=headers)
# response = requests.delete(url+'/api/todo/delete/undone',headers=headers)
# response = requests.get(url+'/api/todo/search?keyword=4&page=1&per_page=2',headers=headers)
response = requests.get(url+'/api/todo/history')
# response = requests.post(url+'/api/todo/add',post_data,headers=headers)
# response = requests.post(url+'/api/login',post_data2)
# response = requests.get(url+'/api/index',headers=headers)
# response = requests.patch(url+'/api/todo/change/13/done',patch_data,headers=headers)
print(response.url)

if response.status_code==200 or response.status_code==201:
    print(response.json())
    # print(response.headers)
    # print(response.text)
else:
    print(response.status_code)


