#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import timeunit
import bs4
from selenium import webdriver
import os

studyName = os.path.basename(__file__).split('.')[0]


# 其中一张试卷全部为富文本提交
def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele


def getAnswerElementEquals(elements, neirong, i, meidaotiyouduoshaogexuanxiang):
    elements = elements[i * meidaotiyouduoshaogexuanxiang:(i + 1) * meidaotiyouduoshaogexuanxiang]
    for ele in elements:
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text:
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

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position
def judgeQueTitle(elements1p, title):
    if isinstance(elements1p, list):
        for ele in elements1p:
            if title + "（" in ele.text:
                rightTiGan.append(ele)
                return True
    else:
        if title in elements1p.text:
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
        result.append(i.strip().split(reg)[1])
    return result
    # split = answer.split("\n")
    # for i in split:
    #     if len(i) < 2:
    #         continue
    #     i_split = i.split("（")
    #     # 如果选项里有括号
    #     leftIndex = i.find("（")
    #     rightIndex = find_last(i, "）")
    #     ans = i[leftIndex + 1:rightIndex]
    #     map[i_split[0]] = ans.strip()
    # return map


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

    # split = answer.split("\n")
    # for i in split:
    #     if len(i) < 2:
    #         continue
    #     i_split = i.split("（")
    #     #如果选项里有括号
    #     leftIndex=i.find("（")
    #     rightIndex=find_last(i,"）")
    #     ans = i[leftIndex+1:rightIndex]
    #     map[i_split[0].strip()] = ans.strip().split(reg)
    # return map


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
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer2(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer4(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer5(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer6(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer7(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer8(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer9(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer10(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer11(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer12(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''32.经济
33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''41.活动效果; 活动主体; 实施活动的环境; 活动目标
42.综合性; 定量性; 实用性; 预测性
43.静态分析与动态分析相结合以动态分析为主原则; 满足可比的原则（产量、成本、时间等）; 定性分析与定量分析相结合，以定量分析为主原则'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''32.经济
    33.收集整理基础数据→编制经济分析报表→财务分析→国民经济分析→综合分析与评价 
    34.②→①→④→③→⑤ '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
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


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454074'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454075'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454076'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454077'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454078'
xingkao6 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454079'
xingkao7 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454080'
xingkao8 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454081'
xingkao9 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454082'
xingkao10 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454083'
xingkao11 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454084'
xingkao12 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=454085'

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
    #     if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #         writeAnswer1(browser)
    #     wait3AndCloseTab(browser)

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

    enterTest(browser, xingkao9)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer9(browser)
    wait3AndCloseTab(browser)

    enterTest(browser, xingkao10)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer10(browser)
    wait3AndCloseTab(browser)

    enterTest(browser, xingkao11)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer11(browser)
    wait3AndCloseTab(browser)

    enterTest(browser, xingkao12)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer12(browser)
    wait3AndCloseTab(browser)

    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(2)
