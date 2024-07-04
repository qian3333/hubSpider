原作者https://github.com/srx-2000/spider_collection/commits?author=srx-2000
由@qian333更新与2024/7/2
删除了自动登录功能并绕开recaptcha验证，修复了一些环境配置问题
**功能**

​	通过用户给出的关键词，爬取该关键词搜索到的所有的视频，并将这些视频以.mp4的的形式保存在本地电脑

​	**环境**

1. windows11
2. python3.7

​	**使用方法**

1. 首先需要一个可以带动整个电脑科学上网的vpn或机场**这个大家自己找一下哈**
2. 需要使用到的库已经放在requirements.txt，使用pip安装的可以使用指令`pip install -r requirements.txt`。如果国内安装第三方库比较慢，可以使用以下指令进行清华源加速`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`
3. 如果出现了scrapy库安装失败的问题可以尝试这个命令进行安装`pip install scrapy -i http://pypi.douban.com/simple --trusted-host pypi.douban.com`
4. 具备了以上两个条件之后，我们就可以进入`search_parser.py`文件中将`key`修改成你要搜索的内容即可，然后运行`search_parser.py`即可，在运行之后应该会在video目录下得到一个`video_url.txt`文件，里面就是搜索到的所有的与关键词相关的页面了。
5. 之后，我们只需要直接进入`downloader.py`文件，运行即可。此时会在控制台让你分别输入，邮箱和密码（没有xvideos网站账号的去网站注册一个就OK，免费的）。输入邮箱和密码后，首先会解析刚刚获取到的所有的页面，而后会逐个下载，下载的mp4文件会存在video目录下。

> **注意** 在spiders目录下会有一个`cookies.txt`文件，其中保存着你登录后留下的cookies，是下载视频的必须品，所以不要轻易删掉该文件。【暂时已弃用】

​	**技术栈**

1. requests
2. json
3. parsel（xpath筛选器）
4. os
5. cookiejar（模拟登陆保存cookies）【暂时删去】
6. scrapy（自动迭代）
7. time
8. contextlib
9. queue
10. threading

​	**debug**

1.请将downloader.py中的cookie替换成你自己的cookie
2.请将downloader.py中的path，替换成video_id.txt,video_url.txt以及你希望下载的地址
3.出现错误AttributeError: ‘AsyncioSelectorReactor‘ object has no attribute ‘_handleSignals‘请运行如下命令

# 删除最新版本Twisted
pip ubinstall Twisted
# 重新下载
pip install Twisted==22.10.0

4.出现requests.exceptions.SSLError: HTTPSConnectionPool问题报错请重新安装正确版本的cryptography以及opensll
-

