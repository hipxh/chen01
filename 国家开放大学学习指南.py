#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread
from chooseClass import chooseClassPage
import timeunit
import os
from selenium import webdriver

studyName = os.path.basename(__file__).split('.')[0]


# 其中一张试卷全部为富文本提交
def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele


def getAnswerElementEquals(elements, neirong, i, meidaotiyouduoshaogexuanxiang, tiaoguoxuanxiangshu=0):
    elements = elements[i * meidaotiyouduoshaogexuanxiang + tiaoguoxuanxiangshu:(
                                                                                            i + 1) * meidaotiyouduoshaogexuanxiang + tiaoguoxuanxiangshu]
    for ele in elements:
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text:
            return ele


# 单选和多选在一页
def getAnswerElementEqualsdanxuanduoxuaninOnePage(elements, neirong, i, meidaotiyouduoshaogexuanxiang,
                                                  danxuanLabelLength):
    elements = elements[danxuanLabelLength + i * meidaotiyouduoshaogexuanxiang:(
                                                                                           i + 1) * meidaotiyouduoshaogexuanxiang + danxuanLabelLength]
    for ele in elements:
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text:
            return ele


def getAnswerElementEquals433(elements, neirong, i):
    if i == 1:
        elements = elements[0:16]
    if i == 2:
        elements = elements[16: 28]
    for ele in elements:
        if "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele


def getAnswerElementEqualsFinal(elements, neirong, i, danxuanRatios, duoxuanCheckboxs):
    if i == 1:
        elements = elements[0:danxuanRatios]
    if i == 2:
        elements = elements[danxuanRatios: danxuanRatios + duoxuanCheckboxs]
    for ele in elements:
        if "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele


def getAnswerElementEquals4(elements, neirong, i):
    if i == 1:
        elements = elements[0:16]
    if i == 2:
        elements = elements[16: 32]
    for ele in elements:
        if "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele


def getAnswerElementEquals222(elements, neirong, i):
    if i == 1:
        elements = elements[0:8]
    if i == 2:
        elements = elements[8: 16]
    for ele in elements:
        if "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele


rightTiGan = []


def judgeQueTitle(elements1p, title):
    if isinstance(elements1p, list):
        for ele in elements1p:
            if title + "（" in ele.text or title + "(" in ele.text:
                rightTiGan.append(ele)
                return True
    else:
        if title in elements1p.text:
            rightTiGan.append(elements1p)
            return True


# 2019年11月16日17:01:07眼睛看瞎了,不能一个个去word取答案.没有标准格式就自己创造.
def danxuanAutoAnswer(answer, map):
    split = answer.split("")
    for i in split:
        if len(i) < 2:
            continue
        i_split = i.split("（")
        map[i_split[0].strip()] = i_split[1].split("）")[0].strip()
    return map


def danxuanAutoAnswerFix(answer, reg):
    result = []
    split = answer.split("\n")
    for i in split:
        result.append(i.strip())
    return result


def duoxuanAutoAnswerFix(answer, reg, reg2):
    # map={}
    # split = answer.split("\n")
    # for i in split:
    #     map[i.split(reg)[0].strip()] = i.split(reg)[-1].split(reg2)
    # return map
    # 2019年11月18日11:44:49惊人发现,Python的map在mac下有序,在win下无序
    listList = []
    split = answer.split("\n")
    for i in split:
        if "hx" in i:
            reg2 = "hx"
        listList.append(i.split(reg)[-1].split(reg2))
    return listList


def duoxuanAutoAnswer(answer, map):
    split = answer.split("")
    for i in split:
        if len(i) < 2:
            continue
        i_split = i.split("（")  # 2019年11月17日14:25:30bug,如果选项里有括号,则报错,此处应取第一个左括号的前面和最后一个右括号的右边,怕耽误速度,暂不处理
        map[i_split[0].strip()] = i_split[-1].split("）")[0].strip().split("; ")
    return map


def pdAutoAnswer(answer, list):
    split = answer.split("")
    for i in split:
        if len(i) < 2:
            continue
        if '错' in i.split("（")[1]:
            list.append(i.split("（")[0].strip())
    return list


def pdUtil5(list, elements1p, ratios, titleIndex, danxuantiLength, panduanIndex):
    a = 1
    for timu in list:
        if (judgeQueTitle(elements1p[titleIndex], timu)):  # 如果题干在错的list里,就点击错误
            a = 0
            ratios[danxuantiLength * 4 + panduanIndex * 2 + 1].click()
            break
    if a == 1:  # 如果把错题都走了一遍仍然为1,则该判断题是对的
        ratios[danxuantiLength * 4 + panduanIndex * 2].click()
    time.sleep(0.1)


# start to answer.
def writeAnswer1(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 2单
    dxAnswer = '''国家开放大学是一所与普通高校学习方式完全相同的大学
只有在面对面教学的课堂上才能完成学习任务'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 5判断
    pdAnswer = '''对
对
错
错
错'''
    pdAnswer = danxuanAutoAnswerFix(pdAnswer, ".")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2, 8)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer2(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 2单
    dxAnswer = '''8
专业综合实践
被评为优秀毕业生
小学、初中
入学注册时'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 5判断
    pdAnswer = '''对
错
对
错
错'''
    pdAnswer = danxuanAutoAnswerFix(pdAnswer, ".")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2, 20)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


