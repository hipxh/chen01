#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import bs4
from selenium import webdriver
import os

from selenium.webdriver.common.keys import Keys
from browsermobproxy import Server
import requests
import uuid

studyName = os.path.basename(__file__).split('.')[0]


# 其中一张试卷全部为富文本提交
def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele


def getAnswerElementEquals(elements, neirong, i, meidaotiyouduoshaogexuanxiang):
    for ele in elements:  # or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
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
    result = {}
    split = answer.split("\n")
    for i in split:
        i = i.split("题目：")[1]
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
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：—                      — Please call me Mary. That's my first name.	答案：How shall I address you?
题目：— Excuse me,                      — Yes, it's 8633-2788. If you have any other questions, don't he sitate to ask.	答案：could you please tell me what's the telephone number on my desk?
题目：— Hello, I'm David Chen. Nice to meet you.—                      .	答案：Nice to meet you too.
题目：— Hi, I'm Melinda Smith, the new secretary. Nice to meet you here.— Hi, I'm Mike Brown from the Training Center.                 	答案：I hope you'll be happy working here.
题目：— Sally,                  , Mary Brown.— Nice to meet you. I'm Sally Johnson, the Sales Manager.	答案：this is our new secretary
题目：“Isn't it impolite to call people by their first names?” The underlined word is of the same word class as         .	答案：interesting
题目：Don't be afraid         ask a lot of questions.	答案：to
题目：Hello, everyone. I'd like to         to you our new secretary, Melinda Smith.	答案：introduce
题目：I like the working atmosphere here.It's very         . 	答案：friendly
题目：I think          is impolite to call people by their first names.	答案：it
题目：I'm looking forward to          together with you.	答案：working
题目：If you have any questions here, please tell us. We'll all be          to help you.	答案：ready
题目：Keeping eye contact makes the other person          welcome and comfortable.	答案：feel
题目：People here usually          each other by their first names instead of family names.	答案：call
题目：Smile a lot and be         friendly as possible to everyone you meet.	答案：as'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 3)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "翻译：从以下A" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：A; 子问题 4：B; 子问题 5：A'''
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
        dxindex += 1

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
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目： —        ?— My mother is retired. My father is a manager. 	答案： What do your parents do.
题目： Children under fifteen are not permitted to see such kind of movies ______ bad for their mental development.	答案：as is
题目：－ What is your job? － I'm ____________ accountant.	答案：a
题目：— I'd like to apply for a library card.  —             	答案： Fill out the application form first, please.
题目：— It's rather cold in here. Do you mind if I close the window?— ____	答案：No, go ahead. 
题目：— May I use your bike for a moment?—                      .	答案：By all means.
题目：— Wow, this place is amazing.— ________________	答案：Thank you.
题目：Charles regretted __ the TV set last year. The price has now come down.	答案：buying
题目：Had you come five minutes earlier, you ____ the train to Beijing. But now you missed it.	答案：would have caught
题目：How do I _______ the gym? （考点：动词词组的使用）	答案：get to
题目：I have been looking forward to       from my parents. 	答案： hearing
题目：I'm a deputy manager. I ________ an IT company. 	答案：work for
题目：It's high time that he settled down in the country and ______ a new life. 	答案：started
题目：Professor Smith promised to look ______ my paper, that is, to read it carefully before the defense. 	答案：over
题目：With his work completed, the manager stepped back to his seat, feeling pleased ______ he was a man of action.  	答案：that'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath(
                    "./../input[last()]").click()  # find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1
        print(dxindex)

    listAnswer2 = []
    dxindex = 0
    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：part-time; 子问题 2：special; 子问题 3：need; 子问题 4：look after; 子问题 5：cool'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1

    else:
        if "翻译：从以下A、B、C" in browser.page_source:
            dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：C; 子问题 4：B; 子问题 5：A'''
        if "完形填空：阅读下面的短文，根据文章内容从A、B、" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：C; 子问题 5：B'''
        if "阅读理解：阅读下面的短文，根据文章内容从A、B、C" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：C; 子问题 4：B; 子问题 5：A'''
        if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确为“T”，错误为“F”" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：T; 子问题 4：F; 子问题 5：T'''

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
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：       your plan and don't stop until it is finished.	答案：Follow
题目：______ has not yet been decided. 	答案：When to hold the meeting
题目：—                     — I'm not sure what I'll do. I hope to watch TV and enjoy myself.	答案：What are your plans for summer vacation?
题目：—                      — Nothing much.	答案：What's up?
题目：—                       — I'm afraid not. But I'll be free this afternoon. 	答案：Can you spare me a few minutes now?
题目：— Hey, Derek, which do you think is harder to learn, marketing or designing?—                       	答案：Personally, I think designing is more difficult.
题目：— We'll have a charity book sale together with Menglin Publishing House next month.                     — Yes. I think the Music Square is large enough. 	答案：Could you give any suggestion on the location?
题目：She hasn't the funds to        her design.	答案：carry out
题目：She kept on ______  although she was tired.	答案：working
题目：The work was done        her instructions.	答案：according to 
题目：Through the work plan, the team leader is able to ______ the tasks at hand, the deadlines for completion, and the responsible parties for effective management.	答案：identify
题目：Within the team, a work plan can tell each member what ______ and why.	答案：is being done
题目：You can pick a specific time and place and ask them ______ they want to go.	答案：if
题目：Your goal is to publish a book and have _____ manuscript sent out to publishers by November 2016.	答案：the'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "听录音" in browser.page_source:

        if len(browser.find_elements_by_class_name("custom-select")) > 0:
            dxAnswer = '''子问题 1：2; 子问题 2：1; 子问题 3：0; 子问题 4：3; 子问题 5：4'''
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
        if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：T'''
        if "听力理解：请听下面的对话，根据对话内容进行判断，正确写“T”错误写“F”" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：T; 子问题 4：F; 子问题 5：F'''
        if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：C; 子问题 4：A; 子问题 5：B'''
        if "翻译：从以下A、B、C三个选项中选出与英文最适合的中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：B; 子问题 4：C; 子问题 5：A'''

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


