#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import timeunit
import bs4
from selenium import webdriver

#click test right now.判断一下,防止多次考试
def readyToTest(browser):
    readyTest = browser.find_element_by_xpath('//button[@type="submit"]')
    if '再次' not in readyTest.text:
        if '现在' in readyTest.text or '继续' in readyTest.text:
            readyTest.click()
            return 1
    return 0

def getAnswerElement(elements,neirong):
    for ele in elements:
        if neirong in ele.text:
            return ele

def getAnswerElementEquals(elements,neirong):
    for ele in elements:
        if neirong == ele.text:
            return ele

#start to answer.
def writeAnswer1(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "国家开放大学是一所与普通高校学习方式完全相同的大学")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "只有在面对面教学的课堂上才能完成学习任务")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    #接下来五个判断题,因为顺序不可能变,所以可写死,前面占了8个ratio,所以9,12,13,16,18
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[8].click()
    time.sleep(200)
    ratios[11].click()
    time.sleep(200)
    ratios[12].click()
    time.sleep(200)
    ratios[15].click()
    time.sleep(200)
    ratios[17].click()
    #end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer2(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "8")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "被评为优秀毕业生")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "专业综合实践")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "入学注册时")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "小学、初中")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    #接下来五个判断题,因为顺序不可能变,所以可写死,前面占了20个ratio,所以21,23,26,28,30
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[20].click()
    time.sleep(200)
    ratios[22].click()
    time.sleep(200)
    ratios[25].click()
    time.sleep(200)
    ratios[27].click()
    time.sleep(200)
    ratios[29].click()
    time.sleep(200)
    #end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(200)
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer3(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "www.ouchn.edu.cn")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[5].click()
    time.sleep(200)
    ratios[7].click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "毕业论文")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)

    #多选
    rightAnswer = getAnswerElement(elements1, "形成性考核")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "终结性考核")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "半开卷")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 闭卷")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 开卷")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "大学英语")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "计算机应用基础")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "身份证")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "学生证")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "准考证")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)


    #接下来五个判断题,因为顺序不可能变,所以可写死,前面占了20个ratio,所以13,16,17,20,22,24
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[12].click()
    time.sleep(200)
    ratios[15].click()
    time.sleep(200)
    ratios[16].click()
    time.sleep(200)
    ratios[19].click()
    time.sleep(200)
    ratios[21].click()
    time.sleep(200)
    ratios[23].click()
    #end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(200)
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    time.sleep(200)
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer4(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "能为用户提供浏览网页的功能")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "WinRAR")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "abc@ouchn.com")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "IE")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "全文搜索引擎")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    #接下来五个判断题,因为顺序不可能变,所以可写死,前面占了20个ratio,所以21,23,26,28,30
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[20].click()
    time.sleep(200)
    ratios[22].click()
    time.sleep(200)
    ratios[25].click()
    time.sleep(200)
    ratios[27].click()
    time.sleep(200)
    ratios[29].click()
    #end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(200)
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    time.sleep(200)
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer5(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "学习中心学生工作部门")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "毕业论文")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "专业在读优秀学")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "远程接待中心")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 学习中心")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(200)
    # 多选
    rightAnswer = getAnswerElement(elements1, "评优表彰")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "奖（助）学金")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "学生活动")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "虚拟学生社区")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "个性化服务")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)

    rightAnswer = getAnswerElement(elements1, "总部组织的全国学生活动")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "分部组织的学生活动")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "学习中心组织的学生活动")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "学生会组织的学生活动")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "学生社团组织的学生活动")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)

    rightAnswer = getAnswerElement(elements1, "已修完40%以上本专业课程学分")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "本专业课程平均成绩不低于70分")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, "需再获得30%以上的课程学分")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)



    rightAnswer = getAnswerElement(elements1, ". 电话")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 在线答疑")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 邮箱")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 传真")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 信函")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 学生会")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 学生社团")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)
    rightAnswer = getAnswerElement(elements1, ". 校友会")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(200)

    #end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    time.sleep(200)
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


#找到学习指南的进入学习按钮
def enterStudy(browser):
    studys = browser.find_elements_by_css_selector("button[class='btn bg-primary']")
    for s in studys:
        if '家开放大学学习指南' in s.find_element_by_xpath("./..").find_element_by_xpath("./..").find_element_by_xpath("./..").find_element_by_xpath("./h3").text:
            s.click()


def enterTest(browser,xkurl):
    enterStudy(browser)  # 进入学习的按钮会新开一个tab
    windowstabs = browser.window_handles
    browser.switch_to.window(windowstabs[1])
    browser.find_elements_by_css_selector('img[class="pull-right"]')  # find一下,保证新页面加载完成
    browser.get(xkurl)  # 先考形1

