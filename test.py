from selenium import webdriver

browser = webdriver.Chrome()#打开浏览器
browser.get('https://www.baidu.com')#输入网址
print (browser.page_source)#打印网页的源码
browser.close()#关闭浏览器的该页面
