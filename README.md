# 吃客行网站模仿

Web期末作业

## 使用

安装依赖:`pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/`

运行：
1. `export FLASK_APP=app.py`
2. `flask run --host=0.0.0.0`

后台运行: `nohup flask run --host=0.0.0.0 > myweb.log 2>&1 &`

访问:`http://localhost:5000`

## 需求分析

1. **登录/注册**
2. **文章管理**
3. **首页**
4. **探索页面**
5. **用户个人中心(用户文章管理,用户账户管理,用户信息管理)**
6. **发布菜品页面**
7. **评论功能**

## 技术选型

前端: 

- 三件套 HTML+CSS+JavaScript
- 组件库 BootStrap

后端:
- Python 3.10
- Flask(web框架)
- MySQL 5.7 

部署: 
-  Nginx+FastCGI