def writeAnswer4(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：______, after introduction, you can ask about their journey.	答案：To break the ice
题目：—                      — It takes about 3 hours .	答案：How long will the journey take ?
题目：—  — It's lovely. I have never been to such beautiful place like that.	答案：How about your trip?
题目：—             — Please accept my sincere regrets for not being able to join you.	答案：I'm just wondering if you could come to join us.
题目：— Do you have any plans for tomorrow morning?—      	答案：No. I have nothing planned tomorrow.
题目：— I'd like to invite you for dinner on Saturday.—         	答案：Thank you for your kind invitation. I'll be there on time.
题目：A good tour guide tells visitors  ______.	答案：What they couldn't miss during the trip
题目：If there are changes, don't forget _____ the related persons know. 	答案：to let
题目：On their arrival, you should ______the following points.	答案：pay attention to
题目：Scientists have made great contributions        development of our human beings.	答案：to
题目：She feel very tired and was glad to        him.	答案：lean on
题目：The environmentalists and wild goats’ ______ on the vast grasslands was a good indication of the better environment.	答案：attendance
题目：The Two parties made it clear that they would not _____ the invitation unless the Centre reduced its tax component. 	答案：accept
题目：We have to       at the hotel before 6 pm.	答案：check in'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
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
        dxindex += 1

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
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目： I'm afraid I won't be available then. I ____ a friend off at five this afternoon.	答案：will be seeing
题目：— Dad, this is my roommate, Andrea.— ________	答案：Hello, Andrea. I've heard so much about you.
题目：— Hello, I'd like to speak to Phil.— He's out to lunch now. _______ 	答案：Would you mind calling back later?
题目：— I would like to make an appointment for the meeting. Which day would you prefer, Tuesday or Thursday?— _____ 	答案：Well, either time will do.
题目：— Mom, must I finish my homework now?— No, you ______. You may have supper first.	答案：needn't
题目：— Unbelievable! I have failed the driving test again! — _________________This is not the end of the world.	答案：Cheer up!
题目：— Would you mind helping me for a minute, Barbara?— _________________What do you want me to do?	答案：I'd be glad to.
题目：Can we ______ another worker to help Jimmy or find another solution?	答案：assign
题目：He has been looking forward to _____ to England for a long time.	答案：going
题目：Mr. White ______ short stories, but he ______ a TV play these days. 	答案：writes, is writing
题目：The company hosted a(n) ______ for their new staff.	答案：reception
题目：The question never ______ in discussion.	答案：came up
题目：They were successful ______ a communication satellite.	答案：in launching'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0

    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：mail; 子问题 2：letter; 子问题 3：August; 子问题 4：visa; 子问题 5：wonderful'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "完型填空：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项将其补充完整" in browser.page_source:
            dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：A; 子问题 4：C; 子问题 5：B'''
        elif "听力理解：请听下面的对话，根据对话内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：A; 子问题 4：C; 子问题 5：B'''
        elif "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
            dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：F'''

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


def writeAnswer6(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：______ means to do what you should do on time.	答案：To be punctual
题目：—                      — The round-trip air fare for a person is only $188.	答案：What is the exact air fare?
题目：— Hello, this is John speaking. Could I speak to Mike?—                      	答案：Hold the line, please.
题目：— Hello. Sky Travel Agency. May I help you?—                        	答案：Yes, I'd like to make reservations to Beijing on the flight ZH8147 at 6:00 pm on December 19th.
题目：— May I speak to Tom?— I'm sorry. He isn't in the office now.—                                         — Yes, of course.	答案：Can I leave a message？
题目：— This is Melinda speaking from Qiaoxiang Community Service Center. — Let me see. There will be some visits to our community library and learning center.	答案：I'm calling for the arrangement of the visit next Monday.
题目：Can you explain your arrangements        ?	答案：in detail   
题目：Do not do anything _____ should go against his will.	答案：that
题目：Do you require a deposit（定金）to        a reservation?	答案：confirm
题目：Mike ______ his colleagues when the phone rang. 	答案：was talking with
题目：Most tour companies ______ advance payment when a booking is made.	答案：insist on 
题目：She wants a job where ______ .	答案：her management skills can be put to good use
题目：This is true of management ______ of workers.	答案：as well as
题目：When will the General Manager be         ?	答案：available'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：ride; 子问题 2：drinking; 子问题 3：lives; 子问题 4：safer; 子问题 5：safely'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "完型填空：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项将其补充完整" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：A; 子问题 5：C'''
        if "翻译：从以下A、B、C三个选项中选出与英文最适合的中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：C; 子问题 5：B'''
        if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：A; 子问题 4：C; 子问题 5：B'''
        if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：F'''

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


def writeAnswer7(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：______the paperless management is widely used now, some important files are still kept as hard copies. 	答案：Although
题目：______you deal with the data files, the more familiar you get with them.	答案：The more
题目：—                    — I've called the maintenance worker.	答案：This copier needs repairing.
题目：—                    — It's my pleasure．	答案：Would you please fax the document for me?
题目：— Can you copy these papers for me?—                      	答案：Ok. Just wait a moment please.
题目：— I've got the system running, but I can't open my file.—            	答案：Let me see if I can get it to work.
题目：— Will you show me how to use this software?—            	答案：Sure. You'll master it in no time.
题目：A secretary must ______ big pile of files and correspondence in office.	答案：deal with
题目：Copying files under Linux is similar ______ copying files under DOS.	答案：to
题目：I'll make a list of all the documents on this file ______ make it more clearly. 	答案：in order to
题目：Mary has been a secretary in this company ______she graduated from Beijing University.	答案：since
题目：Nowadays office work can be done by hand ______ very fast speed.	答案：at
题目：Please see the suggestions below to ______ that your files are not lost.	答案：make sure
题目：Such office software is popular ______ the executive secretaries .	答案：with
题目：The secretary has a lot of things to take up in the office since she ______ away for quite a few days.	答案：has been'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0

    if "完型填空：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项将其补充完整" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：B; 子问题 4：A; 子问题 5：C'''
    if "听力理解：请听下面的对话，根据对话内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：C; 子问题 4：A; 子问题 5：A'''
    if "阅读理解：阅读下面的短文，根据文章内容进行判断，正确写“T”错误写“F”" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：F; 子问题 5：T'''

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


def writeAnswer8(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：________ wine do you need for the party?	答案：How much
题目：— Are you ready, folks?— ________________	答案：Yes, I'm ready. I'll have the vegetable salad.
题目：— Good morning, can I help you?— ________________ 	答案：I'd like to borrow a book named Gone With the Wind from your library.
题目：— Hello, Yang Lin speaking.— ________________ 	答案：This is Carol here.
题目：— Hey, You look so pale. What's wrong?— ________________	答案：I didn't sleep well last night.
题目：— Please give me a hand to print out the report, won't you?— ____	答案：Of course I will.
题目：Does David ______?	答案：like flying
题目：He ____ lunch in the canteen right now.	答案：is having
题目：He can ______________ good English.	答案：speak
题目：I have an English class          a week.	答案：three times
题目：I usually go to the office ________ train. 	答案：by
题目：It was on the beach ______ Miss White found the kid lying dead.	答案：that
题目：Neither John ________ his father was able to wake up early enough to catch the morning train.	答案：nor
题目：The Foreign Language Department is on _____ second floor.	答案：the
题目：You have more apples than _____ do. But _____ are better than yours.	答案：we, ours'''

    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "听录音" in browser.page_source:
        dxAnswer = '''子问题 1：traffic accident; 子问题 2：too fast; 子问题 3：driving; 子问题 4：coming from; 子问题 5：check on'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "翻译：从以下A、B、C三个选项中选出与英文最适合的中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：A; 子问题 2：A; 子问题 3：C; 子问题 4：B; 子问题 5：B'''
        if "听力理解：请听下面的对话，根据对话内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：A; 子问题 4：B; 子问题 5：B'''
        if "阅读理解：阅读下面的短文，根据文章内容从A、B、C三个选项中选出一个最佳选项" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：B; 子问题 4：A; 子问题 5：C'''

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
            browser.find_element_by_xpath('//i[@class="funGsClose closeBtn"]').click()  # find一下,保证新页面加载完成
        except:
            pass
        browser.get(xkurl)  # 先考形1
    else:
        return 0


# 2.立即考试.判断一下,防止多次考试
def readyToTest(browser):
    time.sleep(2)
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


def fill2SaveAnswer(_contentList):
    need = {}
    answers = []
    attempt = ''
    sesskey = ''
    contentType = ''
    for i in _contentList:
        o = {}
        o['Content-Disposition: form-data; name=\"' + i["name"] + '\"'] = i["value"]#.encode("utf-8")
        answers.append(o)
        if 'attempt' in i['name']:
            attempt = i["value"]
        if 'sesskey' in i['name']:
            sesskey = i["value"]

    need['answers'] = answers
    need['attempt'] = attempt
    need['sesskey'] = sesskey
    return need


def trans2text(answers,randomType):
    randomType = '--'+randomType
    finalStr=''
    for i in answers:
        for o in i.items():
            finalStr+=randomType
            finalStr+="\n"
            finalStr+=o[0]
            finalStr+="\n"
            finalStr+=o[1]
            finalStr+="\n"
    finalStr+=randomType
    finalStr+='--'
    return finalStr

def saveTest2GetAnswer(browser, proxy):
    proxy.new_har("guokai", options={'captureHeaders': True, 'captureContent': True})  # 准备抓请求
    time.sleep(66)
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(2)

    result = proxy.har
    randomType=''
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        print(_url)
        if "/processattempt" in _url:
            _request = entry['request']
            for head in _request['headers']:
                if 'Content-Type' in str(head):
                    for o in head.items():
                        for j in o:
                            if "bound" in j:
                                randomType = j.split('=')[1]

    print(randomType)









    for entry in result['log']['entries']:
        _url = entry['request']['url']
        print(_url)
        if "/autosave" in _url:
            _request = entry['request']
            _contentList = _request['postData']['params']  # 此时的请求参数相当于list,全部为正确答案
            _headers={'Referer': 'http://hubei.ouchn.cn/mod/quiz/attempt.php',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
'Accept-Encoding': 'gzip, deflate',
'Content-Length': '3592',
'Host': 'hubei.ouchn.cn',
'Connection': 'Keep-Alive'
}

            _headers['Cookie'] = _request['headers'][-1]['value']

            # randomType = '----WebKitFormBoundaryrUjxjyen'+str(uuid.uuid1()).split("-")[0]
            _headers['Content-Type'] = 'multipart/form-data; boundary='+randomType
            need = fill2SaveAnswer(_contentList)
            _headers2 = {'Referer': 'http://hubei.ouchn.cn/mod/quiz/summary.php?attempt='+need['attempt'],
'Cache-Control': 'max-age=0',
'Origin': 'http: // hubei.ouchn.cn',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Content-Length': '3592',
'Host': 'hubei.ouchn.cn',
'Connection': 'Keep-Alive'}
            file_write_obj = open("tempAns.txt", 'w')
            file_write_obj.write(trans2text(need['answers'],randomType))
            file_write_obj.close()
            files = {'file': open('tempAns.txt', 'rb')}
            r = requests.post('http://hubei.ouchn.cn/mod/quiz/processattempt.php',files=files, headers=_headers)
            print(r)
            time.sleep(2)
            _headers2['Cookie'] = _request['headers'][-1]['value']
            _headers2['Content-Type'] = 'application/x-www-form-urlencoded'
            r2 = requests.post('http://hubei.ouchn.cn/mod/quiz/processattempt.php',data='attempt=' + need['attempt'] + '&finishattempt=1&timeup=0&slots=&sesskey=' + need['sesskey'], headers=_headers2)
            print(r, r2)


# 等待三秒,让我们看到卷子已经答题提交完成,然后关tab,切到第一个tab,再进学习
def wait3AndCloseTab(browser):
    time.sleep(2)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1.5)


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439905'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439913'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439919'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439925'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439931'
xingkao6 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439937'
xingkao7 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439943'
xingkao8 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=439949'

dict = {'port': 39999}
server = Server(r'/Users/hanxu/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy', options=dict)
server.start()
proxy = server.create_proxy()

option = webdriver.ChromeOptions()
option.add_argument('--proxy-server={0}'.format(proxy.proxy))
option.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=option)
# browser.maximize_window()  #max_window

browser.get('http://student.ouchn.cn/')
browser.implicitly_wait(15)  # wait

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
            browser.find_elements_by_xpath('//input[@type="radio"]')[0].click()
            # time.sleep(1)
            # browser.find_elements_by_xpath('//input[@type="radio"]')[1].click()
            saveTest2GetAnswer(browser, proxy)
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
