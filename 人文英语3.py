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
    dxAnswer = '''题目： —Do you have much experience with caring for babies?—    .	答案：Yes, I do. I often take care of kids in my free time.
题目： Lily is a good student except ________ she is a little bit careless.	答案：that 
题目：—How do you feel about your family life? —                      .	答案：Not bad. I think it is a good choice to be a full-time mother.
题目：—It's raining so heavily outside. I'm terribly anxious about my son's safety.—                      .	答案：Don't worry about him. He will come back safe and sound.
题目：—Ken did badly in his math test. I'm terribly worried about the result.—                      .	答案： Come on. It isn't the end of the world.
题目：—Our son has picked up some bad habits recently, and I am really worried about it.—                      .	答案：Cheer up. I believe he will overcome it.
题目：He asked me ___________ Zhang Hua came to school or not. 	答案： whether
题目：I want to know________ . 	答案：what his name is
题目：It is said that ______ 2000 factories were closed down during the economic crisis. 	答案： approximately
题目：The birth rate of the country decreases ______ with years.	答案：progressively
题目：This movie is ________ that one. 	答案：as interesting as
题目：Tom won the first prize of oral English contest, which is beyond his _.	答案：expectation
题目：We consider it necessary ______ Tom should improve his behavior.	答案： that 
题目：We often compare children ______ flowers.	答案： to
题目：Young people ______ 62% of University teaching staff.	答案：comprise'''
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
    if "选择题（每题" in browser.page_source:
        dxAnswer='''子问题 1：C; 子问题 2：B; 子问题 3：C; 子问题 4：B; 子问题 5：A'''
    if "正误判断" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：T; 子问题 4：T; 子问题 5：F'''

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
    dxAnswer = '''题目： —Do you mind if I record your lecture?—                      .	答案：No，not at all.
题目： —Linda, what's wrong with your grandmother?—                      .	答案：She hurt her leg.
题目：—I'm sorry to hear that your grandmother is ill in hospital.—  	答案： It's very kind of you.
题目：—Is your grandmother getting well now?—                      .	答案：Yes, she is much better now.
题目：—Looking after a baby is not an easy job, is it?—                      .	答案：No, it isn't.'''
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
    if "阅读短文" in browser.page_source:
        dxAnswer='''子问题 1：A; 子问题 2：B; 子问题 3：B; 子问题 4：A; 子问题 5：C'''

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
    dxAnswer = '''题目： He asked John ______ he could swim.	答案： if 
题目： He is worth ____________.	答案：trusting
题目：John asked me _______ to visit his uncle's farm with him.	答案：whether I would like
题目：She _________ the children not to make any noise.	答案：told 
题目：She is a ___________ woman. 	答案：confident young
题目：She said she __________ lost a pen.	答案：had
题目：There is only one thing that people can't _____________you, and that is your wisdom.	答案：take away from
题目：We found him ___________ in the laboratory.	答案： working
题目：We must keep our classroom _____________.	答案：clean
题目：You'd better ________ to hospital at once. 	答案：go'''
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
    if "选择题（每题" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：C; 子问题 3：A; 子问题 4：B; 子问题 5：B'''
    if "正误判断" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：T; 子问题 4：F; 子问题 5：F'''

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
    dxAnswer = '''题目： I have trouble in ________ my homework. 	答案：doing
题目： This plant can't be exposed ____________strong sunshine.	答案：to
题目：– Brand was Jane's brother!–          he reminded me so much of Jane!	答案：No wonder 
题目：– How about going to the cinema?– ___________	答案： Sounds like a good idea!
题目：– May I open the window to let in some fresh air?–______	答案：Go ahead!
题目：– Ok, I'll fix your computer right now.– Oh, take your time. _____	答案：I'm in no hurry.
题目：– Susan, will you please go and empty that drawer?  –   	答案： What for？
题目：A dictionary may define genetics _________ simply “the science of the study of heredity”.	答案：as
题目：He asked his neighbor to ________  his house.	答案：keep an eye on
题目：People __________ foxes __________ clever but sly animals. 	答案：consider…as'''
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
        dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：B; 子问题 5：B'''
    if "正误判断" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：T'''

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
    dxAnswer = '''题目： I have no idea _____ to make my speech interesting.	答案：how  
题目： My suggestion is that Tom _____ to see a doctor at once. 	答案：go
题目：- I'm sorry for breaking the cup.- Oh, ____ . I've got plenty.	答案：forget it
题目：-I've been using the computer for a long time and my neck doesn't feel well.-____________________	答案：You'd better stop the work and take a rest.
题目：-It's rather cold in here. Do you mind if I close the window?-_______.	答案：No, go ahead
题目：-Must I finish the report today?-_____. You can finish it tomorrow.	答案：No, you don't have to
题目：-We've worked for a long time, what about stopping a while to have a rest?-_____________________.	答案：That's a good idea.
题目：Does the design _____ the needs of our users? 	答案：meet
题目：He left the company by mutual ______ last September. 	答案：consent
题目：Nowadays people spend more time exercising to keep _____. 	答案：fit
题目：Parents transmit some of their _____ to their children. 	答案：characteristics 
题目：People wear _____ suits on formal occasions.	答案：formal 
题目：The company is trying every _____ to improve the quality of products. 	答案：means
题目：The news came _____ we won the first prize in the competition. 	答案：that  
题目：We have worries _____ we'll miss the best selling season of the skirts. 	答案：that '''
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
    if "翻译" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：A; 子问题 4：C; 子问题 5：A'''

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
    dxAnswer = '''题目： ___________ was not very wise.	答案：Telling her the truth
