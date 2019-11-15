#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import timeunit
import bs4
from selenium import webdriver

studyName='公共行政学'


def getAnswerElement(elements,neirong):
    for ele in elements:
        if neirong in ele.text:
            return ele

def getAnswerElementEquals(elements,neirong):
    for ele in elements:
        if "A. "+neirong == ele.text or "B. "+neirong == ele.text or "C. "+neirong == ele.text or "D. "+neirong == ele.text :
            return ele

#start to answer.
def writeAnswer1(browser):
    browser.find_element_by_id("id_subject").send_keys("简单生活 快乐工作")
    time.sleep(2)
    browser.switch_to.frame("id_message_ifr")
    browser.find_element_by_id("tinymce").send_keys("生活回归简单，心就简单，周末爬山、郊游、走亲访友与自然一体，乐山乐水！制定目标，规划方向，努力向前，永不言败！爱工作，爱自己，爱家！快乐工作，迎接每一个美好的明天。仰望星空，足踏实地，以德服人。")
    browser.switch_to.default_content()
    browser.find_element_by_id("id_submitbutton").click()
    #2019年11月14日20:04:03为了寻找富文本框浪费了n多时间
    # try:
    #     browser.execute_script("$('#tinymce').innerText='生活回归简单，心就简单，周末爬山、郊游、走亲访友与自然一体，乐山乐水！制定目标，规划方向，努力向前，永不言败！爱工作，爱自己，爱家！快乐工作，迎接每一个美好的明天。仰望星空，足踏实地，以德服人。'")
    # except:
    #     pass


def writeAnswer2(browser):
    browser.find_element_by_xpath('//a[@title="添加..."]').click()
    time.sleep(2)
    browser.find_elements_by_xpath('//span[@class="fp-repo-name"]')[2].click()
    time.sleep(2)
    #文件下载地址
    browser.find_element_by_id("fileurl").send_keys("https://ftp.bmp.ovh/imgs/2019/11/ab598b96131eb86b.png")
    browser.find_element_by_xpath("//button[@class='fp-login-submit btn-primary btn']").click()
    time.sleep(20)#上传,可能很慢
    browser.find_element_by_xpath("//a[@class='fp-file']").click()
    time.sleep(1)
    browser.find_element_by_xpath("//button[@class='fp-select-confirm btn-primary btn']").click()

    #end answer
    browser.find_element_by_xpath('//input[@name="submitbutton"]').click()

def writeAnswer3(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "只能充当领导的")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "牢记领导对问题的预判来筛选一")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "易出成果原")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "查与代办相结")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "息量越大越好")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "要有“诚心")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "士通电话，男士先")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "年龄")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "务招待费")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "4.5厘")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    #接下来10个判断题,因为顺序不可能变,所以可写死,前面占了40个ratio,所以41,44,45,48,50,51,53,56,58,59
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[40].click()
    time.sleep(0.1)
    ratios[43].click()
    time.sleep(0.1)
    ratios[44].click()
    time.sleep(0.1)
    ratios[47].click()
    time.sleep(0.1)
    ratios[49].click()
    time.sleep(0.1)
    ratios[50].click()
    time.sleep(0.1)
    ratios[52].click()
    time.sleep(0.1)
    ratios[55].click()
    time.sleep(0.1)
    ratios[57].click()
    time.sleep(0.1)
    ratios[58].click()
    time.sleep(0.1)
    #end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer4(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElementEquals(elements1, "书信")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "抄送下级机")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "符合公文格式标")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "政府经常越过省政府直接向国务院")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "约束性")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "中约首部分要使用相关单位或个人的简")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "交起草部门补充或修")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "出版的杂志的赠阅")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "分纸型")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "以印制成纸质文件分发")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    #接下来10个判断题,因为顺序不可能变,所以可写死,前面占了40个ratio,所以41,44,46,47,50,51,53,56,57,60
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[40].click()
    time.sleep(0.1)
    ratios[43].click()
    time.sleep(0.1)
    ratios[45].click()
    time.sleep(0.1)
    ratios[46].click()
    time.sleep(0.1)
    ratios[49].click()
    time.sleep(0.1)
    ratios[50].click()
    time.sleep(0.1)
    ratios[52].click()
    time.sleep(0.1)
    ratios[55].click()
    time.sleep(0.1)
    ratios[56].click()
    time.sleep(0.1)
    ratios[59].click()
    time.sleep(0.1)
    #end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer5(browser):
    elements1 = browser.find_elements_by_xpath('//label')
    browser.find_element_by_id("quiznavbutton1").click()
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "茶歇")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "百人上下至数百")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "时间成")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "会议参加人")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "公开性会议信")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "以惠己为原")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "经常性")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "转移焦点原")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "How do you d")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "的工作超出自己一般职责时，立刻说“N")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    browser.find_element_by_xpath('//input[@name="next"]').click()
    #接下来10个判断题,因为顺序不可能变,所以可写死,前面占了40个ratio,所以41,44,46,48,49,52,53,55,57,59
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    ratios[0].click()
    time.sleep(0.1)
    ratios[3].click()
    time.sleep(0.1)
    ratios[5].click()
    time.sleep(0.1)
    ratios[7].click()
    time.sleep(0.1)
    ratios[8].click()
    time.sleep(0.1)
    ratios[11].click()
    time.sleep(0.1)
    ratios[12].click()
    time.sleep(0.1)
    ratios[14].click()
    time.sleep(0.1)
    ratios[16].click()
    time.sleep(0.1)
    ratios[18].click()
    time.sleep(0.1)
    #end answer
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    #save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


