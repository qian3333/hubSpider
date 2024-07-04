import os
import sys
# 用来解决在cmd中运行无法导入ThreadPool包的问题
rootPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
file_path = ''
videoId_path = ''
download_path = ''
sys.path.append(rootPath)
import requests
import json
import parsel
import time
from hubSpider.spiders.ThreadPool import ThreadPool

class xhub():
    parse_count=0
    url_list = []
    cookies = ''
    headers = {
               "Cookie":cookies,
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
               }
    # def login_save_cookie(self):
    #     """
    #     登录并保存cookie到本地
    #     :return:
    #     """
    #     login_page = "https://www.xvideos.com/account"
    #
    #     headers = {
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #         "Connection": "keep-alive",
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Origin": "https://www.xvideos.com",
    #         "Referer": "https://www.xvideos.com/account",
    #         "Sec-Fetch-Dest": "document",
    #         "Sec-Fetch-Mode": "navigate",
    #         "Sec-Fetch-Site": "same-origin",
    #         "Sec-Fetch-User": "?1",
    #         "Upgrade-Insecure-Requests": "1",
    #         "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
    #         "Accept-Encoding": "gzip, deflate, br"
    #         }
    #
    #     login_page_response = requests.get(url=login_page, headers=headers)
    #     token = parsel.Selector(login_page_response.text).xpath("//input[@name='signin-form[csrf_token]']/@value").getall()
    #     url = 'https://www.xvideos.com/account'
    #     data = {"signin-form[votes]":"",
    #             "signin-form[subs]":"",
    #             "signin-form[post_referer]":login_page,
    #             "signin-form[csrf_token]":token,
    #             "signin-form[login]":self.login_email,
    #             "signin-form[password]":self.login_password}
    #     # 使用session发起post请求来获取登录后的cookie,cookie已经存在session中
    #     response = self.session.post(url=url, data=data)
    #     # 把cookie保存到文件中
    #     self.session.cookies.save()
    #     print(self.session.cookies)

    # def read_cookie(self):
    #     """
    #     读取cookie进入登录后的页面
    #     :return:
    #     """
    #     list=[]
    #     with open(file="cookies.txt",encoding="utf-8") as f:
    #         for i in f:
    #             list.append(i.strip("\n"))
    #     f.close()
    #     self.cookies=list[-1].split(": ")[-1]
    #     self.headers["Cookie"]=self.cookies

    def login_y_n(self):
        """
        判断用户是否已经登录，我们这里使用的方法是：找一个视频id，然后尝试下载这个视频，如果返回的结果是可以下载，那么就是登录了
        :return:
        """
        home_url="https://www.xvideos.com/"
        response_text=requests.get(url=home_url).text
        id=parsel.Selector(response_text).xpath("//div/@data-id").get()
        print("测试视频id【用于测试是否登录成功】："+id)
        url = 'https://www.xvideos.com/video-download/'+id
        response = requests.get(url = url,headers=self.headers,allow_redirects=False) # allow_redirects =False不允许重定向到登录页面
        if not response.text.__contains__("true"):
            return False
        else:
            print("登录成功！")
            return True

    def parse_url(self,url):
        id_list=[]
        title_list=[]
        html=requests.get(url=url,headers=self.headers).text
        id_list.extend(parsel.Selector(html).xpath("//div/@data-id").getall())
        title_list.extend(parsel.Selector(html).xpath("//div/p/a/@title").getall())
        print("已解析完页面："+url)
        self.parse_count+=1
        with open(videoId_path, mode="a",encoding='utf-8') as f:
            for i in range(0,len(id_list)):
                f.write(id_list[i]+"-"+title_list[i]+"\n")
                # print(id_list[i]+"-"+title_list[i])
        f.close()

    def download(self,id_string):
        url="https://www.xvideos.com/video-download/{video_id}/".format(video_id=id_string.split("-")[0])
        single_response = requests.get(url=url,headers=self.headers)
        json_result=json.loads(single_response.content)
        file_name=id_string.split("-")[1]
        print("开始下载:"+file_name)
        video=requests.get(url=json_result["URL"])
        with open(download_path + file_name+".mp4", mode='wb') as w_f:
            w_f.write(video.content)
            print("保存成功："+file_name)
        w_f.close()

    def parse_all(self,thread_num):
        pool=ThreadPool(thread_num)
        f=open(file_path,mode="r",encoding="utf-8")
        lines=f.readlines()
        total_num=len(lines)
        for i in lines:
            pool.run(func=self.parse_url,args=(i.strip("\n"),))
        pool.close()
        if total_num==pool.run_sum_time:
            print("待解析页面个数："+str(pool.run_sum_time))
        return total_num
        # return True

    def download_all(self,thread_num):
        pool = ThreadPool(thread_num)
        f = open(videoId_path, mode="r", encoding="utf-8")
        for i in f:
            pool.run(func=self.download, args=(i.strip("\n"),))
            # print(i)
        pool.close()

if __name__ == '__main__':
    xhub=xhub()
    file_flag=os.path.exists(videoId_path)
    if not file_flag:
        total_num = xhub.parse_all(20)
        print("." * 30 + "正在请求解析" + "." * 30)
        while True:
            if total_num == xhub.parse_count:
                break
            else:
                time.sleep(1)
    else:
        f_r = open(videoId_path,mode="r",encoding="utf-8")
        f_len =len(f_r.readline())
        f_r.close()
        if f_len == 0:
            total_num=xhub.parse_all(20)
            print("."*30+"正在请求解析"+"."*30)
            while True:
                if total_num==xhub.parse_count:
                    break
                else:
                    time.sleep(1)
    print("." * 30 + "解析已完成" + "." * 30)
    if xhub.login_y_n():
        xhub.download_all(20)
    else:
        print("登录失败，请自己准备cookie并填在16行处")


