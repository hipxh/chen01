#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from selenium import webdriver
import os



studyName = os.path.basename(__file__).split('.')[0]


# 其中一张试卷全部为富文本提交
def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele


def getAnswerElementEquals(elements, neirong, key,i, meidaotiyouduoshaogexuanxiang):
    may = None
    for ele in elements:  # or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text
        _key = ele.text.replace(' ', '')
        _key = _key.replace(' ', '')
        if neirong == _key or "A." + neirong == _key or "B." + neirong == _key or "C." + neirong == _key or "a." + neirong == _key or "b." + neirong == _key or "c." + neirong == _key:
            may = ele
            if ele.find_element_by_xpath("./../../../../div[@class='qtext']").text[-3:] in key.strip():
                return ele
    return may

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

#111
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
    dxAnswer = '''题目：－How’s your mother doing?答案：She is very well
题目：— Do you mind if I record your lecture?— _________________. Go ahead.答案：Not at al
题目：— I was worried about my math, but Mr. White gave me an A.答案：Congratulations!
题目：—Can you go skating with us this afternoon? 答案：have to
题目：—I’m terribly sorry that I’ve spilled some coffee on the table.答案：It doesn’t matter
题目：—Would you like to go to the concert with us? 答案：I wish I could
题目：―Whose textbook is this?  ―It _______ John’s. It has his name on it.答案：must be
题目：He is ________ this company. 答案：in charge of
题目：He says what he thinks and does what he wants to do, ________ other people’s feelings. 答案：regardless of
题目：He was always ______ in sharing his enormous knowledge.答案：generous
题目：His action is always ______ with his words．答案：consistent
题目：More than 30 people ______ the position.答案：applied for
题目：One day, our dreams will ____________ reality. 答案：turn into
题目：The enemy has strengthened their ______ position.答案：defensive
题目：We think that Smith should be told about his ______ condition as soon as possible.答案：physical'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key, dxindex, 3)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0


    if "请听下面的对话" in browser.page_source:
        dxAnswer = '''子问题 1：meet; 子问题 2：call; 子问题 3：number; 子问题 4：really; 子问题 5：forward'''
        if len(browser.find_elements_by_class_name("custom-select")) > 0:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_class_name("custom-select"):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
        else:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
    else:
        if "The houses we live in are very" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：C; 子问题 3：A; 子问题 4：B; 子问题 5：C'''
        elif "There are more ants than any other kinds" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：A; 子问题 3：C; 子问题 4：C; 子问题 5：A'''
        elif "根据文章内容进行判断" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：T'''
        elif "中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：C; 子问题 3：A; 子问题 4：B; 子问题 5：A'''

        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
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
    dxAnswer = '''题目： Hiring a good employ may cost much money and time, _______, it can win much more for答案：however
题目：________  a company really wants is a candidate ________ has the right skills.答案：What…that
题目：My name is Helen, and I was born in 1980. My major was electrical engineering.答案：Tell me your name, please.
题目：—                     ？— I have worked for IBM for 3 years.答案：What is your working experience?
题目：— Hi, Helen, I’ll have an interview tomorrow. I’m afraid I can’t make it.答案：Sure, you can. Take it easy.
题目：—May I ask you why you left the former company？答案：Because I want to change my working environment and seek new challenges.
题目：—What starting salary do you expect?答案： I'd like to start at ￥5000 a month. 
题目：Hiring the right employee _ you ___ a thousand times over in high employee morale. 答案：pays…back
题目：I’m writing to ________ a position as a computer engineer in your company. 答案：apply for
题目：The candidate should dress in a manner that is appropriate to the position _ he is答案：for which
题目：These tips may help you avoid ________ bad employees for your company.答案：hiring
题目：We should take the degree ________ account when we recruit a new secretary.答案：into
题目：You also should send a resume ________ the employer know more information about you.答案：to let
题目：You can try these methods to keep your interview anxiety ________ control. 答案：under
题目：You must ________ the annual certification of employment online within 15 days. 答案：submit'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
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
    if "听录音222" in browser.page_source:
        dxAnswer = '''子问题 1：part-time; 子问题 2：special; 子问题 3：need; 子问题 4：look after; 子问题 5：cool'''
        if len(browser.find_elements_by_class_name("custom-select")) > 0:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_class_name("custom-select"):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1
        else:
            for an in dxAnswer.split("; "):
                listAnswer2.append(an.split("：")[-1])
            for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
                sel.send_keys(listAnswer2[dxindex])
                dxindex += 1

    else:
        if "中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：B; 子问题 3：A; 子问题 4：C; 子问题 5：A'''
        elif "Stress around interviews is often" in browser.page_source:
            dxAnswer = '''子问题 1：B; 子问题 2：B; 子问题 3：A; 子问题 4：A; 子问题 5：C'''
        elif "practice makes perfect" in browser.page_source:
            dxAnswer = '''子问题 1：A. so; 子问题 2：C. asked; 子问题 3：B. simply; 子问题 4：C. whether; 子问题 5：B. confidence'''
        elif "根据文章内容进行判断" in browser.page_source:
            dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：T'''

        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
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
    dxAnswer = '''题目： ______ you prepare cross training plans, you need to consider both the company benefits答案：As