题目： _________, the number of private cars will increase sharply in the coming couple of years. 	答案：Undoubtedly
题目： Hardly had the train arrived at the destination when the passengers ________ out in no time. 	答案：flooded
题目： It is an open secret _____he is not a qualified manager. 	答案：that 
题目： The more people you know, ___________ knowledge you get. 	答案：the more
题目：Good friends means sharing happiness but also sadness ____ each 	答案：with
题目：It is in the afternoon _______ he got the bad news.	答案：that
题目：This is an opportunity to _______ the reputation of the company. 	答案：enhance
题目：Without your help, I ______ obtained today's success. 	答案：would not have
题目：You'd better        listening to the teacher in the lesson.	答案：pay attention to'''
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
    if "选择题（每题" in browser.page_source:#选择题（每题
        dxAnswer = '''子问题 1：D; 子问题 2：B; 子问题 3：E; 子问题 4：A; 子问题 5：C'''
    if "正误判断" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：F'''

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
    dxAnswer = '''题目：_________ we've no money, we can't buy it.	答案：Since
题目：Apple developed its iPad-based textbooks in ____________ with major textbook publishers.	答案：conjunction
题目：But the Internet can bring some ________ effects, too. The most common one, some teenagers are addicted to computer games on the Internet. 	答案：negative
题目：I have _________ some courses and software to my Smartphone, and I find they are very interesting and easy to use. 	答案：downloaded
题目：No more having to buy expensive textbooks which you will only use for a year or two and then sell or _______ away. 	答案：give
题目：Quizzes are part of the lecture program to keep students engaged and keep them _________, for students to be able to check that they understood what was covered.	答案：thinking
题目：Smartphone makes it simple ________ us ________ take a photo. 	答案：for…to
题目：Some universities offer free, non-credit MOOCs __________ to anyone in the world.	答案：available
题目：We can certainly deliver high-quality education to many students at much ________ cost.	答案：lower
题目：Well, that's to say, every coin has two sides, ________ technology.	答案：so does '''
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
    if ">判断题" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：F'''
    if "选择题（每题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：B; 子问题 4：A; 子问题 5：C'''

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
    dxAnswer = '''题目： I hope you are making ________ for continuous education in your life. 	答案：room
题目： Mr. Wang, _________, is coming up to us.	答案：our new teacher 
题目： One big         of formal education is the high cost. 	答案：disadvantage
题目：_________ the regular classes, you can also attend many different seminars and take part in many extracurricular activities. 	答案：Apart from
题目：– Did you enjoy your college life?– ______	答案：Yes, it was rich and colorful. 
题目：– How long have you been graduated from your college?–         	答案： I've been graduated for five years.
题目：– I often feel lonely when I engage in my online learning. ________I join the online course community.	答案：How do you solve this problem?
题目：– The advancement of technology has boosted the pace of our lives, and requires us to learn something new every day.答案：That is the reason why
题目：– What are your great strengths?–                      	答案：I am very active in discussion.
题目：By making learning possible anytime and anywhere, distance education is a powerful tool _________ supporting lifelong learning. 	答案：for 
题目：I have just finished the        in the online forum. 	答案：discussion
题目：It is believed lifelong learning is a crucial response to the challenge of the global ________ economy. 	答案：knowledge
题目：Lifelong learning is both formal and non-formal; and the boundaries between face-to-face teaching and ___________ education are increasingly blurred. 	答案：distance
题目：The advancement of technology has boosted the pace of our lives, and requires us to learn ___________ every day just to stay current in the workplace. 	答案：something new
题目：The fact ________ that we are behind the other classes.	答案：remains '''
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
    if "判断正误" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：T; 子问题 5：T'''

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


xingkao1 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474416'
xingkao2 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474417'
xingkao3 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474418'
xingkao4 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474419'
xingkao5 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474420'
xingkao6 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474422'
xingkao7 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474421'
xingkao8 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474423'

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