# 形考三单选多选判断在一个页面
def writeAnswer3(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 2单
    listdxanswer = ['www.ouchn.cn']
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 5判断
    pdAnswer = ['错']
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

        # 2单
        dxAnswer = '''国开在线
毕业论文'''
        listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
        dxindex = 0
        for an in listdxanswer:
            anEle = getAnswerElementEquals(elements1, an, dxindex, 4, 6)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
            dxindex += 1

        # 多选紧急处理,
        mulAnswer = '''1.形成性考核；终结性考核
2.学习导学资料；浏览课程视频；完成形成性考核任务；学习拓展知识；完成终结性考核
3.开卷；半开卷；闭卷
4.身份证；学生证；准考证'''
        dxindex = 0
        mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "；")
        time.sleep(2)
        for value in mapmulAnswer:
            for v in value:
                anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5, 14)  # 找到指定的那个label选项
                if anEle is not None:
                    anEle.find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
            dxindex += 1

        # 6判断
        pdAnswer = '''错
对
错
错
错
错'''
        pdAnswer = danxuanAutoAnswerFix(pdAnswer, ".")
        dxindex = 0
        for pd in pdAnswer:
            anEle = getAnswerElementEquals(elements1, pd, dxindex, 2, 34)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
            dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer4(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 2单
    dxAnswer = '''能为用户提供浏览网页的功能
abc@ouchn.com
WinRAR
全文搜索引擎
IE'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 5判断
    pdAnswer = '''对
错
对
错
错'''
    pdAnswer = danxuanAutoAnswerFix(pdAnswer, ".")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2, 20)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


# 形考五单选多选判断在一个页面
def writeAnswer5(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 2单
    dxAnswer = '''学习中心学生工作部门
国家开放大学各专业在读优秀学生
本专业课程平均成绩和综合实践（毕业论文、毕业设计、毕业作业）成绩均不低于75分
应届本科和专科毕业生
远程接待中心'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 多选紧急处理,
    mulAnswer = '''1.评优表彰；奖（助）学金；学生活动；虚拟学生社区；个性化服务
1.已修完40%以上本专业课程学分；hx本专业课程平均成绩不低于70分；hx已获得过奖学金的学生再次申请奖学金时，需再获得30%以上的课程学分。
1.总部组织的全国学生活动；hx分部组织的学生活动；hx学习中心组织的学生活动；hx学生会组织的学生活动；hx学生社团组织的学生活动；hx
1.学生会；学生社团；校友会
1.电话；在线答疑；邮箱；传真；信函'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "；")
    time.sleep(2)
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5, 20)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
        dxindex += 1


    # 6判断
    pdAnswer = '''错
对
对
错
对'''
    pdAnswer = danxuanAutoAnswerFix(pdAnswer, ".")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2, 45)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1


    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


# 找到指定的课程名称,未找到返回0
def enterStudy(browser):
    time.sleep(5)  # 此处根据网络情况等待,才能拿到完整的科目列表
    page_chooseClass = chooseClassPage(browser)
    studys = page_chooseClass.btns_enter_answer
    for s in studys:
        if studyName in s.find_element_by_xpath("./..").find_element_by_xpath("./..").find_element_by_xpath(
                "./..").find_element_by_xpath("./h3").text:
            s.click()
            return 1
    return 0


# 1.找到办公室管理的进入学习按钮
def enterTest(browser, xkurl):
    enterStudy(browser)  # 进入学习的按钮会新开一个tab
    time.sleep(1)
    windowstabs = browser.window_handles
    if len(windowstabs) > 1:  # 如果没找到课程,至少别报错
        browser.switch_to.window(windowstabs[1])
        browser.find_elements_by_css_selector('img[class="pull-right"]')  # find一下,保证新页面加载完成
        browser.get(xkurl)  # 先考形1
    else:
        return 0


# 2.立即考试.判断一下,防止多次考试
def readyToTest(browser):
    readyTest = browser.find_element_by_xpath('//button[@type="submit"]')
    if '再次' not in readyTest.text:
        if '现在' in readyTest.text or '继续' in readyTest.text:
            readyTest.click()
            return 1
    return 0


# 论坛形式试卷进入方法
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


area = ''


option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=option)
# browser.maximize_window()  #max_window

browser.get('http://student.ouchn.cn/')
browser.implicitly_wait(8)  # wait

file = open(studyName + '.txt')
keys = []
for line in file.readlines():
    keys.append(line.strip())

for key in keys:
    username = key.split("\t")[0]
    password = key.split("\t")[1]

    if "42101" in username[2:9]:
        area = 'wuhan'
    elif "44101" in username[2:9]:
        area = 'guangzhou'
    elif "42001" in username[2:9]:
        area = 'hubei'

    xingkao1 = 'http://' + area + '.ouchn.cn/mod/quiz/view.php?id=562696'  # 注意这一地址是forum,非正常试卷
    xingkao2 = 'http://' + area + '.ouchn.cn/mod/quiz/view.php?id=562708'
    xingkao3 = 'http://' + area + '.ouchn.cn/mod/quiz/view.php?id=562718'
    xingkao4 = 'http://' + area + '.ouchn.cn/mod/quiz/view.php?id=562732'
    xingkao5 = 'http://' + area + '.ouchn.cn/mod/quiz/view.php?id=562748'

    # login
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_css_selector('button[value="login"]').click()
    # enter study...此处要注意,不同账号进来看到的开放大学指南的位置不同,要动态抓元素...2019年11月13日09:10:54发现不用抓元素,直接根据URL进入国开开放指南页面,并且形考1-5的URL也是指定的,所以不用抓元素

    if enterTest(browser,xingkao1)!=0:
        if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer1(browser)
        wait3AndCloseTab(browser)

        enterTest(browser,xingkao2)
        if readyToTest(browser)==1:#除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer2(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao3)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
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
        print(username,"----------------------")
    else:
        print(username,"----------------------没找到课程")
# 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(6)
