#encoding: utf-8
"""
从国家统计局爬取行政区划信息
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from lxml import etree
import time,random


start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html'
base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/'
headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}


level_class = ['citytr', 'countytr', 'towntr', 'villagetr']


def get_url_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
    driver = webdriver.Chrome(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe", options=chrome_options)
    driver.get(url)  # 打开网页网页
    driver.implicitly_wait(10)  # 等待加载六秒
    return driver.page_source


def recursive_get(base_url, level, lst_father, fout):
    """
    递归的解析网页
    :param base_url: 当前页面的url
    :param level: 0,1,2,3,层级
    :param lst_father: 已经找到的层级列表
    fout: 写文件的句柄
    :return:
    """
    print('get...', base_url)
    time.sleep(0.15)
    class_name = level_class[level]

    try:
        resp = requests.get(base_url, headers=headers, verify=False)
        text = resp.text.encode('ISO-8859-1').decode('gbk')
        html = etree.HTML(text)
        trs = html.xpath(f"//tr[@class='{class_name}']")
    except Exception as e:
        print(e)
        text = get_url_selenium(start_url)
        html = etree.HTML(text)
        trs = html.xpath(f"//tr[@class='{class_name}']")

    if level == 3:
        # 最后一级，可以写入数据了
        for tr in trs:
            tds = tr.xpath("./td/text()")
            viliage_name = str(tds[2])
            item = lst_father + [viliage_name]
            print('get one ', item)
            fout.write('{}\t{}\t{}\t{}\t{}\n'.format(*item))
        return
    else:
        for tr in trs:
            tds = tr.xpath("./td")
            if len(tds) == 2:
                a = tds[1].xpath("./a")
                if len(a) == 1:
                    href = a[0].xpath('./@href')[0]
                    text = a[0].xpath('./text()')[0]
                    lst_father.append(str(text))
                    segs = base_url.split('/')
                    bbase = '/'.join(segs[0:-1]) + '/' + str(href)
                    recursive_get(bbase, level + 1, lst_father, fout)
                    lst_father.pop()


def get_province(fout):
    resp = requests.get(start_url, headers=headers, verify=False)
    try:
        text = resp.text.encode('ISO-8859-1').decode('gbk')
    except Exception as e:
        print(e)
        text = get_url_selenium(start_url)
    html = etree.HTML(text)
    tds = html.xpath('//tr[@class="provincetr"]/td')

    for i, td in enumerate(tds):
        a = td.xpath('./a')
        if len(a) == 1:
            href = a[0].xpath('./@href')[0]
            text = a[0].xpath('./text()')[0]
            lst_father = [str(text)]
            recursive_get(base_url + str(href), 0, lst_father, fout)



if __name__ == '__main__':
    output_fn = r'./data/xingzhengquhua.tsv'
    with open(output_fn, 'w', encoding='utf-8') as fout:
        get_province(fout)
