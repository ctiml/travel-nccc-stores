from pyquery import PyQuery as pq
import urllib.request
import csv
import time
from converter import Converter

converter = Converter()

page = 1
count = 50
city = "007"
# 台北市 001
# 新北市 003
# 桃園市 007

host = 'http://travel.nccc.com.tw'
path = '/NASApp/NTC/servlet/com.du.mvc.EntryServlet'
url_template = host + path + '?' + 'Action=RetailerList&Type=GetFull&Request=NULL_NULL_NULL_{2}_NULL_NULL_NULL_NULL_NULL_0_{0}_{1}_0'

with open("data/{0}.csv".format(city), 'w') as csvfile:
    header = [
        '縣市名稱',
        '鄉鎮名稱',
        '行業別',
        '行業細項分類',
        '特約商店名稱',
        '電話',
        '地址',
        '簽約日',
        '預定解約日',
        '收單機構'
    ]
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(header)

    while True:
        print("page: {0}".format(page))
        resp = urllib.request.urlopen(url_template.format(page, count, city))
        d = pq(resp.read())
        links = d('table table table table td[align=center] a')
        if links.size() == 0:
            break

        for link in links:
            # import code; code.interact(local=locals())
            if link.text != '詳細內容':
                continue
            time.sleep(0.1)
            print("open {0}".format(link.attrib['href']))
            detail_url = host + link.attrib['href']
            detail = urllib.request.urlopen(detail_url)
            dd = pq(detail.read())
            trs = dd('table table table table tr')
            values = []
            for tr in trs:
                fonts = pq(tr).find('font')
                if fonts.size() < 2:
                    continue
                value = converter.t(fonts[1].text.strip())
                values.append(value)
            writer.writerow(values)
        page += 1
