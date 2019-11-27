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
    dxAnswer = '''题目：– Do you think I can borrow your bike for a few hours?答案：I'm sorry, but I really need it this afternoon.
题目：– Excuse me, could you tell the time?答案：It's three thirty by my watch.
题目：– Good afternoon. Can I help you?答案：I need to buy a birthday present for my son.
题目：– Hello, may I speak to John?答案：Just a second, please.
题目：– Thank you for your invitation.答案：It's a pleasure.
题目：As the bus came round the corner, it ran ________ a big tree by the roadside.答案：into
题目：Both the kids and their parents __________English, I think. I know it from their accent.答案：are
题目：Did you notice the guy _________head looked like a big potato?答案：whose
题目：John's father _________ mathematics in this school ever since he graduated from Harvard答案：has taught
题目：Never before _________ see such a terrible car accident on the road!答案：did I
题目：On average, a successful lawyer has to talk to several ________ a day.答案：clients
题目：Our house is about a mile from the railway station and there are not many houses答案：in between
题目：Professor Smith promised to look _ my paper, that is, to read it carefully before the答案：over
题目：What is the train ___________ to Birmingham?答案：fare
题目：When Lily came home at 5 pm yesterday, her mother ______dinner in the kitchen.答案：was cooking'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "排序题" in browser.page_source:
        dxAnswer='''子问题 1：C; 子问题 2：E; 子问题 3：A; 子问题 4：D; 子问题 5：B'''
    if "判断题" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：T; 子问题 4：F; 子问题 5：F'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：B; 子问题 4：C; 子问题 5：A'''

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
    browser.find_elements_by_xpath('//input[@name="next"]')[1].click()
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
    dxAnswer = '''题目：– How many languages does Peter speak?答案：Five languages.
题目：– Something went wrong with my television last night.答案：I'm sorry to hear that.
题目：– Would you like something to drink? What about a cup of tea?答案：No, thanks.
题目：– You are late. The discussion started 30 minutes ago.答案：I am really sorry.
题目：– Your ID card, please.答案：Here you are.
题目：_________ the War of Independence, the United States was an English colony.答案：Before
题目：Eggs, though rich in nourishments, have ________ of fat.答案：a large number
题目：Every year thousands of lives ________ in road accidents because of careless driving.答案：are lose
题目：Had you come five minutes earlier, you _________ the train to Birmingham. But now you答案：would have caught
题目：If she wants to stay thin, she must make a __________ in her diet.答案：change
题目：No matter _________, the little sisters managed to round the sheep up and drive them答案：how hard it was snowing
题目：The student were all entertained in a Mexican restaurant, at Professor Brian's ________答案：expense
题目：The young lady coming over to us _______ our English teacher; the way she walks tells us答案：must be
题目：Tom, what did you do with my documents? I have never seen such a ________ and答案：mess
题目：You shouldn't ________ your time like that, Bob; you have to finish your school work答案：kill'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "排序题" in browser.page_source:
        dxAnswer='''子问题 1：E; 子问题 2：B; 子问题 3：C; 子问题 4：A; 子问题 5：D'''
    if "选择题" in browser.page_source:
        dxAnswer='''子问题 1：B; 子问题 2：C; 子问题 3：A; 子问题 4：A; 子问题 5：C'''
    if "正误判断题" in browser.page_source:
        dxAnswer='''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：F'''

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


# 有两个选择题的题干一样，答案不一样
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
    dxAnswer = '''题目：- Good morning, sir. May I help you?答案：Yes, I need some salt.
题目：– I didn't know my identity card was needed, sir.答案：Sorry, but that's no excuse.
题目：Although he did not know London well, he made his way _____ to the airport.答案：easily enough
题目：-Can you go out with us for dinner this evening?答案：Thanks a lot, but I'm busy tonight.
题目：Do you know the man _______ under the apple tree?答案：lying
题目：-Excuse me, where is Dr Smith's office?答案：Sorry, I don't know. But you can ask the man over there.
题目：Harry, who had failed in the final exam, had a great worry ________ his mind.答案：on
题目：I don't know the park, but it's _________ to be quite beautiful. 答案：said
题目：Is the library ________ now? No, it's ______.答案：open; closed
题目：Mike is better than Peter ________ swimming. 答案：at
题目：Nancy is ________ girl.答案：an eighteen-year-old
题目：The baby is hungry, but there's ________ milk in the bottle.答案：little
题目：-These are certainly beautiful flowers. Thank you very much.答案：It's my pleasure.
题目：They have learned about _____in recent years.答案：hundreds of English words
题目：Two thousand dollars ____ enough for the car.答案：is'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "排序题" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：E; 子问题 3：C; 子问题 4：A; 子问题 5：D'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：A; 子问题 4：C; 子问题 5：C'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：C; 子问题 3：C; 子问题 4：A; 子问题 5：B'''

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


