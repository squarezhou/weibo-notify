新微博提醒GTalk机器人
===================

安装
---

1. 修改config_sample.ini为config.ini，并填写相关配置  
2. 导入weibo.sql到MySQL  
3. 运行init.py初始化数据  
4. 执行robot.py启动GTalk机器人  
5. 执行fetch.py启动微博机器人

使用
---

1. GTalk添加Robot（weibonotifyrobot@gmail.com）  
2. 发送命令（add/delete/list）到Robot，订阅微博账号  
3. Robot将在指定账号有新微博发表1分钟内通过GTalk给您提醒

---

**Powered By** 

- [python](http://www.python.org/)
- [pyxmpp](https://github.com/Jajcus/pyxmpp)
- [mysql](http://www.mysql.com/)
- [weibo api](http://open.weibo.com/)


**Change Log:** 

2012-11-19:  
> 修复MySQL超时自动断开BUG  
> 自动接受用户邀请  
> 限制订阅总数  
> 优化代码

2012-11-18:  
> 修改逻辑实现，不再抓取用户主页，改用机器人账号关注方式  
> 获取数据使用微博API代替网页抓取  
> 使用mysql代替sqlite3  
> 使用配置文件  
> 优化逻辑，减少网络请求

2012-11-17:  
> 修正Daemon下文件路径问题

2012-11-16:  
> 调通完善整个流程  
> robot.py、fetch.py Daemon化

2012-11-15:  
> 使用pyxmpp实现GTalk机器人自动管理订阅

2012-11-12:  
> 优化新微博判断  
> 使用pygtalkrobot发送微博通知  
> 改用pyxmpp发送微博通知

2012-11-11:  
> 项目初始化，完成微博主页抓取和解析
