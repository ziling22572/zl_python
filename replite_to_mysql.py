# coding = utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import json

'''读取excle'''
# import xlrd

'''写入excel数据(A1,A2....)'''
# from openpyxl import Workbook
# from openpyxl import load_workbook
'''从下标(0,0)'''
import xlwt
import xlsxwriter

# 引入自定义类
# from com.zl.replite import goods

'''
@author ziling 
@since 20201015
@desc 小商品爬虫案例参考
步骤1：通过url获取html/js源码（选取需要爬虫的商品类型，价格区间）
【例如 帽子，5-50：http://www.sphunpi.com/gallery--n,帽子_p,5,50-grid.html】（备注：帽子->中文编码转换 utf-8: content="text/html; charset=utf-8" ）
步骤2：解析url获取html的源码，然后解析源码获取对应的字段值,封装json数组
步骤3：通过excle写入【可以通过windows定时job每天抓最新的】路径；E:\python_job_excel\项目名\商品名称\日期\商品编号.xlxs（中文路径）
步骤4：通过mysql持久化到数据库（忽略）
'''


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


# 解析html,获取商品link
def prase_html(html_info, product_list):
    try:
        # 解析html代码
        bsObj = bs(html_info, "html.parser")
        pattern = re.compile("http://www.sphunpi.com/product-\d{5}.html")
        # imageList是存放img标签的列表--http://www.sphunpi.com/product-23623.html
        imageList = bsObj.findAll("a", {"href": re.compile(pattern)})
        for line in imageList:
            searchObj = re.search(r'http://www.sphunpi.com/product-\d{5}.html', str(line), re.M | re.I)
            if searchObj:
                # 获取子页面连接link
                # print(searchObj.group())
                product_list.append(searchObj.group())
    #     用非重复集合存储
    # arry = pattern.findall(str(imageList))
    # print(str(arry))
    # soup = bs(html_info, 'lxml')
    # 拉去标签<div class="items-gallery ">中的代码
    # print(soup.find_all('div', class_='items-gallery'))
    # for i in soup.select('a href'):
    #     print(str(i))
    # result_herf = soup.find_all('' + str(i), class_='entry-title');
    # 　　　　 print(result_herf)
    except Exception as e:
        print("异常信息：" + e)
    return product_list


# 解析商品-html,获取字段值
'''
商品名称 特色 商品编号 货号 计量单位 批发价 商品链接
'''


def prase_html_link(url, html_info):
    try:
        # 解析html代码
        bsObj = bs(html_info, "html.parser")
        pattern = re.compile("goods-action")
        # imageList是存放img标签的列表--http://www.sphunpi.com/product-23623.html
        imageList = bsObj.findAll("form", {"class": re.compile(pattern)})
        # print(str(imageList))
        # print(imageList)
        # 正则表达式匹配字段 用\"转义表示一个双bai引号。
        goodsname = re.search(r'<h1 class="goodsname">(.*)</h1>', str(imageList), re.M | re.I)
        goodsfeature = re.search(r'<p class="brief">(.*)</p>', str(imageList), re.M | re.I)
        goodscode = re.search(r'<ul class="goodsprops clearfix"> <li><span>商品编号：</span>(.*)</li><li><span>货　　号',
                              str(imageList), re.M | re.I)
        goodshh = re.search(r'<span id="goodsBn">(.*)</span></li>', str(imageList), re.M | re.I)
        goodsprice = re.search(r'<span class="price1">(.*)</span> </li>', str(imageList), re.M | re.I)
        # goods_image_link = re.search(r'small:(.*),big:', str(imageList), re.M | re.I)
        print("商品链接：" + url)
        if goodsname:
            goodsname = goodsname.group().replace("<h1 class=\"goodsname\">", "").replace("</h1>", "")
            print("商品名称：" + goodsname)
        if goodsfeature:
            goodsfeature = goodsfeature.group().replace("<p class=\"brief\">", "").replace("</p>", "")
            print("商品特色：" + goodsfeature)
        if goodscode:
            goodscode = goodscode.group().replace("<ul class=\"goodsprops clearfix\"> <li><span>商品编号：</span>",
                                                  "").replace("</li><li><span>货　　号", "")
            print("商品编号：" + goodscode)
        if goodshh:
            goodshh = goodshh.group().replace("<span id=\"goodsBn\">", "").replace("</span></li>", "")
            print("货　　号：" + goodshh)
        if goodsprice:
            goodsprice = goodsprice.group().replace("<span class=\"price1\">", "").replace("</span> </li>", "")
            print("厂批发价：" + goodsprice)
        # Python 字典类型转换为 JSON 对象
        data1 = {
            'goodsname': goodsname,
            'goodsfeature': goodsfeature,
            'goodscode': goodscode,
            'goodshh': goodshh,
            'goodsprice': goodsprice,
            'url': url
        }
        json_str = json.dumps(data1)
        print("Python 原始数据：", repr(data1))
        print("JSON 对象：", json_str)
        # 插入集合
        goodinfos.append(json_str)
        # if goods_image_link:
        #     goods_image_link = goods_image_link.group().replace("{small:", "").replace(",big:", "")
        #     print("图片链接：" + goods_image_link)

    except Exception as e:
        print("异常信息" + str(e))


