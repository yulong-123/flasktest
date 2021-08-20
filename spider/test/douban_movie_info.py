import csv
import pymysql
import requests
import re
from lxml import html
import time
import urllib3
from requests.adapters import HTTPAdapter

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 "
                  "Safari/537.36 "
}
# 登录cookie
cookies = {
    'cookie': 'bid=6FCmhKNa1w4; _pk_id.100001.4cf6=ceb7fbafd88cc5a3.1628004712.4.1628351691.1628349206.; '
              '__utma=30149280.938933265.1628004713.1628347555.1628351667.4; '
              '__utmz=30149280.1628351667.4.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
              '__utma=223695111.2907145.1628004713.1628347555.1628351667.4; '
              '__utmz=223695111.1628351667.4.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
              'll="118171"; __utmc=30149280; __utmc=223695111; '
              '__gads=ID=3079da3ba023265b-221fbb33b4ca00ea:T=1628227315:RT=1628227315:S=ALNI_MaAmvAbbApoQUiZY2TZl0zb'
              '-Z7IWA; _vwo_uuid_v2=DD248B2E2CCFE8C81933C50AA7E69DB54|91b6eb559712f54f614adc4058fcfc80; ct=y; '
              '__yadk_uid=j2GbBBO2b7ZOS9L5vXWhHp4mqMHHVsKW; ap_v=0,6.0; dbcl2="243865833:P/TAfzu+YFg"; ck=kCXi; '
              '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1628351666%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; '
              '_pk_ses.100001.4cf6=*; __utmb=30149280.0.10.1628351667; __utmb=223695111.0.10.1628351667; '
              'push_noty_num=0; push_doumail_num=0 '
}


# 设置代理池
def get_proxy():
    # 5000：settings中设置的监听端口，不是Redis服务的端口
    return requests.get("http://127.0.0.1:5000/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5000/delete/?proxy={}".format(proxy))


# 读取电影url
urls = []
with open('豆瓣电影链接.csv', 'r') as f:
    reader = csv.reader(f)
    urls = [row[0] for row in reader]

for i in range(0, len(urls)):
    url = urls[i]
    time.sleep(1)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    s.keep_alive = False
    # 请求页面
    urllib3.disable_warnings()
    retry_count = 5
    proxy = get_proxy().get("proxy")
    print(proxy)
    while retry_count > 0:
        try:
            r = requests.get(url=url, headers=headers, timeout=5, cookies=cookies, verify=False,
                             proxies={"http": "http://{}".format(proxy)})
            etree = html.etree
            selector = etree.HTML(r.text)

            # 获取电影名称
            moviename = []
            try:
                moviename = selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0]  # 电影名
                if moviename == "":
                    moviename = None
            except Exception as e:
                moviename = None
            print("moviename :{}".format(moviename))

            # 获取电影评分
            score = []
            try:
                score_list = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
                score = score_list[0].replace("\t", "").replace("\n", "")
                if score == "":
                    score = None
            except Exception as e:
                score = None
            print("score :{}".format(score))

            # 获取电影上映时间
            showtime = []
            try:
                st = selector.xpath('//*[@id="content"]/h1/span[2]/text()')[0]  # 上映日期
                showtime = st.replace("(", "").replace(")", "")
                if showtime == "":
                    showtime = None
            except Exception as e:
                showtime = None
            print("time :{}".format(showtime))

            # 获取电影片长
            mins = []
            try:
                mins_list = re.findall('片长:</span>.*?>(.*?)</span>', r.text, re.S)  # 片长
                mins = mins_list[0].replace(' ', '').replace('分钟', '')
                if mins == "":
                    mins = None
            except Exception as e:
                mins = None
            print("mins :{}".format(mins))

            # 获取电影类型
            genres_list = []
            try:
                genres_list = re.findall('<span property="v:genre">(.*?)</span>', r.text, re.S)
                genres_list = '/'.join(genres_list)
                if genres_list == "":
                    genres_list = None
            except Exception as e:
                genres_list = None
            print("genres_list :{}".format(genres_list))

            # 获取电影制片地区
            area_list = []
            try:
                area_list = re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>', r.text, re.S)
                area_list = '/'.join(area_list).replace(' ', '')
                if area_list == "":
                    area_list = None
            except Exception as e:
                area_list = None
            print("area_list :{}".format(area_list))

            # 获取电影导演
            directors_list = []
            try:
                d_list = selector.xpath('//div[@id="info"]/span[1]/span[2]/a/text()')  # 导演
                if len(d_list) > 2:
                    for i in range(0, 3):
                        directors_list.append(d_list[i])
                else:
                    for j in range(0, len(d_list)):
                        directors_list.append(d_list[j])
                directors_list = '/'.join(directors_list)
                if directors_list == "":
                    directors_list = None
            except Exception as e:
                directors_list = None
            print("directors_list :{}".format(directors_list))

            # 获取电影编剧
            scriptwriters_list = []
            try:
                w_list = selector.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')  # 编剧
                if len(w_list) > 2:
                    for i in range(0, 3):
                        scriptwriters_list.append(w_list[i])
                else:
                    for j in range(0, len(w_list)):
                        scriptwriters_list.append(w_list[j])
                scriptwriters_list = '/'.join(scriptwriters_list)
                if scriptwriters_list == "":
                    scriptwriters_list = None
            except Exception as e:
                scriptwriters_list = None
            print('scriptwriters_list :{}'.format(scriptwriters_list))

            # 获取电影主演
            actors_list = []
            try:
                actors = selector.xpath('//*[@id="info"]/span[3]/span[2]')[0]  # 演员
                a_list = actors.xpath('string(.)').replace(' ', '').split('/')  # 标签套标签，用string(.)同时获取所有文本
                if len(a_list) > 2:
                    for i in range(0, 3):
                        actors_list.append(a_list[i])
                else:
                    for j in range(0, a_list):
                        actors_list.append(a_list[j])
                actors_list = '/'.join(actors_list)
                if actors_list == "":
                    actors_list = None
            except Exception as e:
                actors_list = None
            print('actors_list :{}'.format(actors_list))

            # 获取电影评价
            comments = []
            try:
                comments = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')[0]
                if comments == "":
                    comments = None
            except Exception as e:
                comments = None
            print("comments :{}".format(comments))

            # 获取IMDb
            IMDb = []
            try:
                # IMDb = re.findall('<span class="pl">IMDb:</span> (.*?)<br></div>', r.text, re.S)[0]
                IMDb = re.findall('<span class="pl">IMDb:</span> tt([0-9][\d]{4,8})', r.text, re.S)[0]
                IMDb = "tt" + IMDb
                if IMDb == "":
                    IMDb = None
            except Exception as e:
                IMDb = None
            print("IMDb :{}".format(IMDb))

            try:
                # 打开数据库连接
                conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test',
                                       charset='utf8')
                # 使用cursor方法创建一个游标
                cursor = conn.cursor()
                # # 执行sql语句
                query = 'insert into db_movies(url, moviename, score, showtime, genres, areas,' \
                        ' mins, directors, scriptwriters, actors, comments, IMDb) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                values = (
                    url, moviename, score, showtime, genres_list, area_list, mins, directors_list, scriptwriters_list,
                    actors_list, comments, IMDb)
                cursor.execute(query, values)
                # 提交之前的操作，如果之前已经执行多次的execute，那么就都进行提交
                conn.commit()
            except Exception as e:
                print(e)
                # 回滚
                conn.rollback()
            # 关闭cursor对象
            cursor.close()
            # 关闭数据库连接
            conn.close()
            break
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
