import json
import requests
import re
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.charts import Bar

# 待爬取豆瓣网址
url = "https://movie.douban.com/j/search_subjects?type=tv&tag=美剧&sort=recommend&page_limit=1&page_start="
# 防止反爬头部
header = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) "
                  "CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1 "
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
# 初始化num，rate_none
num = 0
rate_none = 0

all_rate = []
all_title = []
all_url = []
# 通过while循环一条一条爬取电影数据
with open("douban_movies.text", 'a+', encoding='utf8') as file:
    while num < 1000:
        url1 = url + str(num)  # url拼接
        res = requests.get(url1, headers=header, cookies=cookies)  # 通过request的get方法获取网址
        json_str = res.content.decode('utf8')  # 获取页面数据，并以utf格式展示
        ret = json.loads(json_str)  # 通过json转义
        # print(str(num + 1) + "\t" + str(res.status_code) + str(ret))  # 打印出状态码和一条电影数据
        # if...else判断是否为空（{'subjects': []}）
        if str(ret) == "{'subjects': []}":
            print("爬取结束")
            break
        # 否则添加数据到字典，并将num自增
        else:
            # 定义一个字典来存放豆瓣电影数据
            # 每次循环都将字典重置为空
            move = {}
            moves_rate = re.findall(r"(\d?\.\d+)", str(ret))  # 正则表达式获取电影评分
            # 将正则的列表格式转为数字格式
            for i in moves_rate:
                moves_rate = float(i)
            # print(moves_rate)
            # 判断评分是否为空
            if not moves_rate:
                num += 1
                rate_none += 1
                print(str(num) + "\t" + "rate为空")
                continue
            else:
                moves_title = re.findall(r"'title': '(.*)', 'url'", str(ret))  # 正则表达式获取电影名称
                for i in moves_title:
                    moves_title = str(i)
                # print(moves_title)
                moves_url = re.findall(r"'url': '(.*)', 'playable'", str(ret))  # 正则表达式获取电影链接
                for i in moves_url:
                    moves_url = str(i)
                # print(moves_url)
                # 添加到字典
                move['rate'] = moves_rate
                move['title'] = moves_title
                move['url'] = moves_url
                num += 1
                all_rate.append(moves_rate)
                all_title.append(moves_title)
                all_url.append(moves_url)
                # 写入douban_movies2.text文件
                file.write(str(move))
                file.write('\n')  # 写入换行
print(str(num + 1) + "\t" + str(res.status_code) + str(ret))
print("爬取条数：" + str(num))
print("评分为空数：" + str(rate_none))
print("有效条数：" + str(num - rate_none))
print(all_rate)
print(all_title)
print(all_url)

# 定义一个字典，用于计算次数
# data_count = []
#
#
# def ciyun(str, data_count):
#     data_count = []
#     num_count = {}
#     for i in str:
#         if i in num_count:
#             num_count[i] += 1
#         else:
#             num_count[i] = 1
#     # print(str)
#     # print(num_count)
#     for item in num_count.items():
#         data_count.append(item)
#     # print(data_count)


# ciyun(all_rate, all_rate)
# (
#     WordCloud().add(series_name="电影评分", data_pair=all_rate, word_size_range=[10, 100]).render("电影评分.html")
# )
#
# ciyun(all_title, all_title=[])
# (
#     WordCloud().add(series_name="电影名称", data_pair=all_title, word_size_range=[10, 100]).render("电影名称.html")
# )
# ciyun(all_url, all_url=[])
# (
#     WordCloud().add(series_name="电影链接", data_pair=all_url, word_size_range=[10, 100]).render("电影链接.html")
# )


bar = Bar()
bar.add_xaxis(all_title)
bar.add_yaxis("电影评分", all_rate)
bar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)))
bar.render()