# print("===========================================================================================>\r")


# 获取子页面html信息
def request_from_link(url, headers):
    # print(spider(url, headers))
    prase_html_link(url, spider(url, headers))


# 生产excle
def take_goods_to_excel(goodinfos):
    # pass
    # 创建excle \\代表/
    # mywb = Workbook("E:\\python_job_excel\\sphunpi\hat\\"+ str(time.strftime("%Y_%m_%d", time.localtime()))+".xlxs")
    mywb = xlsxwriter.Workbook(r'E:\python_job_excel\hat.xlsx')
    sheet1 = mywb.add_worksheet(name=str(time.strftime("%Y_%m_%d", time.localtime())) + "_sphunpi_hat")
    # 定义excle头字段
    sheet1.write(0, 0, '物品序号')
    sheet1.write(0, 1, '物品名称')
    sheet1.write(0, 2, '特色相关')
    sheet1.write(0, 3, '物品编码')
    sheet1.write(0, 4, '物品货号')
    sheet1.write(0, 5, '厂批发价')
    sheet1.write(0, 6, '商品链接')
    # // index表示这是第几张工作表，从零开始；，title是工作表的名字
    # mywb.create_sheet(index=0, title='sphunpi_hat')
    # sheet = mywb.active;  # 获取初始的sheet
    # row = 1;  # 单元格的行从0开始
    # row1 = 2;
    # col = 65;#单元格的列 从 'A' 开始
    # i=1;
    # sheet[chr(col) + str(row)] = "goodslinenum"
    # sheet[chr(col + 1) + str(row)] = "goodsname"
    # sheet[chr(col + 2) + str(row)] = "goodsfeature"
    # sheet[chr(col + 3) + str(row)] = "goodscode"
    # sheet[chr(col + 4) + str(row)] = "goodshh"
    # sheet[chr(col + 5) + str(row)] = "goodsprice"
    # sheet[chr(col + 6) + str(row)] = "url"
    i = 0;
    for js_str in goodinfos:
        i += 1;
        # 将 JSON 对象转换为 Python 字典
        data2 = json.loads(js_str)
        print("data2['goodsname']: ", data2['goodsname'])
        sheet1.write(i, 0, str(i))
        sheet1.write(i, 1, str(data2['goodsname']))
        sheet1.write(i, 2, str(data2['goodsfeature']))
        sheet1.write(i, 3, str(data2['goodscode']))
        sheet1.write(i, 4, str(data2['goodshh']))
        sheet1.write(i, 5, str(data2['goodsprice']))
        sheet1.write(i, 6, str(data2['url']))
    mywb.close();


if __name__ == '__main__':
    # 物品名称
    item_name = "帽子";
    # 价格区间从,价格区间至
    price_from, price_to = 5, 50;
    # 爬虫页数(测试爬取一页)
    page_size = 1
    # 排序方式(新旧发布：1，旧新发布：2，价格由低到高：3，价格由低到高：4)
    order_no = 4
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
# 实时动态网页url，爬取前9页
for i in range(page_size):
    sph_url = "http://www.sphunpi.com/gallery--n," + item_name + "_p," + str(price_from) + "," + str(
        price_to) + "-" + str(order_no) + "--" + str(i) + "--grid.html";
    print("爬虫开始,URL:[" + sph_url + "]------------------------" + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                               time.localtime()));
    # 获取html
    html_info = spider(sph_url, headers)
if html_info != None:
    # print(html_info)
    # print("==========================================================\r\n")
    # 解析获取有用的商品超链接集合
    product_list = []
product_list_url_link = prase_html(html_info, product_list)
goodinfos = []
for i in range(int(product_list_url_link.__len__() / 3)):
    # print("商品链接index_" + str(i + 1) + ",url=" + product_list_url_link[3 * i])
    # print("子商品链接数==>:" + product_set.__len__())
    # if product_list_url_link != None:
    #     print(product_list_url_link.__len__())
    #     循环去捞每个子页面里面的有用的数据到Excel或者存储到数据库中
    print("爬取第" + str(i + 1) + "个商品开始...")
    request_from_link(product_list_url_link[3 * i], headers)
# 将 JSON 对象转换为 Python 字典
# for js_str in goodinfos:
#     data2 = json.loads(js_str)
#     print("data2['goodsname']: ", data2['goodsname'])
take_goods_to_excel(goodinfos)
print("======================>ok")
