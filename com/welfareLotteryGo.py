'''
Welfare Lottery 双色球爬取2003->至今
'''
# coding = utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import json
import pymysql


# 解析html,获取商品link
def prase_html(html_info):
    try:
        # 解析html代码
        bsObj = bs(html_info, "html.parser")
        nameList = bsObj.findAll("tr")
        for name in nameList:
            if (str(name).__contains__("<td class=\"th\"")):
                continue
            prase_info_tolink(str(name))
    except Exception as e:
        print("异常信息：" + e)


# 解析,获取字段值
'''
number	    bigint	11	0	True		主键
qihao	    varchar	255	0	True		期号
date	    varchar	255	0	False		开奖时间
result	    varchar	255	0	False		双色球开奖结果
detailurl	varchar	255	0	False		开奖记录url彩票开奖公告		

'''


def prase_open_html(html_url):
    try:
        html_link_info = spider(html_url, headers)
        prase_info_todb(html_link_info, html_url)
    except Exception as e:
        print("异常信息：" + e)


def prase_info_todb(html_info, html_url):
    try:
        # 解析html代码
        bsObj = bs(html_info, "html.parser")
        pattern = re.compile("result_con")
        pattern1 = re.compile("kj_num")
        info = bsObj.findAll("div", {"class": re.compile(pattern)})
        numberinfo = re.search(r'<p>双色球第(.*)期开奖结果</p>', str(info), re.M | re.I)
        number = numberinfo.group().replace("<p>双色球第", "").replace("期开奖结果</p>", "")
        qihao = numberinfo.group().replace("<p>", "").replace("</p>", "")
        dateinfo = re.search(r'<p>开奖时间：(.*)</p>', str(info), re.M | re.I)
        date = dateinfo.group().replace("<p>开奖时间：", "").replace("</p>", "")

        imageList = bsObj.findAll("div", {"class": re.compile(pattern1)})
        result = ""
        for item in imageList:
            img = str(item).replace("<div class=\"kj_num\">", "").replace("<img alt=\"\" src=\"js/kj_js_css/img/",
                                                                          "").replace(".png\">", "").replace(".png\"/>",
                                                                                                             "").replace(
                "</img></img></img></img></div>", "").replace("\n", ",")
            listimage = img.split(",")
            # print(listimage)
            result = handle(listimage)
        res = str(result).replace(", 7)", "").replace("(", "")
        print(number + "--" + qihao + "--" + date + "--" + res)
        excute_sql = "INSERT INTO welfarelottery (number, qihao, date, result, detailurl, createtime, updatetime)VALUES('" + number + "','" + qihao + "','" + date + "'," + res + ", '" + html_url + "', SYSDATE(), SYSDATE() )"
        dosql(excute_sql)

    except Exception as e:
        print("异常信息：" + e)


def handle(listimage):
    nums = ""
    try:
        for index in range(len(listimage)):
            # if (str(listimage[index]) == ""):
            #     continue
            if (index == (len(listimage) - 1)):
                nums += "'" + str(listimage[index]) + "'"
            # for  item in listimage:
            else:
                nums += "'" + str(listimage[index]) + "',"
        return getinfofromsql(nums)
    except Exception as e:
        print("异常信息：" + e)


def dosql(excute_sql):
    conn = pymysql.connect(host="localhost", user="root", password="root", database="ziling_api", charset="utf8")
    # 连接database
    cursor = conn.cursor()
    try:
        print(excute_sql)
        # print("执行db:=====>" + sql)
        cursor.execute(excute_sql)
        # 提交到数据库执行
        conn.commit()
        print("---------插入成功------------")
    except Exception as e:
        print("异常信息：" + e)
        conn.rollback()
    finally:
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()


def delete_mysql():
    conn = pymysql.connect(host="localhost", user="root", password="root", database="ziling_api", charset="utf8")
    # 连接database
    cursor = conn.cursor()
    try:
        excute_sql = "delete from welfarelottery"
        # print("执行db:=====>" + sql)
        cursor.execute(excute_sql)
        # 提交到数据库执行
        conn.commit()
        print("---------删除成功------------")
    except Exception as e:
        print("异常信息：" + e)
        conn.rollback()
    finally:
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()


def getinfofromsql(nums):
    conn = pymysql.connect(host="localhost", user="root", password="root", database="ziling_api", charset="utf8")
    # 连接database
    cursor = conn.cursor()
    try:
        # 定义要执行的SQL语句
        sql = "select GROUP_CONCAT(a.number),count(*) as size from welfarelotterypnginfo a where a.pngnumber in (" + str(
            nums) + ")"
        # print("执行db:=====>" + sql)
        cursor.execute(sql)
        # 获取结果
        results = cursor.fetchall()
        # print(results.__getitem__(0))
        return results.__getitem__(0)
    except Exception as e:
        print("异常信息：" + e)
    finally:
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()


# 解析url获取html
def spider(url, headers):
    try:
        if url != None:
            r = requests.get(url=url, headers=headers)
            html = r.text
            # print(html)
            if r.status_code != 200:
                print("异常！" + str(r.status_code))
                return None
            else:
                # print("成功连接url")
                return html
    except ValueError:
        print("URL不能为空！")


def prase_info_tolink(html_info):
    try:
        # 解析html代码
        bsObj = bs(html_info, "html.parser")
        imageList = bsObj.findAll("a", {"target": "_blank"})
        for name in imageList:
            if (str(name).__contains__("双色球开奖结果第")):
                continue
            prase_open_html(str(name).replace("\" target=\"_blank\">开奖记录</a>", "").replace("<a href=\"", ""))
    except Exception as e:
        print("异常信息：" + e)


if __name__ == '__main__':
    # 从第一页1-200页【目前最大133】
    maxpage = 133
    # 封装代理请求报文头Request Header，不然会403
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=1752a704362300-0d31194b55a3e9-f7b1332-144000-1752a70436358f; CNZZDATA80623485=cnzz_eid%3D791043234-1602733251-%26ntime%3D1602733251; bdshare_firstime=1602734801902; JS_SESSIONID=4qdbcg7hrj58wb5r2y5c3smkq68u2ols',
        # 'Host': 'www.sphunpi.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    # 爬虫前先清除历史数据
    delete_mysql()
    # 实时动态网页url
    for i in range(maxpage):
        sph_url = "https://www.cjcp.com.cn/kaijiang/ssqmingxi_" + str(i + 1) + ".html";
        print(
            "爬虫开始,第【" + str(i + 1) + "】页，URL:[" + sph_url + "]-->" + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                   time.localtime()));
        # 获取html
        html_info = spider(sph_url, headers)
        if html_info != None:
            prase_html(html_info)

    print("======================>ok")
