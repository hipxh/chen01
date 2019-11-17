#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import timeunit
import bs4
from selenium import webdriver
import os

studyName = os.path.basename(__file__).split('.')[0]


def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele

def getAnswerElementEquals(elements, neirong):
    for ele in elements:
        if "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele

def getAnswerElementEquals433(elements, neirong,i):
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


def judgeQueTitle(elements1p, title):
    if isinstance(elements1p, list):
        for ele in elements1p:
            if title in ele.text:
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


def duoxuanAutoAnswer(answer, map):
    split = answer.split("")
    for i in split:
        if len(i) < 2:
            continue
        i_split = i.split("（")
        map[i_split[0].strip()] = i_split[1].split("）")[0].strip().split("; ")
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
        if (judgeQueTitle(elements1p[titleIndex], timu)):
            a = 0
            ratios[danxuantiLength * 4 + panduanIndex * 2 + 1].click()
    if a == 1:  # 如果把错题都走了一遍仍然为1,则该判断题是对的
        ratios[danxuantiLength * 4 + panduanIndex * 2].click()
    time.sleep(0.1)


# start to answer.
def writeAnswer1(browser):  # 2019年11月16日12:29:09这是首套出现同一题号题目不同的情况,开始处理
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//p')
    # 判断题,选项位置不变
    if (judgeQueTitle(elements1p, "管理会计与财务会计对企业经营活动和其他经济事项的确定标准是相同的") or judgeQueTitle(elements1p,
                                                                                       "管理会计与财务会计对企业经营活动和其他经济事项的确定标准是相同的")):
        ratios[1].click()
    else:
        ratios[0].click()
    time.sleep(0.1)

    # 单选
    elements1 = browser.find_elements_by_xpath('//label')
    if (judgeQueTitle(elements1p, "并向企业内部提供信息的是")):
        rightAnswer = getAnswerElementEquals(elements1, "管理会计")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "产品生产决策属于")):
        rightAnswer = getAnswerElement(elements1, "短期经营决策")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "管理会计的服务侧重于")):
        rightAnswer = getAnswerElementEquals(elements1, "企业内部的经营管理")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "哪个选项不属于管理会计和财务会计的区别")):
        rightAnswer = getAnswerElementEquals(elements1, "最终目标不同")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "现代管理会计的核心")):
        rightAnswer = getAnswerElementEquals(elements1, "规划与控制会计")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "代企业会计的两大分支：除了财务会计还有")):
        rightAnswer = getAnswerElementEquals(elements1, "管理会计")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)

    # 多选
    time.sleep(0.1)
    if (judgeQueTitle(elements1p, "管理会计的内容包括（")):
        rightAnswer = getAnswerElementEquals(elements1, "规划与控制会计")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "预测与决策会计")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "业绩评价会计")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "管理会计和财务会计的区别（")):
        rightAnswer = getAnswerElementEquals(elements1, "资料时效不同")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "职能目标不同")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "会计主体不同")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "信息精确度不同")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "核算依据不同")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "属于短期经营决策的有（")):
        rightAnswer = getAnswerElementEquals(elements1, "产品成本决策")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "产品生产决策")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "销售定价决策")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "预测与决策会计主要包括（")):
        rightAnswer = getAnswerElementEquals(elements1, "长期投资决策")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "短期经营决策")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals(elements1, "经营预测")
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer2(browser):
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    if (judgeQueTitle(elements1p, "变动成本具有以下特征（")):
        rightAnswer = getAnswerElementEquals433(elements1, "单位变动成本的不变性", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "变动成本总额的正比例变动性", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "成本按习性进行分类，变动成本包括（")):
        rightAnswer = getAnswerElementEquals433(elements1, "变动生产成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "变动推销及管理费用", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "变动制造费用", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "直接材料", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "成本按性态进行分类，将直接材料、直接人工、变动性制造费用三项数额合计后统称为（")):
        rightAnswer = getAnswerElementEquals433(elements1, "变动生产成本", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "成本习性分析的方法包括（")):
        rightAnswer = getAnswerElementEquals433(elements1, "历史资料分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "技术测定法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "直接分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "成本习性具有（")):
        rightAnswer = getAnswerElementEquals433(elements1, "相对性", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "可能转化性", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "暂时性", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "单位固定成本在相关范围内的变动规律为（")):
        rightAnswer = getAnswerElementEquals433(elements1, "随业务量的增加而减少", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "固定成本具有以下特征（")):
        rightAnswer = getAnswerElementEquals433(elements1, "固定成本总额的不变性", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "单位固定成本的反比例变动性", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "广告费属于（")):
        rightAnswer = getAnswerElementEquals433(elements1, "酌量性固定成本", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "历史资料分析法包括（")):
        rightAnswer = getAnswerElementEquals433(elements1, "散布图法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "高低点法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "回归直线法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "则该企业成品库的人工成本属于（")):
        rightAnswer = getAnswerElementEquals433(elements1, "延期变动成本", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)

    if (judgeQueTitle(elements1p, "按完全成本法计算的营业利润为（")):
        rightAnswer = getAnswerElement(elements1, "7000 元", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "下列成本项目中，属于变动成本构成内容的是")):
        rightAnswer = getAnswerElement(elements1, "生产产品使用的原材料", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "下列各项中，能构成变动成本法产品成本内容的是")):
        rightAnswer = getAnswerElementEquals433(elements1, "变动生产成本", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "下列项目中， 属于混合成本类型的有（")):
        rightAnswer = getAnswerElementEquals433(elements1, "阶梯式混合成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "低坡式混合成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "标准式混合成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "下列选项中，哪个不属于变动成本（")):
        rightAnswer = getAnswerElementEquals433(elements1, "按直线法计提的固定资产折旧费", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "在变动成本法下，其利润表所提供的中间指标是（")):
        rightAnswer = getAnswerElementEquals433(elements1, "贡献边际", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "在变动成本法与完全成本法下，引起分期损益产生差异的原因是")):
        rightAnswer = getAnswerElementEquals433(elements1, "固定性制造费用", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "在我国，下列成本项目中属于固定成本的是（")):
        rightAnswer = getAnswerElementEquals433(elements1, "广告费", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "保险费", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "按平均年限法计提的折旧费", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "在相关范围内保持不变的有（")):
        rightAnswer = getAnswerElementEquals433(elements1, "单位变动成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "固定成本总额", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "制造成本亦称生产成本，是指为生产产品或提供劳务而发生的成本。制造成本按照成本项目分类，还可以细分成")):
        rightAnswer = getAnswerElementEquals433(elements1, "制造费用", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "直接材料", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals433(elements1, "直接人工", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)

    # 判断题,选项位置不变
    if (judgeQueTitle(elements1p[7], "变动性制造费用不能列入变动成本法下产品成本。") or judgeQueTitle(elements1p[7],
                                                                                "然后根据总成本和单位变动成本来确定固定成本的一种成本估计方法") or
            judgeQueTitle(elements1p[7], "在变动成本法下，其利润表所提供的中间指标是营业利润。") or judgeQueTitle(elements1p[7],
                                                                                        "企业中的原材料和计件工资制下的生产工人工资应列入固定成本。")):
        ratios[17].click()
    else:
        ratios[16].click()
    time.sleep(0.1)
    if (judgeQueTitle(elements1p[8], "变动性制造费用不能列入变动成本法下产品成本。") or judgeQueTitle(elements1p[8],
                                                                                "然后根据总成本和单位变动成本来确定固定成本的一种成本估计方法") or
            judgeQueTitle(elements1p[8], "在变动成本法下，其利润表所提供的中间指标是营业利润。") or judgeQueTitle(elements1p[8],
                                                                                        "企业中的原材料和计件工资制下的生产工人工资应列入固定成本。")):
        ratios[19].click()
    else:
        ratios[18].click()
    time.sleep(0.1)
    if (judgeQueTitle(elements1p[9], "变动性制造费用不能列入变动成本法下产品成本。") or judgeQueTitle(elements1p[9],
                                                                                "然后根据总成本和单位变动成本来确定固定成本的一种成本估计方法") or
            judgeQueTitle(elements1p[9], "在变动成本法下，其利润表所提供的中间指标是营业利润。") or judgeQueTitle(elements1p[9],
                                                                                        "企业中的原材料和计件工资制下的生产工人工资应列入固定成本。")):
        ratios[21].click()
    else:
        ratios[20].click()
    time.sleep(0.1)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer3(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    if (judgeQueTitle(elements1p, "当单价上涨，而其他因素不变时，会引起（")):
        rightAnswer = getAnswerElementEquals4(elements1, "保本点降低 ，利润增加", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "当单位变动成本单独增加而其他因素均不变时，会引起（")):
        rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "某产品单位变动成本30元，贡献毛益率为70%，则该产品单价为（")):
        rightAnswer = getAnswerElementEquals4(elements1, "100", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "某公司单位变动成本为6元，单价为10元，计划销售600件，欲实现利润740元，固定成本应控制在（")):
        rightAnswer = getAnswerElementEquals4(elements1, "1660元", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "某企业只生产一种产品，该产品的贡献毛益率为70%，本期销售额为20")):
        rightAnswer = getAnswerElementEquals4(elements1, "40000", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "生产多品种产品企业测算综合保本销售额=固定成本总额÷")):
        rightAnswer = getAnswerElementEquals4(elements1, "综合贡献边际率", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "列有关贡献边际率与其它指标关系的表达式中，唯一正确的是")):
        rightAnswer = getAnswerElementEquals4(elements1, "贡献边际率+变动成本率=1", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "销售收入为40 万元，贡献毛益率为60% ，其变动成本总额为")):
        rightAnswer = getAnswerElementEquals4(elements1, "16", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "售比重分别为40%和60%,则用加权平均法计算综合贡献毛益率为")):
        rightAnswer = getAnswerElementEquals4(elements1, "28%", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "已知某企业某产品的单价为50元，保本销售量")):
        rightAnswer = getAnswerElementEquals4(elements1, "20元/件", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "单位变动成本3元，固定成本总额600元，则保本销")):
        rightAnswer = getAnswerElementEquals4(elements1, "300件", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)

    if (judgeQueTitle(elements1p, "从保本图得知（")):
        rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "当企业处于保本状态时，意味着（")):
        rightAnswer = getAnswerElementEquals4(elements1, "总收入等于总成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "贡献边际等于固定成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "利润为零", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "对传统式本量利分析图的解释，下列各项中不正确的是（")):
        rightAnswer = getAnswerElementEquals4(elements1, "在成本水平不变的情况下，单价越高，保本点越高", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "在单价、固定成本不变的情况下，单位变动成本越高，保本点越低", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "贡献毛益率的计算公式可表示为（")):
        rightAnswer = getAnswerElementEquals4(elements1, "1-变动成本率", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "固定成本÷保本销售额", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "贡献毛益÷销售收入", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)

    if (judgeQueTitle(elements1p, "列条件中，能使保本点提高的有（")):
        rightAnswer = getAnswerElementEquals4(elements1, "固定成本提高", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "单位变动成本提高", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "单价降低", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "8元，固定成本总额为2000元，单位变动成本为5元，计划产销量为600件")):
        rightAnswer = getAnswerElementEquals4(elements1, "提高单价1.67元", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "减少固定成本1000元", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "提高产销量333件", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "下列各式中，计算结果等于固定成本的有（")):
        rightAnswer = getAnswerElementEquals4(elements1, "销售额×（1-变动成本率）-利润", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "销售额×贡献毛益率-利润", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "单位贡献毛益×销售量-利润", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "贡献毛益-利润", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)

    if (judgeQueTitle(elements1p, "下列各项中，属于本量利分析应当研究的内容有（")):
        rightAnswer = getAnswerElementEquals4(elements1, "销售量、成本与利润的关系", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "成本与利润的关系", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "销售量与利润的关系", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "在下列项目中，能够决定保本点大小的因素有（")):
        rightAnswer = getAnswerElementEquals4(elements1, "固定成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "销售单价", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "单位变动成本", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "销售量不变的情况下， 如果保本点降低，则（")):
        rightAnswer = getAnswerElementEquals4(elements1, "盈利区的三角形面积有所扩大", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals4(elements1, "亏损区的三角形面积有所缩小", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)

    # 判断题,选项位置不变
    if (judgeQueTitle(elements1p[8], "变动成本率和贡献毛益率的关系是变动成本率大于贡献毛益率。") or judgeQueTitle(elements1p[8],
                                                                                      "传统式本量利分析图的横轴表示销售收入和成本，纵轴表示销售量。") or
            judgeQueTitle(elements1p[8], "单一品种情况下，保本点销售量随着贡献边际率的上升而上升。") or judgeQueTitle(elements1p[8],
                                                                                          "当企业生产经营多种产品时，无法使用本量利分析法。") or
            judgeQueTitle(elements1p[8], "贡献毛益， 又称边际贡献、边际利润等。它是指产品销售收入减去全部成本后的余额。") or judgeQueTitle(elements1p[8],
                                                                                                     "若单价与单位变动成本同方向同比例变动 ，则保本点业务量不变。")):
        ratios[17].click()
    else:
        ratios[16].click()
    time.sleep(0.1)

    if (judgeQueTitle(elements1p[9], "变动成本率和贡献毛益率的关系是变动成本率大于贡献毛益率。") or judgeQueTitle(elements1p[9],
                                                                                      "传统式本量利分析图的横轴表示销售收入和成本，纵轴表示销售量。") or
            judgeQueTitle(elements1p[9], "单一品种情况下，保本点销售量随着贡献边际率的上升而上升。") or judgeQueTitle(elements1p[9],
                                                                                          "当企业生产经营多种产品时，无法使用本量利分析法。") or
            judgeQueTitle(elements1p[9], "贡献毛益， 又称边际贡献、边际利润等。它是指产品销售收入减去全部成本后的余额。") or judgeQueTitle(elements1p[9],
                                                                                                     "若单价与单位变动成本同方向同比例变动 ，则保本点业务量不变。")):
        ratios[19].click()
    else:
        ratios[18].click()
    time.sleep(0.1)
    if (judgeQueTitle(elements1p[10], "变动成本率和贡献毛益率的关系是变动成本率大于贡献毛益率。") or judgeQueTitle(elements1p[10],
                                                                                       "传统式本量利分析图的横轴表示销售收入和成本，纵轴表示销售量。") or
            judgeQueTitle(elements1p[10], "单一品种情况下，保本点销售量随着贡献边际率的上升而上升。") or judgeQueTitle(elements1p[10],
                                                                                           "当企业生产经营多种产品时，无法使用本量利分析法。") or
            judgeQueTitle(elements1p[10], "贡献毛益， 又称边际贡献、边际利润等。它是指产品销售收入减去全部成本后的余额。") or judgeQueTitle(elements1p[10],
                                                                                                      "若单价与单位变动成本同方向同比例变动 ，则保本点业务量不变。")):
        ratios[21].click()
    else:
        ratios[20].click()
    time.sleep(0.1)

    if (judgeQueTitle(elements1p[11], "变动成本率和贡献毛益率的关系是变动成本率大于贡献毛益率。") or judgeQueTitle(elements1p[11],
                                                                                       "传统式本量利分析图的横轴表示销售收入和成本，纵轴表示销售量。") or
            judgeQueTitle(elements1p[11], "单一品种情况下，保本点销售量随着贡献边际率的上升而上升。") or judgeQueTitle(elements1p[11],
                                                                                           "当企业生产经营多种产品时，无法使用本量利分析法。") or
            judgeQueTitle(elements1p[11], "贡献毛益， 又称边际贡献、边际利润等。它是指产品销售收入减去全部成本后的余额。") or judgeQueTitle(elements1p[11],
                                                                                                      "若单价与单位变动成本同方向同比例变动 ，则保本点业务量不变。")):
        ratios[23].click()
    else:
        ratios[22].click()
    time.sleep(0.1)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer4(browser):
    # 试卷222布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    if (judgeQueTitle(elements1p, "经营预测必须以客观准确的历史资料和合乎实际的经验为依据， 该特点是")):
        rightAnswer = getAnswerElementEquals222(elements1, "客观性", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "可以掌握未来的成本水平及其变动趋势的预测")):
        rightAnswer = getAnswerElementEquals222(elements1, "成本预测", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "利用产品销售量在不同生命周期阶段上的变化趋势进行销售预测的方法是")):
        rightAnswer = getAnswerElementEquals222(elements1, "产品生命周期法", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "某服装生产企业，2015年实际销售收入20 万元，2016年")):
        rightAnswer = getAnswerElementEquals222(elements1, "1.76", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "某小家电生产企业5月实际销售台灯为6000台，原来预测该月销售量为5")):
        rightAnswer = getAnswerElementEquals222(elements1, "5800", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "适用于全部经营预测分析的方法是")):
        rightAnswer = getAnswerElementEquals222(elements1, "因果预测法", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "一定时间推广以后，产品已经在市场上占有一定份额，销售量迅速增加，是指产")):
        rightAnswer = getAnswerElementEquals222(elements1, "成长期", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "售预测时应考虑外部因素和内部因素，外部因素不包")):
        rightAnswer = getAnswerElementEquals222(elements1, "信用政策", 1)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
        time.sleep(0.1)

    if (judgeQueTitle(elements1p, "根据所采用的具体数学方法的不同，趋势预测分析法分为")):
        rightAnswer = getAnswerElementEquals222(elements1, "移动加权平均法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "移动平均法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "算术平均法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "指数平滑法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "经营预测的基本方法可以归纳为哪两类")):
        rightAnswer = getAnswerElementEquals222(elements1, "定量预测分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "定性预测分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "利润预测常用的相关比率是（")):
        rightAnswer = getAnswerElementEquals222(elements1, "销售利润率", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "利润增长百分率", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "销售成本利润率", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "利润预测的方法主要有（")):
        rightAnswer = getAnswerElementEquals222(elements1, "本量利分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "经营杠杆系数分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "敏感性分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "相关比率分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)

    if (judgeQueTitle(elements1p, "平滑指数法实质上属于")):
        rightAnswer = getAnswerElementEquals222(elements1, "特殊的加权平均法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "趋势外推分析法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "平均法", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "下列选项中， 哪些是经营预测的内容")):
        rightAnswer = getAnswerElementEquals222(elements1, "成本预测", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "销售预测", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "利润预测", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
    if (judgeQueTitle(elements1p, "影响销售的外部因素主要有")):
        rightAnswer = getAnswerElementEquals222(elements1, "企业的市场占有率", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "同业竞争动向", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "经济发展趋势", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)
        rightAnswer = getAnswerElementEquals222(elements1, "需求动向", 2)
        rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
        time.sleep(0.1)

    # 判断题,选项位置不变
    if (judgeQueTitle(elements1p[4], "9月实际销售量为500 千克， 原来预测该月销售量为480") or judgeQueTitle(elements1p[4],
                                                                                       "上的变化趋势进行销售预测的方法是推销员判断") or
            judgeQueTitle(elements1p[4], "适用于销售波动较大的产品的预测方法是移动平均法。")):
        ratios[9].click()
    else:
        ratios[8].click()
    time.sleep(0.1)

    if (judgeQueTitle(elements1p[5], "9月实际销售量为500 千克， 原来预测该月销售量为480") or judgeQueTitle(elements1p[5],
                                                                                       "上的变化趋势进行销售预测的方法是推销员判断") or
            judgeQueTitle(elements1p[5], "适用于销售波动较大的产品的预测方法是移动平均法。")):
        ratios[11].click()
    else:
        ratios[10].click()
    time.sleep(0.1)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer5(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''定价决策的基本目标不包括下列哪一项（贡献毛益总额最大）。
    某企业生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20元，而且需购买生产设备，每年发生专属固定费用2 000元；如果外购，单价为30元。企业应选择（外购）。
    如果开发新产品需要增加专属固定成本，在决策时作为判断方案优劣的标准是各种产品的（剩余贡献毛益总额）。
    剩余贡献毛益等于（贡献毛益总额-专属固定成本）。 
    为了弥补生产能力不足的缺陷，增加有关装置、设备、工具等长期资产而发生的成本是（专属成本）。
    下列情况中，亏损产品应该停产的条件是（亏损产品的贡献毛益小于零）。
    新产品开发决策中，如果不追加专属成本，且生产经营能力不确定时，决策应采用的指标是（贡献毛益）。
    在经营决策过程中，由于选取最优方案而放弃次优方案所丧失的潜在收益，也就是选择目前接受的方案所付出的代价，这是指（机会成本）。
    在决策过程中，由于选取最优方案而放弃次优方案所丧失的潜在收益，也就是选择目前接受的方案所付出的代价的成本是（机会成本）。
    在需求导向的定价策略中，对于弹性较小的产品，可以（制定较高的价格）。
    差量成本也称为差别成本，形成成本差异的原因是（生产能力利用程度不同）。'''
    mapdxanswer = danxuanAutoAnswer(dxAnswer, {})
    for key, value in mapdxanswer.items():
        if (judgeQueTitle(elements1p, key)):
            rightAnswer = getAnswerElementEqualsFinal(elements1, value, 1, 16, 20)
            rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
            time.sleep(0.1)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.1)

    mulAnswer = '''定价策略的主要类型有（需求导向的定价策略; 利益导向的定价策略; 竞争导向的定价策略; 成本导向的定价策略）。 
    定价决策的影响因素有（政策与法律的约束; 产品的市场生命周期; 供求关系; 产品的价值）。
    关于变动成本加成定价，下列说法正确的有（成本加成率=贡献毛益÷变动成本; 单位价格=单位-单位变动成本。
    某企业现有生产设备可用于甲、乙、丙三种产品的生产，相关资料如表所示。下列说法正确的有（乙丙两种产品的差别收入为162000元; 甲产品贡献毛益总额为160000元; 甲乙两种产品的差别利润为82000元 ）。
    某企业现有用于新产品生产的剩余生产工时为3 000小时，有甲、乙、丙三种新产品可供投入生产，但由于剩余生产能力有限，公司只能选择一种产品进行生产。有关资料如下表所示，不需追加专属成本。下列说法中正确的有（该企业应生产丙产品; 生成丙产品可以获得利润7500元; 乙产品的贡献毛益总额为5250元; 甲产品的单位贡献毛益为70元）。
    某企业新投产一种甲产品，预计年产销量1 000件，生产中耗用直接材料250 000元，直接工资50 000元，制造费用50 000元。经研究决定，在产品完全成本的基础上加成40%作为产品的目标售价。下列说法正确的是（单位甲产品的完全成本为350元; 甲产品的目标售价为490元）。
    企业短期经营决策的特点有（是多种方案的选择; 有明确的目标; 着眼于未来）。
    生产决策要解决的问题主要有三个，即（如何组织和实施生产 ; 利用现有生产能力生产什么产品; 各种产品的生产量是多少 ）。 
    属于相关成本的是（付现成本; 重置成本; 专属成本; 机会成本）。
    影响短期经营决策的因素主要包括（相关收入; 相关成本; 相关业务量 ）。'''
    mapmulAnswer = duoxuanAutoAnswer(mulAnswer, {})
    for key, value in mapmulAnswer.items():
        print(key, value)
        if (judgeQueTitle(elements1p, key)):
            for v in value:
                rightAnswer = getAnswerElementEqualsFinal(elements1, v, 2, 16, 20)
                rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
                time.sleep(0.1)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)

    pdAnswer = '''边际收入是指业务量增加或减少一个单位所引起的收入变动。（对）
    差量收入是指与特定决策方案相联系、能对决策产生重大影响、决策时必须予以充分考虑的收入。（错）
    根据顾客的不同需求，区别对待，采用不同的定价方式，属于成本导向的定价策略。（错）
    机会成本是指在决策过程中，由于选取最优方案而放弃次优方案所丧失的潜在收益，也就是选择目前接受的方案所付出的代价。（对）
    跨国公司为了实现整体利益最大化，可以根据不同国家和地区在税率、汇率、外汇管制等方面的差异而采取不同的转移定价政策。这种定价策略属于竞争导向的定价策略。（错）
    亏损产品满足单价大于其单位变动成本条件下时，就不应当停产。 （对）
    相关成本分析法是指在备选方案收入相同的情况下，只分析各备选方案增加的固定成本和变动成本之和，采用这一方法必须是在备选方案业务量确定的条件下。（对）
    相关业务量是指在短期经营决策中必须重视的，与特定决策方案相联系的产量或销量。（对）
    以利益为导向的定价策略是根据企业追求利润最大化这一目标，采用不同的定价策略。（对）
    在变动成本加成定价法下，成本加成率=贡献毛益÷变动成本。（对）
    在新产品开发决策中，如果不追加专属成本时，决策方法可为利润总额比对法。（错）
    专属成本是指明确归属于特定决策方案的固定成本。（对）
    变动成本加成法是以产品生产的完全成本作为定价基础，加上一定比例的利润来确定产品价格的一种方法。（错）
    长期经营决策是对企业的生产经营决策方案进行经济分析。（错）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 8, 4, 0)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 9, 4, 1)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 10, 4, 2)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 11, 4, 3)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer6(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''是按复利计算的某一特定金额在若干期后的本利和（ 复利终值 ）。
    不考虑货币时间价值的项目评价指标是（平均报酬率）。
    递延年金的特点是（没有第一期的支付额 ）。
    某股票每年的股利为8元，若某人想长期持有，则其在股票价格为（80）时才愿意买？假设银行的存款利率为10%。
    某人每年末将5000元资金存入银行作为孩子的教育基金，假定期限为10年，10%的年金现值系数为2.594，年金终值系数为15．937。到第10年末，可用于孩子教育资金额为（79685）元。
    能使投资方案的净现值等于零的折现率是（内含报酬率 ）。
    下列项目中，不属于现金流出项目的是（折旧费 ）。
    现金流量中的各项税款是指企业在项目生产经营期依法缴纳的各项税款，其中不包括（ 增值税）。
    在项目投资决策的现金流量分析中使用的“营运资本”是指（ 付现成本）。
    在长期投资决策的评价指标中，哪个指标属于反指标（投资回收期 ）。
    下列项目中哪个属于普通年金终值系数（F/A,i,n ）。'''
    mapdxanswer = danxuanAutoAnswer(dxAnswer, {})
    for key, value in mapdxanswer.items():
        if (judgeQueTitle(elements1p, key)):
            rightAnswer = getAnswerElementEqualsFinal(elements1, value, 1, 16, 20)
            rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
            time.sleep(0.1)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.1)

    mulAnswer = '''固定资产更新改造项目，涉及（固定资产; 开办费; 无形资产 ）投资。
年金需要同时满足以下哪三个条件（连续性; 等额性; 同方向性 ）。
投资项目现金流出量是指整个投资和回收过程中所发生的实际现金支出，主要包括（垫付的流动资金; 建设投资支出; 营运资本 ）。
投资项目现金流出量主要包括（ 建设投资支出; 营运资本; 各项税款; 垫付流动资金）。
相比短期经营决策，长期投资决策具有（风险高; 周期长; 投入多 ）等特点。
项目的动态评价指标包括（ 获利指数; 净现值）。
项目计算期包括（生产经营期; 达产期; 试产期; 建设期 ）。
项目经营期内的净现金流量是指项目投产后，在整个生产经营期内正常生产经营所发生的现金流入量与流出量的差额。其计算公式为：（税后净利+年折旧+年摊销额; 营业收入－付现成本－所得税 ）。
一个投资方案可行性的评价标准有（投资方案的平均报酬率≥期望的平均报酬率; 投资方案的净现值≥0 ）。
在长期投资决策的评价指标中，哪些考虑了货币资金的时间价值（ 获利指数; 净现值; 内含报酬率）。
长期投资决策的过程比较复杂，需要考虑的因素很多。其中主要的因素包括（投资项目计算期; 货币时间价值; 资本成本; 现金流量 ）。
长期投资决策中关于现金流量的假设有（建设期投入全部资金假设; 全投资假设; 现金流量符号假设; 项目计算期时点假设 ）。'''
    mapmulAnswer = duoxuanAutoAnswer(mulAnswer, {})
    for key, value in mapmulAnswer.items():
        print(key, value)
        if (judgeQueTitle(elements1p, key)):
            for v in value:
                rightAnswer = getAnswerElementEqualsFinal(elements1, v, 2, 16, 20)
                rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
                time.sleep(0.1)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)

    pdAnswer = '''非折线指标又称为动态评价指标，包括净现值、获利指数和内含报酬率。（错）
净现值是指项目投产后各年报酬的现值合计与投资现值合计之间的差额。（错）
内插法是一种近似计算的方法，它假定当自变量在一个比较小的区间范围内，自变量与因变量之间存在着线性关系；只有在按逐次测试逼近法计算内部收益率时，才有应用内插法的必要。（错）
如果某投资方案净现值指标大于零，则该方案的静态投资回收期一定小于基准回收期。（错）
如果某一投资项目所有的正评价指标均小于或等于相应的基准指标，反指标大于或等于基准指标，则可以断定该投资项目完全具备财务可行性。（错）
无论在什么情况下，都可以采用列表法直接求得不包括建设期的投资回收期。（错）
运用内插法近似计算内部收益率时，为缩小误差，两个近似净现值所相对应的折现率之差通常不得大于5%。（对）
在更新改造投资项目决策中，如果差额投资内部收益率小于设定折现率，就应当进行更新改造。（错）
在互斥方案的选优分析中，若差额内部收益率指标大于基准折现率或设定的折现率时，则原始投资额较小的方案为较优方案。（错）
如果某期累计的净现金流量等于零，则该期所对应的期间值就是包括建设期的投资回收期。（对）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 8, 4, 0)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 9, 4, 1)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 10, 4, 2)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 11, 4, 3)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer7(browser):
    # 试卷444布局
    # div class="qtext",2019年11月16日14:32:26发现bug,如果有一模一样的选项,系统默认勾选第一个,逻辑略复杂,暂不处理.并非一定要满分.
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''"按照“以销定产”模式，预算的编制起点是（销售预算）。
对任何一个预算期、任何一种预算费用项目的开支都不是从原有的基础出发，根本不考虑基期的费用开支水平，一切以零为起点，这种编制预算的方法是（零基预算）。
企业编制全面预算的依据是 （战略目标与战略计划）。
下列各项中，其预算期可以不与会计年度挂钩的预算方法是（滚动预算）。
下列哪项不属于经营预算（现金预算 ）。
下列预算中，属于财务预算的是（  现金收支预算 ）。
以业务量、成本和利润之间的逻辑关系，按照多个业务量水平为基础，编制能够适应多种情况预算的一种预算方法是（ 弹性预算）。
预算最基本的功能是（控制业务）。
在编制预算时以不变的会计期间（定期预算）。'''
    mapdxanswer = danxuanAutoAnswer(dxAnswer, {})
    for key, value in mapdxanswer.items():
        if (judgeQueTitle(elements1p, key)):
            rightAnswer = getAnswerElementEqualsFinal(elements1, value, 1, 16, 12)
            rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
            time.sleep(0.1)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.1)

    mulAnswer = '''按编制预算的时间特征不同，编制预算的方法可以分为（滚动预算; 定期预算）。
