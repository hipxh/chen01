#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

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
    result = []
    split = answer.split("\n")
    for i in split:
        result.append(i.strip().split(reg)[1])
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

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position
def duoxuanAutoAnswer2(answer, map,reg):
    split = answer.split("")
    for i in split:
        if len(i) < 2:
            continue
        i_split = i.split("（")
        # 如果选项里有括号
        leftIndex = i.find("（")
        rightIndex = find_last(i, "）")
        ans = i[leftIndex + 1:rightIndex]
        map[i_split[0].strip()] = ans.strip().split(reg)
    return map
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
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0


    # 1单
    dxAnswer = '''1.18'''
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



    mulAnswer = '''2.控制技术; 通信技术; 传感技术; 计算机技术
    3.小型化; 系统化;  网络化; 数字化; 智能化
    4.信息技术或工具; 信息生产者; 信息
    5.加工; 存储; 检索; 传递; 采集
    6.信息化组织; 信息化评价; 信息化规划; 信息化实施
    7.物联网; 智慧地球;  云计算; 大数据; 移动互联网'''
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
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后input重新拿,这一页有填空题

    dxAnswer = '''1.A
    2.B
    3.C
    4.D'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
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


    # 1单
    dxAnswer = '''1.信息化战略规划'''
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

    #多选（题目顺序不变）
    mulAnswer = '''2.信息化体系架构设计; 环境分析; 信息技术标准; 信息化战略; 项目分派和管理
    3.信息化战略目标设计和制定; 能力和现状分析; 基础信息调研   
    4.使信息技术与组织战略保持一致，增强组织的竞争力; 最大限度地避免“信息孤岛”出现; 降低信息化建设的整体风险和投资成本; 改善业务部门与信息部门间的交流和合作，使信息化工作有序进行'''
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
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后input重新拿,这一页有填空题

    #填空
    dxAnswer = '''1.C
    2.A
    3.B
    4.D'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

