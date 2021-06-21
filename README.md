# python-COVID-19-data-visualization
这是我的毕业设计

这是一个从数据接口获得疫情数据，尔后对数据进行可视化后使用网页展示出来的项目。本项目已经上线运行，网址是[http://www.silyahuukou.cn:5000/picture](http://www.silyahuukou.cn:5000/picture)

文件中的`main1`，`main2`，`main3`分别是三个爬虫文件，分别负责从api接口获取数据，从网站爬取新闻标题，从api接口爬取用于疫情预测的数据

在file文件夹中有关于毕设的相关文件已经很清楚的对项目进行了较为详细的说明，在此不再敖述

## 使用方法

文件夹中是目前运行在ubuntu服务器中的项目文件的副本，想要在云服务器中运行代码，需要如下步骤

1. 对`main1`，`main2`，`main3`三个爬虫文件设置定时运行，以便获取最新数据
2. 安装`chorme`
3. 修改`main2`文件中`chormedriver`的路径为合适的路径

然后就可以运行
