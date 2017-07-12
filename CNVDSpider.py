#coding:UTF-8
import logging
import urllib
from urllib import request

import bs4
import re
from bs4 import BeautifulSoup
from pymysql import NULL

import sys
sys.path.append('/path/to/your/module')

import MysqlSQLalchemy
import Webdriver
from config import Config


class getCNVD():
    def __init__(self):
        self.mysqlSQLalchemy = MysqlSQLalchemy.MysqlSQLalchemy()
        self.header = Config().header
        self.data = []

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler('cnvd.log')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        # logging.basicConfig(filename='cnvd.log',
        #                     level=logging.INFO,
        #                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        #                     datefmt='%a, %d %b %Y %H:%M:%S',
        #                     filemode='w')
        # self.logger = logging.getLogger('cnvd.log')

    def getUrls(self,num):
        Max_Num = 10
        urls = []
        self.logger.info("开始页面%s",str(num))
        start_url = "http://ics.cnvd.org.cn/?max=20&offset="+str(num)

        req = request.Request(start_url, headers=self.header)
        for i in range(Max_Num):
            try:
                resp = request.urlopen(req)
                break
            except urllib.error.URLError as e:
                if e.code == 500:
                    if i < Max_Num:
                        continue
                    else:
                        print("10次之后还是失败")
                        self.logger.info(start_url + " : 10次之后还是失败")
                else:
                    print("获取URL页面错误：" + e.code)
                    return
        content = resp.read()
        # print(content)
        # content = Webdriver.Webdriver().getPage_source(start_url)

        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        result = soup.findAll('td', style="text-align:left;padding-left:10px;")
        print(start_url, " 页面获取到的url个数: ", len(result))
        self.logger.info(start_url, " 页面获取到的url个数: ", len(result))
        for i in result:
            urls.append(i.a['href'])
        return urls

    def getDate(self, url):
        content = Webdriver.Webdriver().getPage_source(url)
        soup = BeautifulSoup(content, "html.parser", from_encoding='UTF-8')

        Webdriver.Webdriver().close()

        chname = soup.find('div', class_='blkContainerSblk').h1.getText()
        messageResult = {}
        messageResult['chname'] = chname
        HtmlTable = soup.findAll("table", class_="gg_detail")
        result2 = HtmlTable[0].tbody

        TRlist = result2.findAll('tr')
        for trlist in TRlist:
            if trlist.td.string == "影响产品":
                impact_productSum = ''
                if "影响产品" not in messageResult:
                    messageResult["impact_product"] = []
                for td in trlist.td.next_siblings:
                    if type(td) == bs4.element.Tag:
                        for k in td:
                            impact_product = ''
                            if type(k) == bs4.element.Tag:
                                impact_product = re.sub("(\t|\n|\r|\040)*", "", k.getText())
                            else:
                                impact_product = re.sub("(\t|\n|\r|\040)*", "", k.string)
                            if impact_product != "":
                                if impact_productSum == '':
                                    impact_productSum = impact_product
                                else:
                                    impact_productSum = impact_productSum + ',' + impact_product

                messageResult['impact_product'].append(impact_productSum)
            else:
                name = trlist.td.string;
                if name in Config.vul_list:
                    codename = Config.vul_list[name]
                    for td in trlist.td.next_siblings:
                        if type(td) == bs4.element.Tag:
                            tdText = re.sub(r"(\r|\t|\n|\040)*", "", td.getText())
                            if len(tdText):
                                if codename in messageResult:
                                    messageResult[codename].append(tdText)
                                else:
                                    messageResult[codename] = tdText
                else:
                    self.logger.warning("未收入的标签：%s", name)
        for name in Config.vul_list:
            if Config.vul_list[name] not in messageResult:
                messageResult[Config.vul_list[name]] = NULL
        self.mysqlSQLalchemy.CNVD_insert(messageResult)

    # 判断是否是已经爬过的信息
    # 即判断cnvd-id是否存在
    def isExist(self, cnvd_id):
        list = self.mysqlSQLalchemy.CNVD_selectBycnvdId(cnvd_id)
        if len(list) == 1:
            return True # 表示存在该条信息
        elif len(list) == 0:
            return False # 表示不存在该条信息
        else:
            print("查询出错")
            return

    def getPageNum(self):
        content = Webdriver.Webdriver().getPage_source("http://ics.cnvd.org.cn/")
        soup = BeautifulSoup(content, "html.parser", from_encoding='UTF-8')
        step = soup.findAll("a", class_="step")
        pageNum = step[len(step)-1].get_text()
        return int(pageNum)

    # 爬取全部信息
    def spiderAll(self):
        pageNum = self.getPageNum()
        # 从最后一页开始爬取
        for i in range(pageNum)[::-1]:
            urls = self.getUrls(i*20)
            for url in urls:
                u = url.split("/")
                cnvdId = u[len(u)-1]
                if self.isExist(cnvdId) == False:
                    self.getDate(url) # 不存在该信息则获取并插入


    # 更新数据
    # 存在的问题：如果在未更新完的情况下程序被终止时才重新运行更新数据 这会丢失中间的一些数据
    def update(self):
        pageNum = self.getPageNum()
        # 从第一页开始更新数据
        for i in range(pageNum):
            urls = self.getUrls(i * 20)
            for url in urls:
                u = url.split("/")
                cnvdId = u[len(u) - 1]
                if self.isExist(cnvdId) == False:
                    self.getDate(url)  # 不存在该信息则获取并插入
                elif self.isExist(cnvdId) == True:
                    return # 存在该信息 则退出
