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
    dxAnswer = '''题目：— Hi! How are you doing? — ________________	答案：I'm doing well.
题目：—Albert, this is Jim.     —______________ Jim?	答案：How do you do,
题目：—Hi, Wang Xin，nice to meet you!  —Hi, Liu Hui, ________________	答案：nice to meet you too.
题目：—How about going to the class together? —_______________	答案：That sounds great.
题目：—What is your major? —_______________	答案：Education.
题目：Bai Mei don't know Liu Hui, so Zhuang Hua _________ her to Liu Hui. 	答案：introduce
题目：I _____________ an Open University student.	答案：am
题目：I enjoy__________ books in the library.	答案：reading
题目：I would _________ any weakness and any fear.	答案：overcome
题目：People can't live without____________ sun.	答案：the
题目：She is ____________ General Manager of___________ big company.	答案：the, a
题目：Social workers should learn how to _________ people.	答案： look after
题目：They _____________ some social work at the weekends.	答案：do
题目：They work in the same company and they are __________ with each 	答案：familiar
题目：When you feel _________, you should go to see a doctor.	答案：sick'''
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
    if "翻译题" in browser.page_source:
        dxAnswer='''子问题 1：C; 子问题 2：A; 子问题 3：C; 子问题 4：B; 子问题 5：B'''
    elif "判断正误题" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：T'''
    elif "完形填空题" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：A; 子问题 5：C'''
    elif "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：C; 子问题 3：C; 子问题 4：B; 子问题 5：B'''

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
    dxAnswer = '''题目：- Are you a member of the _________?  - I'm her brother.	答案：household
题目：- Can we _________ you anything? Coffee? Whiskey? -No，thank you.	答案：offer
题目：– I can show you around, if you like.– ________________	答案：Sure. Thank you.
题目：– What is so special about this Social Work Center?– _________________	答案：It offers help to homeless people.
题目：–Are you settling in well here in this city?– _________________	答案：Everything is going OK. Thank you!
题目：–Do you like seafood.– _________________	答案：Not really.
题目：–Thank you for sharing this with me.– _________________	答案：My pleasure!
题目：I saw him _________, and afterwards he was caught by the police.	答案：steal
题目：The number of these families has increased ______ 40 percent in the past ten years. 	答案：by
题目：They live next to this mountain for _________. 	答案：generations
题目：They must try to _________ the boundaries of knowledge. 	答案：extend
题目：We lived in the same village then and had an amazing _________	答案：childhood
题目：Well, I heard him _________ he'd cover the afternoon shift.	答案：say
题目：Well, I hope you _________ coming to the party tomorrow afternoon.	答案：are all
题目：You'll _________ have your own room.	答案：each'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()#find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1
        print(dxindex)

    listAnswer2=[]
    dxindex=0
    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：part-time; 子问题 2：special; 子问题 3：need; 子问题 4：look after; 子问题 5：cool'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1

    else:
        if "判断正误题" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：T; 子问题 5：T'''
        if "填空题" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：E; 子问题 3：D; 子问题 4：B; 子问题 5：A'''
        elif "翻译题" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：B; 子问题 4：A; 子问题 5：B'''

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
    dxAnswer = '''题目：______recent report stated that the number of Spanish speakers in the U.S .would be higher than the number of English speaker by_____ year 2090.	答案：A, the
题目：— Haven't seen you for ages, Mike. ________________?— Pretty good. Everything goes well.	答案：How's it going
题目：— Hi, Tom, how's everything with you?— ________, and how are you?	答案：Hm, not too bad
题目：—Oh, no! It's raining. We can't go skating on the square.— ________	答案：What a shame !
题目：—Shall we play football after class together?—______ _______	答案：Great, that's a good idea.
题目：—Tomorrow will be fine. Shall we go out for a picnic?—___________.	答案：Sounds great
题目：A student will probably attend four or five courses during each _______.	答案：semester
题目：He ________ her a beautiful hat on her next birthday.	答案：is going to give
题目：He is respected as a very aggressive and ________ executive.	答案：competitive
题目：I would like to do the job ________ you don't force me to study.	答案：as long as
题目：If it rains tomorrow, we _________ to picnic.	答案：won't go
题目：Jim is one of the most popular ________ in my company.	答案：colleagues
题目：The train is running fifty miles ______.	答案：an hour
题目：Tom is good at playing ________ piano.	答案：the
题目：We can't afford a bicycle, ________a car. 	答案：let alone'''
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
    if "听录音" in browser.page_source:

        if len(browser.find_elements_by_class_name("custom-select")) > 0:
            dxAnswer = '''子问题 1：on your mind; 子问题 2：the beginning of; 子问题 3：get along with; 子问题 4：Try your best; 子问题 5：make friends'''
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_class_name("custom-select"):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
        else:
            dxAnswer = '''子问题 1：mind; 子问题 2：beginning; 子问题 3：sure; 子问题 4：best; 子问题 5：friends'''
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
    else:
        if "判断题" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：T; 子问题 4：F; 子问题 5：T'''
        else:
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
    dxAnswer = '''题目：______________he left school at 16, he still managed to become a great writer.	答案：Even though