财务预算主要包括（ 预计利润表; 预计资产负债表; 现金收支预算 ）。
滚动预算按其预算编制和滚动的时间单位不同可分为（混合滚动; 逐月滚动; 逐季滚动=）。
全面预算按其内容和功能不同可以分为（ 资本预算; 经营预算; 财务预算）。 
相对于固定预算而言，弹性预算的优点有（预算使用范围宽; 预算可比性强）。
预算编制的程序包括（ 审查平衡; 下达目标 ; 议批准并下达执行 ; 编制上报 ）。
预算控制的程序包括以下步骤（ 反馈结果; 分析偏差; 下达执行; 采取措施 ）。
预算控制的方法主要包括（预算授权控制 ; 预算调整控制 ; 预算审核控制）。
算的基本功能主要包括（评价业绩  ; 控制业务 ; 整合资源 ; 确立目标）。 
预算控制的原则主要包括（全员控制 ; 全程控制 ; 全面控制）。 '''
    mapmulAnswer = duoxuanAutoAnswer(mulAnswer, {})
    for key, value in mapmulAnswer.items():
        print(key, value)
        if (judgeQueTitle(elements1p, key)):
            for v in value:
                rightAnswer = getAnswerElementEqualsFinal(elements1, v.strip(), 2, 16, 12)
                rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
                time.sleep(0.1)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.1)

    pdAnswer = '''弹性预算方法的优点是不受现有费用项目限制，能够调动各方面降低费用的积极性和有助于企业未来发展。（错）