#暂时没有做writeAnswer3
def writeAnswer3(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')

    # 下拉选择框
    listAnswer2 = []
    dxindex = 0
    dxAnswer = '''子问题 1：确定信息化目标; 子问题 2：明确相应的活动; 子问题 3：进行活动与资源的匹配; 子问题 4：建立信息化组织机构; 子问题 5：赋予各类人员相应的责、权、利; 子问题 6：将各部分融合为有机整'''
    for an in dxAnswer.split("; "):
        listAnswer2.append(an.split("：")[-1])
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex += 1



    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(2)


    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后input重新拿,这一页有填空题
    # 填空
    dxAnswer = '''1.C
        2.A
        3.D
        3.B
        4.B
        2.A
        3.C
        4.D'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1




    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
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

    # 判断题（顺序不变）
    pdAnswer = '''1.对 
       2.错 
       3.对
        4.错'''
    listpdanswer = danxuanAutoAnswerFix(pdAnswer, ".")

    dxindex = 0
    for an in listpdanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    # 10单选
    dxAnswer = '''1.满足甚至超越项目利益相关人的需求
    2.10
    3.项目综合计划
    4.范围计划、进度计划、成本计划'''
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

    # 多选（题目顺序不变）
    mulAnswer = '''1.工作分解; 项目背景描述; 范围核实与确认; 范围定义
       2.整体变更控制; 质量控制; 成本控制; 范围控制进度控制'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
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

    # 判断题（顺序不变）
    pdAnswer = '''1.错
        2.对 
        3.对'''
    listpdanswer = danxuanAutoAnswerFix(pdAnswer, ".")

    dxindex = 0
    for an in listpdanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    # 10单选
    dxAnswer = '''1.系统规划
     2.一致性
     3.适应性维护 
     4.统一'''
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

    # 多选（题目顺序不变）
    mulAnswer = '''1.软件; 处理规程; 硬件; 数据; 人
        2.技术安全; 行为规范; 实体安全
        3.配置管理; 问题管理; 性能管理; 故障管理
        4.信息公开; 信息市场管理; 信息采集; 信息安全; 信息资源利用'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer6(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    #一道单选题C
    ratios[2].click()
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(2)
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    #两道多选题
    mulAnswer='''通过对中国林业网的内外部评价，极大地促进了林业网站的集成与发展，达到了的（以评促建;以评促用;以评促进;以评促管）。
    国家信息化测评中心经过多年的研究与实践，提出并发布了企业信息化评价的指标体系，它包括：（评议指标;补充（效能）指标;基本指标）'''
    mapmulAnswer = duoxuanAutoAnswer2(mulAnswer, {}, ";")
    for key, value in mapmulAnswer.items():
        if (judgeQueTitle(elements1p, key)):
            for v in value:
                currentelements1 = rightTiGan[-1].find_element_by_xpath("./../..//div[last()]")
                currentelements1 = currentelements1.find_elements_by_xpath(".//label")
                rightAnswer = getAnswerElementEqualsFinal(currentelements1, v.strip(), 3, 1 * 4, 1 * 5)
                if rightAnswer is None:
                    canTakeWrongNum = canTakeWrongNum + 1
                else:
                    rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
                time.sleep(0.1)

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(2)

    # 下拉选择框
    listAnswer2 = []
    dxindex = 0
    dxAnswer = '''子问题 1：明确评价主体和客体; 子问题 2：确定评价目的、原则及其指标体系; 子问题 3：确定评价模型; 子问题 4：调查、统计各指标值; 子问题 5：评价计算与分析'''
    for an in dxAnswer.split("; "):
        listAnswer2.append(an.split("：")[-1])
    for sel in browser.find_elements_by_class_name("custom-select"):
        sel.send_keys(listAnswer2[dxindex])
        dxindex += 1

    # end answer
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer7(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')

    # 10单选
    dxAnswer = '''1.内网、外网、公网 
        2.养老助残服务智慧平台'''
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

    # 多选（题目顺序不变）
    mulAnswer = '''1.职责; 人员; 岗位; 信息; 关系
           2.企业; 政府机构; 事业单位; 其他
           3.智慧大脑; 智慧神经; 智慧感知'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer8(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''是指由存货的买价和运杂费等构成的成本，其总额取决于采购数量和单位采购成本（购置成本）。
    成本差异是指在标准成本控制系统下，企业在一定时期生产一定数量的产品所发生的实际成本与（标准成本 ）之间的差额。
    某公司生产甲产品100件，实际耗用工时为200小时，单位产品标准工时为1.8小时，标准工资率为5元/小时，实际工资率为4.5元/小时，则直接人工效率差异为（100元 ）。
    一般情况下，对直接材料用量差异负责的部门应该是（ 生产部门）。
    在变动成本法下，标准成本卡不包括（固定制造费用 ）。 '''
    mapdxanswer = danxuanAutoAnswer(dxAnswer, {})
    for key, value in mapdxanswer.items():
        if (judgeQueTitle(elements1p, key)):
            rightAnswer = getAnswerElementEqualsFinal(elements1, value, 1, 8, 4)
            rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
            time.sleep(0.1)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.1)

    mulAnswer = '''下列影响再订货点的因素是（ 安全存量; 订货提前期; 存货日均耗用量）。
    三差异分析法，是指将固定制造费用的成本差异分解为（耗费差异; 能力差异; 能量差异）来进行分析的。
    取得成本是下列哪些选择之和（购置成本; 订货变动成本; 订货固定成本 ）。
    下列可以影响直接材料用量差异的原因有（材料的质量; 工人的技术熟练程度; 工人的责任感; 材料加工方式的改变）。'''
    mapmulAnswer = duoxuanAutoAnswer(mulAnswer, {})
    for value in mapmulAnswer:
        print(key, value)
        if (judgeQueTitle(elements1p, key)):
            for v in value:
                rightAnswer = getAnswerElementEqualsFinal(elements1, v.strip(), 2, 8, 4)
                rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
                time.sleep(0.1)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)

    pdAnswer = '''从实质上看，直接工资的工资率差异属于价格差异。（对）
    全面成本控制原则就是要求进行全过程控制。（错）
    缺货成本是简单条件下的经济批量控制必须考虑的相关成本之一。（错）
    在标准成本控制系统中，成本超支差应记入成本差异账户的贷方。（错）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 3, 2, 0)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 4, 2, 1)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer9(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''当产品的市场价格不止一种时，供求双方有权在市场上销售或采购，且供给部门的生产能力不受限制时，应当作为内部转移价格的是（双重市场价格）。
建立责任会计的目的是为了（实现责、权、利的协调统一 ）。
利润中心和投资中心的区别在于，不对（投资效果 ）负责。
下列不属于责任中心考核指标的是（ 产品成本）。
以市场价格作为基价的内部转移价格主要适用于自然利润中心和（投资中心 ）。'''
    mapdxanswer = danxuanAutoAnswer(dxAnswer, {})
    for key, value in mapdxanswer.items():
        if (judgeQueTitle(elements1p, key)):
            rightAnswer = getAnswerElementEqualsFinal(elements1, value, 1, 8, 4)
            rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
            time.sleep(0.1)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.1)

    mulAnswer = '''内部转移价格的作用（有利于分清各个责任中心的经济责任; 有利于正确评价各责任中心的经营业绩; 有利于进行正确的经营决策 ）。
投资中心的考核指标包括（ 投资报酬率; 剩余收益）。
责任中心的设置应具备的条件（责任者; 经营绩效; 资金运动; 职责和权限 ）。
酌量性成本中心发生的费用包括以下哪些（管理费用; 销售费用 ）。'''
    mapmulAnswer = duoxuanAutoAnswer(mulAnswer, {})
    for value in mapmulAnswer:
        print(key, value)
        if (judgeQueTitle(elements1p, key)):
            for v in value:
                rightAnswer = getAnswerElementEqualsFinal(elements1, v.strip(), 2, 8, 4)
                rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
                time.sleep(0.1)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)

    pdAnswer = '''利润或投资中心之间相互提供产品或劳务，最好以市场价格作为内部转移价格。（对）
剩余收益指标的优点是可以使投资中心的业绩评价与企业目标协调一致。（对）
一般来讲，成本中心之间相互提供产品或劳务，最好以“实际成本”作为内部转移价格。（错）
因利润中心实际发生的利润数大于预算数而形成的差异是不利差异。（错）
责任会计制度的最大优点是可以精确计算产品成本。（对）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 3, 2, 0)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 4, 2, 1)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer10(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''平衡计分卡从四个方面来设计出相应的评价指标，来反映企业的整体运营状况，为企业的平衡管理和战略实现服务，其中不包括（ 销售视角  ）。
作业成本法的核算对象是（作业）。 
作业成本法首先将（间接费用 ）按作业成本库进行归集。'''
    mapdxanswer = danxuanAutoAnswer(dxAnswer, {})
    for key, value in mapdxanswer.items():
        if (judgeQueTitle(elements1p, key)):
            rightAnswer = getAnswerElementEqualsFinal(elements1, value, 1, 4, 5)
            rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
            time.sleep(0.1)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.1)

    mulAnswer = '''EVA在技术方法上对经济利润的改进处是（对会计报表进行调整 ; 引进了资本资产定价模型 ; 矫正了传统财务指标的信息失真 ）。
平衡计分卡的四个视角是（财务视角 ; 内部业务流程视角; 学习与成长视角; 客户视角 ）。
在ABC中，依据作业是否会增加顾客价值，分为（ 不增值作业 ; 增值作业 ）。'''
    mapmulAnswer = duoxuanAutoAnswer(mulAnswer, {})
    for value in mapmulAnswer:
        print(key, value)
        if (judgeQueTitle(elements1p, key)):
            for v in value:
                rightAnswer = getAnswerElementEqualsFinal(elements1, v.strip(), 2, 4, 5)
                rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
                time.sleep(0.1)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)

    pdAnswer = '''在作业成本法下，成本动因是导致成本发生的诱因，是成本分配的依据。（对）
经济增加值与会计利润的主要区别在于会计利润扣除债务利息，而经济增加值扣除了股权资本费用，而不不扣除债务利息。（错）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 2, 1, 0)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
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
    time.sleep(3.5)


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=459952'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=459953'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=459954'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=459955'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=459956'
xingkao6 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=459957'
xingkao7 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=459958'

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
        if readyToTestForum(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
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


    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(4)