def wait3AndCloseTab(browser):
    time.sleep(3)  # 等待三秒,让我们看到卷子已经答题提交完成,然后关tab,切到第一个tab,再进学习
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

#open brower
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

enterStudynkzn='http://hubei.ouchn.cn/course/view.php?id=4279'
xingkao1='http://hubei.ouchn.cn/mod/quiz/view.php?id=475518'
xingkao2='http://hubei.ouchn.cn/mod/quiz/view.php?id=475530'
xingkao3='http://hubei.ouchn.cn/mod/quiz/view.php?id=475544'
xingkao4='http://hubei.ouchn.cn/mod/quiz/view.php?id=475558'
xingkao5='http://hubei.ouchn.cn/mod/quiz/view.php?id=475574'



option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=option)
# browser.maximize_window()  #max_window

browser.get('http://student.ouchn.cn/')
browser.implicitly_wait(8)  #wait

# accountMap={"1942001413987":"19841020"}

#login
browser.find_element_by_id("username").send_keys("1942001413987")
browser.find_element_by_id("password").send_keys("19841020")
browser.find_element_by_css_selector('button[value="login"]').click()
#enter study...此处要注意,不同账号进来看到的开放大学指南的位置不同,要动态抓元素...2019年11月13日09:10:54发现不用抓元素,直接根据URL进入国开开放指南页面,并且形考1-5的URL也是指定的,所以不用抓元素

enterTest(browser,xingkao1)
if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    writeAnswer1(browser)
wait3AndCloseTab(browser)

enterTest(browser,xingkao2)
if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    writeAnswer2(browser)
wait3AndCloseTab(browser)

enterTest(browser,xingkao3)
if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    writeAnswer3(browser)
wait3AndCloseTab(browser)

enterTest(browser,xingkao4)
if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    writeAnswer4(browser)
wait3AndCloseTab(browser)

enterTest(browser,xingkao5)
if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    writeAnswer5(browser)
wait3AndCloseTab(browser)


#5个形考走完提交之后直接换账号
browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")

# browser.find_element_by_id("username").send_keys("1942001418567")
# browser.find_element_by_id("password").send_keys("19991014")
# browser.find_element_by_css_selector('button[value="login"]').click()
# #enter study...此处要注意,不同账号进来看到的开放大学指南的位置不同,要动态抓元素...2019年11月13日09:10:54发现不用抓元素,直接根据URL进入国开开放指南页面,并且形考1-5的URL也是指定的,所以不用抓元素
#
# enterTest(browser,xingkao1)
# if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
#     writeAnswer1(browser)
# wait3AndCloseTab(browser)
#
# enterTest(browser,xingkao2)
# if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
#     writeAnswer2(browser)
# wait3AndCloseTab(browser)
#
# enterTest(browser,xingkao3)
# if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
#     writeAnswer3(browser)
# wait3AndCloseTab(browser)
#
# enterTest(browser,xingkao4)
# if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
#     writeAnswer4(browser)
# wait3AndCloseTab(browser)
#
# enterTest(browser,xingkao5)
# if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
#     writeAnswer5(browser)
# wait3AndCloseTab(browser)














#2019年11月12日16:46:35发现找不到下拉按钮,测试问题所在
# print(len(browser.find_element_by_css_selector(".sectionname")))

# browser.manage().timeouts().implicitlyWait(5, );
# soup = bs4.BeautifulSoup(browser.page_source, "lxml")
# print(len(soup.select("a")))
# selectas = soup.select("a")
# xingkaos=[]
# for xka in selectas:
#     print(xka.string)
    # if "href" in xka.string:
    #     print(xka.attrs['href'])
    # if "http://hubei.ouchn.cn/mod/quiz/view.php" in xka.text:
    #     xingkaos.append(xka)

# browser.get(xingkaos[0].get("href"))




#因为不跳新页面,所以tab无需处理,并且不抓形考元素,也直接跳url
# #there is another tab,switch to the tab and get xingkaos and get to there.
# windowstabs=browser.window_handles
# browser.switch_to.window(windowstabs[1])
# #click options
# browser.find_elements_by_css_selector('img[class="pull-right"]')[1].click()
# xingkao1=browser.find_elements_by_css_selector('a[href^="http://hubei.ouchn.cn/mod/quiz/view.php"]')[0].get_attribute("href")
# #get the xingkao url
# browser.get(xingkao1)



#2019年11月13日10:15:26浪费时间在cookie上
# ck = browser.get_cookies()
# browser.get(enterStudynkzn)#经过测试,必须进入一下学习,才能通过url进考试页,,2019年11月13日09:51:16还是点击吧,不跳tab的话,找不到ck
# browser.find_elements_by_css_selector('img[class="pull-right"]')
# browser.delete_all_cookies()
# for k in ck:
#     browser.add_cookie(k)
# browser.refresh()
# browser.find_elements_by_css_selector('img[class="pull-right"]')