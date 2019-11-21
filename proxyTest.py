import time

from selenium import webdriver
from browsermobproxy import Server

#browsermobproxy相当于是fiddler.专门抓网页请求用的.
# 1.程序开始,先把fiddler设个端口,启动fiddler.拿到proxy.
dict={'port':39999}
server = Server(r'/Users/hanxu/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy',options=dict)
server.start()
proxy = server.create_proxy()


#2.启动Chrome浏览器,把proxy设置进去
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(35)

#3.开始请求,在需要抓包的步骤后提醒proxy开始抓包,即new_bar
base_url = "https://dmp-test.mypaas.com.cn/login?returnUrl=https%3A%2F%2Fdmp-test.mypaas.com.cn%2Fdataview%2Fshare%2F39f1990e-664d-d4a4-f966-86b685b69c0a%3Fcode%3Dtest"
driver.get(base_url)
driver.find_element_by_xpath('//input[@id="login_account"]').send_keys("junlin")#填写账号密码
driver.find_element_by_xpath('//input[@id="login_password"]').send_keys("123")
time.sleep(2)
driver.find_element_by_xpath('//button[@id="login_btn"]').click()#登录
driver.find_element_by_xpath('//td[contains(text(), "第一")]').click()#点击第一事业部
proxy.new_har("kappa", options={'captureHeaders': True, 'captureContent': True})#准备抓请求
driver.find_element_by_xpath('//td[contains(text(), "第一")]')
time.sleep(5)
result = proxy.har


#4.对抓包结果进行分析,拿到想要的结果
for entry in result['log']['entries']:
    _url = entry['request']['url']#拿抓到的所有url
    print(_url)
    # 根据URL找到数据接口
    if "/data" in _url:#找到需要的url
        _response = entry['response']#拿该url的response
        _content = _response['content']['text']#取出response文本值
        # 获取接口返回内容
        print(_content.encode().decode('unicode_escape'))#response里中文Unicode乱码,转个码

#关闭fiddler,关闭浏览器.
server.stop()
driver.quit()
