import csv
import json
import time

import requests
import re

# 请求头
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

# 爬取豆瓣电视剧网址
# 获取电视剧详情页url
douban_tv_urls = []


def get_tv_url(url):
    try:
        num = 0
        while num < 1000:
            url1 = url + str(num)
            res = requests.get(url1, headers=header, cookies=cookies)
            json_str = res.content.decode('utf8')
            ret = json.loads(json_str)
            if str(ret) == "{'subjects': []}":
                break
            else:
                tv_urls = re.findall(r"'url': '(.*)', 'playable'", str(ret))
                for i in tv_urls:
                    if i in douban_tv_urls:
                        continue
                    else:
                        douban_tv_urls.append(i)
            num += 1
            time.sleep(2)
    except Exception as e:
        print(e)


# 保存详情页url到csv文件
def save_tv_url():
    try:
        for douban_tv_url in douban_tv_urls:
            with open("豆瓣电视剧链接.csv", "a+", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([douban_tv_url])
    except Exception as e:
        print(e)


def main():
    tv_tags = ['热门', '美剧', '英剧', '英剧', '韩剧', '日剧', '国产剧', '港剧', '日本动画', '综艺', '纪录片']
    for tag in tv_tags:
        url = "https://movie.douban.com/j/search_subjects?type=tv&tag="+tag+"&sort=recommend&page_limit=1&page_start="
        get_tv_url(url)
        print(tag+"获取完成")
        print("--------------")
    save_tv_url()


if __name__ == '__main__':
    main()
    print("保存完成")
    print("豆瓣电视剧url数量为："+str(len(douban_tv_urls)))
