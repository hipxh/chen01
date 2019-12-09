#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import time
from threading import Thread

import timeunit
import bs4
from selenium import webdriver

studyName=os.path.basename(__file__).split('.')[0]

def getAnswerElement(elements,neirong):
    for ele in elements:
        if neirong in ele.text:
            return ele

def getAnswerElementEquals(elements,neirong):
    for ele in elements:
        if "A. "+neirong == ele.text or "B. "+neirong == ele.text or "C. "+neirong == ele.text or "D. "+neirong == ele.text  or "E. "+neirong == ele.text:
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
    time.sleep(20)
    #end answer
    browser.find_element_by_xpath('//input[@name="submitbutton"]').click()

def writeAnswer3(browser):
    #保证进来的是第一页
    browser.find_element_by_id("quiznavbutton1").click()
    #走来四个富文本
    time.sleep(4)#等待富文本加载完成
    line = browser.page_source
    # matchObj = re.match('(.*)id=\"(.*):2_answer_id_ifr', line, re.M | re.I)
    frameId = line.split(":2_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId+":2_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "管理层次是指公共组织内部划分管理层级的数额。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":3_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "行政规章是指特定的行政机关根据法律和法规，按照法定程序制定的具有普遍约束力的规范性文件的总称。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":4_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "行政决策参与是指行政领导者个人或集体在行政决策时，专家学者、社会团体、公众等对决策提出意见或建议的活动。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":5_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "行政效率是指公共组织和行政工作人员从事公共行政管理工作所投入的各种资源与所取得的成果与效益之间的比例关系。"
    )
    browser.switch_to.default_content()

    elements1 = browser.find_elements_by_xpath('//label')
    #如下是正常操作,该套试卷形考1两道单选
    rightAnswer = getAnswerElement(elements1, "梁启超")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "官僚制理论")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "美国社会与公共")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "垄断资本主义时期")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "芬兰")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "决策权力")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "英")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "平行")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "党的纪律检查机关和行政")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "德鲁克")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    time.sleep(0.1)
    #下一页
    browser.find_element_by_xpath('//input[@name="next"]').click()
    elements1 = browser.find_elements_by_xpath('//label')
    time.sleep(4)
    # 多选
    rightAnswer = getAnswerElement(elements1, "斯密斯堡")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "汤姆森")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "怀特")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "西蒙")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "棱柱型公共行政模式")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "衍射型公共行政模式")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "融合型公共行政模式")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "布莱克")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "莫顿")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "德")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "智")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "能")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "勤")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElementEquals(elements1, "绩")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "现场监督")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)
    rightAnswer = getAnswerElement(elements1, "跟踪监督")
    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    time.sleep(0.1)

    try:
        browser.switch_to.frame(frameId+":24_answer_id_ifr")
        browser.find_element_by_id("tinymce").send_keys(
            "（1）直接生产和提供公共物品，弥补市场不足的职能；（2）规范和稳定市场秩序，确保自由竞争的职能；（3）对经济进行宏观调控的职能，确保国民经济平衡发展的职能；（4）改善收入分配；（5）管理国有资产的职能。"
        )
        browser.switch_to.default_content()
        browser.switch_to.frame(frameId + ":25_answer_id_ifr")
        browser.find_element_by_id("tinymce").send_keys(
            "（1）行政执行的主体是行政机关及行政人员。（2）行政执行是一种具有目标导向的活动。（3）行政执行是一种实施性质很强的活动，是务实性的、付诸于实际的行动，它需要通过一定的具体步骤或实际行动来落实政策。（4）行政执行是一种行政法律行为。（5）行政执行活动还具有强制性。"
        )
        browser.switch_to.default_content()
        browser.switch_to.frame(frameId + ":27_answer_id_ifr")
        browser.find_element_by_id("tinymce").send_keys(
            "（1）经济体制决定并制约行政体制，行政体制也影响和制约经济发展；（2）政治体制决定行政体制，行政体制是政治体制的重要组成部分；（3）行政体制的核心问题是行政权的划分和公共组织设置，以及对政府系统的各级各类政府部门职权的配置；（4）科学技术推动行政体制的变革；（5）文化对行政体制的重要价值作用。"
        )
        browser.switch_to.default_content()
        browser.switch_to.frame(frameId + ":28_answer_id_ifr")
        browser.find_element_by_id("tinymce").send_keys(
            "（1）行政监督机关依法行使职权，不受其他部门、社会团体和个人干涉的原则；（2）实事求是，重证据、重调查研究的原则；（3）在适用法律和行政纪律上人人平等的原则；（4）教育与惩处相结合的原则；（5）监督检查与改进工作相结合的原则；（6）监督工作依靠群众的原则。"
        )
        browser.switch_to.default_content()
    except:
        browser.find_element_by_id(frameId+":24_answer_id").send_keys(
            "（1）直接生产和提供公共物品，弥补市场不足的职能；（2）规范和稳定市场秩序，确保自由竞争的职能；（3）对经济进行宏观调控的职能，确保国民经济平衡发展的职能；（4）改善收入分配；（5）管理国有资产的职能。"
        )

        browser.find_element_by_id(frameId+":25_answer_id").send_keys(
            "（1）行政执行的主体是行政机关及行政人员。（2）行政执行是一种具有目标导向的活动。（3）行政执行是一种实施性质很强的活动，是务实性的、付诸于实际的行动，它需要通过一定的具体步骤或实际行动来落实政策。（4）行政执行是一种行政法律行为。（5）行政执行活动还具有强制性。"
        )

        browser.find_element_by_id(frameId+":27_answer_id").send_keys(
            "（1）经济体制决定并制约行政体制，行政体制也影响和制约经济发展；（2）政治体制决定行政体制，行政体制是政治体制的重要组成部分；（3）行政体制的核心问题是行政权的划分和公共组织设置，以及对政府系统的各级各类政府部门职权的配置；（4）科学技术推动行政体制的变革；（5）文化对行政体制的重要价值作用。"
        )

        browser.find_element_by_id(frameId+":28_answer_id").send_keys(
            "（1）行政监督机关依法行使职权，不受其他部门、社会团体和个人干涉的原则；（2）实事求是，重证据、重调查研究的原则；（3）在适用法律和行政纪律上人人平等的原则；（4）教育与惩处相结合的原则；（5）监督检查与改进工作相结合的原则；（6）监督工作依靠群众的原则。"
        )
        browser.switch_to.default_content()

    # end answer
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
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
    time.sleep(2)
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

file=open(studyName+'.txt')
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

    enterTest(browser,xingkao1)
    if readyToTestForum(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer1(browser)
    wait3AndCloseTab(browser)

    # enterTest(browser,xingkao2)
    # if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer2(browser)
    # wait3AndCloseTab(browser)

    enterTest(browser,xingkao3)
    if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer3(browser)
    wait3AndCloseTab(browser)


    #5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(6)
