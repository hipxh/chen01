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


def getAnswerElementEquals(elements, neirong, i, meidaotiyouduoshaogexuanxiang):
    for ele in elements:#or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele

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
    dxAnswer = '''题目：_____dangerous it is to ride fast on a busy road!答案：How
题目：_____pity you missed the lecture again!答案：What a
题目：-. What do you think about my hometown?答案：The greatest part about the town, in my opinion, is the beautiful lake and mountain. 
题目：-What about mailing it in the fastest way?答案：By air mail
题目：-Would you like me to help you to make a plan today for the summer vacation?答案：It is nice of you to say so, but I'm busy tonight.
题目：-Wow! This is a marvelous room! You must spend a lot of time and energy in it.答案：Thanks you. It really cost me that much.
题目：–How far is the Great Bay from your house?答案：The Great Bay is five minutes away from my house and it's fantastic.
题目：A double room with a balcony overlooking the sea had been _____ for him.答案：reserved
题目：At a time of this economic crisis, our _____ should be very clear about what we need to do.答案：priority
题目：Criminals are given the _____ of going to jail or facing public humiliation.答案：option
题目：If there is any change about the time of the meeting, please notify us _____.答案：in advance
题目：The Chinese Red Cross contributed a _____ sum to the relief of the physically disabled.答案：generous
题目：There _____ two hundred dollars to pay.答案：is
题目：There must be something wrong with my computer, _____ there?答案：isn't'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "英译汉" in browser.page_source:
        dxAnswer='''子问题 1：A; 子问题 2：C; 子问题 3：C; 子问题 4：A; 子问题 5：B'''
    if "补全对话内容。" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：E; 子问题 4：B; 子问题 5：D'''
    if "判断正误。" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：T; 子问题 5：F'''
    if "完成选择题。" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：C; 子问题 4：C; 子问题 5：C'''

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
    dxAnswer = '''题目：—Can I take your order, madam?答案：Yes. I'd like an Italian soup to start with and then some fried noodles
题目：—Do you mind if I ask you why you choose to be a volunteer?答案：Of course not. Well, you know volunteering is a great way to get work experience!
题目：—What are you going to do in the 2022 Winter Olympics?答案：I'm going to be a volunteer.
题目：—What's your plan for the summer vacation?答案：I'm planning to go to Italy.
题目：—Would you like anything else？答案：I'd like some cookies.
题目：After cleaning the floor, I went on ________the window.答案：to clean
题目：Do not think that you are helping others who are not fortunate, but think of it as _______?答案：exchange
题目：He looked _______ after reading the newspaper．答案：worried
题目：I __________ his efforts and I wish him well. 答案：appreciate
题目：If you take the ________ to learn a new skill, you will grasp it quickly.答案：initiative
题目：They found all the guests _____ when they woke up.答案：gone
题目：We walked down the stairs____________ taking the elevator.答案：instead of
题目：When people try to call their doctors during off hours, they usually hear a recorded答案：emergency
题目：When we heard of it, we were deeply _________．答案：moved
题目：Will the AIDS patients benefit ______ the new drug?答案：from'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "结合上下文内容补全填空。" in browser.page_source:
        dxAnswer = '''子问题 1：assisting; 子问题 2：out; 子问题 3：most; 子问题 4：enabled; 子问题 5：asking for'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "英译汉" in browser.page_source:
            dxAnswer='''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：A; 子问题 5：C'''
        if "判断正误。" in browser.page_source:
            dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：F'''
        if "完成选择题。" in browser.page_source:
            dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：B; 子问题 4：A; 子问题 5：C'''

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
    dxAnswer = '''题目：— Can I ask you for some questions, Frank?答案：Sure, go ahead
题目：— I have a toothache.答案：Why don't you go to the dentist?
题目：— I'd like to invite you to my birthday party on Saturday evening.答案：Thank you for your invitation. I'm very happy to join the party.
题目：— What presents should I take to my friend for his house-warming party, Tom?答案：I advise a handy DIY tool box, which he can use in daily life.
题目：—Would you be interested in coming to the cinema with me tonight?答案：That's very kind of you. Thanks.
题目：All of these presents _________ good to me. 答案：sound
题目：At the presentation, there will be several students _______ recognition awards from the答案：receiving
题目：He refused _______ my suggestions.答案：to accept
题目：I'm ______ because there are so many options. I can't make a decision.答案：puzzled
题目：Many students at the school _______ on a project which relates to the unemployment答案：have been working
题目：There are a lot of _______for presents for birthday party.  答案：options
题目：We look forward to ______ to his wedding ceremony. 答案：coming
题目：We will invite Professor Johnson to ______ our conference next Monday. 答案：attend
题目：You can _____ some bottles of wine, or some chocolates, or a bunch of flowers.答案：bring along
题目：You make the reservation, and I'll _______it in writing. 答案：confirm'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "英译汉" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：B; 子问题 3：A; 子问题 4：A; 子问题 5：B'''
    if "补全对话内容" in browser.page_source:
        dxAnswer = '''子问题 1：D; 子问题 2：B; 子问题 3：A; 子问题 4：E; 子问题 5：C'''
    if "判断正误" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：T'''
    if "完成选择题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：B; 子问题 4：A; 子问题 5：B'''

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
    dxAnswer = '''题目：— ___________ ?— I wonder if you could practice interviewing with me in advance.答案：What can I do for you?
题目：— Are you confident enough?答案：Yes, I think being confident is one of my strong points.
题目：— Do you think you are the suitable person for this position?答案：Yes. I'm hard working and I think I am suitable for this position.
题目：—What kind of work have you been doing up to now?答案：I have been an English teacher for two years.
题目：—Why do you want to leave your previous job?答案：I'm hoping to have a better position.
题目：A successful cover letter will make a great _________.答案：impression
题目：I ________in the company since I came to the city. 答案：have worked
题目：I think I am _______ for this position.答案：competent
题目：It is good _______ chess after supper.答案：playing
题目：It will be a sad thing ______ with her. 答案：parting
题目：Provide any information specifically _______ in the job advertisement such as availability答案：requested
题目：The cover letter will be seen first. ________, it must be very well written.答案：Therefore
题目：Three short paragraphs are quite _________ when you write a cover letter. 答案：sufficient
题目：We can act ______ the interview.答案：out
题目：Your background is ________ to the position you are seeking. 答案：relevant'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "判断正误。" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：F'''
    if "英译汉" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：B; 子问题 5：B'''
    if "补全对话内容" in browser.page_source:
        dxAnswer = '''子问题 1：D; 子问题 2：A; 子问题 3：B; 子问题 4：E; 子问题 5：C'''
    if "完成选择题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：A; 子问题 4：C; 子问题 5：C'''

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


    # 5单
    dxAnswer = '''题目：- Do you often surf on the Internet?答案：Yes. I use it a lot.
题目：- Hey, what are you doing in that room?答案：I am preparing for the test next week.
题目：- Oh, amazing! Could you give me more information about it?答案：Sure. You can find more on this website.
题目：- The Internet is magic. Can we get everything from it?答案：Well, it is impossible. We put something, and we can get something out.
题目：– Putting on a happy face makes us feel better.答案：I agree with you.
题目：As long as the learners have ________ to a digital device which is linked up to the Internet,答案：access
题目：Baidu is good for Chinese searches, ________ Yahoo is better for searching data in English. 答案：while
题目：Company employees are expected to use the Internet in ________ with these rules.答案：line
题目：Emails sent through the company email system ________ not have content that is答案：should
题目：Entertainment is one of the ________ reasons people like the Web.答案：leading
题目：In doing so, they have opportunities to learn from professors they ________ would not be答案：otherwise
题目：It is common practice now ________ the web for resources and information for homework. 答案：to search
题目：Social apps like QQ or WeChat have become our ________ for staying connected with答案：means
题目：Surfing on the Internet has almost become a matter of ________.答案：routine
题目：There's ________ strange about you. That's all right.答案：nothing'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0

    if "阅读理解：结合上下文内容补全填空。" in browser.page_source:
        dxAnswer = '''子问题 1：set up; 子问题 2：broke down; 子问题 3：another; 子问题 4：1970s; 子问题 5：cheaper'''
        if len(browser.find_elements_by_xpath('//input[@type="text"]')) > 1:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
        else:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_class_name("custom-select"):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
    else:
        if "英译汉" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：B; 子问题 3：C; 子问题 4：A'''
        if "补全对话内容" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：E; 子问题 3：C; 子问题 4：A; 子问题 5：D'''
        if "判断正误" in browser.page_source:
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
    dxAnswer = '''题目： He played a Chinese folk __________ on the piano. 答案：melody 
