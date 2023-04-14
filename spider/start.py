# 姓名：刘爱婧
# 开发时间：2023/3/5 10:48
from scrapy import cmdline

cmdline.execute('scrapy crawl getspider'.split())  #getmenu应该换成自己创建的爬虫器名称，我上面创建的爬虫器名称是getmenu

