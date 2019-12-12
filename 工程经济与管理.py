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


def danxuanAutoAnswerFix(answer, reg):
    result = []
    split = answer.split("\n")
    for i in split:
        result.append(i.strip().split(reg,1)[1].strip())
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
        listList.append(i.strip().split(reg,1)[-1].split(reg2))
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
    time.sleep(0.4)


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
            time.sleep(0.4)
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
            time.sleep(0.4)
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
                time.sleep(0.4)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer2(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''错对'''
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''12.资金在生产和流通中随时间推移而产生的增值
13.现金流量图是表示资金在不同时间点流入与流出的情况 
14.现金流量的大小、方向和作用点 
15.现金流入量 
16.流动资金 
17.前期投入的资金越多，资金的负效益越大 
18.资金用途特点 
19.先到手的资金可以用来投资而产生新的价值 
20.社会平均利润率的高低 
21.社会平均利润率越高则利率越高 
22.11.35%  
23.10.47% 
23.D
24.41700 元 
25.1490 元 
25.第一年年初
26.前者比后者大 
27.丁方案 
28.复利计息 
29.考虑货币时间价值的价值相等 
30.资金周转速度增大，资金增值率不变 
31.现值  
31.P 一定，n 相同，i 越高，F 越大  
32.（A/P,i,n） 
33.计息周期1年 
34.利息是衡量资金时间价值的相对尺度 
34.计息周期增加，年有效利率增加 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''36.箭线长短应能体现现金流量数值的差异; 横轴表示时间轴，向右延伸表示时间的延续; 箭线与时间轴的交点即为现金流量发生的时点; 垂直箭线代表不同时点的现金流量情况 
37.资金数量的多少; 资金周转的速度; 资金投入和回收的特点; 资金的使用时间 
38.通货膨胀; 借出资本风险的大小; 金融市场上借贷资本的供求情况; 社会平均利润率的高低 
39.一般而言，资金时间价值应按间断复利计算方法计算; 资金投人生产经营才能增值，因此其时间价值是在生产、经营中产生的 
40.投资风险的大小往往影响利率的高低; 在通常情况下，社会平均收益率决定的利率水平; 利率高低受资金供求关系影响; 利率是以信用方式动员和筹集资金的动力 
41.折旧; 通货膨胀 
42.流动资金; 建设投资; 经营成本 
43.利率或折现率; 资金发生的地点; 资金量的大小 
44.F=A(P/A,i,6)(F/P,i,8); A. F=A(F/A,i,6)(F/P,i,2) 
45.(P/F，i，n) = (A/F，i，n) × (P/A，i，n); (A/P，i，n) = (F/P，i，n ) × (A/F，i，n) 
46.名义利率; 实际利率 
47.当名义利率一定是，有效利率随计息周期的变化而变化; 有效利率包括计息周期有效利率和利率周期的有效利率; 当计息周期与利率周期相同时，名义利率等于有效利率; 名义利率是计息周期利率与一个利率周期内计息周期数的乘积'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿
    #计算题,相当于单选
    dxAnswer = '''48.20924.38
49.1638 
50.104.62 
51.6.15%，12.683%  
52.178604.53 
53.1234万元 
54.317.25万元'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.错
2.对
3.对
4.错
5.对
6.对
7.错 
8.对 
9.对 
10.错 '''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.经营成本＝总成本费用-折旧费-摊销费-利息支出-维简费 
2.现金支出'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''3.固定资产投资; 流动资金 
4.城市轨道交通工程; 市政工程; 桩基工程 
5.工程排污费; 住房公积金; 失业保险费 
6.建筑安装工程投资; 工程建设其它投资; 设备及工器具投资 
7.原油; 金属矿产; 天然气; 盐 
8.年数和折旧法; 双倍余额递减法 
9.建设单位管理费; 研究试验费; 工程监理费; 生活家具购置费 '''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''1.242 
2.2/10，480万元 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer4(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.对 
2.对 
3.对 
4.错 
5.错 
6.错 
7.错 
8.错 
9.错 
10.对 '''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.2万 
2.7年 
3.内部收益率受项目初始投资规模和项目计算期内各年净收益大小的影响 
4.财务净现值大于零  
5.财务内部收益率 
6.年净利润与技术方案资本金
7.37.5% 
8.Pt≤Pc 
9.FNPV>0 
10.FIRRA与FIRRB的关系不确定 
11.投资收益率 
12.动态分析指标中最常用的指标是动态技资回收期 
13.融资后分析中的静态分析 
14.年平均净收益额与技术方案投资额的比率 
15.息税前利润 
16.小于400万元
17.839万元 
18.大于基准收益率 
19.基准收益率应不低于min{单位资金成本，单位投资机会成本} 
20.财务净现值越大 
21.财务净现值减小 ，财务内部收益率不变 
22.提高基准收益率  
23.7.7%，21万元 
24.财务内部收益率大于基准收益率时，技术方案在经济上可以接受 
25.对某一技术方案，可能不存在财务内部收益率 
26.15.51%
27.方案B 
27.若△IRR> ic ，则投资大的方案较优'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.净年值; 内部收益率; 资金利润率 
2.动态投资回收期是累计净现值等于零时的年份; 动态投资回收期法和 IRR 法在方案评价方面是等价的; 当 ic=IRR 时，动态投资回收期等于项目寿命周期 
3.增量内部收益率法; 净年值法 ; 研究期法 '''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    #计算题,相当于单选
    dxAnswer = '''1.4.33年 
2.323.7万元，可行 
3.17.76%  
4.32.48 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer5(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.对 
2.对 
3.错 
4.错 
5.对 
6.错 
7.错 
8.错 
9.错
10.对'''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.产品价格→投资额→经营成本 
2.M 级 
3.风险保留 
4.市场风险 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.确定项目财务上的可靠性; 提高投资决策的科学性 
2.敏感性分析; 盈亏平衡分析 
3.实物产销量; 生产能力利用率; 年销售收入; 单位产品售价 
4.半可变（或半固定）成本; 固定成本; 可变成本 
5.修理费; 无形资产及其他资产摊销费; 折旧费; 工资及福利费 
6.敏感度系数大于零 ，评价指标与不确定性因素同方向变化; 敏感度系数的绝对值越大 ，表明评价指标对于不确定性因素越敏感 
7.技术方案总技资; 产销量; 产品价格; 经营成本 
8.敏感性分析图可以同时反映多个因素的敏感性分析结果; 敏感度系数提供了各不确定因素变动率与评价指标变动率之间的比例; 敏感性分析图中的每一直线的斜率反映了技术方案经济效果评价指标对该不确定因素的敏感程度 
9.潜在的损失是风险存在的充分条件; 经济主体是风险成立的基础; 不确定性是风险存在的必要条件 
10.理论风险; 纯风险 
11.动态风险; 静态风险 
12.客观风险; 主观风险 
13.财产风险; 信用风险; 技术风险; 责任风险 '''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1


    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer6(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.对 
2.对 
3.错 
4.错 
5.对 
6.错 
7.对 
8.对 
9.错 
10.错 '''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.租赁资产管理费
2.融资租赁是融资与融物相结合的筹资方式 
3.不能将租赁资产列入资产负债表，也不能对租赁资产提取折旧 
3.自营租赁'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.投融资主体; 投融资模式 
2.既有法人为扩大生产能力而兴建的扩建项目或原有生产线的技术改造项目; 与既有法人的资产以及经营活动联系密切的项目; 既有法人为新增生产经营所需水、电、汽等动力供应及环境保护设施而兴建的项目; 既有法人具有融资的经济实力并承担全部融资责任的项目 
3.吸收新股东投资; 政府投资; 原有股东增资扩股; 发行股票 
4.抵押债券; 信用债券 
5.以“产品支付”为基础的模式; 以“杠杆租赁”为基础的模式; 以“设施使用协议”为基础的模式; ABS模式 '''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1


    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer7(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.对 
2.对 
3.对 
4.错 
5.错 
6.对 
7.错 
8.对 
9.对 
10.对 
11.对 
12.错 
13.对 
14.错 
15.对 
11.错 '''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.项目建议书被批准之后 
2.可行性研究 
3.影子价格及评价参数选取 
4.商场观察 
5.面谈调查 
6.准确性较高 
7.针对性较强 
7.建设项目可行性研究需进行多学科论证 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.项目建设必要性; 项目建设的经济合理性; 项目建设的技术可行性 
2.与项目协作单位签订经济合同的依据; 作为经济主体投资决策的依据; 作为筹集资金和向银行申请贷款的依据; 作为该项目工程建设的基础资料 
3.费用省; 获取资料速度快 
4.未来各种市场行情发生的概率; 产出物的市场价格; 销售量和投入物; 寿命周期 
5.因果分析法; 时间序列分析法; 专家判断法 
6.德尔菲法; 专家会议法; 个人判断法 '''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1


    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer8(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.对 
2.对 
3.对 
4.错 
5.错 
6.对 
7.对 
8.错
9.错 
10.错
11.错 
11.对'''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.投资各方现金流量表 
2.100 元 
3.量入偿付法 
4.含增值税价格 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.借款还本付息计划表; 资产负债表 
2.总投资收益率; 项目资本金净利润率 
3.分项比例估算法; 资金周转率法; 生产规模指数法; 单元指标估算法 
4.计算费用效益分析指标并进行方案比选; 识别国民经济效益与费用; 计算和选取影子价格; 编制费用效益分析报表 '''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer9(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.对 
2.错 
3.对 
4.错 
5.对 
6.对 
7.对 
8.错'''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.清偿能力 
2.8% 
3.1.08%  
4.1 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.评价的计算期相同; 评价方法相同; 评价的基础工作相同  
2.评价内容不同; 两种评价使用的参数不同; 费用和效益的含义及划分范围不同'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1


    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer10(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.错 
2.错 
3.对 
4.对 '''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1


    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer11(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.错 
2.对 
3.对 
4.对 
5.错 
6.对
7.错 
8.错 
8.错 
10.错 
11.错 
12.错
13.错 
14.错 
15.错 
11.对 '''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.技术进步使设备的有形磨损加快，无形磨损减缓 
2.性能更好耗费更低的代替设备出现 
3.8000 
4.自然寿命 
5.经济寿命
6.设备的技术寿命主要是由设备的无形磨损决定的 
7.一般寿命不同时可以采用净现值法
8.8'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.设备连续使用导致零部件磨损; 设备长期闲置导致金属件锈蚀; 设备使用期限过长引起零部件老化 
1.设备耗损虽在允许范围之内 ，但技术已经陈旧落后 ，能耗高、使用操作条件不好; 设备损耗严重 ，大修后性能、精度仍不能满足规定工艺要求的 ; 设备役龄长 ，大修虽然能恢复精度，但经济效果上不如更新; 设备对环境污染严重 ，技术经济效果很不好'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer12(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    pdAnswer = '''1.对 
2.对 
3.错 
4.对'''
    dxindex = 0
    listdxanswer = danxuanAutoAnswerFix(pdAnswer, ".")
    for pd in listdxanswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    dxAnswer = '''1.成本低，功能大 
2.节约型 
3.产品功能与其全部费用的比值 
4.功能 
5.价值=功能／费用 
6.功能分析
7.功能价值低 、改善期望值大的功能 
8.方案四 
9.产品价值的提高 
10.功能定义→功能整理→功能成本分析→功能评价→确定改进范围'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''1.产品功能不变，降低成本; 产品成本不变，提高功能水平; 降低产品成本，提高功能水平 
2.在生产经营上有迫切需要的产品或项目; 改善价值上有巨大潜力的产品或项目; 对国计民生有重大影响的项目 
3.便于功能评价; 明确对象的组成和承担的功能; 便于构思新方案 
4.适量增加成本，大幅度提高项目功能和适用性; 在保证建设工程质量和功能的前提下，通过合理的组织管理措施降低成本; 通过采用新方案，既提高产品功能，又降低成本; 通过设计优化，在成本不变的前提下，提高产品功能 
5.确定改进对象; 功能评价; 功能成本分析 
6.ABC分析法经验分析法; 价值指数法; 百分比法 
7.专家函询法; 模糊目标法; 头脑风暴法'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(2)
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
    time.sleep(3)
    windowstabs = browser.window_handles
    if len(windowstabs) > 1:  # 如果没找到课程,至少别报错
        browser.switch_to.window(windowstabs[1])
        browser.find_elements_by_css_selector('img[class="pull-right"]')  # find一下,保证新页面加载完成
        browser.get(xkurl)  # 先考形1
    else:
        return 0


# 2.立即考试.判断一下,防止多次考试
def readyToTest(browser):
    time.sleep(2)
    readyTest = browser.find_element_by_xpath('//button[@type="submit"]')
    if '再次' not in readyTest.text:
        if '现在' in readyTest.text or '继续' in readyTest.text:
            readyTest.click()
            time.sleep(2)
            return 1
    return 0


# 论坛形式试卷进入方法
def readyToTestForum(browser):
    time.sleep(3)
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
    time.sleep(6)