# 有两个选择题的题干一样，答案不一样
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
    dxAnswer = '''题目：— Can you tell me where I can park the car?答案：Well, just over there
题目：— Could I talk to Prof. Lee?答案：Yes, speaking 
题目：— I've got a bad cold today.答案： Oh, dear! I hope you get better soon
题目：— Sam, this is my friend, Jane.答案： Glad to meet you, Jane 
题目：— What's the matter with you?答案：I feel a bit sick
题目： I was giving a talk to a large group of people，the same talk I ___to half a dozen other答案：had given
题目： Neither John         his father was able to wake up early enough to catch the morning答案：nor
题目： The atmosphere            certain gases mixed together in definite proportions.答案：consists of 
题目： The new order means _____ overtime. 答案：working
题目： With his work completed, the manager stepped back to his seat, feeling pleased ____ he答案：that
题目：It is said that _____ boys in your school like playing football in their spare time, though答案：quite a few
题目：Jane's dress is similar in design            her sister's.答案：to
题目：She has two best friends. _____of them is in the country.答案：Neither
题目：The sports meeting was put off till the next week            rain.答案： because of
题目：Today's weather is _____worse than yesterday's.答案：much '''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "排序题" in browser.page_source:
        dxAnswer = '''子问题 1：E; 子问题 2：C; 子问题 3：D; 子问题 4：B; 子问题 5：A'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：C; 子问题 4：C; 子问题 5：C'''
    if "正误判断题" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：F'''


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
    dxAnswer = '''题目：— Can you help me clear up the mess?答案： No problem
题目：— Have a nice holiday, Ted.答案：Thank you, and you too
题目：— How was the journey to London?答案：It went very well
题目：— What's the best way to get to the Empire Hotel from here?答案： Walking through the wood
题目：— You needn't do the work till after the New Year.答案：Oh, good! Thank you.
题目： He is fond of playing ____ piano while his brother is interested in listening to ___ music. 答案： the; /    
题目： Important ________ his discovery might be, it was regarded as a matter of no account in答案： as  
题目：_______ her and then try to copy what she does.答案： Watch 
题目：_______ tomorrow's lessons, Frank has no time to go out with his friends. 答案： Not having prepared 
题目：__________ these honours he received a sum of money. 答案：Besides 
题目：A police officer claimed that the young man had attempted to __________ paying his fare.答案： avoid
题目：I want to buy a ______ wallet for him. 答案： small black leather 
题目：The young ______ interested in pop music. 答案：are
题目：This kind of material expands _________ the temperature increasing. 答案： with  
题目：Will you _____ me a favor, please?答案：do '''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "填写主题句" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：E; 子问题 3：A; 子问题 4：B; 子问题 5：D'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：A; 子问题 4：C; 子问题 5：B'''
    if "正误判断题" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：F; 子问题 5：T'''

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

# 有两个选择题的题干一样，答案不一样
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
    dxAnswer = '''题目：— Are you on holiday here?答案：No, we aren't. We live here 
