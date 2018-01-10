# coding:utf-8

from lxml import etree
from urllib import request
import xlsxwriter
import time
from models import session,Qshi


class QiuSHi_Lxml:
    def __init__(self):
        self.page = 1
        self.endpage = 35
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        self.logo_list = []
        self.author_list = []
        self.content_list = []
        self.img_list = []
        self.logoPath = 'static/logoimgs/'
        self.imgPath = 'static/imgs/'
        self.filePath = 'static/qiushi.txt'
        self.xlsxPath = 'static/qiushi.xlsx'

    def get_html(self, url):
        req = request.Request(url=url, headers=self.headers)
        html_byte = request.urlopen(req)
        html = html_byte.read().decode('utf-8')
        return html

    def get_data(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        content = selector.xpath('//div[@id="content-left"]')
        logo_item = content[0].xpath('//div[@class="author clearfix"]/a[1]/img/@src|//div[@class="author clearfix"]/span/img/@src')
        author_item = content[0].xpath('//div[@class="author clearfix"]/a[1]/img/@alt|//div[@class="author clearfix"]/span/img/@alt')
        img_item = content[0].xpath('//div[@class="thumb"]/a/img/@src')
        content_span = content[0].xpath('//div[@class="content"]/span[1]')#过滤掉了<br>只有文本  ！！有<查看全文>的没有爬完  正确的应该爬取每个人的文章地址，进入然后爬取内容
        content_item=[]
        for i in content_span:
            content_item.append(i.xpath('string(.)'))

        for v in logo_item:
            self.logo_list.append(v)
        for v in author_item:
            self.author_list.append(v)
        for v in content_item:
            self.content_list.append(v)
        for v in img_item:
            self.img_list.append(v)

    def download_img(self,list,path):#下载图片
        for v in list:
            url='http:'+v
            img_str=str(v).rsplit('/',1)[1]
            name=path+img_str
            request.urlretrieve(url,name)
            time.sleep(0.5)
            print('------------------------------------------------------------')
            print('%s下载成功！'%img_str)
            print('------------------------------------------------------------')

    def storage_in_mysql(self):
        for v in range(0,len(self.logo_list)):
            name=self.author_list[v]
            content=self.content_list[v]

            logo_url=self.logo_list[v]
            logo_str=str(logo_url).rsplit('/',1)[1]
            logo=self.logoPath+logo_str

            img_url = self.img_list[v]
            img_str = str(img_url).rsplit('/', 1)[1]
            img = self.imgPath + img_str

            data = Qshi(name=name, logo=logo, content=content, img=img)
            session.add(data)
            session.commit()
            print('第%d条数据存储成功！'%v)
        session.close()

    def output_txt(self):
        f = open(self.filePath, 'w', encoding='utf-8')
        try:
            for v in range(0, len(self.logo_list)):
                f.write('头像地址' + self.logo_list[v] + '\r\n')
                f.write('用户名：' + self.author_list[v] + '\r\n')
                f.write('内容:' + self.content_list[v] + '\r\n')
                f.write('图片地址：' + self.img_list[v] + '\r\n\r\n')
                # print('文件写入成功...')
        finally:
            f.close()

    def output_xlsx(self):
        row = 1
        col = 0
        w = xlsxwriter.Workbook(self.xlsxPath)
        worksheet = w.add_worksheet(u"所有数据")
        worksheet.write("A1", u"头像地址")
        worksheet.write("B1", u'用户名')
        worksheet.write('C1', u'内容')
        worksheet.write('D1', u'图片地址')
        for v in range(0, len(self.logo_list)):
            worksheet.write(row, col, self.logo_list[v])
            worksheet.write(row, col + 1, self.author_list[v])
            worksheet.write(row, col + 2, self.content_list[v])
            worksheet.write(row, col + 3, self.img_list[v])
            row += 1
        w.close()

    """    
        row=0
        col=1
        x=xlsxwriter.Workbook(self.xlsxPath)
        worksheet=x.add_worksheet(u'所有数据')
        worksheet.write('A1',u'头像地址')
        worksheet.write('A2',u'昵称')
        worksheet.write('A3',u'内容')
        worksheet.write('A4',u'图片地址')
        for v in  range(0,len(self.logo_list)):
            worksheet.write(row,col,self.logo_list[v])
            worksheet.write(row+1,col,self.author_list[v])
            worksheet.write(row+2,col,self.content_list[v])
            worksheet.write(row+3,col,self.img_list[v])
            col+=1
        x.close()
    """

    def main(self):
        print('开始爬虫...')
        URL = 'https://www.qiushibaike.com/pic/page/' + str(self.page) + '/?s=5049862'
        while self.page <= self.endpage:
            self.get_data(URL)
            print('第%d页成功！'%self.page)
            self.page += 1
            time.sleep(1)
        # self.download_img(self.logo_list,self.logoPath)
        # self.download_img(self.img_list,self.imgPath)
        print(len(self.logo_list))
        # for v in self.logo_list:
        #     print(v)
        print(len(self.author_list))
        print(len(self.content_list))
        print(len(self.img_list))
        self.storage_in_mysql()
        # self.output_xlsx()
        print("爬取成功！")


Spider = QiuSHi_Lxml()
Spider.main()