题目：—______________________—Everything is going smoothly.答案：How is everything going?
题目：—______—In total, it should be about 15,000 RMB for the three-daytraining.答案：How much have you budgeted for the training?
题目：—_________—It might be a good idea to read some simplified books first. 答案：What books would you recommend?
题目：—Any suggestions for the project?—______________________答案：I advise you to put more hands in this project.
题目：—Should I leave earlier tomorrow morning?—______________________答案：Yes, it’s better to leave earlier to avoid the morning traffic.
题目：According to theirfeedback sheets, the participants are all _____with the training.答案：satisfied
题目：American young people would rather ______ advice from strangers.答案：get
题目：Anyone who has worked here for over three years is   for sick pay.答案：eligible
题目：Does his absence  to your work?答案：make a difference
题目：How many players does a baseball team？答案：consist of
题目：Participants have _____the Productivity Analysis Worksheet.答案：completed
题目：The training is _____positive results on the job they are presently _____.答案：bringing about, doing 
题目：We need to carry out a proper  of the new system.答案：evaluation
题目：Write the telephone number down you forget.答案：in case'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath(
                    "./../input[last()]").click()  # find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "听录音222" in browser.page_source:

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
        if "根据文章内容进行判断" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：T; 子问题 4：T; 子问题 5：F'''
        elif "PPHC and Gooseneck" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：B; 子问题 4：C; 子问题 5：A'''
        elif "Want to keep your staff" in browser.page_source:
            dxAnswer = '''子问题 1：A. offer; 子问题 2：C. Whatever; 子问题 3：B. ultimately; 子问题 4：B. needed; 子问题 5：C. continuing'''
        elif "中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：A; 子问题 4：B; 子问题 5：B'''

        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
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
    dxAnswer = '''题目：______ the feedback is very helpful for planning future meetings and events.答案：Getting
题目：—        ?— It will be held on the 3rd floor of Shakiraton Hotel.答案：What is the address of your speech
题目：— How do you think of the theme of our event?答案：It’s pretty good.
题目：— Let’s make plan first for our events, shall we?.  答案：OK, let’s do it.
题目：— What kind of event are you going to plan?答案：A birthday party for my brother.
题目：— Your plan is perfect and I believe that it will be a great success .答案：Thank you very much.
题目：Are you familiar ______the saying, “it’s not what you know, but who you know”? In答案：with
题目：At the end of the day, you want all attendees _____ your event to remember this key答案：leaving
题目：He keeps on his focus on      money.答案：making
题目：Let’s ______ our plan.答案：start
题目：The success of our event is____ to the sponsor.答案：related
题目：They have disagreement __the plan of celebrating the founding of the community.答案：on
题目：This involves ______ the high-level reasoning behind your intentions for the event.答案：identifying
题目：We should keep in mind        the feedback is very helpful for planning future meetings答案：that
题目：Your long-term success in event planning will be based       the experience you had.答案：on'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath(
                    "./../input[last()]").click()  # find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "中文翻译" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：B; 子问题 3：A; 子问题 4：C; 子问题 5：A'''
    elif "Successful and memorable" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：C; 子问题 3：B; 子问题 4：C; 子问题 5：A'''
    elif "Successful events don't" in browser.page_source:
        dxAnswer = '''子问题 1：B. planning; 子问题 2：A. bigge; 子问题 3：C. miss; 子问题 4：C. Whether; 子问题 5：B. appeal to'''
    elif "根据文章内容进行判断" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：T'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an.split("：")[-1])
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
    dxAnswer = '''题目：____ face-to-face interviews, questionnaires are cheaper for collecting data from a large答案：Compared to
