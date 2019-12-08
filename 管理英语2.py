#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import bs4
from selenium import webdriver
import os

from selenium.webdriver.common.keys import Keys

studyName = os.path.basename(__file__).split('.')[0]


# 其中一张试卷全部为富文本提交
def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele


def getAnswerElementEquals(elements, neirong, key,i, meidaotiyouduoshaogexuanxiang):
    may = None
    for ele in elements:  # or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text:
            may = ele
            if ele.find_element_by_xpath("./../../../../div[@class='qtext']").text[-3:] in key.strip():
                return ele
    return may

#单选和多选在一页
def getAnswerElementEqualsdanxuanduoxuaninOnePage(elements, neirong, i, meidaotiyouduoshaogexuanxiang,danxuanLabelLength):
    elements = elements[danxuanLabelLength+i * meidaotiyouduoshaogexuanxiang:(i + 1) * meidaotiyouduoshaogexuanxiang+danxuanLabelLength]
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
    result = {}
    split = answer.split("\n")
    for i in split:
        i=i.split("题目：")[1]
        result[i.strip().split(reg)[0].strip()] = i.strip().split(reg)[1].strip()
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
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0


    # 5单
    dxAnswer = '''题目：— Do you mind if I record your lecture?	答案：Not at all
题目：—I’m terribly sorry that I’ve spilled some coffee on the table.	答案：It doesn’t matter
题目：－How’s your mother doing?	答案：She is very well
题目：He was always ______ in sharing his enormous knowledge. 答案：generous 
题目：He is ________ this company 答案： in charge of
题目：One day, our dreams will ____________ reality. 答案：turn into
题目：More than 30 people ______ the position	答案：applied for'''

    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 3)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    #题库此处有问题
    if "翻译：从以下A" in browser.page_source:
        dxAnswer='''子问题 1：C; 子问题 2：A; 子问题 3：A; 子问题 4：B; 子问题 5：A'''
    if "听力理解：请听下面的对话" in browser.page_source:
        dxAnswer = '''子问题 1：meet; 子问题 2：call; 子问题 3：number; 子问题 4：really; 子问题 5：forward'''
    if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：A; 子问题 3：B; 子问题 4：C; 子问题 5：B'''
    if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：F'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an[-1])
    print(listAnswer2)
    print(len(browser.find_elements_by_class_name("custom-select")))
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex+=1



    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer2(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：— Hi, Helen, I’ll have an interview tomorrow. I’m afraid I can’t make it. 	答案： Sure, you can. Take it easy
题目：—What starting salary do you expect? 	答案：I'd like to start at ￥5000 a month
题目：—May I ask you why you left the former company？	答案：Because I want to change my working environment and seek new challenges
题目：I’m writing to ________ a position as a computer engineer in your company. 	答案： apply for
题目：You also should send a resume ________ the employer know more information about you	答案：to let
题目：— I have worked for IBM for 3 years	答案：What is your working experience
题目：The candidate should dress in a manner that is appropriate to the position ________ he is applying.	答案： for which'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()#find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1
        print(dxindex)


    listAnswer2 = []
    dxindex = 0
    dxAnswer = '''选择判断题 1：T;  2：F; 3：F;  4：T;  5：T'''

    #选择题
    dxAnswer = '''题目：The old saying “practice makes perfect” applies to interviewing too 	答案： 古话“熟能生巧”对面试准备也是适用的。
    题目：A bad hire not just wastes your time and money, but also impacts the team spirit and company morale 	答案：招聘到不合格的员工即浪费时间和金钱，而且还会影响整个团队精神和公司士气。
    题目：The more familiar interviewing feels to you, the less anxiety you will feel with the process.	答案：你对面试越熟悉，在面试过程中你的焦虑就会越少
    题目：Stress around interviews is often influenced by our assumptions we make to ourselves about the process 	答案：来自面试的压力会影响我们对面试过程的推测。
    题目：We can’t possibly get the work done by October	答案：十月份前我们不可能做完这项工作'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an[-1])
    print(listAnswer2)
    print(len(browser.find_elements_by_class_name("custom-select")))
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex += 1


    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer3(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0


    # 5单
    dxAnswer = '''题目：—______________________ —Everything is going smoothly.	答案：How is everything going?
题目：—______________________ —It might be a good idea to read some simplified books first. 	答案：What books would you recommend?
题目：—Should I leave earlier tomorrow morning?
—______________________	答案： Yes, it’s better to leave earlier to avoid the morning traffic.
题目：Anyone who has worked here for over three years is   for sick pay.	答案：eligible 
题目：American young people would rather ______ advice from strangers. 	答案：get'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0

    if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：B; 子问题 4：C; 子问题 5：B'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an[-1])
    print(listAnswer2)
    print(len(browser.find_elements_by_class_name("custom-select")))
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex+=1


    dxAnswer = '''题目：—Any suggestions for the project?—______________________	答案： I advise you to put more hands in this project.
        题目：—______________________—In total, it should be about 15,000 RMB for the three-daytraining. 	答案：How much have you budgeted for the training? 
        题目：—Should I leave earlier tomorrow morning?—______________________	答案： Yes, it’s better to leave earlier to avoid the morning traffic. 
        题目：Does his absence  to your work?	答案：make a difference 
        题目：______ you prepare cross training plans, you need to consider both the company benefits and the employee benefits. 	答案：As 
        题目：Participants have _____the Productivity Analysis Worksheet 	答案：completed  '''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer4(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0


    # 5单
    dxAnswer = '''题目：— What kind of event are you going to plan?—                      	答案： A birthday party for my brother
题目：—                      ?— It will be held on the 3rd floor of Shakiraton Hotel	答案：What is the address of your speech
题目：— Your plan is perfect and I believe that it will be a great success — ________________	答案：Thank you very much
题目：Are you familiar ______the saying, “it’s not what you know, but who you know”? In event planning, networking is key!	答案：with 
题目：______ the feedback is very helpful for planning future meetings and events	答案：Getting 
题目：— How do you think of the theme of our event?— ________________	答案：It’s pretty good
题目：Let’s ______ our plan.	答案：start '''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    #此题题库少了选择判断题
    if "听力理解：请听下面的对话，根据对话内容进行判断，正确写“T”错误写“F”" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：T'''
    if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：B; 子问题 4：B; 子问题 5：A'''
    if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：T; 子问题 3：T; 子问题 4：F; 子问题 5：F'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an[-1])
    print(listAnswer2)
    print(len(browser.find_elements_by_class_name("custom-select")))
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex+=1



    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer5(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 选择判断题无答案
    # 5单
    dxAnswer = '''题目：— What’s your view on our questionnaire?— ________________	答案：First of all .We’d better change our question order
题目：—                      ?—Twice a week	答案：How often do you use our company’s product
题目：— Thank you very much for answering our questions. It really helps our market research a lot. — ________________ 	答案： It’s my pleasure
题目：Questionnaires are not suitable_____some people 	答案：for 
题目：Where are you used to____ vegetables? 	答案：buying
题目：— Would you mind filling the questionnaire for me?	答案： No problem. Just give me your questionnaire
题目：The Jiahe Community Service Center is about to ______ service for residents	答案：provide'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0




    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer6(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：— I am sorry. Now what were we talking about?—                     .	答案：You were saying that you used to be a teacher
题目：— What do you think of your mother’s advice?—                     .	答案： It doesn’t fit us, actually
题目：— How do you like living in Beijing?—                    .答案： I love it. Beijing is such a beautiful city 
题目：They have learned about ______ in recent years	答案：hundreds of English words 
题目：— Did the medicine make you feel better?  — No. The more        ,        I feel.	答案：medicine I take; the worse
题目：— This jacket is so good.                     ?— It’s 200 yuan. I can give you special 20% discount on it.	答案： How much is it
题目：The music           like the singing of a bird	答案：sounds   
题目：Her article is ____ in her class	答案： the best'''

    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0

    if "翻译：从以下A、B、C三个选项中选出与英文最适合的中文翻译" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：A; 子问题 4：B; 子问题 5：B'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an[-1])
    print(listAnswer2)
    print(len(browser.find_elements_by_class_name("custom-select")))
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex+=1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer7(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0


    # 5单
    dxAnswer = '''题目：—Hello, is that service center? The elevator of our apartment doesn’t work.—	答案：Sorry, I’ll have it checked out at once
题目：—Customer: We have ordered for almost one hour. Why is it so hard to get our dishes ready in your restaurant?—Waiter:   	答案： I’m really sorry about that
题目：—                     ?—That’s great! 	答案：How about going to dinner at the Mexican restaurant tonight 
题目：The heating system of our apartment broke down so I made a ______ call to the community service center.	答案：complaint
题目：They          since last night. They are about to finish the work. 答案： have been cleaning the system
题目：—                       — Neither do I. Look at our community, it is such a mess  答案：I really don’t think our service center is satisfying
题目：We are under ______ to finish the task within such limited time	答案：pressure
题目：I don’t know         . I just arrived here two minutes ago	答案：what’s going on'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0

    if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：A; 子问题 5：B'''
    if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：T; 子问题 5：F'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an[-1])
    print(listAnswer2)
    print(len(browser.find_elements_by_class_name("custom-select")))
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex+=1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer8(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0


    # 5单
    dxAnswer = '''题目：—Would you mind answering some questions about your annual report? — ________.	答案：No, as long as it doesn’t take long
题目：—                     ?—It will take at least two weeks.	答案：How soon will you finish our annual report
题目：—How did your talk with the community resident go? 　—________ He seemed to accept my explanation，but he didn’t sign his name here 答案：I’m not sure
题目：I’m confident in these as long as we ________ the needs of the community residents and improve our service quality.  	答案：keep an eye on
题目：The investor should be aware of the limitations of the financial statement analysis ____ the annual report. 	答案：based on
题目：—Good morning, Sunshine Community Center! May I help you?—                     .	答案：I need a plumber to repair the water pipe in my kitchen
题目：The new year is just _________.	答案：around the corner
题目：People ______ find useful information from the annual report	答案：could'''

    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0

    if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：T'''
    if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：A; 子问题 3：C; 子问题 4：B; 子问题 5：B'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an[-1])
    print(listAnswer2)
    print(len(browser.find_elements_by_class_name("custom-select")))
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()



# 找到指定的课程名称,未找到返回0
def enterStudy(browser):
    studys = browser.find_elements_by_css_selector("button[class='btn bg-primary']")
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
        try:
            browser.find_element_by_xpath('//div[@class="help_close"]').click()  # find一下,保证新页面加载完成
        except:
            pass
        browser.get(xkurl)  # 先考形1
    else:
        return 0


# 2.立即考试.判断一下,防止多次考试
def readyToTest(browser):
    readyTest = browser.find_element_by_xpath('//input[@type="submit"]')
    if '再次' not in readyTest.get_attribute("value"):
        if '现在' in readyTest.get_attribute("value") or '继续' in readyTest.get_attribute("value"):
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


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437530'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437536'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437544'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437550'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437555'
xingkao6 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437562'
xingkao7 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437568'
xingkao8 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437578'

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

    # login
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_css_selector('button[value="login"]').click()
    # enter study...此处要注意,不同账号进来看到的开放大学指南的位置不同,要动态抓元素...2019年11月13日09:10:54发现不用抓元素,直接根据URL进入国开开放指南页面,并且形考1-5的URL也是指定的,所以不用抓元素

    if enterTest(browser, xingkao1) != 0:
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer1(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao2)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer2(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao3)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer3(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao4)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer4(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao5)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer5(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao6)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer6(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao7)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer7(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao8)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer8(browser)
        wait3AndCloseTab(browser)

    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(6)
