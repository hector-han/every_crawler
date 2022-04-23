"""
全国农产品商务信息公共服务平台
从这个网站上爬取农产品价格
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time,random

# 鸡蛋
# url_template = 'http://nc.mofcom.gov.cn/channel/jghq2017/price_list.shtml?par_craft_index=13079&craft_index=13245&par_p_index=&p_index=&startTime={}&endTime={}'
# 苹果
url_template = 'http://nc.mofcom.gov.cn/channel/jghq2017/price_list.shtml?par_craft_index=13076&craft_index=13097&par_p_index=&p_index=&startTime={}&endTime={}'


def crawl_given_time_interval(startDate, endDate):
    global cur_page
    url = url_template.format(startDate, endDate)
    print("begin to craw url ", url)
    startTime = time.time()  # 获取开始时的时间
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
    driver = webdriver.Chrome(r"C:\software\chromedriver.exe", options=chrome_options)

    # option = webdriver.ChromeOptions()
    # option.add_argument('--proxy--server=112.84.55.122:9999')  # 使用代理IP

    driver.get(url)  # 打开网页网页
    driver.implicitly_wait(6)  # 等待加载六秒

    alert = driver.switch_to.alert  # 切换到alert
    # print('alert text : ' + alert.text) #打印alert的文本
    alert.accept()  # 点击alert的【确认】按钮
    validity = driver.find_element_by_xpath('//*[@id="formJghqIndex"]/div/input[1]')
    validity.clear()  # 清空输入框
    randomNumber = random.randrange(1000, 9999, 1)  # 随机生成一个四位数的验证码
    validity.send_keys(randomNumber)  # 输入随机验证码
    driver.find_element_by_xpath('//*[@id="formJghqIndex"]/div/input[2]').click() # 点击确定
    time.sleep(5)
    driver.implicitly_wait(5)
    html = etree.HTML(driver.page_source)
    select_pages = html.xpath("/html/body/section/div/div[1]/div[4]/a")
    select_pages = [p.text.strip() for p in select_pages] # [1,2,3,4,418,下一页]
    try:
        endpage = int(select_pages[-2])
    except IndexError as e:
        print(e)
        print(select_pages)
        raise e
    beginpage = cur_page
    print("开始爬取，起始页={}，结束页={}".format(beginpage, endpage))

    # 选择起始页
    search = driver.find_element_by_xpath('//*[@id="gotopage"]')  # 定位输入框节点
    search.clear()  # 清空搜索框
    search.send_keys(beginpage)  # 输入关键词
    driver.find_element_by_xpath('/html/body/section/div/div[1]/div[4]/input[2]').click()
    time.sleep(2)
    next_page(driver, beginpage, endpage, startDate, endDate)

    endTime = time.time()  # 获取结束时的时间
    useTime = (endTime - startTime) / 60
    driver.quit()  # 推出并关闭浏览器
    print("该次所获的信息一共使用%s分钟" % useTime)


# 点击下一页
def next_page(driver, beginpage, endpage, startDate, endDate):
    global cur_page
    for page in range(beginpage, endpage + 1, 1):
        cur_page = page
        print("~~~~~~~~~~正在爬取第%s页，一共有%s页~~~~~~~~~" % (page, endpage))
        get_html(driver, startDate, endDate)
        # 点击下一页
        driver.find_element_by_xpath('/html/body/section/div/div[1]/div[4]/a[last()]').click()
        time.sleep(1)


# 获取网页源码并解析
def get_html(driver, startDate, endDate):
    driver.implicitly_wait(10)
    source = driver.page_source  # 获取源代码
    html = etree.HTML(source)  # 使用lxml解析网页
    page_data = spider(html)
    saveData(page_data, startDate, endDate)


def spider(html):
    page_data = []
    for tr in html.xpath('/html/body/section/div/div[1]/table/tbody/tr'):
        time = tr.xpath('./td[1]/text()')
        if len(time) != 0:
            goods = tr.xpath('./td[2]/span/text()')[0]
            price = tr.xpath('./td[3]/span/text()')[0]
            unit = tr.xpath('./td[3]/text()')[0]
            market = tr.xpath('./td[4]/a/text()')[0]
            # link = 'http://nc.mofcom.gov.cn/' + tr.xpath('./td[4]/a/@href')[0]
            data = [time[0], goods, price, unit, market]  # 生成数组
            page_data.append(data)
    return page_data


def saveData(page_data, startDate, endDate):
    with open('./data/ap_{}_{}.csv'.format(startDate, endDate), mode='a', encoding='utf-8', newline='\n') as fout:
        for data in page_data:
            fout.write(','.join(data))
            fout.write('\n')


if __name__ == '__main__':
    dates = [a + '-' + b for a in ['2018', '2019'] for b in ['01', '04', '07', '10']]
    dates.insert(0, '2017-10')
    dates.append('2020-01')
    dates.append('2020-04')
    print(dates)
    length = len(dates)
    i = 0
    cur_page = 1
    while i < length - 1:
        startDate = dates[i] + '-02'
        endDate = dates[i+1] + '-01'
        try:
            crawl_given_time_interval(startDate, endDate)
            i += 1
            cur_page = 1
        except Exception as e:
            print(e)



