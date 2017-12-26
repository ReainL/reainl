# 晨报新闻安装部署文档
##一.技术选型
1.requests作为爬虫程序处理网络请求的框架

2.Beautiful作为解析网页的dom解析器

3.数据库用postgresql,自动化测试工具使用的是谷歌浏览器的测试软件chromedriver

##二.开发环境
1.下载安装python3.4,debian8最新发行版自带python3.4版本，可通过在终端输入python3测试；若系统没有python3.4，使用以下命令安装:
```
# apt-get install python3.4
```
2.安装python包管理工具pip
```
# apt-get install python3-pip
```
3.下载安装pandas、python-dateutil、numpy、requests、bs4、selenium、psycopg2、lxml、tushare、forex_python、sqlalchemy包
```
# apt-get install python3-pandas
# pip3 install python-dateutil
# pip3 install numpy
# pip3 install requests
# pip3 install bs4
# pip3 install selenium
# pip3 install psycopg2
# pip3 install lxml
# pip3 install tushare
# pip3 install forex_python
# pip3 install sqlalchemy
```
4.下载谷歌浏览器,终端输入以下命令
```
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# dpkg -i google-chrome*; sudo apt-get -f install
```

下载与当前谷歌浏览器对应的chromedriver,下载地址如下(二选一)：
https://npm.taobao.org/mirrors/chromedriver/
http://chromedriver.storage.googleapis.com/index.html

谷歌浏览器对应的chromdriver版本：
http://blog.csdn.net/huilan_same/article/details/51896672

5.配置postgresql数据库
```
# apt-get install -y postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4 postgresql-server-dev-9.4
```
6. 安装postgresql图形化客户端
```
# apt-get install pgadmin3
```
##三.前期准备
1.创建数据库表：在pgadmin III使用如下表语句创建table 
	
新闻表：
```
CREATE TABLE public.news_cj(
        news_date character varying(20),
        spider_data timestamp,
        news_source text,
        news_type text,
        news text
);
```

|       字段名      |    字段说明    |
|      :----:      |    :-----:    |
|     news_data    |    新闻日期    |
|     spider_data  |    操作时间    |
|     news_source  |    新闻来源    |
|     news_type    |    新闻类型    |
|     news         |    新闻内容    |
2.晨报相关指数信息及涨跌幅数据库：middle_news_market会自动创建

|        字段名     |    字段说明    |
|       :----:     |    :-----:    |
|       code       |    指数代码    |
|       name       |    指数名称    |
|       change     |    涨跌幅      |
|       open       |    字段说明    |
|      preclose    |    开盘点位    |
|      close       |    收盘点位    |
|      high        |    最高点位    |
|      low         |    最低点位    |
|      volume      |    成交量(手)  |
|      amount      | 成交金额（亿元）|
3.美元指数信息表
```
CREATE TABLE public.stock_code (
        stock_time character(20),
        spider_data timestamp,
        stock_name bpchar(5) NULL,
        stock_price numeric(5,4) NULL,
        stock_applies numeric(5,4) NULL
);
```
|       字段名       |    字段说明    |
|      :----:       |    :-----:    |
|     stock_time    |    行情时间    |
|     spider_data   |   操作时间    |
|     stock_name    |    指数名称    |
|     stock_price   |    指数价格    |
|     stock_applies |    涨跌幅      |
##四、项目工程目录
系统各个模块之间的联系如下：

- common/pgutils.py:主要连接postgresql数据库
- db_init/morningdata.sql:主要是数据库建表语句
- config.py:调用配置文件
- index_read_time.py:主要是通过第三方包对相关指数信息及涨跌幅的信息进行采集
- new_cj.py:主要是对新浪财经及华尔街见闻进行数据采集
- settings.conf.template:主要是项目的一些配置文件模板,需拷贝至当前目录配置环境
- logging.conf.template:主要是项目的日志文件模板
- task_morning.sh:shell脚本执行程序


	