题目： Never give up __________ your better life. 答案：striving for   
题目：__________ is forbidden in public places. 答案： Smoking
题目：— ______________ .—Oh, that's too bad.答案：I regret to say that we cannot make it on time.
题目：— How are you feeling today?答案：I feel a little sad.   
题目：—Honey, I regret quarreling with you.答案：So do I. 
题目：—You blame me for that, don't you?—No, _________________.答案：of course not.
题目：—You seem a little blue today. What's the matter?答案：It's been a difficult day.
题目：As one of family members, Lisa also pays a  __________of the rent, electricity and phone答案：share
题目：He speaks German, but his native  __________is French. 答案：tongue
题目：I don't regret __________ the concert yesterday because I am more willing to celebrate my答案：missing 
题目：I should __________ Alex this morning, but I forgot. 答案：have phoned
题目：My parents never let me __________ online games.  答案：play   
题目：She is due to  __________ a speech on the social work tomorrow. 答案：deliver
题目：You should stop __________ others down and learn from them. 答案：putting'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "结合上下文内容补全填空。" in browser.page_source:
        dxAnswer = '''子问题 1：ways; 子问题 2：lasting; 子问题 3：better; 子问题 4：was; 子问题 5：Secondly'''
        if len(browser.find_elements_by_xpath('//input[@type="text"]')) > 1:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
        else:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_class_name("custom-select"):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
    else:
        if "为句子选择正确的翻译" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：B; 子问题 4：A; 子问题 5：B'''
        if "判断正误" in browser.page_source:
            dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：F'''
        if "匹配段落大意" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：E; 子问题 3：A; 子问题 4：D; 子问题 5：B'''

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
    dxAnswer = '''题目： In a car accident, you should ________ the other car's number in order to report to the答案：keep in mind