题目：— Do you mind if I read the newspaper on the table?答案：Go ahead, please
题目：— Is it going to be warm next week?答案： Yes, it is 
题目：— What do you usually do in your spare time?答案：Reading
题目：— What's the fare to the museum?答案： Five dollars
题目： Would you like something ______________?答案：to drink
题目：_______________ is the population of Paris?答案：What
题目：As the busiest woman there, she made ______________ her duty to look after all the other答案：it
题目：Before the final examination, some students have shown ______ of tension. They even答案：signs
题目：It was getting __________, he had to stop to have a rest.  答案：darker and darker
题目：It's a good idea. But who's is going to _______ the plan?答案：carry out
题目：It's bad _____ for you to smoke in the public places where smoking is not allowed.答案：behavior
题目：The problem is not _____ so easy as you think. It's far from being settled.答案：nearly
题目：The wild flowers looked like a soft orange blanket ______________ the desert.答案：covering
题目：The young actor who had been thought highly of _______ to be a great disappointment.答案：turned out'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：A; 子问题 3：C; 子问题 4：B; 子问题 5：C'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：B; 子问题 4：C; 子问题 5：C'''
    if "正误判断" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：T'''


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


# 有两个选择题的题干一样，答案不一样
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
    dxAnswer = '''"题目：— Here you are, Sir.答案：Thank you very much
"题目：— May I speak to Prof . Li please?答案：I'm afraid you've got the wrong number 
"题目：— So sorry to trouble you.答案：It's a pleasure
"题目：— What does your English teacher look like?答案：She looks much like her mother
"题目：— Would you like a tea?答案：Yes, please
"题目：--Did the medicine make you feel better?--No. The more __________, ___________ I feel.答案：medicine I take; the worse
"题目：Have you ever visited the Summer Palace, _____ there are many beautiful halls, ridges答案：where
"题目：How can he _____________ if he is not _____________?答案：hear; listening
"题目：It is not until you have lost your health _____________ you know its value.答案：that
"题目：It's high time that he settled down in the country and __________ a new life.答案：started
"题目：The computer system ___________suddenly while he was searching for information on the答案：broke down
"题目：The film brought the hours back to me _________ I was taken good care of in that remote答案：when
"题目：The red flower goes from one to __________ in the class.答案：another
"题目：There's lots of fruit _________ the tree. Our little cat is also in the tree.答案：on
"题目：Two days is not enough for him to finish the work. He needs __________ day.答案：a third '''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：C; 子问题 4：A; 子问题 5：A'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：C; 子问题 4：A; 子问题 5：C'''
    if "正误判断题" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：T'''

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

# 有两个选择题的题干一样，答案不一样
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
    dxAnswer = '''"题目：— Have you ever been to Tokyo?答案：No, but I hope to go there next year
"题目：— How are you feeling now?答案：Much better
"题目：— How long will you be away from Italy?答案：About a month
"题目：— What time does the train leave?答案：At half past five
"题目：— What's the weather like in this area?答案：It's rainy
"题目：_____________ no need _____________ the radio as I'm used to studying with it on.答案：There's; turning off
"题目：All students are required to translate this poem ________English into Chinese.答案：from
"题目：By the year 2020, China's population probably _________1.4 billion.答案：will have reached
"题目：He studied hard at school when he was young, _________contributed a lot to his success.答案：which
"题目：He would be studying at the university now if he ________the entrance examination.答案：had passed
"题目：How much has the company ________________ this year?答案：brought in
"题目：In _____________, the northerners have a particular liking for dumplings while the答案：general
"题目：It is no use _________to remember only grammar rules.答案：trying
"题目：The old houses are being pulled down to ______________ a new office block.答案：make room for
"题目：This overcoat cost _______________. What's more, they are ________small for me.答案：too much; much too '''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1, value, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.2)
        dxindex += 1

    listAnswer2=[]
    dxindex=0
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：C; 子问题 4：B; 子问题 5：B'''
    if "选择题" in browser.page_source:
        dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：A; 子问题 5：B'''
    if "正误判断题" in browser.page_source:
        dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：T'''

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
        browser.find_element_by_xpath('//div[@class="help_close"]').click()  # find一下,保证新页面加载完成
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


xingkao1 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474590'
xingkao2 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474591'
xingkao3 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474592'
xingkao4 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474593'
xingkao5 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474594'
xingkao6 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474595'
xingkao7 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474596'
xingkao8 = 'http://guangzhou.ouchn.cn/mod/quiz/view.php?id=474597'

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

    # if enterTest(browser, xingkao1) != 0:
        # if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        #     writeAnswer1(browser)
        # wait3AndCloseTab(browser)

    # enterTest(browser, xingkao2)
    # if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer2(browser)
    # wait3AndCloseTab(browser)

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
