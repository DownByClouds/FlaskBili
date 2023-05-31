# Flask_BiliDOWNLOADER

用Flask构建一个B站视频解析网站。

## 使用Flask的原因

> 1.Flask:Flask扩展丰富，不臃肿，可自由选择组合各种插件，性能优越，相比其他的web框架十分的轻量级，设计哲学很优雅，易于学习，小型的项目快速的开发，大型的项目也没压力。非常的灵活。


## Flask特点
* 轻量级web应用框架
* WSGI工具箱采用Werkzeug
* 模板引擎采用Jinja2
* Flask使用BSD授权
* 微内核框架
   * 称为“microframework”,简单的核心，用extension添加其功能。
   * 没有默认的数据库，窗体验证工具。
   * 保留扩展的弹性，可用Flask-extension加入这些功能：ORM、窗体验证工具、文件上传、各种开放式身份验证技术。
   
## 本项目采用的技术
* post、get请求、请求异常处理；
* 模板自定义转义、定义过滤器、定义全局上下文处理器、Jinja2语法、包含继承、定义宏等；
* 使用Flask-wtf定义表单模型、字段类型、字段验证、视图处理表单、模板使用表单；
* Falsk-sqlalchemy定义数据库模型、添加数据、修改、查询、删除数据、数据库时间、数据迁移；


## 主要结构

**项目包含**：用户登录及注册 / 视频解析 / 历史记录查询



## 数据库设计

> 对于前台的模型有以下几个表：
* 用户（user）
* 提交记录（post）


其中的关系：

| 用户表（user）|          |
| ---------- | -----------|
| id   | 编号，整型，主键，自动递增   | 
| username   | 昵称，字符串型，唯一  | 
| password    | 密码，字符串型   |
| email  | 邮箱，字符串型，唯一   |

| 提交记录表（post） |              |
| id     | 编号，整型，主键，自动递增   |
| content   | 视频标题，字符串型，唯一   |
| timestamp| 添加时间，日期时间类型，默认为当前的时间   |
| user_id | 外键，关联用户模型   |



## 运行本项目

终端中输入：
```
python myblog.py runserver
```

## 界面截图
登录
![登录](..\app\static\img\login_ex.png)
注册
![注册](..\app\static\img\register_f.png)
主页
![主页](..\app\static\img\index_ex.png)













   
   
    