题目： Keep an eye for your belongings in the bus station _______ they might be stolen by答案：in case
题目： We should provide useful information for the police no matter there is a ______ or not. 答案：reward
题目：— How can I get legal advice for free?答案：You can go to a law firm and ask about that.
题目：— I think riding a bike anywhere is healthy and convenient, but I'm afraid the bike would 答案：Why don't you take a lock with you?
题目：— Our trademark has been infringed by our competitor. What can we do?答案：You can file an action in the district court.
题目：— There are so many strange phone calls nowadays. I'm fed up with those calls.答案：you'd better be careful of the telecommunication frauds.
题目：— This is Huangdu police station. What can I do for you?答案：My daughter is missing.
题目：A car accident may happen when you ________ a parking space.答案：are looking for
题目：In a civil case, one party may file an action, the other party may or may not ____ the claim. 答案：admit
题目：Mary's talking to the lawyer about her competitor who ________ on her trademark.答案：is infringing
题目：The mother ________ her daughter for 2 hours. 答案：has been looking for
题目：The police officer is determining who is going to be responsible ______ the traffic答案：for
题目：This time tomorrow you _________ in the court for the trademark case. 答案：will be standing
题目：We have to collect enough evidence to show that we ________ a lot of damages. 答案：have suffered'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "英译汉" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：A; 子问题 4：C; 子问题 5：A'''
    if "补全文章内容。" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：B; 子问题 4：F; 子问题 5：E; 子问题 6：D'''
    if "判断正误" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：F'''
    if "完成选择题" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：A; 子问题 4：C; 子问题 5：C'''

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
    dxAnswer = '''题目： Juvenile delinquency ___________criminal acts committed by children or teenagers,答案：means
题目： Relationships and friendships can ________ gangs. 答案：lead to
题目：— _____________ .— I agree with you.答案：I think we should bring back death penalty for serious crimes.
题目：— I was robbed when I was travelling in India.— I am sorry to hear that.____________.答案：It seems that go travelling alone in India is not that safe for a young lady like you.
题目：— Our city is getting safer and safer.答案：I hope there will be no crimes any more.
题目：— There are more and more Internet crimes.答案：I think we should introduce more regulations to supervise the Internet.
题目：— There was a gunshot in the cinema last night.— I heard about it, and __ .答案： I hope there would be no more gunshot in the future.
题目：He _______________ because of breaking into a store. 答案：was punished
题目：He was held in the police station because he ___________ to an offence. 答案： linked 
题目：If I ______ the mayor of the city, I would introduce severe punishment for crimes. 答案：were
题目：Juvenile delinquency will be ______ by peer pressure. 答案：affected
题目：Several factors are ________ in the process of development.答案：at play
题目：The global network _______ by a single leak. 答案：can be destroyed
题目：The world has difficulty _______ web security. 答案：in keeping
题目：There are more and more crimes ______ a lack of rules and regulations. 答案：because of'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "结合上下文内容补全填空" in browser.page_source:
        dxAnswer = '''子问题 1：with; 子问题 2：after; 子问题 3：well; 子问题 4：when; 子问题 5：anything'''
        if len(browser.find_elements_by_xpath('//input[@type="text"]')) > 1:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
        else:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_class_name("custom-select"):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
    else:

        if "英译汉" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：C; 子问题 3：B; 子问题 4：B; 子问题 5：A'''
        if "判断正误" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：F'''
        if "完成选择题" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：B; 子问题 4：B; 子问题 5：C'''


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


xingkao1 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474332'
xingkao2 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474333'
xingkao3 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474334'
xingkao4 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474335'
xingkao5 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474336'
xingkao6 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474337'
xingkao7 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474338'
xingkao8 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474339'

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
    time.sleep(2)
