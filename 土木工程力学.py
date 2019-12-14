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
        neirong = neirong.replace(' ', '')
        _xuanxiang = ele.text.replace(' ', '')
        if neirong == _xuanxiang or "A." + neirong == _xuanxiang or "B." + neirong == _xuanxiang or "C." + neirong == _xuanxiang or "D." + neirong == _xuanxiang or "E." + neirong == _xuanxiang or "a." + neirong == _xuanxiang or "b." + neirong == _xuanxiang or "c." + neirong == _xuanxiang or "d." + neirong == _xuanxiang or "e." + neirong == _xuanxiang:
            return ele
def getAnswerElementEqualsNotJudge(elements, neirong, i, meidaotiyouduoshaogexuanxiang):
    # elements = elements[i * meidaotiyouduoshaogexuanxiang:(i + 1) * meidaotiyouduoshaogexuanxiang]
    for ele in elements:
        neirong = neirong.replace(' ', '')
        _xuanxiang = ele.text.replace(' ', '')
        if neirong == _xuanxiang or "A." + neirong == _xuanxiang or "B." + neirong == _xuanxiang or "C." + neirong == _xuanxiang or "D." + neirong == _xuanxiang or "E." + neirong == _xuanxiang or "a." + neirong == _xuanxiang or "b." + neirong == _xuanxiang or "c." + neirong == _xuanxiang or "d." + neirong == _xuanxiang or "e." + neirong == _xuanxiang:
            return ele
#单选和多选在一页
def getAnswerElementEqualsdanxuanduoxuaninOnePage(elements, neirong, i, meidaotiyouduoshaogexuanxiang,danxuanLabelLength):
    elements = elements[danxuanLabelLength+i * meidaotiyouduoshaogexuanxiang:(i + 1) * meidaotiyouduoshaogexuanxiang+danxuanLabelLength]
    for ele in elements:
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text:
            return ele
        neirong = neirong.replace('',' ')
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

#没有题号只有答案,则不需要后面的参数
def danxuanAutoAnswerFix(answer, reg):
    result = []
    split = answer.split("\n")
    for i in split:
        result.append(i.strip())
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
        listList.append(i.strip().split(reg2))
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


def pdAutoAnswer(answer, list,reg):
    split = answer.split("\n")
    # for i in split:
    #     if len(i) < 2:
    #         continue
    #     if '错' in i.split("。	")[1]:
    #         list.append(i.split("。	")[0].strip())
    for i in split:
        if len(i) < 2:
            continue
        if '错' in i.split(reg)[1]:
            list.append(i.split(reg)[0].strip()[1:])
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
    time.sleep(0.4)


# start to answer.5单5多5判断
def getTkAnswers(tkAnswer, reg, reg2):
    list = []
    for an in tkAnswer.split("\n"):
        for i in an.strip().split(reg)[1].split(reg2):
            list.append(i)
    return list

