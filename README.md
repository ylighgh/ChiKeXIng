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
2. **用户管理,文章管理**
3. **首页(展示菜品样式)**
4. **用户个人中心**
5. **发布菜品页面**
6. **关于我们/联系我们/隐私政策**

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