滚动预算方法是以基期成本费用水平为基础，结合预算期业务量水平及有关降低成本的措施，通过调整有关原有费用项目而编制预算的方法。（错）
企业关于日常经营活动如销售、采购、生产等需要多少资源以及如何获得和使用这些资源的计划，是指特种决策预算。 （错）
企业预算总目标的具体落实以及将其分解为责任目标并下达给预算执行者的过程称为预算编制。（对）
相对于固定预算而言，弹性预算的优点预算成本低，工作量小。（错）
与固定预算相对应的预算是增量预算。 （错）
资本预算是全面预算体系的中心环节。（错）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 7, 4, 0)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 8, 4, 1)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 9, 4, 2)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
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
    for key, value in mapmulAnswer.items():
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
    for key, value in mapmulAnswer.items():
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
    for key, value in mapmulAnswer.items():
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
    browser.switch_to.window(windowstabs[1])
    browser.find_elements_by_css_selector('img[class="pull-right"]')  # find一下,保证新页面加载完成
    browser.get(xkurl)  # 先考形1


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


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480017'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480018'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480019'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480020'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480021'
xingkao6 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480022'
xingkao7 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480023'
xingkao8 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480024'
xingkao9 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480025'
xingkao10 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=480026'

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

    # enterTest(browser, xingkao1)
    # if readyToTestForum(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer1(browser)
    # wait3AndCloseTab(browser)

    # enterTest(browser, xingkao2)
    # if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer2(browser)
    # wait3AndCloseTab(browser)
    #
    # enterTest(browser, xingkao3)
    # if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer3(browser)
    # wait3AndCloseTab(browser)
    #
    # enterTest(browser, xingkao4)
    # if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer4(browser)
    # wait3AndCloseTab(browser)
    #
    # enterTest(browser, xingkao5)
    # if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer5(browser)
    # wait3AndCloseTab(browser)
    # enterTest(browser, xingkao6)
    # if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #     writeAnswer6(browser)
    # wait3AndCloseTab(browser)
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

    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(2)