def writeAnswer1(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')

    #选择填空题
    tkAnswer = '''1.C B A
2.C B A
3.B A C D
4.B C A F E D
5.A B
6.B C'''
    dxindex = 0
    listAnswer2 = getTkAnswers(tkAnswer,"."," ")
    for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
        sel.send_keys(listAnswer2[dxindex])
        dxindex+=1
        time.sleep(0.4)


    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    #随机单选
#     dxAnswer = '''无多余约束的几何不变体系
# 几何可变体系
# 可变体系
# 瞬变体系
# 有一个多余约束的几何不变体系
# 有两个多余约束的几何不变体系
# 结点处各杆端之间的夹角保持不变
# 三铰两两相联，三铰不在一直线上
# 可变体系
# 无多余约束的几何不变体系'''
#     listdxanswer = danxuanAutoAnswerFix(dxAnswer, "")
#     dxindex = 0
#     for an in listdxanswer:
#         anEle = getAnswerElementEqualsNotJudge(elements1, an, dxindex, 4)  # 找到指定的那个label选项
#         if anEle is not None:
#             anEle.find_element_by_xpath("./../input[last()]").click()
#             time.sleep(0.4)
#         dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''·多余约束是体系中不需要的约束。	错
·刚结点可以承受和传递力，但不能承受和传递力矩。	错
·铰结点不仅能承受和传递力，而且能承受和传递力矩。	错
·仅利用变形协调条件不能唯一确定全部反力和内力的结构称为超静定结构。	错
·仅利用静力平衡条件即可确定结构全部反力和内力，且解答唯一，这样的结构称为静定结构。	对
·连接4个刚片的复铰相当于4个约束。	错
·两个刚片用不全平行也不全交于一点的三根链杆相联,组成的体系是无多余约束的几何不变体系。	对
·两个刚片用一个铰和一根链杆相联，组成的体系是无多余约束的几何不变体系。	错
·两根链杆的约束作用相当于一个单铰。	错
·如果体系的计算自由度大于零，那么体系一定时几何可变体系。	对
·如果体系的计算自由度等于其实际自由度，那么体系中没有多余约束。	对
·如果体系的计算自由度小于或着等于零，那么体系一定是几何不变体系。	错
·如果在一个体系中增加一个约束，而体系的自由度并不因此减少，则称此约束为多余约束。	对
·三个刚片用三个单铰两两相联，组成的体系是无多余约束的几何不变体系。	错
·瞬变体系在很小的荷载作用下会产生很大的内力。	对
·体系的实际自由度绝对不小于其计算自由度。	对
·一个点在平面内的自由度等于1。	错
·一个体系是有n个多余约束的几何不变体系，那么去掉n个约束后就成为无多余约束的几何不变体系。	错
·一体系是有n个自由度的几何可变体系，加入n个约束后就成为无多余约束的几何不变体系。	错
·在一个体系上添加或去掉一个二元体不会改变原体系的几何组成性质。	对'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [],"。	")
    for pdindex in range(10):
        pdUtil5(pdWrongAnswer, qtexts, ratios, pdindex+1, 0, pdindex)
        time.sleep(0.4)


    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    # browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    # browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer2(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')

    #选择填空题
#     tkAnswer = '''1.C B A
# 2.C B A
# 3.B A C D
# 4.B C A F E D
# 5.A B
# 6.B C'''
#     dxindex = 0
#     listAnswer2 = getTkAnswers(tkAnswer,"."," ")
#     for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
#         sel.send_keys(listAnswer2[dxindex])
#         dxindex+=1
#         time.sleep(0.4)
#
#
#     browser.find_element_by_xpath('//input[@name="next"]').click()
#     time.sleep(4)
#     elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    #随机单选
    dxAnswer = '''BD两截面间的相对转动
A、D连线的转动
A截面转角
图片
30kN·m（左侧受拉）
1.5m下拉
图片
图片
图片
0
FPa（上表面受拉）
图片上拉
图片
图片
BC部分
AB部分
图片
6
7
7根
轴向变形
图片
图片
位移
无关
虚功原理
剪力图
发生变形和位移
荷载'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''桁架结构在结点荷载作用下，杆内只有剪力。	对
基本附属型结构的计算顺序是：先计算附属部分后计算基本部分。	对
结点荷载作用下的桁架结构中，杆件内力不是只有轴力。	错
静定多跨梁中基本部分、附属部分的划分与所承受的荷载无关。	对
静定结构的内力和反力与杆件截面的几何尺寸有关。	错
静定结构的内力与材料的性质无关。	对
两个三铰拱，拱高_f、_跨度_l_均相同，但荷载不同，其合理拱线也不同。	对
某荷载作用下桁架可能存在零杆，它不受内力，因此在实际结构中可以将其去掉。	错
三铰拱的拱高_f_越大，水平推力也越大。	错
三铰拱水平推力的大小，不仅与拱高_f_有关，而且与拱轴线形状有关。	错
试判断下列弯矩图是否正确。	错
所谓合理拱轴线，是指在任意荷载作用下都能使拱处于无弯矩状态的轴线。	错
图示多跨静定梁仅_AB_段有内力。	对
图示多跨静定梁仅_FD_段有内力。	对
图示刚架_CD_部分的内力为零。	对
图示刚架，_AB_部分的内力为零。	对
图示刚架弯矩图的形状是否正确。	错
图示桁架结构中不包括支座链杆，有5个杆件轴力为0 。	错
图示桁架中FN1=0。	错
图示两个单跨梁，同跨度同荷载。但横截面形状不同，故其内力也不相同。	错
图示两根梁的内力相同，变形也相同。	错
图示为梁的虚设力状态，按此力状态及位移计算公式可求出AB两点的相对线位移。	对
图示悬臂梁截面A的弯矩值是ql2。	错
外力作用在基本部分上时，附属部分的内力、变形和位移均为零。	错
依据静力平衡条件可对静定结构进行受力分析，这样的分析结果是唯一正确的结果。	对
用平衡条件能求出全部内力的结构是静定结构。	对
在跨度、荷载不变的条件下，控制三铰拱水平反力的唯一参数是拱高。	对'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [],"。	")
    for pdindex in range(10):
        pdUtil5(pdWrongAnswer, qtexts, ratios, pdindex+1, 0, pdindex)
        time.sleep(0.4)

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    # browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    # browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')

    #选择填空题
#     tkAnswer = '''1.C B A
# 2.C B A
# 3.B A C D
# 4.B C A F E D
# 5.A B
# 6.B C'''
#     dxindex = 0
#     listAnswer2 = getTkAnswers(tkAnswer,"."," ")
#     for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
#         sel.send_keys(listAnswer2[dxindex])
#         dxindex+=1
#         time.sleep(0.4)
#
#
#     browser.find_element_by_xpath('//input[@name="next"]').click()
#     time.sleep(4)
#     elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    #随机单选
    dxAnswer = '''多余约束的数目
相对值有关
绝对值有关
以上四种原因
多余约束处的位移协调条件
多余未知力
几何不变体系
图片
图片
图片
图片
组合结构
7
4
6
3次
2
只有剪力和只有弯矩同时满足
AB杆无轴力
轴力
转角
图片
图片
图片'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''超静定次数一般不等于多余约束的个数。（ ）	错
超静定结构的力法基本结构是唯一的。（ ）	错
超静定结构的内力与材料的性质无关。 （ ）	错
超静定结构的内力状态与刚度有关。（ ）	对
超静定结构由于支座位移可以产生内力。 （ ）	对
超静定结构支座移动时，如果刚度增大一倍，内力也增大一倍，而位移不变。（ ）	对
对称结构在反对称荷载作用下，对称轴穿过的截面只有反对称的内力。（ ）	对
计算超静定结构的位移时，虚设力状态可以在力法的基本结构上设。（ ）	对
力法的基本方程使用的是位移条件；该方法只适用于解超静定结构。（ ）	对
力法典型方程的等号右端项不一定为0。 （ ）	对
力法典型方程是根据平衡条件得到的。（ ）	错
力法计算的基本体系不能是可变体系。（ ）	对
求超静定结构的位移时，可将虚拟单位荷载加在任意静定的基本体系上。（ ）	对
同一结构的力法基本体系不是唯一的。（ ）	对
同一结构选不同的力法基本体系，所得到的力法方程代表的位移条件相同。（ ）	错
同一结构选不同的力法基本体系所得到的力法方程代表的位移条件不同。（ ）	错
同一结构选不同的力法基本体系所得到的最后结果是相同的。（ ）	对
图示（a）、（b）两个结构中，A端的支反力完全相同。（ ）	错
图示超静定结构去掉杆件①、②、③后为一静定梁，故它是三次超静定结构。（ ）	错
图示结构的超静定次数是n=3。 （ ）	对
图示结构有两次超静定。（ ）	错
图示两个单跨梁，同跨度同荷载。但横截面形状不同，故其内力也不相同。（ ）	错
温度改变对超静定结构不产生内力和反力。（ ）	错
温度改变在静定结构中不引起内力；温度改变在超静定结构中引起内力。（ ）	对
用力法计算超静定结构，选取的基本结构不同，所得到的最后弯矩图也不同。（ ）	错
用力法计算超静定结构，选取的基本结构不同，则典型方程中的系数和自由项数值也不同。（ ）	对
在荷载作用下，超静定结构的内力分布与各杆刚度的绝对值有关。（ ）	错
在力法计算时，多余未知力由位移条件来求，其他未知力由平衡条件来求。（ ）	对
在下图所示结构中若增大柱子的EI值，则梁跨中点截面弯矩值减少。（ ）	对
支座位移引起的超静定结构内力，与各杆刚度的相对值有关。 （ ）	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [],"。")
    for pdindex in range(10):
        pdUtil5(pdWrongAnswer, qtexts, ratios, pdindex+1, 0, pdindex)
        time.sleep(0.4)

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    # browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    # browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer4(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')

    #选择填空题
#     tkAnswer = '''1.C B A
# 2.C B A
# 3.B A C D
# 4.B C A F E D
# 5.A B
# 6.B C'''
#     dxindex = 0
#     listAnswer2 = getTkAnswers(tkAnswer,"."," ")
#     for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
#         sel.send_keys(listAnswer2[dxindex])
#         dxindex+=1
#         time.sleep(0.4)
#
#
#     browser.find_element_by_xpath('//input[@name="next"]').click()
#     time.sleep(4)
#     elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    #随机单选
    dxAnswer = '''仅AB、BE杆产生弯矩
平衡方程
绕杆端顺时针转动
第i个附加约束中的约束反力
第i个附加约束中的约束反力
铰结点数
结点位移
与结构的形式有关
4
3
3
3
2
10
－2  KN·m
5i
8i
图片
图片
（2）、（3）的固定端弯矩相同
远端支承
剪力图反对称
A端转动时产生的A端弯矩
1
杆端弯矩
1kN·m
8
图片
图片
—10kN·m
交于该结点的固定端弯矩之和
分配系数小于1
同时满足以上条件
远端支承'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''当_AB_杆件刚度系数时，杆件的B端为定向支座。	错
分配系数表示A节点作用单位力偶时，AB杆A端所分担得的杆端弯矩。	对
力矩分配法适用于连续梁。	对
力矩分配法适用于连续梁和有侧移刚架。	错
力矩分配法适用于所有超静定结构的计算。	错
能用位移法计算的结构就一定能用力矩分配法计算。	错
如果位移法基本体系的附加约束中的反力（矩）等于零，则基本体系就与原结构受力一致，但变形不一致。	错
图示结构用位移法求解，基本未知量的数目是2。	错
位移法的基本方程使用的是平衡条件，该方法只适用于解超静定结构。	错
位移法的基本结构不是唯一的。	错
位移法的基本结构是超静定结构。	对
位移法的基本体系是一组单跨超静定梁。	对
位移法的基本未知量与超静定次数有感，位移法不能计算静定结构。	错
位移法典型方程中的主系数恒为正值，副系数恒为负值。	错
位移法典型方程中的自由项是外因作用下附加约束上的反力。	对
位移法可用来计算超静定结构也可用来计算静定结构。	对
位移法只能用于超静定结构。	错
用力矩分配法计算结构时，汇交于每一结点各杆端分配系数总和为1，则表明分配系数的计算无错误。	错
用力矩分配法计算结构时，结点各杆端力矩分配系数与该杆端的转动刚度成正比。	对
用位移法计算荷载作用下的超静定结构，采用各杆的相对刚度进行计算，所得到的节点位移不是结构的真正位移，求出的内力是正确的。	对
用位移法解超静定结构时，附加刚臂上的反力矩是利用结点平衡求得的。	对
在多结点结构的力矩分配法计算中，可以同时放松所有不相邻的结点以加速收敛速度。	对
在力矩分配法中，当远端为定向支座时，其传递系数为1。	错
在力矩分配法中，规定杆端力矩绕杆端顺时针为正，外力偶绕节点顺时针为正。	对
在力矩分配法中，结点各杆端分配系数之和恒等于1。	对
在力矩分配中，当远端为定向支座时，其传递系数为0。	错
在下图所示的连续梁中，节点B的不平衡力矩等于，,其中M＝－30。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [],"。	")
    for pdindex in range(10):
        pdUtil5(pdWrongAnswer, qtexts, ratios, pdindex+1, 0, pdindex)
        time.sleep(0.4)

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    # browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    # browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer5(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')

    #选择填空题
#     tkAnswer = '''1.C B A
# 2.C B A
# 3.B A C D
# 4.B C A F E D
# 5.A B
# 6.B C'''
#     dxindex = 0
#     listAnswer2 = getTkAnswers(tkAnswer,"."," ")
#     for sel in browser.find_elements_by_xpath('//input[@type="text"]'):
#         sel.send_keys(listAnswer2[dxindex])
#         dxindex+=1
#         time.sleep(0.4)
#
#
#     browser.find_element_by_xpath('//input[@name="next"]').click()
#     time.sleep(4)
#     elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    #随机单选
    dxAnswer = '''1
频率与周期
a为P=1在C左时产生的Qc
自振频率
1
4
单位移动荷载
杆件为刚性杆
虚位移原理
刚体虚功原理
质点位移
直线段组成
w与wD的关系不确定
D点产生的Mk值
1
1
单位移动荷载的位置
全为零
振幅
不确定
增大EI
图片
(a)=(b)
图片
图片
图片
图片
图片'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''从形状上看连续梁影响线是曲线段图形。	对
对于弱阻尼情况，阻尼越大，结构的振动频率越小。	对
反映结构动力特性的参数是振动质点的振幅。	错
结构的动力位移总是要比静力位移大一些。	错
结构的自振频率与结构的刚度及动荷载的频率有关。	错
结构的自振频率与结构中某杆件的刚度无关。	错
结构的自振频率与质量、刚度及荷载有关。	错
静定结构的内力和反力影响线是直线或者折线组成。	对
具有集中质量的体系，其振动自由度就等于其集中质量数。	错
弱阻尼自由振动是一个衰减振动。	对
图示简支梁支座反力_FyB_的影响线是正确的。	错
图示结构_A_截面剪力影响线在_B_处的竖标为1。	对
图示结构_A_截面弯矩影响线在_A_处的竖标为_l_。	错
图示结构影响线的 _AC_ 段纵标为零 。	对
图示梁支座反力_FyA_的影响线与的影响线相同。	错
图示体系有1个振动自由度。	对
图示体系有3个振动自由度。	错
图示影响线是A截面的弯矩影响线。	对
图示影响线是C截面的弯矩影响线。	对
图示影响线中K点的竖坐标表示P=1作用在K点时产生的K截面的弯矩。	错
外界干扰力既不改变体系的自振频率，也不改变振幅。	错
弯矩影响线竖坐标的量纲是长度。	对
无阻尼单自由度体系自由振动时，质点的速度和加速度在同一时刻达到最大值。	错
一般情况下，振动体系的振动自由度与超静定次数无关。	对
影响线的横坐标是单位荷载的位置。	对
由于弱阻尼，结构的自由振动不会衰减。	错
在结构动力计算中，四质点的振动体系，其振动自由度一定为4。	错
在结构动力计算中，一个质点的振动体系，其振动自由度一定为1。	错
增大结构的刚度可以减小结构的位移，这句话也适用于动荷载作用下的结构。	错
自由振动过程中无外荷载作用。	对
阻尼对体系的频率无影响，所以计算频率时不用考虑阻尼。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [],"。	")
    for pdindex in range(10):
        pdUtil5(pdWrongAnswer, qtexts, ratios, pdindex+1, 0, pdindex)
        time.sleep(0.4)

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿
    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    # browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    # browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

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

def writeAnswerFaTie(browser,title,body):
    time.sleep(2)
    browser.find_element_by_id("id_subject").send_keys(title)
    time.sleep(6)
    browser.switch_to.frame("id_message_ifr")
    browser.find_element_by_id("tinymce").send_keys(body)
    browser.switch_to.default_content()
    browser.find_element_by_id("id_submitbutton").click()
# 等待三秒,让我们看到卷子已经答题提交完成,然后关tab,切到第一个tab,再进学习
def wait3AndCloseTab(browser):
    time.sleep(2)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1.5)


xingkao1  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=479236'
xingkao2  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=479237'
xingkao3  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=479238'
xingkao4  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=479239'
xingkao5  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=479240'


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


    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(6)
