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
        "管理层次也称组织层次，是描述组织纵向结构特征的一个概念，指公共组织内部划分管理层级的数额。如果以构成组织纵向结构的各级管理组织来定义，管理层次就是指从组织最高一层管理组织到最低一级管理组织的各个组织等级。每个组织等级就是一个管理层次。一个企业的管理层次的多少表明其组织结构的纵向复杂程度。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":3_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "行政规章是指特定的行政机关根据法律和法规，按照法定程序制定的具有普遍约束力的规范性文件的总称。行政规章简称规章。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":4_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "行政决策是指行政机关为履行行政职能，就面临的需要解决的公共问题，从实际出发，为实现特定的行政管理目标，实现公共利益，制定和选择行动方案的活动。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":5_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "行政效率是公共行政活动的起点,也是落脚点.政府管理国家和社会的各个方面的公共事务,都必须讲投入产出和成本效益,都必须讲效率.行政效率在公共行政活动一开始,就作为重要的因素来指导公共行政活动.高效率就是低成本,高产出,是实现公共利益的重要方面。"
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

    browser.switch_to.frame(frameId+":24_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "我国政府的经济职能主要包括四个方面：①经济调节，政府要按照市场经济规律履行好经济调节的职能，对经济运行实施宏观调控。②市场监管，政府要加大力度整顿和规范市场经济秩序。假冒伪劣商品、文化市场混乱、工程质量低劣等问题比较突出。这些都表明政府的市场监管力度不够，政府市场监管的职能还不到位。③社会管理政府要进一步加强社会管理职能。在现代社会中，随着民主政治的发展和公民素质的提高，政府社会管理职能要与充分发挥公民自我管理和社区自治有机结合起来。良好的社会管理不仅是构建和谐社会的基本要求，也是促进经济增长、社会全面发展的重要手段。④公共服务政府要提供更多的公共服务。提供公共产品，如基础教育、公共卫生、公共文化、社会保障、科学技术、体育休闲、基础设施、环境保护、发布公共信息等。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":25_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "行政执法是行政机关及行政人员依法实施行政决策，以实现预期行政目标和社会目标的活动的总和。理解行政执行的含义，应把握的要点是：1、行政执行的主体是行政机关及行政人员；2、行政执行是一种具有目标导向的活动；3、行政执行是一种实施性质很强的活动，是务实性的、付诸于实际的行动，它需要通过一定的具体步骤或实际行动来落实政策；4、行政执行是一种行政法律行为；5、行政执行活动还具有强制性。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":27_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "（1）行政体征必须体现政治和政治体制的要求，是实现政治统治目标，加强政府合法性功能的体制性的和强制性的工具。（2）国家意志和公共利益必须通过行政系统贯彻才能实现。执政党只有经过政府的贯彻执行其政策，才能实现其政策目标。（3）行政体制是以各级各类行政组织有效地管理社会公共事务为价值的。政府公平、高效地处理社会公共事务，满足广大公众的要求，就扩大了政治统治基础。那种认为公共行政是纯事务性的管理是不符合实际的。"
    )
    browser.switch_to.default_content()
    browser.switch_to.frame(frameId+":28_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1）.行政监督机关依法行使职权,不受其他部门,社会团体和个人干涉的原则.这一原则有三点基本含义:(1)依法监督;(2)自主行使监督权;(3)监督机关依法行使职权不受其他部门,社会团体和个人的干涉。2）.实事求是,重证据,重调查研究的原则.贯彻实施这一项原则,对于搞好各项监督工作,具有十分重要的作用.这一原则的基本内容有三点:(1)坚持实事求是;(2)重证据;(3)重调查研究。3）.在适用法律和行政纪律上人人平等的原则.在适用法律和行政纪律上人人平等的原则,是指行政监督机关在查处违法违纪案件等工作中,在适用法律和行政纪律上,对任何监督对象都要一律平等,不允许任何人有超越法律,法规和行政纪律的特权。4）.教育与惩处相结合的原则.这一原则是行政监督机关在查处违法违纪案件等工作中必须遵循的一项基本原则.行政监督机关是维护法律的专门机构,通过严肃惩处违法违纪者,可以给监督对象以正确的导向,让他们认识到法律是必须遵守的,违反了就要受到惩处,从而增强遵纪守法的自觉性,并遏制和防范腐败行为的发生.通过惩处,教育那些违反违法违纪的人员认识错误,改正错误,做好工作,将功补过;同时,通过案件的解剖,分析产生错误的客观环境和主观原因,总结教训,来对广大的监督对象进行法制和纪律教育,促使他们增强法制观念,纪律观念和遵纪守法的自觉性,为搞好廉政,勤政建设提供思想保证.5）.监督检查与改进工作相结合的原则.这一原则要求行政监督机关必须把履行职责同要达到的目的统一起来.行政监督机关通过监督检查,在发现,揭露存在的缺点和错误,对违法违纪者给予应得的惩罚的同时,要通过发现问题,执行法律,去分析产生错误的客观环境和主观原因,研究纠正错误,改进工作的对策和措施,以改善公共行政管理。6,监督工作依靠群众的原则.这一原则体现了党的群众路线的精神和要求,是做好新时期行政监督工作的基本保证。"
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

    # enterTest(browser,xingkao1)
    # if readyToTestForum(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer1(browser)
    # wait3AndCloseTab(browser)

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
    time.sleep(2)