题目：–Happy New Year!– ________________	答案：The same to you.
题目：–What will you buy for the Spring Festival?– ________________	答案：I will buy gifts for my family.
题目：–Would you like to come to my house for dinner Sunday night?– _____	答案：All right! Thanks for inviting me.
题目：–Would you mind joining us?– _________________	答案：No, of course not.
题目：Everything in it ___________ that Jacob is a Christian.	答案：suggests
题目：He______________ to Shanghai for I saw here a minute ago.	答案：can't have gone
题目：I am very familiar with him, so I recognized his voice ___________.	答案：immediately
题目：I thought you_______ like something to read. So I have brought you some books.	答案：would
题目：It's been a(n) ___________ tradition ever since. People celebrate it every year.	答案：annual
题目：Many western festivals are ___________ at the very beginning.	答案：religious
题目：Peter_______ come with us tonight, but he isn't very sure.	答案：may
题目：The Mid-Autumn Festival falls on the fifteenth day of the eighth ______ month.	答案：lunar
题目：This is not like him. Something_______ be wrong.	答案：must'''
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
    if "填空" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：D; 子问题 3：A; 子问题 4：E; 子问题 5：B'''
    elif "判断正误" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：T; 子问题 5：T'''
    else:
        dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：A; 子问题 4：C; 子问题 5：B'''

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
    dxAnswer = '''题目： The street is ________ for five cars to go side by side.	答案：wide enough
题目：_______ students are playing on the ground.	答案：A number of
题目：— Morning, boys and girls! Please try your best in today's exam! Good luck to all of you!— ________________	答案：Thanks!
题目：—Congratulations! I just heard the news about your promotion.—____	答案：Thank you.
题目：—I was worried about my driving test, but I passed it.— __________	答案：Congratulations! That's not easy.
题目：—I won the first prize in today's speech contest.— _____________	答案：Congratulations!
题目：—You won the first prize in the Physics competition.—__________________. I made several terrible mistakes.	答案：You must be joking
题目：As a result of his hard work, he has gained ________ to the Beijing University. 	答案：admission
题目：Our classroom is___________beautiful than theirs.	答案：much more
题目：The CEO ________ that Tony was appointed as the manager of the marketing department in today's meeting.	答案：announced
题目：The higher the temperature is, __________ the liquid evaporates.	答案： the faster
题目：The novel I bought last week is_______ of reading, I think.	答案：worthy
题目：They got there an hour __________ than the others.	答案：earlier
题目：Tom is considered to be _________ the other students in her class.	答案：as intelligent as'''
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

    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：mail; 子问题 2：letter; 子问题 3：August; 子问题 4：visa; 子问题 5：wonderful'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "翻译题" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：A; 子问题 5：A'''
        elif "判断题" in browser.page_source:
            dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：T'''
        else:
            dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：C; 子问题 4：B; 子问题 5：A'''

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
    dxAnswer = '''题目：—Are you ready to take a ride in my new sports car?—                      .	答案：Yes, I'd love to.
题目：—Ok, I'll drink my last can of beer when I drive home.—               	答案：No way. You'll be stopped by the police.
题目：—Seat belts save lives.—               	答案：It's true. I agree.
题目：—Though I have been drinking, I can drive home safely.—No, I will be the driver.	答案：When you drink, you can't drive.
题目：—Why did you stop my car, police officer?—You just ran a red light.     	答案：Your driver's license please.
题目：Don't forget to ___________ your seat belt when you're driving.	答案：put on
题目：He ______ in jail because he broke the traffic law last night.	答案：drank
题目：He suggested that the drunk driver _________.	答案：be punished
题目：John ________ three bottles of beer just now, so he can't drive himself home now.	答案：did drink
题目：The _________ driver was seriously hurt in the traffic accident.	答案：40-year-old
题目：The __________ were shocked to see the workers pulling the car along the street.	答案：passers-by
题目：The couple was _________ that they could not drive home.	答案：so drunk
题目：The police asked the driver to __________ the car to have an alcohol test.	答案：pull over
题目：You'd better ____________ the car because you are drunk.	答案： let me drive'''
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
    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：ride; 子问题 2：drinking; 子问题 3：lives; 子问题 4：safer; 子问题 5：safely'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "翻译题" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：B; 子问题 4：A; 子问题 5：C'''
        if "判断题" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：F'''
        if "完型填空" in browser.page_source or "阅读理解：完形填空" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：B; 子问题 4：C; 子问题 5：C'''

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
    dxAnswer = '''题目：____ day of June is International Children's Day.	答案：The first
题目：____she wins  ____loses, this is her last chance. 	答案：Whether……or
题目：—But actually, I'm at work. So rather not wait. Would you mind taking a message?—. Go ahead.	答案：No, not at all.
题目：—Hello, Can I speak to Liu Hui, please?—____________________	答案：Yes, speaking.
题目：—Hello, May I speak to Zhang Hua?—___________________I'm afraid he isn't in at the moment.	答案：One moment, please.
题目：—Is that Jim speaking?—No.___________________	答案：This is Tom.
题目：—Social Work Service Center!—Hello, May I speak to Zhang Hua? 	答案：Can I help you ?
题目：Bankers were __________ of  a world banking crisis.	答案：fearful
题目：He made up a good __________for staying at home.	答案：excuse
题目：He usually __________from headache.	答案：suffers
题目：Listen! The baby ____ in the next room.	答案：is crying
题目：The government ____them with accommodation. 	答案：provides
题目：The old lady __________Tom for breaking the window. 	答案：blamed
题目：The pace of __________ growth is picking up.	答案：economic
题目：You are ____ to finish your homework on time. 	答案：supposed'''
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

    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：F'''
    elif "翻译题" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：B; 子问题 4：A; 子问题 5：C'''
    elif "填写主题句" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：E; 子问题 4：C; 子问题 5：D'''
    elif "完型填空" in browser.page_source or "阅读理解：完形填空" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：A; 子问题 4：B; 子问题 5：C'''

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
    dxAnswer = '''题目：—                — It's dark brown.	答案：What color is his hair?
题目：—                     — Less than 50 miles per hour.	答案：How fast were you driving?
题目：—Did you see the car before it hit you?—                  	答案：No, I didn't.
题目：—How about his weight?—                 	答案：Medium, maybe a bit on the heavy side.
题目：—Which direction were you heading?—                    	答案：I was heading from east to west.
题目：He gave no _______ of being a suspect.	答案：indication
题目：Kids must __________ when they walk to school.	答案：be on their guard
题目：The case happened _________ Tuesday afternoon.	答案：on
题目：The firefighters are going to ______________ the cause of the fire.	答案：look into
题目：The girl _____________ the case to the staff when her parents arrived.	答案：was reporting
题目：The gunman stood ____________ the theatre and shoot at the audience inside.	答案：at the front of
题目：The police saw him _________ on the ground when they arrived.	答案：lying
题目：The schools informed the parents _____ the case immediately.	答案：of
题目：The traffic accident _________ three days ago.	答案：took place
题目：They often saw me ____________.	答案：out and about'''
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
    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：traffic accident; 子问题 2：too fast; 子问题 3：driving; 子问题 4：coming from; 子问题 5：check on'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "翻译题" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：B; 子问题 4：A; 子问题 5：C'''
        elif "判断正误题" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：T; 子问题 5：F'''
        else:
            dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：C; 子问题 4：B; 子问题 5：A'''

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


xingkao1 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474515'
xingkao2 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474516'
xingkao3 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474517'
xingkao4 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474518'
xingkao5 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474519'
xingkao6 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474520'
xingkao7 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474521'
xingkao8 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474522'

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=option)
browser.maximize_window()  #max_window

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