题目：—                ?—Twice a week.答案：How often do you use our company’s product
题目：— Our company is doing a customer service questionnaire .May I take you a moment?答案：By all means
题目：— Thank you very much for answering our questions. It really helps our market research答案：It’s my pleasure.
题目：— What’s your view on our questionnaire_?_— ________________答案：First of all .We’d better change our question order.
题目：— Would you mind filling the questionnaire for me?答案：No problem. Just give me your questionnaire.
题目：Customers  ______ refuse to filling the questionnaire are not permitted to buy the答案：Who
题目：I’d like to_______ that the staff member who served me didn’t really seem to know答案：point out
题目：Our company will _____the customers’ suggestions.答案：respond to
题目：Questionnaires are easy to ____.答案：analyze
题目：Questionnaires are not suitable_____some people.答案：for
题目：The Jiahe Community Service Center is about to ______ service for residents.答案：provide
题目：The quality of questionnaire will_____how much information we know from our答案：affect
题目：Where are you used to____ vegetables?答案：buying
题目：You need to _____ those questionnaire papers for your company.答案：hand out'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath(
                    "./../input[last()]").click()  # find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0

    if "听录音222" in browser.page_source:
        dxAnswer = '''子问题 1：mail; 子问题 2：letter; 子问题 3：August; 子问题 4：visa; 子问题 5：wonderful'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：A; 子问题 4：B; 子问题 5：B'''
        elif "Questionnaires can be" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：C; 子问题 3：A; 子问题 4：A; 子问题 5：B'''
        elif "The qualities of a" in browser.page_source:
            dxAnswer = '''子问题 1：A. writing; 子问题 2：A. Secondly; 子问题 3：C. In order to; 子问题 4：B. In a word; 子问题 5：A. help'''
        elif "根据文章内容进行判断" in browser.page_source:
            dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：F; 子问题 5：T'''

        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
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
    dxAnswer = '''题目：— Can you stay here longer?—    , but I have to be back tomorrow.答案：I’d love to
题目：— Did the medicine make you feel better?  — No. The more           I feel.答案：medicine I take; the worse
题目：— How do you like living in Beijing?答案：I love it. Beijing is such a beautiful city
题目：— I am sorry. Now what were we talking about?答案：You were saying that you used to be a teacher
题目：— This jacket is so good.   ?— It’s 200 yuan. I can give you special 20% discount on it.答案：How much is it
题目：— What do you think of your mother’s advice?答案：It doesn’t fit us, actually
题目：Her article is ____ in her class.答案：the best
题目：I didn’t do ______ last week.答案：anything
题目：I have coffee            breakfast time.答案：at
题目：I like cooking for my friends in            free time. 答案：my
题目：I would rather ______ two weeks earlier.答案：you had come here
题目：Look! __________.答案：Here comes the bus
题目：The music           like the singing of a bird.答案：sounds
题目：They have learned about ______ in recent years.答案：hundreds of English words
题目：You’d better have your hair _____ before going to your friend’s wedding. 答案：cut'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath(
                    "./../input[last()]").click()  # find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "听录音222" in browser.page_source:
        dxAnswer = '''子问题 1：ride; 子问题 2：drinking; 子问题 3：lives; 子问题 4：safer; 子问题 5：safely'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：A; 子问题 4：B; 子问题 5：B'''
        elif "Everyone wants to" in browser.page_source:
            dxAnswer = '''子问题 1：B. affected; 子问题 2：C. but; 子问题 3：A. strain; 子问题 4：C. assumed; 子问题 5：A. consequently'''
        elif "Mary began playing" in browser.page_source:
            dxAnswer = '''子问题 1：C; 子问题 2：B; 子问题 3：A; 子问题 4：B; 子问题 5：B'''
        elif "根据文章内容进行判断" in browser.page_source:
            dxAnswer = '''子问题 1：F; 子问题 2：F; 子问题 3：F; 子问题 4：T; 子问题 5：T'''

        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
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
    dxAnswer = '''题目：—        — Neither do I. Look at our community, it is such a mess.答案：I really don’t think our service center is satisfying.
题目：—                     ?—That’s great! 答案：How about going to dinner at the Mexican restaurant tonight
题目：—Customer: We have ordered for almost one hour. Why is it so hard to get our dishes 答案：I’m really sorry about that.
题目：—Hello, is that service center? The elevator of our apartment doesn’t work.答案：Sorry, I’ll have it checked out at once.
题目：—Why do you look unhappy. What’s the matter?答案：I’m rather disappointed with the poor quality of the radio I’ve just bought.
题目：I don’t know         . I just arrived here two minutes ago.答案：what’s going on
题目：It is only by agreeing with their view point and          that you will resolve the situation答案：suggesting a possible solution
题目：Our workers have been checking the heating system since you called us. I          you it will答案：assure
题目：The heating system of our apartment broke down so I made a ______ call to the答案：complaint
题目：The more information you can get,          in your field. 答案：the more competitive you will be 
题目：They          since last night. They are about to finish the work. 答案：have been cleaning the system
题目：They promised          the car for us.答案：to repaired
题目：We          it very much that you’ve come to give us a timely ride. Otherwise we would答案：appreciate
题目：We are under ______ to finish the task within such limited time.答案：pressure
题目：We feel          with the inconvenience the service center brought us. 答案：disappointed'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath(
                    "./../input[last()]").click()  # find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0

    if "中文翻译" in browser.page_source:
        dxAnswer = '''子问题 1：C; 子问题 2：A; 子问题 3：A; 子问题 4：B; 子问题 5：C'''
    elif "Imagine this situation" in browser.page_source:
        dxAnswer = '''子问题 1：B. it; 子问题 2：A. which; 子问题 3：C. favours; 子问题 4：A. as; 子问题 5：B. with'''
    elif "Angry customers" in browser.page_source:
        dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：B; 子问题 4：C; 子问题 5：C'''
    elif "根据文章内容进行判断" in browser.page_source:
        dxAnswer = '''子问题 1：F; 子问题 2：T; 子问题 3：F; 子问题 4：T; 子问题 5：F'''

    for an in dxAnswer.split("; "):
        listAnswer2.append(an.split("：")[-1])
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
    dxAnswer = '''题目：_____ the fog, we should have reached the annual meeting site on time. 答案：But for
题目：—                      ?— It costs us ten thousand dollars.答案：How much does the printing of the annual report cost
题目：—                     ?—It will take at least two weeks.答案：How soon will you finish our annual report
题目：—Good morning, Sunshine Community Center! May I help you?答案：I need a plumber to repair the water pipe in my kitchen
题目：—How did your talk with the community resident go? 　　答案：I’m not sure.
题目：—Would you mind answering some questions about your annual report? 　　答案：No, as long as it doesn’t take long
题目：I’m confident in these as long as we ________ the needs of the community residents and答案：keep an eye on
题目：If I _____ you, I _____ more attention to the independent auditors’ report and financial statements in the annual report.答案：were; would pay
题目：People ______ find useful information from the annual report.答案：could
题目：The investor should be aware of the limitations of the financial statement analysis答案：based on
题目：The new year is just _________.答案：around the corner
题目：Under no circumstance _____ to tell lies to the public.答案：are the companies allowed
题目：We have to ______ our annual work report to the manager next week. 答案：hand in
题目：When reading the annual report, we should look out ______ the areas where the company did not comply with the regulations.答案：for
题目：When stating problems, we can make a _____ with those from last year. 答案：comparison'''

    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEquals(elements1, value,key,  dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath(
                    "./../input[last()]").click()  # find_element_by_xpath("./../input[last()]").
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.5)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0
    if "听录音222" in browser.page_source:
        dxAnswer = '''子问题 1：traffic accident; 子问题 2：too fast; 子问题 3：driving; 子问题 4：coming from; 子问题 5：check on'''
        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
        for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
            sel.send_keys(listAnswer2[dxindex])
            dxindex += 1
    else:
        if "中文翻译" in browser.page_source:
            dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：A; 子问题 4：C; 子问题 5：C'''
        elif "If you take the following" in browser.page_source:
            dxAnswer = '''子问题 1：A; 子问题 2：C; 子问题 3：B; 子问题 4：C; 子问题 5：C'''
        elif "根据文章内容进行判断" in browser.page_source:
            dxAnswer = '''子问题 1：T; 子问题 2：F; 子问题 3：T; 子问题 4：T; 子问题 5：T'''
        else:
            dxAnswer = '''子问题 1：A. useful; 子问题 2：A. prefer; 子问题 3：C. no; 子问题 4：B. both; 子问题 5：B. without'''

        for an in dxAnswer.split("; "):
            listAnswer2.append(an.split("：")[-1])
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
            time.sleep(2)
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
xingkao8 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=437573'



option = webdriver.ChromeOptions()
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
            writeAnswer1(browser)
            # saveTest2GetAnswer(browser, proxy)
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
