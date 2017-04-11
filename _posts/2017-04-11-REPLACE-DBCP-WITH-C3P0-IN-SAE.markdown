---
layout:     post
title:      "SAE建议用c3p0代替dbcp"
subtitle:   " \"新浪SAE使用数据库连接池的小结\""
date:       2017-04-11 09:53:00
author:     "Bran"
header-img: "/img/in-post/2017/04/2017-04-11 12345_c3p0.jpg"
catalog: true
tags:
    - dbcp
    - c3p0
    - SAE
---

> “题图 数据库连接c3p0 2017-04-11”

## 0x000 序

- - -
和同事一起给某老板写一套系统，他负责微信端开发，我负责后天系统前后端，微信接口。
花了大概两周把项目写好，我准备部署到新浪SAE上进行测试，也是方便微信端接口调用测试，这样可以不影响我本地后台管理系统代码的修改和升级。

项目上使用的dbcp数据库连接池，只做了最基本的配置
```
dbcp.driverClassName=com.mysql.jdbc.Driver
dbcp.url=jdbc:mysql://localhost:3306/eBaoDemo?useUnicode=true&characterEncoding=UTF-8
dbcp.username=root
dbcp.password=eBao1234
dbcp.initialSize=2
dbcp.maxActive=10
dbcp.maxIdle=3
dbcp.minIdle=2
```
但是测试时每隔一段时间数据库连接就会丢失，查了很多文档发现是SAE的问题。
SAE数据库默认wait timeout = 10s，而且不允许修改。
```
show  global  variables like  'wait_timeout';
```
也就是说在pool里申请了connection如果超过10s不使用，会自动断掉连接。
程序不知道连接以及断掉，仍然从pool里取得connection然后使用，会出现如如EOFException
```
root cause java.io.EOFException: 
	Can not read response from server. Expected to read before connection was unexpectedly lost. 	
	com.mysql.jdbc.MysqlIO.readFully(MysqlIO.java:3039)
```

## 0x001 方案

- - -

### 1 jdbc
不使用数据库连接池，直接使用jdbc，测试成功，但是服务器压力大。

### 2 设置testOnBorrow=true
取得对象时是否进行验证，检查对象是否有效，需要同时设置validationQuery=select 1，测试成功，同样服务器压力大。

### 3 设置 maxWait
参考相关网上文档，设置maxWait=8 < 10s，也就是数据库连接池最大等待时间比数据库连接等待时间稍微短点，测试时大部分成功，但是还是会出现连接失效的状况。

### 4 使用c3p0
设置c3p0的maxIdleTime=8 < 10s，测试成功，完美

```
c3p0.driverClass=com.mysql.jdbc.Driver
c3p0.jdbcUrl=jdbc:mysql://localhost:3306/eBaoDemo?useUnicode=true&characterEncoding=UTF-8
c3p0.user=root
c3p0.password=eBao1234
c3p0.initialPoolSize=5
c3p0.minPoolSize=5
c3p0.maxPoolSize=20
c3p0.maxIdleTime=8
```


## 0x002 总结

- - -

1. 文档的重要性，SAE文档里早就说明了这个问题（不吐糟SAE的问题）
2. 服务器部署及运维需要扎实的功底，想成为一名全面发展的技术人才，知识面必须广
3. 数据库连接池原理需要继续深入，在有限的实践条件下做无限的研究

