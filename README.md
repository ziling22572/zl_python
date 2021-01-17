# zl_python
Python爬虫相关
replite_to_mysql:个人测试注意事项：http://www.sphunpi.com
 1：当前版本python3
 2：使用前请先安装python环境
 3：使用过程中需要导入各种包（可以通过pip install命令或者使用pycharm软件）
requests
BeautifulSoup4
'''读取excle'''
# import xlrd
'''写入excel数据(A1,A2....)'''
# from openpyxl import Workbook
# from openpyxl import load_workbook
'''从下标(0,0)'''
import xlwt
import xlsxwriter
 
福利彩票双色球 https://www.cjcp.com.cn/kaijiang/ssqmingxi_132.html

# 打开数据库连接ip：username、password.schema
 conn = pymysql.connect(host="localhost", user ="root", password ="root", database ="ziling_api", charset ="utf8")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭数据库连接
db.close()

 # 执行SQL语句
    cursor.execute(sql)
    # 获取结果
    results = cursor.fetchall()
    print(results.__getitem__(0))
    print(results.__getitem__(1))
    print(results.__getitem__(2))
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
