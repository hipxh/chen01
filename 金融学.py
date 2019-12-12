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


def pdAutoAnswer(answer, list):
    split = answer.split("\n")
    for i in split:
        if len(i) < 2:
            continue
        if '错' in i.split("。	")[1]:
            list.append(i.split("。	")[0].strip())
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
def writeAnswer1(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''从一个国家（地区）来看，所有经济部门之间的金融活动构成了整个金融体系。	错
调整利率的高低会影响整个社会的投融资决策和经济金融活动。	对
国际投资所引起的资本流动需要依附于真实的商品或劳务交易。	错
货币、汇率、信用、利率、金融工具等是现代金融运作的基本范畴，也是现代金融体系必不可少的基本要素。	对
金融供求及其交易源于社会各部门的经济活动。	对
金融源自社会经济活动并服务于社会经济活动。	对
金融总量是一国各经济主体对内的金融活动的总和。	错
居民会基于流动性、收益性和安全性来进行赤字管理。	错
现代金融体系是一个高风险的组织体系，需要政府的适度调控和合理的监管。	对
只有经济部门存在资金余缺的情况下，才产生了对金融的需求。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''信用证
国际直接投资
居民
外源融资
资金流量表
消费贷款
货币盈余
A和B
金融
政府债券'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''信贷市场; 资本市场; 货币市场; 黄金市场; 衍生金融工具市场
企业是金融机构的服务对象; 企业是金融市场的最主要的参与者; 企业财务活动对宏观金融总量与结构具有决定性影响
利率是利息额与本金之比; 利率是衡量收益与风险的尺度; 利率是现代金融体系的基本要素; 利率的高低会对借贷双方决策产生直接影响; 利率是政府调节社会经济金融活动的工具
在银行存款; 投资股票; 向民间钱庄申请贷款
货币; 汇率; 信用; 利率; 金融工具
存款业务; 贷款业务; 资金清算
国外企业采用合作方式在本国建立新企业; 收购国外企业的股权，并成为绝对最大股东; 将前期投资利润继续投资国外企业
信贷总量; 保险市场规模; 货币总量
增加税收; 向中央银行申请贷款; 发行政府债券
政府投资导致的大量货币收支，对货币流通产生了重要影响; 政府投资带动民间资本，引起整个金融资源的流向发生改变; 政府通过设立主权财富基金，利用外汇储备对国际金融市场产生影响'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer2(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''广义货币量反映的是整个社会潜在的购买能力。	错
国家货币制度由一国政府或司法机构独立制定实施，是该国货币主权的体现。	对
货币天然是金银，金银天然不是货币。	对
货币作为价值贮藏形式的最大优势在于它的收益性。	错
交换媒介职能和资产职能都是货币最基本的职能。	错
金币本位制、金汇兑本位制和金块本位制下主币可以自由铸造，辅币限制铸造。	错
我国货币层次中的M0即现钞是指商业银行的库存现金、居民手中的现钞和企业单位的备用金。	错
我国货币的发行量取决于我国中央银行拥有的黄金外汇储备量。	错
牙买加体系规定美元和黄金不再作为国际储备货币。	错
一定时期内货币流通速度与现金、存款货币的乘积就是货币存量。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''实物货币
金币本位制
金融资产的流动性
商品买卖
货币是固定充当一般等价物的商品
布雷顿森林体系
交换需要说
保持固定汇率
现金
货币增量'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''金币本位制; 金汇兑本位制; 金块本位制
纸币; 存款货币; 银行券
便于携带; 价值较高; 易于保存; 易于分割
选择国际收支的调节方式; 确定国际储备资产; 安排汇率制度
计价单位; 支付手段; 交换手段
税款交纳, 贷款发放, 商品赊销, 工资发放
金属货币增长受储量和开采量的限制，纸币和存款货币的规模央行可以灵活掌握; 金属货币具有内在价值，而纸币和存款货币本身没有内在价值; 金属货币的币值相对稳定，而纸币和存款货币受物价影响较大
人民币不规定含金量，是不兑现的信用货币; 人民币是我国法定计价、结算的货币单位; 人民币采用现金和存款货币两种形式
金融产品创新速度越快，层次划分的变动就越频繁; 随着流动性的减弱，货币包括的范围在扩大
现金; 银行活期存款'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''不管是直接标价法下还是间接标价法下，买入汇率总是低于卖出汇率。	错
布雷顿森林体系下的汇率制度是以黄金——美元为基础的、可调整的固定汇率制。	对
浮动汇率制允许汇率随外汇市场供求关系的变化而自由波动，各国货币当局无需干预外汇市场。	错
根据利率平价理论，利率与汇率的关系是：利率高的国家货币在远期外汇市场上升水，利率低的国家货币在远期外汇市场上贴水。	错
换汇成本是购买力平价在中国的现实运用，所以二者是可以等价的。	错
汇率是两国货币的兑换比率，是一种货币用另一种货币表示的价格。	对
外汇即外国货币。	错
相对购买力平价是指在某一时点上两国货币之间的兑换比例取决于两国物价总水平之比。	错
远期汇率高于即期汇率称为升水；远期汇率低于即期汇率称为贴水。	对
越南盾、缅甸元由于是非自由兑换货币，因而不是外汇。	对'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''相对购买力平价理论
1人民币=0.14064美元
流动债务大于流动债权
黑客入侵外汇交易系统导致损失
国际金本位制下的
以市场供求为基础的、参考一篮子货币进行调节、有管理的浮动汇率制
特别提款权
可调整的固定汇率制
中间汇率
买入汇率和卖出汇率'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''利率高的国家货币在远期外汇市场上贴水; 利率低的国家货币在远期外汇市场上升水; 即期汇率与远期汇率相等时为平价
基本思想是汇率取决于两国货币购买力的相对关系; 绝对购买力平价认为两国货币之间的兑换比率取决于两国物价水平之比 ; 本国货币购买力相对于外国货币购买力下降时，本币趋于贬值; 本国货币购买力相对于外国货币购买力上升时，本币趋于升值
购买力平价理论; 利率平价理论
进出口; 物价; 资本流动; 金融资产的选择
出口增加; 进口减少 
国际借贷理论  ; 利率平价理论; 汇兑心理说; 购买力平价理论
进口商品为非必需品; 出口商品需求弹性高; 国内总供给能力强; 国内具有闲置资源
直接标价法下，外币的数额固定不变，本币的数额随币值变化; 直接标价法下，汇率越高，本币价值越低; 间接标价法下，汇率越高，本币价值越高
以浮动汇率为主导; 以信用本位为基础; 成员国一般可自主决定其汇率安排
电汇汇率是外汇市场的基准汇率; 信汇汇率低于电汇汇率; 票汇汇率低于电汇汇率'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer4(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''高利贷是前资本主义社会的信用形式，在资本主义生产方式确立与现代银行和信用体系建立之后，这一信用形式已不复存在。	错
货币和信用是两个不同的范畴，二者的发展始终保持相对独立的状态。	错
货币借贷是现代信用的惟一形态。	错
商业票据可以通过背书流通转让，发挥货币交换媒介职能，因而被称为商业货币。	对
社会化大生产是信用产生的前提条件。	错
私有财产的出现是借贷关系赖以存在的前提条件。	对
现代经济社会对政府信用利用得越来越多，这主要是由于弥补财政赤字的需要。	对
在筹资成本、投资收益和安全性等方面，直接融资都是优于间接融资的。	错
在现代经济活动中，政府信用主要表现为政府作为债权人而形成的债权。	错
在现代社会中，任何信用活动几乎都是货币运动：信用的扩张与紧缩意味着对货币供给与流通的调整，微观主体的信用活动意味着货币在不同主体之间的流动。	对'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''诚实履行自己的承诺取得他人信任
信用制度
卖方
产权制度
现代经济中广泛存在着赤字和盈余单位
以还本付息为条件的价值单方面转移
贷款
安全性高
安全性
发行政府债券'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''具有利率不稳定且差异大的特点; 高利贷者确定利率有绝对话语权和很大随意性; 高利盘剥招致民众强烈反抗; 是奴隶社会和封建社会基本的信用形式
资金来源于社会各部门暂时闲置的资金，可以达到非常大的规模; 可满足贷款人在数量和期限上的多样化需求
企业; 政府
割断了资金供求双方的直接联系; 增加了筹资者成本并减少了投资者收益; 较难满足新兴产业和高风险项目的融资需求
具有法律保障的承载信用关系的契约;  具有交易对冲能力或变现能力; 能给交易者带来货币或非货币收益; 市场价值变化带来收益与损失的不确定性 
还本付息为条件的借贷活动; 体现债权债务关系; 会涉及道德范畴的信用
银行向客户发行信用卡 ; 银行对消费者发放抵押贷款; 企业以赊销方式对消费者销售商品
私有制的出现; 调剂财富余缺的需要
在现代社会，各经济主体之间都存在着错综复杂的信用关系; 各类经济活动的开展，都需要信用作为支撑; 现代信用活动中，信用工具呈现多样化的趋势
信用档案系统 ; 信用调查系统; 信用评估系统; 信用查询系统; 失信公示系统'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer5(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''当名义利率高于通货膨胀率时，实际利率为负，我们称之为负利率。	错
当一国处于经济周期的危机阶段时，利率会不断下跌。	错
当债券溢价发行时，其到期收益率高于票面利率。	错
费雪效应是指名义利率等于实际利率与通货膨胀率之和。	对
风险相同的债券，因为期限不同而形成不同的利率，我们称之为利率的风险结构。	错
马克思认为，利息在本质上是利润的一部分。	对
物价水平不变从而货币实际购买力不变时的利率我们称为实际利率。	对
远期利率是隐含在给定即期利率中的从现在到未来某一时点的利率。	错
在利率体系中发挥指导性作用的利率是官定利率。	错
在其他条件相同的情况下，现值的大小与贴现率正相关，即贴现率越低，现值越小。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''只有复利才反映了利率的本质
银行超额准备金存款
先外币、后本币，先贷款、后存款  
负；抑制
借贷资本
物价变动率
持有期收益率
未来上市公司的盈利水平有可能降低，会导致资产价格下跌
4％
借贷风险'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''公定利率; 官定利率; 市场利率
长期利率; 短期利率
紧缩的货币政策; 通货膨胀; 经济高增长
名义利率高于预期通货膨胀率时，实际利率为正;名义利率低于预期通货膨胀率时，实际利率为负
法律、习惯; 剩余价值
名义利率扣除通货膨胀率即为实际利率; 实际利率调节借贷双方的经济行为; 名义利率是包含了通货膨胀因素的利率
在繁荣阶段，利率会上升; 在复苏阶段，利率会上升; 在萧条阶段，利率会降低; 在危机阶段，利率会逐渐升高
违约风险; 汇率变动风险; 税收风险 ; 购买力风险; 流动性风险 
抑制物价上涨; 抑制企业对信贷资金的需求; 减少居民个人的消费信贷
债券面额 ;债券的市场价格; 债券期限; 票面利率'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer6(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''柜台交易方式是指在各个金融机构柜台上进行面议、分散交易的方式。	对
黄金现在已经不是货币，只是普通商品，所以黄金市场也不应该算是金融市场。	错
金融机构是金融市场上的最重要的中介机构。	对
金融市场的参与者非常广泛，包括中央银行、金融机构、企业和居民，但是不包括政府在内。	错
居民参与金融市场就是提供资金。。	错
套期保值是衍生金融工具为交易者提供的最主要的功能。	对
外汇市场的功能是为交易者提供外汇资金融通的便利，但是不可以满足投机的需求。	错
衍生金融工具包括期货、期权、互换、债券等各种标准化合约。	错
债券市场既可以属于货币市场的，也可以属于资本市场的。	错
政府是一国金融市场上主要的资金需求者，而中央银行是主要的资金供给者。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''本币汇率升值，本国产品的竞争力增强，出口型企业证券价格就可能上涨
风险低，收益稳定，流动性较强
要素市场
法定存款准备金
2002年
股票
批发市场
零售市场
阿姆斯特丹证券交易所 
公开市场业务操作'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''黄金市场; 证券市场; 衍生工具市场
期货市场; 现货市场
提高保险交易的效率; 可以形成较为合理的交易价格 ; 提供有效的保险供给; 可以提供最广泛的风险分散机制 
人身保险市场 ; 财产保险市场
原保险市场; 再保险市场
资源转化; 资源配置; 价格发现; 风险分散和规避; 宏观调控传导
股票; 债券
优先股; 普通股
价格发现; 套期保值; 投机套利
中长期债券市场; 银行中长期信贷市场; 股票市场'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer7(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''非金融性企业参与回购协议市场的目的是在保持良好流动性的基础上获得更高的收益。	错
货币市场是指以期限在1年以上的金融工具为媒介进行短期资金融通的市场。	错
可转让大额定期存单是金融创新的典型，结合了定期存款的流动性和活期存款的收益性。	错
可转让大额定期存单综合了流动性和收益性，因此利率较高。	错
票据经过银行承兑之后具有相对小的信用风险，是一种信用等级较高的票据。	对
相比将票据持有到期，商业票据的持有者更倾向于在二级市场进行票据转让，因为这样可以获得更高的收益。	错
银行承兑汇票可看做是银行对外提供信用担保的一种形式。	对
中央银行参与回购协议市场的目的是进行货币政策操作。	对
中央银行既可以直接在发行市场上购买国库券，也可以在流通市场上进行国库券买卖。	错
XYZ证券公司预期未来利率会上升，则它可以通过持有期限较长的逆回购协议和期限较短的回购协议来获利。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''货币市场利率
贴现
风险较大
回购市场
再贴现
法定存款准备金
地方政府
高收益性
20%
回购利率'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''14天; 1-4个月; 6个月; 超过6个月
回购期限; 证券流动性
交易期限短; 流动性强; 安全性高; 交易额大
流动性管理; 基准利率生成;
宏观调控; 满足短期融资
安全性; 流动性; 收益性
直接募集; 交易商募集
面额大; 不记名; 金额固定; 允许转让
同业拆借市场; 回购协议市场; 国库券市场; 票据市场
商业银行; 保险公司; 财务公司
证券流动性越高，回购利率越低; 回购期限越长，回购利率越高; 采用实物交割的回购利率较低'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer8(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''产业生命周期各阶段的风险和收益状况不同，但处于产业生命周期不同阶段的产业在证券市场上的表现就不会有较大的差异。	错
发达完善的资本市场是一个多层次的资本市场。	对
广义的资本市场包括中长期债券市场、股票市场和基金市场。	错
汇率政策的调整对证券市场基本上不产生影响。	错
货币政策的调整对证券市场具有持久但较为缓慢的影响。	错
我国资本市场的中小企业板是指主板之外的专为暂时无法上市的中小企业和新兴公司提供融资途径和成长空间的证券交易市场，是对主板市场的有效补充，在资本市场中占据着重要的位置。	错
有效市场假说表明，证券价格由信息所决定，已经包含在当前价格里的信息对于预测未来价格毫无贡献。从这个意义上说，有效市场假说肯定了资本市场的投资分析的作用。	错
在发达的金融市场上，场内交易在交易规模和品种上占有主导地位。	错
在证券发行市场中，证券发行人和证券投资者共同构成市场的参与主体。	错
证券发行方式有私募发行、公募发行、直接发行、间接发行。	对
证券发行市场是投资者在证券交易所内进行证券买卖的市场。	错
证券流通市场上的组织方式主要分为场内交易和场外交易两种。	对
证券商是在证券交易所充当交易中介而收取佣金的商人。	错
证券商与证券经纪人的差别在于证券商自营证券，自负盈亏，风险较大。	对
证券上市也称为证券发行。	错
证券中介机构主要是指作为证券发行人与投资人交易媒介的证券承销人，它通常是负担承销义务的投资银行、证券公司或信托投资公司，其他机构则不能作为证券中介机构。	错
资本市场的是资源有效配置的场所。	对
资本市场的特点之一是交易收益可以确定。	错
资本市场是筹资与投资平台。	对
资本市场有利于促进并购与重组。	对'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''创业板市场
沪港通市场
有价证券市场
增加政府财政收入
筹资的目的是满足周转性资金需要
溢价发行
证监会
1年'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''银行中长期信贷市场; 有价证券市场
长期资本流动; 短期资本流动
主板市场; 中小企业板; 创业板市场; 股份转让报价系统与“新三板”市场; 区域性股权交易市场
中长期债券市场; 股票市场; 基金市场
私募发行; 公募发行; 直接发行; 间接发行
证券发行人; 证券投资者; 证券中介机构
显性成本; 隐性成本
开设股东账户及资金账户; 委托买卖; 竞价成交; 清算、交割与过户
证券经纪人; 证券商
证券交易所交易; 柜台交易; 无形市场交易
宏观经济运行周期; 宏观经济政策; 产业生命周期; 公司状况
技术指标法; 切线法; 形态法; K线法; 波浪法
筹资与投资平台; 资源有效配置的场所; 促进并购与重组; 促进产业结构优化升级
交易工具的期限长; 筹资目的是满足投资性资金需要; 筹资和交易的规模大'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()

def writeAnswer9(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''“受人之托，代人理财”是信托的基本特征，其实质是一种财产转移与管理或安排。	对
储蓄银行是以社员认缴的股金和存款为主要负债、以向社员发放的贷款为主要资产并为社员提供结算等中间业务服务的合作性金融机构。	错
金融机构的产生与发展内生于实体经济活动的需要。	对
金融租赁公司兴起于20世纪初，是为企业技术改造、新产品开发及产品销售提供金融服务，以中长期金融业务为主的非银行金融机构。	错
经纪类证券公司既可从事经纪业务，又可开展自营、承销及其他业务。	错
融资和提供金融服务是金融机构最基本的功能。	对
提供经济保障、稳定社会生活是保险机构的基本作用。	错
我国在1984年形成了以财政部为核心，以工、农、中、建四大专业银行为主体，其他各种金融机构并存和分工协作的金融机构体系。	错
我国在1999年后分业经营的管理体制有所松动，出现混业趋势。	对
小额贷款公司由自然人、企业法人与其他社会组织投资设立，以服务“三农”为宗旨，其和商业银行一样，可吸收公众存款。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''国际货币基金组织
金融资产管理公司
支付结算服务
中国人民银行
投资银行
1953-1978年
合作金融机构
国际清算银行'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''国家开发银行 ; 中国进出口银行; 中国农业发展银行
政策性金融机构 ;  商业性金融机构
财产保险公司; 人寿保险公司; 再保险公司
台湾地区的金融体系包括正式的金融体系与民间借贷两部分; 台湾地区的货币金融体系由“行政院金融监督管理委员会”及“中央银行”共同管理; 港元是由香港政府通过法律授权某些信誉卓著、实力雄厚的大商业银行发行的;  20世纪80年代以后，以银行为主体的澳门金融业已成为澳门经济的四大支柱产业之一
世界银行集团; 国际货币基金组织; 国际清算银行
世界银行; 国际开发协会; 国际金融公司; 多边投资担保机构; 国际投资争端处理中心
独立托管、保障安全; 集合理财、专业管理; 利益共享、风险共担;  严格监管、信息透明; 组合投资、分散风险
信达金融资产管理公司; 东方金融资产管理公司 ; 华融金融资产管理公司; 长城金融资产管理公司
保险公司; 信托投资公司; 财务公司; 金融租赁公司; 证券公司
证券公司;  投资基金管理公司'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer10(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''存款是商业银行最主要的负债业务，一般分为活期存款、定期存款和储蓄存款三类。	对
控股公司制是指由某一个人或某一个集团购买若干家独立银行的多数股票，从而控制这些银行的组织形式。	错
商业银行的产生可概括为：由货币兑换业、货币保管业到货币经营业，进而形成商业银行。	对
商业银行的自有资本属于资产业务范畴。	错
商业银行风险管理包括风险衡量和风险控制两方面内容。	错
商业银行风险管理的重点是将风险控制在可承受的范围之内。	对
商业银行具有内在脆弱性和较强的风险传染性。	对
商业银行是特殊的金融企业。	对
信贷资产是商业银行保持流动性的最重要的资产。	错
一般而言，流动性强的资产盈利性高，而高盈利性往往伴随高风险性。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''信用中介
创新的表外业务
流动性
信用风险
总分行制
英格兰银行
贷款承诺
负债业务
核心资本
风险识别 '''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''贷款承诺; 回购协议; 票据发行便利; 期权; 担保
其他负债业务; 存款业务; 借款业务
单一银行制; 总分行制; 控股公司制; 连锁银行制
盈利性; 安全性; 流动性
可转换性理论; 真实票据理论; 预期收入理论
信用创造; 降低交易成本; 充当信用中介; 充当支付中介; 转移与管理风险
风险较低; 流动性较强; 信用较高
在以客户为中心理念下发展业务; 业务创新; 业务经营互联网化; 业务经营电子化
在以客户为中心理念下发展业务; 业务经营电子化; 业务创新; 业务经营互联网化
代理业务; 结算业务; 信托业务 
同业存款; 库存现金; 存放中央银行'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer11(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''2003年以后监管商业银行的业务经营成为中国人民银行的重要职责之一。	错
充当最后贷款人是中央银行作为“政府的银行”职能的体现。	错
独享货币发行垄断权是中央银行区别于商业银行的最初标志。	对
二元式中央银行制度与邦联制的国家体制相适应，在国内设立中央和地方两级相对独立的中央银行机构，地方机构有较大独立性。	错
美国联邦储备体系的影响遍及全球，其类型与组织形式也属于跨国中央银行制。	错
在组织结构上逐步实行国有化、明确中央银行宏观调控的任务、法律为宏观调控提供保障是中央银行制度完善、健全的标志。	对
中央银行的产生有两条渠道：一是信誉好、实力强的大银行由政府赋予一定的特权而发展为中央银行；二是由政府出面直接组建中央银行。	对
中央银行的存款业务不针对普通公众办理，且不以盈利为主要目的，具有一定的强制性。	对
中央银行的货币发行在资产负债表中列在资产一方。	错
中央银行对金融机构的负债比债权更具主动性和可控性。	错
中央银行是特殊的银行，其职能的发挥要求它必须保持一定的独立性。但是中央银行对政府的独立性总是相对的。因而，中央银行与政府的利益总是冲突的。	错
中央银行虽然也称银行，却是特殊的银行，其特殊性体现为目标与职能的特殊。	错
中央银行业务活动原则中的非盈利性注定了中央银行在其业务活动中不能获得利润。如果中央银行在其业务活动中获得了盈利，则违反其非盈利性业务活动原则。	错
中央银行由于独占货币发行权，因此，只要控制了货币发行，也就控制了货币供给。	错
中央银行作为“政府的银行”，对政府的要求应当有求必应，在政府财政困难时，应当及时出手，确保政府赤字及时得到弥补，不至于威胁到金融体系的稳定。	错
中央银行作为国家宏观经济管理的重要部门，亦是通过强有力的政治权利和行政手段，达到宏观调控的目标。	错
资本业务属于中央银行的资产业务。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''银行的银行
债权
单一中央银行制
提供经济信息服务
充当最后贷款人
政府债券
中央银行
黄金和外汇
二元式中央银行制度
中央银行
中央银行与政府
回笼货币
独享货币发行垄断权
迫使商业银行提高贷款利率
风险性'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''货币发行; 政府存款
成立于1694年的英格兰银行被世界公认为第一家中央银行; 中国人民银行成立于1948年12月1日; 1983年9月，国务院决定中国人民银行专门行使中央银行的职能，标志着现代中央银行制度在我国的确立
国外资产; 对非金融企业债权; 对非货币金融机构债权; 对政府债权; 对存款机构债权
货币发行基金; 业务库的管理
解决银行券分散发行的缺陷的需要; 提高票据交换和清算效率的需要; 充当最后贷款人的需要; 解决政府筹资问题的需要; 金融监管的需要
国外资产业务; 政府债券; 再贴现和再贷款; 对金融机构债权
防止通货膨胀与金融危机 ; 促进经济发展; 保障充分就业; 平衡国际收支
法定业务权力; 法定业务范围; 法定业务限制
非盈利性; 流动性; 公开性; 主动性
发行的银行; 政府的银行; 银行的银行
集中存款准备金; 充当最后贷款人; 组织、参与和管理全国清算业务; 监督管理金融业
主观上不以盈利为目的 ; 不经营普通银行业务; 制定并执行货币政策; 独享货币发行的特权'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer12(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''持有合理的外汇储备资产组合对防范金融风险有重要意义，也是国际储备规模管理的主要内容。	错
存款扩张倍数大小与法定存款准备金率、提现率和超额准备金率之间呈正方向变动的关系。	错
存款扩张倍数或存款乘数，实际上就是货币乘数。	错
对货币需求者来说，重要的是货币具有的购买力高低而非货币数量的多寡，因而比较关心实际货币需求。	对
法定准备金率的高低与商业银行创造存款货币的能力呈正相关关系。	错
工资-价格螺旋上涨引起的通货膨胀是需求拉上型通货膨胀。	错
黄金虽然已经退出了货币历史舞台，但在国际储备资产中仍然是最重要的和占据主要份额的资产。	错
货币供给量是基础货币与存款乘数的乘积。	错
货币供给由中央银行和商业银行的行为共同决定。	对
货币需求量的决定与变化主要受收入、财富等规模变量的影响。	错
剑桥方程式与交易方程式同属古典学派货币需求理论或货币数量论。	对
居民消费价格指数、生产价格指数和GDP平减指数是度量通货膨胀与通货紧缩的共同指标。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''强制储蓄
下降，增加
持币的机会成本越大
投机性货币需求无限大
再贴现 
持久性收入
M2
流通中现金和存款准备金
公众的行为
MV＝PT
已从银行获得贷款的债务人受益
货币乘数 
用外汇储备购买国外资产
货币乘数
存款乘数'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''马克思的货币需求理论; 交易方程式
经常账户; 资本账户 ; 金融账户; 净误差与遗漏; 储备资产
经济发展状况; 货币性因素; 经济结构影响; 外汇投机与国际资本流动; 经济周期影响
货币供给的主体是央行和商业银行; 央行创造现金通货，商业银行创造存款货币
居民的经济行为; 企业的经济行为; 金融机构的经济行为; 政府的经济行为
交易动机; 预防动机; 投机动机
交易性货币需求是收入的增函数; 投机性货币需求是利率的减函数
法定存款准备金率; 提现率（现金漏损率）; 超额准备金率
物价持续下降; 信贷和货币供给量下降; 伴随着经济衰退
经济衰退失业增加; 投资收益下降; 社会生产萎缩; 信用关系断裂; 银行不良贷款上升
强制储蓄信用; 收入分配效应; 资产结构调整效应; 恶性通胀下的危机效应
货币供应量由货币乘数和基础货币决定; 提现率越高，货币供应量越小
中央银行降低法定准备金率; 商业银行减少库存现金的持有规模; 企业增加支票支付的比例
央行购买外汇、黄金; 央行购买政府债券; 央行向商业银行提供再贷款和再贴现; 央行购买金融债券
货币供给与货币需求基本相适应的货币流程状态 ; 是一种在经常发生的货币失衡中暂时达到的均衡状态 ; 是社会总供求均衡的反映
收入; 财富; 金融资产收益率; 机会成本
商业银行在央行存放的超额准备金; 商业银行的库存现金; 企业和家庭持有的现金; 商业银行在央行存放的法定准备金
消费价格指数; 生产价格指数; 国内生产总值平减指数 
中央银行市场干预和调控; 财政收支基本平衡; 经济结构的合理性; 国际收支基本平衡'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer13(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''超额准备金由于不受中央银行直接控制，因而不能作为货币政策的操作指标。	错
充分就业目标就是要消除失业，或将失业率降到极低的水平。	错
从中央银行采取行动到对政策目标产生影响所经过的时间称之为行动时滞。	错
法定存款准备金政策通常被认为是货币政策最猛烈的工具之一。因为它通过决定或改变货币乘数来影响货币供给，因此，即使准备金率调整的幅度很小，也会引起货币供应量的巨大波动。	对
菲利普斯曲线表明物价稳定和充分就业这两个货币政策目标之间存在此消彼长的关系；但是，自然律假说反对这种观点，提出物价稳定和充分就业之间并不矛盾。	对
货币传导论认为，货币政策操作以后，传导主要是通过金融资产价格和信贷渠道完成。	错
货币政策的操作指标处于中介指标与最终目标之间，因而距离最终目标更近。	错
利率作为货币政策的中介指标，优点是可测性和相关性都较强，但抗干扰性较差。	对
量化宽松的货币政策以利率是零或负值为基本特征。	错
我国货币政策目标是“保持货币币值稳定，并以此促进经济增长”，实质上是将经济增长作为基本立足点。	错
选择性货币政策工具通常可在不影响货币供给量的条件下，影响银行体系的资金投向和不同贷款的利率。	对
一般而言，货币政策中介指标的可控性、可测性要强于操作指标，而相关性则弱于操作指标。	错
再贴现政策是三大法宝中唯一一个主动权并非只在中央银行手中的工具。	对
在一般性货币政策工具中，主动性和灵活性强，调控效果最为和缓的是再贴现政策。	错
中央银行在公开市场上卖出有价证券，只是等额地回笼基础货币，而非等额地回收货币供给量。	对'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''币值
稳定货币
银行金融机构至非银行金融机构
准备金和基础货币
道义劝告
基础货币
国际金融危机的冲击或扰动
银行间同业拆借利率
货币供求在数量和结构上的均衡
能避免金融机构的道德风险
金融价格传导论
稳定物价
经济增长与充分就业
法定存款准备金政策
窗口指导'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''货币供应量; 信用总量; 同业拆借利率; 银行超额准备金率
主动性强; 灵活性强; 调控效果和缓，震动性小; 告示效应强
中介指标; 政策目标; 政策工具; 操作指标
金融稳定; 充分就业; 经济增长; 国际收支平衡; 稳定币值
稳定物价与充分就业; 物价稳定与经济增长; 物价稳定与国际收支平衡; 经济增长与国际收支平衡
中央银行要有高度的独立性; 中央银行要有精确预测通货膨胀率的能力; 要确定合理的通货膨胀目标区间
不动产信用控制; 消费信用控制; 优惠利率; 预缴进口保证金; 证券市场信用控制
主动权并非只在中央银行; 调节作用有限; 是中央银行利率; 可能加大金融机构的道德风险
可测性；相关性；抗扰性；可控性
采用信用配额; 规定金融机构流动性比率; 规定利率限额; 直接干预'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer14(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''1994年的金融体制改革以后，中国人民银行先后将其证券、保险、银行监管职责分别转交给了证监会、保监会、银监会，已不再负有金融监管职责，成为专门制定与执行货币政策的机构。	错
各国监管机构对金融机构的监管，主要是对金融机构日常运营的监管。	错
金融监管不是单纯检查监督、处罚或纯技术的调查、评价，而是监管当局在法定权限下的具体执法行为和管理行为。	对
金融监管从对象上看，主要是对商业银行、金融市场的监管，非银行金融机构则不在其列。	错
金融监管中由政府负担的成本是奉行成本。	错
金融体系的负效应表现在金融体系的风险和内在不稳定性等方面。	对
美国和英国都是实行多元化监管体制的代表，其金融监管是由多个监管机构承担的。	错
内部知情人利用地位、职务或业务等便利，利用未公开信息进行有价证券交易或泄露该信息的行为，是典型的证券欺诈。	错
抓住关键问题或重要环节进行特别监管，称为全面监管。	错
资本充足性监管是市场准入监管的主要内容。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''《格拉斯-斯蒂格尔法案》
坚持公开、公平、公正的“三公”原则
保护投资者的合法权益
证券业
中国人民银行
自然理论
严格执法不干涉内部管理 
行政成本
凸显中央银行在监管中的地位，强调宏观审慎监管
单一
混合监管
外部监管与内部自律
国际性法律
间接效率损失
分权型多头监管'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''集中监管体制; 分业监管体制
对证券机构的监管; 对证券市场的监管; 对上市公司的监管
市场准入监管; 日常经营监管; 市场退出监管
资本监管 ; 审慎信贷标准; 流动性风险指标; 贷款损失监管; 其他风险管理要求
金融监管的理论体系; 金融监管的法律体系; 金融监管的组织体系; 金融监管的内容体系
被监管者的道德风险; 妨碍金融创新，导致动态低效率; 削弱竞争，导致静态低效率; 监管过度，导致金融服务效率降低
确保金融稳定安全，防范金融风险; 保护金融消费者权益; 提高金融体系效率; 规范金融机构行为，促进公平竞争
不干涉金融机构内部管理原则; 依法监管与严格执法原则; 综合性与系统性监督原则; “内控”与“外控”相结合的原则; 公平、公正、公开原则
美国; 加拿大
中国人民银行; 银监会; 证监会; 保监会'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer15(browser):
    time.sleep(2)
    elements1 = browser.find_elements_by_xpath('//label')
    print(len(elements1))
    elements1p = browser.find_elements_by_xpath('//p')


    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    qtexts = browser.find_elements_by_xpath('//div[@class="qtext"]')
    pdAnswer = '''当代金融创新革新了传统的业务活动和经营管理方式，加剧了金融业竞争，形成了放松管制的强大压力，但并未改变金融总量和结构。	错
当代金融创新在提高金融宏观、微观效率的同时，也减少了金融业的系统风险。	错
国际货币制度创新的其中一个重要表现是区域性货币一体化趋势，它与国际金融监管创新同属于金融组织结构创新。	错
金融已成为现代经济的核心，现代经济也正逐步转变为金融经济。	对
金融在整体经济中一直居于主导地为，它可以凌驾于经济发展之上。	错
经济货币化与经济商品化成正比，与货币作用力成反比。	错
经济金融化与金融全球化推进了经济、金融相互融合，使金融高度发达，减少了金融的脆弱性。	错
商品化是货币化的前提和基础，商品经济的发展必然伴随着货币化程度的提高。	错
现代金融业的发展在有力推动经济发展的同时出现不良影响和负作用的可能性越来越大。	对
一般地，金融结构越趋于简单化，金融功能就越强，金融发展的水平也就越高。	错'''
    pdWrongAnswer = pdAutoAnswer(pdAnswer, [])
    for pdindex in range(5):
        pdUtil5(pdWrongAnswer, qtexts[13:18], ratios, pdindex, 5, pdindex)
        time.sleep(0.3)


    dxAnswer = '''正比
利大于弊
内生性
良性循环
决定性
正比
国际货币制度的创新
金融风险
金融业务创新
金融相关率'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEqualsNotJudge(elements1[0:20], an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.4)
        dxindex += 1


    mulAnswer = '''新技术在金融业中广泛应用; 金融工具不断创新; 新业务和新交易大量涌现
提高金融机构的运作效率; 提高金融市场的运作效率; 增强金融产业的发展能力; 增强金融作用力
提高了金融资源的开发利用与再配置效率; 社会投融资的满足度和便利度上升; 金融业产值的迅速增长; 增强了货币作用效率
金融活动为经济发展提供基础条件; 金融促进社会储蓄，并促进储蓄转化为投资; 金融活动节约社会交易成本，促进社会交易的发展; 金融业的发展直接为经济发展做出贡献
通过促进国际贸易和国际投资的发展推动世界经济增长; 加强了金融监管领域的国际协调与合作
增大金融风险; 加强了金融监管领域的国际协调与合作; 加快金融危机在全球范围内的传递，增加了国际金融体系的脆弱性
金融机构全球化; 金融业务全球化; 金融市场全球化; 金融监管与协调全球化
投融资功能; 服务功能; 风险管理
经济发展的商品化和货币化程度; 商品经济的发展程度; 信用关系的发展程度; 经济主体行为的理性化程度; 文化、传统、习俗与偏好
制度因素; 金融创新的活跃程度; 开放程度'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEqualsNotJudge(elements1[20:45], v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.4)
        dxindex += 1

    browser.find_element_by_xpath('//input[@type="submit"]').click()
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


xingkao1  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471623'
xingkao2  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471651'
xingkao3  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471679'
xingkao4  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471705'
xingkao5  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471723'
xingkao6  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471741'
xingkao7  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471763'
xingkao8  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471785'
xingkao9  = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471813'
xingkao10 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471841'
xingkao11 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471867'
xingkao12 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471895'
xingkao13 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471921'
xingkao14 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471944'
xingkao15 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=471964'
xingkao16 = 'http://hubei.ouchn.cn/mod/forum/view.php?id=471968'
xingkao17 = 'http://hubei.ouchn.cn/mod/forum/view.php?id=471969'
xingkao18 = 'http://hubei.ouchn.cn/mod/forum/view.php?id=471972'

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

        enterTest(browser, xingkao13)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer13(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao14)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer14(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao15)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer15(browser)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao16)
        if readyToTestForum(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswerFaTie(browser,"汇率","汇率亦称“外汇行市或汇价”。一国货币兑换另一国货币的比率,是以一种货币表示的另一种货币的价格。由于世界各国货币的名称不同,币值不一,所以一国货币对其他国家的货币要规定一个兑换率,即汇率。 而人民币汇率就是人民币兑换另一国货币的比率。 2005年7月21日,人民银行突然宣布,经国务院批准,人民币汇率改为参考一篮子货币,汇率改为1美元兑8.11元人民币,变相升值2%,并且不再与美元挂钩。中国人民银行于每个工作日闭市后公布当日银行间即期外汇市场美元等交易货币对人民币汇率的收盘价,作为下一个工作日该货币对人民币交易的中间价格。每日银行间外汇市场美元对人民币的交易价仍在人民银行公布的美元交易中间价上下千分之三的幅度内浮动,非美元货币对人民币的交易价在人民银行公布的该货币交易中间价上下一定幅度内浮动。人民币汇率一篮子机制就是综合考虑在中国对外贸易、外债(付息)、外商直接投资(分红)等外经贸活动占较大比重的主要国家、地区及其货币,组成一个货币篮子,并分别赋予其在篮子中相应的权重。具体来说,美元、欧元、日元、韩元等自然成为主要的篮子货币。此外,由于新加坡、英国、马来西亚、俄罗斯、澳大利亚、泰国、加拿大等国与中国的贸易比重也较大,它们的货币对人民币汇率也很重要。 从图表中我们看到总体相对稳定的汇率除了人民币汇率单方向升值和贬值的选择以外, 保持相对稳定,也是目前汇率变动的一种选择,很可能也是在当前动荡的国 际经济形势下,人民币汇率最可取的改革思路。")
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao17)
        if readyToTestForum(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswerFaTie(browser,"影响股票价格的各种因素","影响股票价格变动的因素很多，并且错综复杂。但一般传统金融学认为，基本上可分为宏观、中观和微观三类，即宏观因素、行业和区域因素、公司因素。（一）宏观因素它包括对股市及个股可能产生影响的社会、政治、经济、军事、文化等方面的因素。宏观经济因素主要能影响市场中股票价格的因素，包括经济增长、经济景气循环、利率、财政收支、货币供应量、物价和国际收支等。银行存款利率及债券市场利率水平，在影响股票价格的各种经济因素中是最敏感的因素，利率水平与股票价格成反比关系，国家总体经济状况与社会政治局势的稳定性因素也是重点影响因素之一，如通货膨胀，既有刺激股价上扬的作用，也有压抑股价的作用。国家政策因素是指足以影响股票价格变动的国内外重大活动以及政府的政策、措施、法令等重大事件，政府的社会经济发展计划、经济政策的变化、新颁布法令和管理条例等均会影响到股价的变动。（二）行业和区域因素主要是指行业发展前景和区域经济发展状况对股票价格的影响。内容包括行业生命周期、经济周期、行业地位、行业前景、行业动向及子行业方面的情况等对股票价格的影响。（三）公司因素公司因素相对来说更为重要，上市公司的经营状况的好坏对股票价格的影响较大，特别是上市公司的经营管理水平、财务状况、科技开发能力、行业内的竞争实力和竞争地位等从各个不同的方面影响着股票价格")
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao18)
        if readyToTestForum(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswerFaTie(browser,"我国货币政策的主要内容及其实施背景","2008年,在美国次贷危机演变为全球性金融危机的背景下,我国的宏观经济运行发生了转折性变化,经济由持续升温转为步人下行通道,物价涨幅由逐步升高转为持续下降。面对这种金融形势的变化,我国的宏观经济政策由“双防”转向“一保一控”,再转向“保增长”,货币政策则经历由“从紧”到“灵活审慎”、再到“适度宽松”的转变过程。从总体情况看,年初“从紧”的货币政策对抑制通货膨胀、防止经济过热发挥了重要作用,也为我国更好地应对国际金融危机的冲击奠定了基础。2008年7月以后国家实施逐步放松的货币政策对于保持经济较快增长和金融体系平稳运行产生了积极效果。目前国家经济下滑趋势有所抑制,但全球金融危机还有可能进一步恶化,世界经济金融形势也将更为严峻。货币政策需要进一步发挥调节作用,促进同内需求扩大和经济的平稳发展。")
        wait3AndCloseTab(browser)
    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(6)