#找到指定的课程名称,未找到返回0
def enterStudy(browser):
    studys = browser.find_elements_by_css_selector("button[class='btn bg-primary']")
    for s in studys:
        if studyName in s.find_element_by_xpath("./..").find_element_by_xpath("./..").find_element_by_xpath("./..").find_element_by_xpath("./h3").text:
            s.click()
            return 1
    return 0

#1.找到办公室管理的进入学习按钮
def enterTest(browser,xkurl):
    enterStudy(browser)  # 进入学习的按钮会新开一个tab
    time.sleep(1)
    windowstabs = browser.window_handles
    browser.switch_to.window(windowstabs[1])
    browser.find_elements_by_css_selector('img[class="pull-right"]')  # find一下,保证新页面加载完成
    browser.get(xkurl)  # 先考形1

#2.立即考试.判断一下,防止多次考试
def readyToTest(browser):
    readyTest = browser.find_element_by_xpath('//button[@type="submit"]')
    if '再次' not in readyTest.text:
        if '现在' in readyTest.text or '继续' in readyTest.text or '添加' in readyTest.text:
            readyTest.click()
            return 1
    return 0

#论坛形式试卷进入方法
def readyToTestForum(browser):
    readyTest = browser.find_element_by_xpath('//button[starts-with(@id,"single_")]')
    readyTest.click()
    return 1


# 等待三秒,让我们看到卷子已经答题提交完成,然后关tab,切到第一个tab,再进学习
def wait3AndCloseTab(browser):
    time.sleep(2)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1.5)


xingkao1='http://hubei.ouchn.cn/mod/forum/view.php?id=469087'#注意这一地址是forum,非正常试卷
xingkao2='http://hubei.ouchn.cn/mod/assign/view.php?id=469088'
xingkao3='http://hubei.ouchn.cn/mod/quiz/view.php?id=469089'



option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=option)
# browser.maximize_window()  #max_window

browser.get('http://student.ouchn.cn/')
browser.implicitly_wait(18)  #wait

file=open('gonggongxingzhengxue_key.txt')
keys=[]
for line in file.readlines():
    keys.append(line.strip())

for key in keys:
    username=key.split("\t")[0]
    password=key.split("\t")[1]

    #login
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_css_selector('button[value="login"]').click()
    #enter study...此处要注意,不同账号进来看到的开放大学指南的位置不同,要动态抓元素...2019年11月13日09:10:54发现不用抓元素,直接根据URL进入国开开放指南页面,并且形考1-5的URL也是指定的,所以不用抓元素

    # enterTest(browser,xingkao1)
    # if readyToTestForum(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer1(browser)
    # wait3AndCloseTab(browser)

    enterTest(browser,xingkao2)
    if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer2(browser)
    wait3AndCloseTab(browser)

    # enterTest(browser,xingkao3)
    # if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer3(browser)
    # wait3AndCloseTab(browser)


    #5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(2)

# browser.find_element_by_id("username").send_keys("1940.11418567")
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