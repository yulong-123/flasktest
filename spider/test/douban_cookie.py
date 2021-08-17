from selenium import webdriver
import json
import time

web = webdriver.Firefox()
web.get('https://accounts.douban.com/passport/login?source=movie')
web.delete_all_cookies()  # 先删除cookies
time.sleep(30)  # 这个时间用于手动登录,扫码登录可以适当缩短这个等待时间
dictcookies = web.get_cookies()  # 读取登录之后浏览器的cookies
jsoncookies = json.dumps(dictcookies)  # 将字典数据转成json数据便于保存

with open('cookie.txt', 'w') as f:  # 写进文本保存
    f.write(jsoncookies)
print('cookies is ok')
