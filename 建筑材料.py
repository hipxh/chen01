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
def getAnswerElementEqualsZJ(elements, neirong, key,i, meidaotiyouduoshaogexuanxiang):
    may = None
    for ele in elements:
        _key = ele.text.replace(' ', '')
        _key = _key.replace(' ', '')
        if neirong == _key or "A." + neirong == _key or "B." + neirong == _key or "C." + neirong == _key or "D." + neirong == _key:
            may = ele
            if ele.find_element_by_xpath("./../../../../div[@class='qtext']").text[:3] in key.strip():
                return ele
    return may

def getAnswerElementEquals(elements, neirong, i, meidaotiyouduoshaogexuanxiang):
    elements = elements[i * meidaotiyouduoshaogexuanxiang:(i + 1) * meidaotiyouduoshaogexuanxiang]
    for ele in elements:#or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele
def getAnswerElementEqualsPanDuan(elements, neirong, i, meidaotiyouduoshaogexuanxiang):
    elements = elements[80+i * meidaotiyouduoshaogexuanxiang:80+(i + 1) * meidaotiyouduoshaogexuanxiang]
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
        i = i.split("．")[1]
        result[i.strip().split(reg)[0].strip()] = i.strip().split(reg)[1].strip()
    return result
def panduanAutoAnswerFix(answer, reg):
    result = []
    split = answer.split("\n")
    for i in split:
        i = i.split(reg)[0]
        result.append(i.strip()[-1])
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
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''1正确答案是：50%~60%
2.正确答案是：物理性质
3.正确答案是：木材
4.正确答案是：连通孔、封闭孔、半连通孔
5.正确答案是：V1≥V0≥V
6.正确答案是：空隙率
7.正确答案是：堆积密度
9.正确答案是：抗冻性
9.正确答案是：抗冻性
10．正确答案是：热容
11．正确答案是：韧性
12．正确答案是：不确定
13．正确答案是：岩浆岩、沉积岩、变质岩
14．正确答案是：长石
15．正确答案是：石灰、石膏、水玻璃
16．正确答案是：结晶硬化
17． 正确答案是：硫酸钙
18．正确答案是：凝结硬化快
19．正确答案是：碳酸钙
20．正确答案是：煅烧温度过高、煅烧时间过长'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        else:
            anEle = elements1[dxindex*4]
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01.．对”。
判断题02.．错”。
判断题03．对”。
判断题04  错”。
判断题05．对”。
判断题06  “对”。
判断题07． 错”。
判断题08．“对”。
判断题09．“错”。
判断题10．“错”。'''


    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "一提建筑。肯定离不了材料~而建筑科学。讲究的是如何设计的让人更舒适，方便，快捷，健康……如何要达到这一点呢？就是要发展建筑科学。就是要让建筑学更好的去造福人类。完成人类上述需求。研发新材料。怎么节能。怎么舒适，怎么健康。建筑离不了材料~没有材料。就不能完工。所以建筑科学也是一样。二者相辅相成。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "亲水物质： 酒精  甘油 淀粉 纤维素 蛋白质 ......疏水物质：食用油  汽油 柴油 润滑油 ......")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "（1）材料在外力作用下抵抗破坏的能力称为强度。（2）影响材料强度试验结果的因素：")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "天然大理石是地壳中原有的岩石经过地壳内高温高压作用形成的变质岩。属于中硬石材，主要由方解石、石灰石、蛇纹石和白云石组成。其主要成分以碳酸钙为主，约占50%以上。其它还有碳酸镁、氧化钙、氧化锰及二氧化硅等。由于大理石一般都含有杂质，而且碳酸钙在大气中受二氧化碳、碳化物、水气的作用，也容易风化和溶蚀，而使表面很快失去光泽。所以少数的，如汉白玉、艾叶青等质纯、杂质少的比较稳定耐久的品种可用于室外，其他品种不宜用于室外，一般只用于室内装饰面。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "石灰有生石灰（CaO）和熟石灰（Ca(OH)₂），生石灰吸潮或加水就成为熟石灰（因此生石灰可用于防潮干燥）。 熟石灰经调配成石灰浆、石灰膏、石灰砂浆等，用作涂装材料和砖瓦粘合剂。纯碱是用石灰石、食盐、氨等原料经过多步反应制得（索尔维法）。利用消石灰和纯碱反应制成烧碱（苛化法）。 另外，石灰在医药方面也有应用。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "质量吸水率:《建筑材料》形成性考核册答案 w. m, x10 m 29002500/2500 x0 \\frac{29002500}{2500}xI0 2500×1006169 2.密度:《建筑材料》形成性考核册答案 p= fn/J  50/18.5- 2m7 3.体积密度:《建筑材料》形成性考核册答案 R po Vo m/y0  -24-x21vI05-0\\times5-3 2119 4.孔隙率:《建筑材料》形成性考核册答案 PD-×100 2.7-1.71 2.7x1OB363%")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
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
    time.sleep(4)#保证富文本框加载完毕


    # 20单
    dxAnswer = '''01．正确答案是：水泥
02．正确答案是：硅酸盐水泥
03．正确答案是：早期快后期慢
04．正确答案是：0OC
05．正确答案是：以上都是
06．正确答案是：水泥在水化过程中放出的热量
07．正确答案是：氢氧化钙和水化铝酸钙
08．正确答案是：大体积混凝土工程
09．正确答案是：铝酸盐水泥
10．正确答案是：扩大其强度等级范围，以利于合理选用
11．正确答案是：线膨胀系数
12．正确答案是：品种和强度等级
13．正确答案是：气干状态
14．正确答案是：和易性
15．正确答案是：混凝土拌合物的稀稠程度及充满模板的能力
16．正确答案是：坍落度是保水性的指标
17．正确答案是：每立方米混凝土中砂的质量和砂石的总质量之比
18．正确答案是：水泥石与粗骨料的结合面先发生破坏
19．正确答案是：早强剂
20．正确答案是：水灰比、砂率、单位用水量'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．对”。
判断题02．错”。
判断题03．“错”。
判断题04．对”。
判断题05．错”。
判断题06．对”。
判断题07．错”。
判断题08．错”。
判断题09．错”。
判断题10．“对”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "细度是指水泥颗粒总体的粗细程度。水泥颗粒越细，与水发生反应的表面积越大，因而水化反应速度较快，而且较完全，早期强度也越高，但在空气中硬化收缩性较大，成本也较高。如水泥颗粒过粗则不利于水泥活性的发挥。一般认为水泥颗粒小于40μm（0.04mm）时，才具有较高的活性，大于100μm（0.1mm）活性就很小了。硅酸盐水泥和普通硅酸盐水泥细度用比表面积表示。比表面积是水泥单位质量的总表面积")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "水泥的初凝时间是指从水泥加水拌合起至水泥浆开始失去可塑性所需的时间的时间，这个时间对施工影响较大，为了保证有足够的时间在初凝之前完成混凝土的搅拌、运输和浇捣及砂浆的粉刷、砌筑等施工工序，初凝时间不宜过短，为此，国家标准规定硅酸盐水泥的初凝时间不早于45分。短于这个时间很容易导致混凝土还来不及施工就已经失去了塑性。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "砂、石有专门的试验方法，通过不同孔径的筛子进行筛分细算。不同孔径筛子上的筛余量有一定的范围。如果其各个筛的筛余量在标准规定的范围内，那么就称其为连续级配。连续级配对混凝土和易性（尤其是流动性），对强度也有帮助。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1、严格控制水灰比，保证足够的水泥用量；2、合理选择水泥品种；3、选用较好砂、石骨料，并尽量采用合理砂率；4、掺引气剂、减水剂等外加剂；5、掺入高效活性矿物掺料；6、施工中搅拌均匀、振捣密实、加强养护、增加混凝土密实度、提高混凝土质量。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "质量吸水率:《建筑材料》形成性考核册答案 w. m, x10 m 29002500/2500 x0 \\frac{29002500}{2500}xI0 2500×1006169 2.密度:《建筑材料》形成性考核册答案 p= fn/J  50/18.5- 2m7 3.体积密度:《建筑材料》形成性考核册答案 R po Vo m/y0  -24-x21vI05-0\\times5-3 2119 4.孔隙率:《建筑材料》形成性考核册答案 PD-×100 2.7-1.71 2.7x1OB363%")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "施工每立方混凝土各种材料用量：水泥C = 286Kg砂子S = 286×2.28（1 + 0.03）=672Kg石子G = 286×4.47（1 + 0.01）=1291Kg水W = 286×0.64 - 286×2.28×0.03 - 286×4.47×0.01 = 151Kg施工配合比：（286 / 286）：（672 / 286）：（1291 / 286）：（151 / 286）=1: 2.35:4.51: 0.53")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
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
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''01．正确答案是：砌筑砂浆
02．正确答案是：沉入度
03．正确答案是：3
04．正确答案是：中层砂浆
05．正确答案是：水泥砂浆
06．正确答案是：泛霜
07．正确答案是：蒸压灰砂砖
08．正确答案是：陶瓷锦砖
09．正确答案是：玻璃在冲击作用下易破碎，是典型的塑性材料
10．正确答案是：平板玻璃
11．正确答案是：黏土
12．正确答案是：颈缩阶段
13．正确答案是：伸长率
14．正确答案是：沸腾钢
15．正确答案是：冷弯性能
16 . 正确答案是：疲劳破坏
17．正确答案是：若含硅量超过1%时，会增大钢材的可焊性
18．正确答案是：强度提高，伸长率降低
19.  正确答案是：强度提高，塑性和冲击韧性下降
20．正确答案是：增大'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．对”。
判断题02．“对”。
判断题03．错”。
判断题04．“对”。
判断题05．错”。
判断题06．错”。
判断题07．对”。
判断题08．错”。
判断题09．对”。
判断题10．错”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "根据建筑力学分类共分为压力、拉力、扭力、剪力和弯曲五种。再针对各种建筑材料来判断，其中砂浆所承受的力绝大多数是压力，砂浆承受压力的大小也就成为了评判砂浆级别的标准。抗压强度技术指标直接体现了砂浆的受力特点")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "地下水泥砂浆，地上除有水房间外用混合砂浆，有水房间用水泥砂浆")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "最主要是因为釉面砖吸水率较高(国家规定其吸水率小于21%)，容易吸入大量水分，严重的甚至在贴完瓷砖后不久，能够将水泥的脏水从背面吸进来，进入釉面。陶体吸水膨胀后，吸湿膨胀小的表层釉面处于张压力状态下，长期冻融，会出现剥落掉皮现象，还有就是很可能受到温度的影响而脱落，所以釉面砖不能用于室外。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "钢材的屈服点（屈服强度）与抗拉强度的比值，称为屈强比。屈强比越大，结构零件的可靠性越大，一般碳素钢屈强比为0.6-0.65，低合金结构钢为0.65-0.75合金结构钢为0.84-0.86。 机器零件的屈强比高，节约材料，减轻重量。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1、钢材耐腐蚀性差。 2、钢材耐热但不耐火。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "【解】1.计算砂浆的配制强度：查表3－40,取值σ＝1.88MPa. ƒm,o＝ƒ2+0.645σ ＝7.5+0.645×1.88＝8.7MPa 2.计算单位水泥用量： Qc=217Kg(公式打不上去,此题实测强度fce=36MPa) 3.计算单位石灰膏用量： QD ＝QA－Qc ＝350－217＝133kg 4.计算单位砂的用量: Qs＝1× ×（1+w′） ＝1×1450×（1+2％）＝1479kg 5.得到砂浆初步配合比： 采用质量比表示为：水泥∶石灰膏∶砂 Qc：QD：Qs＝217∶133∶1479＝1∶0.61∶6.11")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
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
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''01．正确答案是：聚酯树脂
02．正确答案是：合成树脂
03．正确答案是：63~188kJ/m3
04．正确答案是：塑料和玻璃纤维
05．正确答案是：溶剂
06．正确答案是：结构胶粘剂、非结构胶粘剂、次结构胶粘剂
07．正确答案是：石油沥青
08．正确答案是：油分
09．正确答案是：石油沥青在外力作用下产生变形而不破坏，除去外力后仍保持变形后的形状不变的性质
10．正确答案是：沥青牌号越高，黏性越小，塑性越好
11．正确答案是：建筑石油沥青的软化点过高夏季易流淌，过低冬季易硬脆甚至开裂
12．正确答案是：石油产品系统的轻质油
13．正确答案是：虽然橡胶的品种不同，掺入的方法也有所不同，但各种橡胶沥青的性能几乎一样
14．正确答案是：老化
15．正确答案是：丁苯橡胶
16．正确答案是：温度稳定性
17．正确答案是：纤维饱和点
18．正确答案是：纤维板
19．正确答案是：木材
20．正确答案是：方孔筛'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．“对”。
判断题02．“错”。
判断题03．“对”。
判断题04．“错”。
判断题05“  对”。
判断题06．“对”。
判断题07．对”。
判断题08．对”。
判断题09．对”。
判断题10．“错”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1. 确定要粘接的材料，玻璃粘玻璃， 金属粘玻璃，塑料粘塑料等等2. 确定粘接工艺，是加热固化，UV灯照，还是湿气固化。等等3.确定所需胶粘剂的作用，是用于灌封，密封还是粘接，对粘接强度要求高不高。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "塑料的优点加工特性好2、质轻3、比强度大4、导热系数小5、化学稳定性好6、电绝缘性好7、性能设计性好8、富有装饰性9、有利于建筑工业化塑料的缺点：1、易老化2、易燃3、耐热性差4、刚度小")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "主要分为四种：饱和分、芳香分、胶质和沥青质。饱和分和芳香分是液体的，起到溶剂作用，胶质是胶体状的，沥青质是固体，相当于溶质，起到一定的支架作用")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "这要看矿物填充物的成分了。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "木材的腐朽主要是木材里面有木腐菌、白蚁等生物，他们以木材内部的木质素为食，所以木材会逐渐腐朽，对于木材防腐的措施， 有很多，根据木材的使用环境不同而不同，最常见的是对木材进行防腐处理，处理的方法有喷涂防腐药剂，喷涂油漆，而防腐药剂有很多种，有油性的，也有水溶性的，均能有效防止木材的腐朽，目前室外使用的防腐木主要是通过真空加压防腐处理的方法，通过高压，把水溶性防腐药剂打入木材内部，是木腐菌不能在木材内部生存。之外，也有一种炭化木，他的防腐处理方法跟之前的不同，他是通过对木材进行高温热处理，破坏木材内部物质结构，使木腐菌等生存依赖的物质通过高温脱水，变成以外一种物质，不能够为木腐菌食用，这样达到木材防腐的效果。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1 湿润坍落度筒及其他用具，并把筒房子不吸水的刚性水平底上，然后用脚踩住两个踏板，使坍落度筒在装料时保持位置固定。2 把取得的混凝土试样用小铲分三层均匀的装入桶内，捣实后每层高度为筒高1/3左右，每层用捣棒沿螺旋方向在截面上由外向中心均匀插捣25次，插捣筒边混凝土时，捣棒可以稍稍倾斜，插捣底层时，捣棒应贯穿整个深度。插捣第二层和顶层时，捣棒应插透本层至下一层表面。装顶层混凝土时应高出筒口。插捣过程中，如混凝土坍落到低于筒口，则应随时添加。顶层插捣完后，刮出躲雨的混凝土，并用抹刀抹平。3 清除筒边地板上的混凝土后，垂直平稳的提起坍落度筒。坍落度筒的提高过程应在5~10秒内完成，从开始装料到提起坍落度筒的过程中，应不间断的进行，并应在150S内完成。4 提起筒后，两侧筒高与坍落后混凝土试体最高点之间的高度差，即为混凝土拌合物的坍落度值。 ")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()








def writeAnswer_2(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．材料化学组成的不同是造成其性能各异的主要原因，研究材料的化学组成通常需研究答案：材料的元素组成和矿物组成
2．矿物组成和元素组成是造成材料性能各异主要原因，其中材料的矿物组成主要是指答案：元素组成相同，但分子团组成形式各异的现象
3．材料的微观结构主要是指答案：材料在原子、离子、分子层次上的组成形式　
4．建筑钢材的微观结构形式是答案：晶体结构　
5．下列建筑材料的构造属于致密状构造的是答案：玻璃　
6．下列关于材料构造说法有误的一项是答案：胶合板、复合木地板、纸面石膏板、夹层玻璃都是纤维状构造　
7．材料实体内部和实体间常常部分被空气所占据，一般称材料实体内部被空气所占据的空间为答案：孔隙
8．用来说明材料孔隙状况的三个指标分别是答案：孔隙率、孔隙连通性和孔隙直径　
9．材料在绝对密实状态下，单位体积的质量称为答案：密度
10．材料的密室度指的是答案：材料的体积内，被固体物质充满的程度
11．亲水材料的润湿角一般小于答案：900
12．材料的吸水性是指答案：材料在长期饱和水的作用下，不破坏、强度也不显著降低的性质
13．材料传导热量的能力称为答案：导热性
14．下列关于耐燃性和耐火性说法有误的一项是答案：耐火的材料不一定耐燃，耐燃的一般都耐火
15．材料在外力作用下抵抗破坏的能力称为 答案：强度
16．下列关于材料实验及材料强度实验说法有误的一项是答案：一般情况，试件温度越高，所测强度值越高
17．材料在外力作用下发生变形，当外力解除后，能完全恢复到变形前形状的性质称为材料的 答案：弹性
18．下列关于材料弹性和塑性说法有误的一项是答案：弹性模量E值愈大，说明材料在相同外力作用下的变形愈大
19．在冲击、震动荷载作用下，材料可吸收较大的能量产生一定的变形而不破坏的性质称为 答案：韧性或冲击韧性
20．下列关于韧性和脆性说法有误的一项是 答案：脆性材料的力学性能特点是抗压强度远小于于抗拉强度，破坏时的极限应变值极大
21．材料表面耐较硬物体刻划或压入而产生塑性变形的能力称为 答案：硬度
22．下列关于材料耐磨性说法有误的一项是答案：磨损率等于试件在标准试验条件下磨损前后的质量差与试件受磨表面积之积
23．材料使用过程中，在内、外部因素的作用下，经久不破坏、不变质，保持原有性能的性质称为答案：耐久性
24．下列关于材料耐久性能说法有误的一项是答案：钢材的耐久性，主要取决于其大气稳定性和温度敏感性
25．材料密度试验的目的是答案：测定材料的密度，计算材料的密实度与孔隙率
26．材料密度试验不需要的仪器是答案：游标卡尺
27．材料表观密度试验以两次试验结果的算术平均值之差不应大于答案：0.02g/cm3
28．下列关于材料表观密度试验说法有误的一项是答案：容量瓶法用来测定石子的表观密度，广口瓶法用来测定砂的表观密度
29．几何形状规则的材料在测体积密度时，第一步应答案：用游标卡尺量出试样尺寸，计算出试样的体积
30．下列关于材料体积密度试验说法有误的一项是答案：试验准备时当不规则试样溶于水或其吸水率小于0.5%，则须对试样进行蜡封处理
31．下列关于测定砂、石子堆积密度试验说法有误的一项是答案：堆积密度等于松散堆积密度和紧密堆积密度之和
32．测定砂的堆积密度时，称取试样和容量筒总质量m2，应精确至答案：1g
33．孔隙率P计算公式式中ρ0为答案：材料的表观密度
34．空隙率P′计算公式式中ρ0′为答案：材料的堆积密度'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        _value = value.replace(' ', '')
        value = _value.replace(' ', '')
        anEle = getAnswerElementEqualsZJ(elements1, value, key.replace(' ', ''), dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../input[last()]").click()
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_3(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''01．正确答案是：砌筑砂浆
02．正确答案是：沉入度
03．正确答案是：3
04．正确答案是：中层砂浆
05．正确答案是：水泥砂浆
06．正确答案是：泛霜
07．正确答案是：蒸压灰砂砖
08．正确答案是：陶瓷锦砖
09．正确答案是：玻璃在冲击作用下易破碎，是典型的塑性材料
10．正确答案是：平板玻璃
11．正确答案是：黏土
12．正确答案是：颈缩阶段
13．正确答案是：伸长率
14．正确答案是：沸腾钢
15．正确答案是：冷弯性能
16 . 正确答案是：疲劳破坏
17．正确答案是：若含硅量超过1%时，会增大钢材的可焊性
18．正确答案是：强度提高，伸长率降低
19.  正确答案是：强度提高，塑性和冲击韧性下降
20．正确答案是：增大'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．对”。
判断题02．“对”。
判断题03．错”。
判断题04．“对”。
判断题05．错”。
判断题06．错”。
判断题07．对”。
判断题08．错”。
判断题09．对”。
判断题10．错”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "根据建筑力学分类共分为压力、拉力、扭力、剪力和弯曲五种。再针对各种建筑材料来判断，其中砂浆所承受的力绝大多数是压力，砂浆承受压力的大小也就成为了评判砂浆级别的标准。抗压强度技术指标直接体现了砂浆的受力特点")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "地下水泥砂浆，地上除有水房间外用混合砂浆，有水房间用水泥砂浆")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "最主要是因为釉面砖吸水率较高(国家规定其吸水率小于21%)，容易吸入大量水分，严重的甚至在贴完瓷砖后不久，能够将水泥的脏水从背面吸进来，进入釉面。陶体吸水膨胀后，吸湿膨胀小的表层釉面处于张压力状态下，长期冻融，会出现剥落掉皮现象，还有就是很可能受到温度的影响而脱落，所以釉面砖不能用于室外。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "钢材的屈服点（屈服强度）与抗拉强度的比值，称为屈强比。屈强比越大，结构零件的可靠性越大，一般碳素钢屈强比为0.6-0.65，低合金结构钢为0.65-0.75合金结构钢为0.84-0.86。 机器零件的屈强比高，节约材料，减轻重量。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1、钢材耐腐蚀性差。 2、钢材耐热但不耐火。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "【解】1.计算砂浆的配制强度：查表3－40,取值σ＝1.88MPa. ƒm,o＝ƒ2+0.645σ ＝7.5+0.645×1.88＝8.7MPa 2.计算单位水泥用量： Qc=217Kg(公式打不上去,此题实测强度fce=36MPa) 3.计算单位石灰膏用量： QD ＝QA－Qc ＝350－217＝133kg 4.计算单位砂的用量: Qs＝1× ×（1+w′） ＝1×1450×（1+2％）＝1479kg 5.得到砂浆初步配合比： 采用质量比表示为：水泥∶石灰膏∶砂 Qc：QD：Qs＝217∶133∶1479＝1∶0.61∶6.11")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_4(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''01．正确答案是：聚酯树脂
02．正确答案是：合成树脂
03．正确答案是：63~188kJ/m3
04．正确答案是：塑料和玻璃纤维
05．正确答案是：溶剂
06．正确答案是：结构胶粘剂、非结构胶粘剂、次结构胶粘剂
07．正确答案是：石油沥青
08．正确答案是：油分
09．正确答案是：石油沥青在外力作用下产生变形而不破坏，除去外力后仍保持变形后的形状不变的性质
10．正确答案是：沥青牌号越高，黏性越小，塑性越好
11．正确答案是：建筑石油沥青的软化点过高夏季易流淌，过低冬季易硬脆甚至开裂
12．正确答案是：石油产品系统的轻质油
13．正确答案是：虽然橡胶的品种不同，掺入的方法也有所不同，但各种橡胶沥青的性能几乎一样
14．正确答案是：老化
15．正确答案是：丁苯橡胶
16．正确答案是：温度稳定性
17．正确答案是：纤维饱和点
18．正确答案是：纤维板
19．正确答案是：木材
20．正确答案是：方孔筛'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．“对”。
判断题02．“错”。
判断题03．“对”。
判断题04．“错”。
判断题05“  对”。
判断题06．“对”。
判断题07．对”。
判断题08．对”。
判断题09．对”。
判断题10．“错”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1. 确定要粘接的材料，玻璃粘玻璃， 金属粘玻璃，塑料粘塑料等等2. 确定粘接工艺，是加热固化，UV灯照，还是湿气固化。等等3.确定所需胶粘剂的作用，是用于灌封，密封还是粘接，对粘接强度要求高不高。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "塑料的优点加工特性好2、质轻3、比强度大4、导热系数小5、化学稳定性好6、电绝缘性好7、性能设计性好8、富有装饰性9、有利于建筑工业化塑料的缺点：1、易老化2、易燃3、耐热性差4、刚度小")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "主要分为四种：饱和分、芳香分、胶质和沥青质。饱和分和芳香分是液体的，起到溶剂作用，胶质是胶体状的，沥青质是固体，相当于溶质，起到一定的支架作用")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "这要看矿物填充物的成分了。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "木材的腐朽主要是木材里面有木腐菌、白蚁等生物，他们以木材内部的木质素为食，所以木材会逐渐腐朽，对于木材防腐的措施， 有很多，根据木材的使用环境不同而不同，最常见的是对木材进行防腐处理，处理的方法有喷涂防腐药剂，喷涂油漆，而防腐药剂有很多种，有油性的，也有水溶性的，均能有效防止木材的腐朽，目前室外使用的防腐木主要是通过真空加压防腐处理的方法，通过高压，把水溶性防腐药剂打入木材内部，是木腐菌不能在木材内部生存。之外，也有一种炭化木，他的防腐处理方法跟之前的不同，他是通过对木材进行高温热处理，破坏木材内部物质结构，使木腐菌等生存依赖的物质通过高温脱水，变成以外一种物质，不能够为木腐菌食用，这样达到木材防腐的效果。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1 湿润坍落度筒及其他用具，并把筒房子不吸水的刚性水平底上，然后用脚踩住两个踏板，使坍落度筒在装料时保持位置固定。2 把取得的混凝土试样用小铲分三层均匀的装入桶内，捣实后每层高度为筒高1/3左右，每层用捣棒沿螺旋方向在截面上由外向中心均匀插捣25次，插捣筒边混凝土时，捣棒可以稍稍倾斜，插捣底层时，捣棒应贯穿整个深度。插捣第二层和顶层时，捣棒应插透本层至下一层表面。装顶层混凝土时应高出筒口。插捣过程中，如混凝土坍落到低于筒口，则应随时添加。顶层插捣完后，刮出躲雨的混凝土，并用抹刀抹平。3 清除筒边地板上的混凝土后，垂直平稳的提起坍落度筒。坍落度筒的提高过程应在5~10秒内完成，从开始装料到提起坍落度筒的过程中，应不间断的进行，并应在150S内完成。4 提起筒后，两侧筒高与坍落后混凝土试体最高点之间的高度差，即为混凝土拌合物的坍落度值。 ")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_5(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)#保证富文本框加载完毕


    # 20单
    dxAnswer = '''01．正确答案是：水泥
02．正确答案是：硅酸盐水泥
03．正确答案是：早期快后期慢
04．正确答案是：0OC
05．正确答案是：以上都是
06．正确答案是：水泥在水化过程中放出的热量
07．正确答案是：氢氧化钙和水化铝酸钙
08．正确答案是：大体积混凝土工程
09．正确答案是：铝酸盐水泥
10．正确答案是：扩大其强度等级范围，以利于合理选用
11．正确答案是：线膨胀系数
12．正确答案是：品种和强度等级
13．正确答案是：气干状态
14．正确答案是：和易性
15．正确答案是：混凝土拌合物的稀稠程度及充满模板的能力
16．正确答案是：坍落度是保水性的指标
17．正确答案是：每立方米混凝土中砂的质量和砂石的总质量之比
18．正确答案是：水泥石与粗骨料的结合面先发生破坏
19．正确答案是：早强剂
20．正确答案是：水灰比、砂率、单位用水量'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．对”。
判断题02．错”。
判断题03．“错”。
判断题04．对”。
判断题05．错”。
判断题06．对”。
判断题07．错”。
判断题08．错”。
判断题09．错”。
判断题10．“对”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "细度是指水泥颗粒总体的粗细程度。水泥颗粒越细，与水发生反应的表面积越大，因而水化反应速度较快，而且较完全，早期强度也越高，但在空气中硬化收缩性较大，成本也较高。如水泥颗粒过粗则不利于水泥活性的发挥。一般认为水泥颗粒小于40μm（0.04mm）时，才具有较高的活性，大于100μm（0.1mm）活性就很小了。硅酸盐水泥和普通硅酸盐水泥细度用比表面积表示。比表面积是水泥单位质量的总表面积")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "水泥的初凝时间是指从水泥加水拌合起至水泥浆开始失去可塑性所需的时间的时间，这个时间对施工影响较大，为了保证有足够的时间在初凝之前完成混凝土的搅拌、运输和浇捣及砂浆的粉刷、砌筑等施工工序，初凝时间不宜过短，为此，国家标准规定硅酸盐水泥的初凝时间不早于45分。短于这个时间很容易导致混凝土还来不及施工就已经失去了塑性。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "砂、石有专门的试验方法，通过不同孔径的筛子进行筛分细算。不同孔径筛子上的筛余量有一定的范围。如果其各个筛的筛余量在标准规定的范围内，那么就称其为连续级配。连续级配对混凝土和易性（尤其是流动性），对强度也有帮助。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1、严格控制水灰比，保证足够的水泥用量；2、合理选择水泥品种；3、选用较好砂、石骨料，并尽量采用合理砂率；4、掺引气剂、减水剂等外加剂；5、掺入高效活性矿物掺料；6、施工中搅拌均匀、振捣密实、加强养护、增加混凝土密实度、提高混凝土质量。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "质量吸水率:《建筑材料》形成性考核册答案 w. m, x10 m 29002500/2500 x0 \\frac{29002500}{2500}xI0 2500×1006169 2.密度:《建筑材料》形成性考核册答案 p= fn/J  50/18.5- 2m7 3.体积密度:《建筑材料》形成性考核册答案 R po Vo m/y0  -24-x21vI05-0\\times5-3 2119 4.孔隙率:《建筑材料》形成性考核册答案 PD-×100 2.7-1.71 2.7x1OB363%")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "施工每立方混凝土各种材料用量：水泥C = 286Kg砂子S = 286×2.28（1 + 0.03）=672Kg石子G = 286×4.47（1 + 0.01）=1291Kg水W = 286×0.64 - 286×2.28×0.03 - 286×4.47×0.01 = 151Kg施工配合比：（286 / 286）：（672 / 286）：（1291 / 286）：（151 / 286）=1: 2.35:4.51: 0.53")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_6(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''1正确答案是：50%~60%
2.正确答案是：物理性质
3.正确答案是：木材
4.正确答案是：连通孔、封闭孔、半连通孔
5.正确答案是：V1≥V0≥V
6.正确答案是：空隙率
7.正确答案是：堆积密度
9.正确答案是：抗冻性
9.正确答案是：抗冻性
10．正确答案是：热容
11．正确答案是：韧性
12．正确答案是：不确定
13．正确答案是：岩浆岩、沉积岩、变质岩
14．正确答案是：长石
15．正确答案是：石灰、石膏、水玻璃
16．正确答案是：结晶硬化
17． 正确答案是：硫酸钙
18．正确答案是：凝结硬化快
19．正确答案是：碳酸钙
20．正确答案是：煅烧温度过高、煅烧时间过长'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        else:
            anEle = elements1[dxindex*4]
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01.．对”。
判断题02.．错”。
判断题03．对”。
判断题04  错”。
判断题05．对”。
判断题06  “对”。
判断题07． 错”。
判断题08．“对”。
判断题09．“错”。
判断题10．“错”。'''


    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "一提建筑。肯定离不了材料~而建筑科学。讲究的是如何设计的让人更舒适，方便，快捷，健康……如何要达到这一点呢？就是要发展建筑科学。就是要让建筑学更好的去造福人类。完成人类上述需求。研发新材料。怎么节能。怎么舒适，怎么健康。建筑离不了材料~没有材料。就不能完工。所以建筑科学也是一样。二者相辅相成。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "亲水物质： 酒精  甘油 淀粉 纤维素 蛋白质 ......疏水物质：食用油  汽油 柴油 润滑油 ......")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "（1）材料在外力作用下抵抗破坏的能力称为强度。（2）影响材料强度试验结果的因素：")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "天然大理石是地壳中原有的岩石经过地壳内高温高压作用形成的变质岩。属于中硬石材，主要由方解石、石灰石、蛇纹石和白云石组成。其主要成分以碳酸钙为主，约占50%以上。其它还有碳酸镁、氧化钙、氧化锰及二氧化硅等。由于大理石一般都含有杂质，而且碳酸钙在大气中受二氧化碳、碳化物、水气的作用，也容易风化和溶蚀，而使表面很快失去光泽。所以少数的，如汉白玉、艾叶青等质纯、杂质少的比较稳定耐久的品种可用于室外，其他品种不宜用于室外，一般只用于室内装饰面。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "石灰有生石灰（CaO）和熟石灰（Ca(OH)₂），生石灰吸潮或加水就成为熟石灰（因此生石灰可用于防潮干燥）。 熟石灰经调配成石灰浆、石灰膏、石灰砂浆等，用作涂装材料和砖瓦粘合剂。纯碱是用石灰石、食盐、氨等原料经过多步反应制得（索尔维法）。利用消石灰和纯碱反应制成烧碱（苛化法）。 另外，石灰在医药方面也有应用。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "质量吸水率:《建筑材料》形成性考核册答案 w. m, x10 m 29002500/2500 x0 \\frac{29002500}{2500}xI0 2500×1006169 2.密度:《建筑材料》形成性考核册答案 p= fn/J  50/18.5- 2m7 3.体积密度:《建筑材料》形成性考核册答案 R po Vo m/y0  -24-x21vI05-0\\times5-3 2119 4.孔隙率:《建筑材料》形成性考核册答案 PD-×100 2.7-1.71 2.7x1OB363%")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_7(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)#保证富文本框加载完毕


    # 20单
    dxAnswer = '''01．正确答案是：水泥
02．正确答案是：硅酸盐水泥
03．正确答案是：早期快后期慢
04．正确答案是：0OC
05．正确答案是：以上都是
06．正确答案是：水泥在水化过程中放出的热量
07．正确答案是：氢氧化钙和水化铝酸钙
08．正确答案是：大体积混凝土工程
09．正确答案是：铝酸盐水泥
10．正确答案是：扩大其强度等级范围，以利于合理选用
11．正确答案是：线膨胀系数
12．正确答案是：品种和强度等级
13．正确答案是：气干状态
14．正确答案是：和易性
15．正确答案是：混凝土拌合物的稀稠程度及充满模板的能力
16．正确答案是：坍落度是保水性的指标
17．正确答案是：每立方米混凝土中砂的质量和砂石的总质量之比
18．正确答案是：水泥石与粗骨料的结合面先发生破坏
19．正确答案是：早强剂
20．正确答案是：水灰比、砂率、单位用水量'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．对”。
判断题02．错”。
判断题03．“错”。
判断题04．对”。
判断题05．错”。
判断题06．对”。
判断题07．错”。
判断题08．错”。
判断题09．错”。
判断题10．“对”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "细度是指水泥颗粒总体的粗细程度。水泥颗粒越细，与水发生反应的表面积越大，因而水化反应速度较快，而且较完全，早期强度也越高，但在空气中硬化收缩性较大，成本也较高。如水泥颗粒过粗则不利于水泥活性的发挥。一般认为水泥颗粒小于40μm（0.04mm）时，才具有较高的活性，大于100μm（0.1mm）活性就很小了。硅酸盐水泥和普通硅酸盐水泥细度用比表面积表示。比表面积是水泥单位质量的总表面积")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "水泥的初凝时间是指从水泥加水拌合起至水泥浆开始失去可塑性所需的时间的时间，这个时间对施工影响较大，为了保证有足够的时间在初凝之前完成混凝土的搅拌、运输和浇捣及砂浆的粉刷、砌筑等施工工序，初凝时间不宜过短，为此，国家标准规定硅酸盐水泥的初凝时间不早于45分。短于这个时间很容易导致混凝土还来不及施工就已经失去了塑性。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "砂、石有专门的试验方法，通过不同孔径的筛子进行筛分细算。不同孔径筛子上的筛余量有一定的范围。如果其各个筛的筛余量在标准规定的范围内，那么就称其为连续级配。连续级配对混凝土和易性（尤其是流动性），对强度也有帮助。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1、严格控制水灰比，保证足够的水泥用量；2、合理选择水泥品种；3、选用较好砂、石骨料，并尽量采用合理砂率；4、掺引气剂、减水剂等外加剂；5、掺入高效活性矿物掺料；6、施工中搅拌均匀、振捣密实、加强养护、增加混凝土密实度、提高混凝土质量。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "质量吸水率:《建筑材料》形成性考核册答案 w. m, x10 m 29002500/2500 x0 \\frac{29002500}{2500}xI0 2500×1006169 2.密度:《建筑材料》形成性考核册答案 p= fn/J  50/18.5- 2m7 3.体积密度:《建筑材料》形成性考核册答案 R po Vo m/y0  -24-x21vI05-0\\times5-3 2119 4.孔隙率:《建筑材料》形成性考核册答案 PD-×100 2.7-1.71 2.7x1OB363%")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "施工每立方混凝土各种材料用量：水泥C = 286Kg砂子S = 286×2.28（1 + 0.03）=672Kg石子G = 286×4.47（1 + 0.01）=1291Kg水W = 286×0.64 - 286×2.28×0.03 - 286×4.47×0.01 = 151Kg施工配合比：（286 / 286）：（672 / 286）：（1291 / 286）：（151 / 286）=1: 2.35:4.51: 0.53")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_8(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''01．正确答案是：砌筑砂浆
02．正确答案是：沉入度
03．正确答案是：3
04．正确答案是：中层砂浆
05．正确答案是：水泥砂浆
06．正确答案是：泛霜
07．正确答案是：蒸压灰砂砖
08．正确答案是：陶瓷锦砖
09．正确答案是：玻璃在冲击作用下易破碎，是典型的塑性材料
10．正确答案是：平板玻璃
11．正确答案是：黏土
12．正确答案是：颈缩阶段
13．正确答案是：伸长率
14．正确答案是：沸腾钢
15．正确答案是：冷弯性能
16 . 正确答案是：疲劳破坏
17．正确答案是：若含硅量超过1%时，会增大钢材的可焊性
18．正确答案是：强度提高，伸长率降低
19.  正确答案是：强度提高，塑性和冲击韧性下降
20．正确答案是：增大'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．对”。
判断题02．“对”。
判断题03．错”。
判断题04．“对”。
判断题05．错”。
判断题06．错”。
判断题07．对”。
判断题08．错”。
判断题09．对”。
判断题10．错”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "根据建筑力学分类共分为压力、拉力、扭力、剪力和弯曲五种。再针对各种建筑材料来判断，其中砂浆所承受的力绝大多数是压力，砂浆承受压力的大小也就成为了评判砂浆级别的标准。抗压强度技术指标直接体现了砂浆的受力特点")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "地下水泥砂浆，地上除有水房间外用混合砂浆，有水房间用水泥砂浆")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "最主要是因为釉面砖吸水率较高(国家规定其吸水率小于21%)，容易吸入大量水分，严重的甚至在贴完瓷砖后不久，能够将水泥的脏水从背面吸进来，进入釉面。陶体吸水膨胀后，吸湿膨胀小的表层釉面处于张压力状态下，长期冻融，会出现剥落掉皮现象，还有就是很可能受到温度的影响而脱落，所以釉面砖不能用于室外。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "钢材的屈服点（屈服强度）与抗拉强度的比值，称为屈强比。屈强比越大，结构零件的可靠性越大，一般碳素钢屈强比为0.6-0.65，低合金结构钢为0.65-0.75合金结构钢为0.84-0.86。 机器零件的屈强比高，节约材料，减轻重量。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1、钢材耐腐蚀性差。 2、钢材耐热但不耐火。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "【解】1.计算砂浆的配制强度：查表3－40,取值σ＝1.88MPa. ƒm,o＝ƒ2+0.645σ ＝7.5+0.645×1.88＝8.7MPa 2.计算单位水泥用量： Qc=217Kg(公式打不上去,此题实测强度fce=36MPa) 3.计算单位石灰膏用量： QD ＝QA－Qc ＝350－217＝133kg 4.计算单位砂的用量: Qs＝1× ×（1+w′） ＝1×1450×（1+2％）＝1479kg 5.得到砂浆初步配合比： 采用质量比表示为：水泥∶石灰膏∶砂 Qc：QD：Qs＝217∶133∶1479＝1∶0.61∶6.11")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_9(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''01．正确答案是：聚酯树脂
02．正确答案是：合成树脂
03．正确答案是：63~188kJ/m3
04．正确答案是：塑料和玻璃纤维
05．正确答案是：溶剂
06．正确答案是：结构胶粘剂、非结构胶粘剂、次结构胶粘剂
07．正确答案是：石油沥青
08．正确答案是：油分
09．正确答案是：石油沥青在外力作用下产生变形而不破坏，除去外力后仍保持变形后的形状不变的性质
10．正确答案是：沥青牌号越高，黏性越小，塑性越好
11．正确答案是：建筑石油沥青的软化点过高夏季易流淌，过低冬季易硬脆甚至开裂
12．正确答案是：石油产品系统的轻质油
13．正确答案是：虽然橡胶的品种不同，掺入的方法也有所不同，但各种橡胶沥青的性能几乎一样
14．正确答案是：老化
15．正确答案是：丁苯橡胶
16．正确答案是：温度稳定性
17．正确答案是：纤维饱和点
18．正确答案是：纤维板
19．正确答案是：木材
20．正确答案是：方孔筛'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．“对”。
判断题02．“错”。
判断题03．“对”。
判断题04．“错”。
判断题05“  对”。
判断题06．“对”。
判断题07．对”。
判断题08．对”。
判断题09．对”。
判断题10．“错”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1. 确定要粘接的材料，玻璃粘玻璃， 金属粘玻璃，塑料粘塑料等等2. 确定粘接工艺，是加热固化，UV灯照，还是湿气固化。等等3.确定所需胶粘剂的作用，是用于灌封，密封还是粘接，对粘接强度要求高不高。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "塑料的优点加工特性好2、质轻3、比强度大4、导热系数小5、化学稳定性好6、电绝缘性好7、性能设计性好8、富有装饰性9、有利于建筑工业化塑料的缺点：1、易老化2、易燃3、耐热性差4、刚度小")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "主要分为四种：饱和分、芳香分、胶质和沥青质。饱和分和芳香分是液体的，起到溶剂作用，胶质是胶体状的，沥青质是固体，相当于溶质，起到一定的支架作用")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "这要看矿物填充物的成分了。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "木材的腐朽主要是木材里面有木腐菌、白蚁等生物，他们以木材内部的木质素为食，所以木材会逐渐腐朽，对于木材防腐的措施， 有很多，根据木材的使用环境不同而不同，最常见的是对木材进行防腐处理，处理的方法有喷涂防腐药剂，喷涂油漆，而防腐药剂有很多种，有油性的，也有水溶性的，均能有效防止木材的腐朽，目前室外使用的防腐木主要是通过真空加压防腐处理的方法，通过高压，把水溶性防腐药剂打入木材内部，是木腐菌不能在木材内部生存。之外，也有一种炭化木，他的防腐处理方法跟之前的不同，他是通过对木材进行高温热处理，破坏木材内部物质结构，使木腐菌等生存依赖的物质通过高温脱水，变成以外一种物质，不能够为木腐菌食用，这样达到木材防腐的效果。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1 湿润坍落度筒及其他用具，并把筒房子不吸水的刚性水平底上，然后用脚踩住两个踏板，使坍落度筒在装料时保持位置固定。2 把取得的混凝土试样用小铲分三层均匀的装入桶内，捣实后每层高度为筒高1/3左右，每层用捣棒沿螺旋方向在截面上由外向中心均匀插捣25次，插捣筒边混凝土时，捣棒可以稍稍倾斜，插捣底层时，捣棒应贯穿整个深度。插捣第二层和顶层时，捣棒应插透本层至下一层表面。装顶层混凝土时应高出筒口。插捣过程中，如混凝土坍落到低于筒口，则应随时添加。顶层插捣完后，刮出躲雨的混凝土，并用抹刀抹平。3 清除筒边地板上的混凝土后，垂直平稳的提起坍落度筒。坍落度筒的提高过程应在5~10秒内完成，从开始装料到提起坍落度筒的过程中，应不间断的进行，并应在150S内完成。4 提起筒后，两侧筒高与坍落后混凝土试体最高点之间的高度差，即为混凝土拌合物的坍落度值。 ")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_10(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)  # 保证富文本框加载完毕

    # 20单
    dxAnswer = '''1正确答案是：50%~60%
2.正确答案是：物理性质
3.正确答案是：木材
4.正确答案是：连通孔、封闭孔、半连通孔
5.正确答案是：V1≥V0≥V
6.正确答案是：空隙率
7.正确答案是：堆积密度
9.正确答案是：抗冻性
9.正确答案是：抗冻性
10．正确答案是：热容
11．正确答案是：韧性
12．正确答案是：不确定
13．正确答案是：岩浆岩、沉积岩、变质岩
14．正确答案是：长石
15．正确答案是：石灰、石膏、水玻璃
16．正确答案是：结晶硬化
17． 正确答案是：硫酸钙
18．正确答案是：凝结硬化快
19．正确答案是：碳酸钙
20．正确答案是：煅烧温度过高、煅烧时间过长'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        else:
            anEle = elements1[dxindex*4]
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01.．对”。
判断题02.．错”。
判断题03．对”。
判断题04  错”。
判断题05．对”。
判断题06  “对”。
判断题07． 错”。
判断题08．“对”。
判断题09．“错”。
判断题10．“错”。'''


    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "一提建筑。肯定离不了材料~而建筑科学。讲究的是如何设计的让人更舒适，方便，快捷，健康……如何要达到这一点呢？就是要发展建筑科学。就是要让建筑学更好的去造福人类。完成人类上述需求。研发新材料。怎么节能。怎么舒适，怎么健康。建筑离不了材料~没有材料。就不能完工。所以建筑科学也是一样。二者相辅相成。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "亲水物质： 酒精  甘油 淀粉 纤维素 蛋白质 ......疏水物质：食用油  汽油 柴油 润滑油 ......")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "（1）材料在外力作用下抵抗破坏的能力称为强度。（2）影响材料强度试验结果的因素：")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "天然大理石是地壳中原有的岩石经过地壳内高温高压作用形成的变质岩。属于中硬石材，主要由方解石、石灰石、蛇纹石和白云石组成。其主要成分以碳酸钙为主，约占50%以上。其它还有碳酸镁、氧化钙、氧化锰及二氧化硅等。由于大理石一般都含有杂质，而且碳酸钙在大气中受二氧化碳、碳化物、水气的作用，也容易风化和溶蚀，而使表面很快失去光泽。所以少数的，如汉白玉、艾叶青等质纯、杂质少的比较稳定耐久的品种可用于室外，其他品种不宜用于室外，一般只用于室内装饰面。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "石灰有生石灰（CaO）和熟石灰（Ca(OH)₂），生石灰吸潮或加水就成为熟石灰（因此生石灰可用于防潮干燥）。 熟石灰经调配成石灰浆、石灰膏、石灰砂浆等，用作涂装材料和砖瓦粘合剂。纯碱是用石灰石、食盐、氨等原料经过多步反应制得（索尔维法）。利用消石灰和纯碱反应制成烧碱（苛化法）。 另外，石灰在医药方面也有应用。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "质量吸水率:《建筑材料》形成性考核册答案 w. m, x10 m 29002500/2500 x0 \\frac{29002500}{2500}xI0 2500×1006169 2.密度:《建筑材料》形成性考核册答案 p= fn/J  50/18.5- 2m7 3.体积密度:《建筑材料》形成性考核册答案 R po Vo m/y0  -24-x21vI05-0\\times5-3 2119 4.孔隙率:《建筑材料》形成性考核册答案 PD-×100 2.7-1.71 2.7x1OB363%")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer_11(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)#保证富文本框加载完毕


    # 20单
    dxAnswer = '''01．正确答案是：水泥
02．正确答案是：硅酸盐水泥
03．正确答案是：早期快后期慢
04．正确答案是：0OC
05．正确答案是：以上都是
06．正确答案是：水泥在水化过程中放出的热量
07．正确答案是：氢氧化钙和水化铝酸钙
08．正确答案是：大体积混凝土工程
09．正确答案是：铝酸盐水泥
10．正确答案是：扩大其强度等级范围，以利于合理选用
11．正确答案是：线膨胀系数
12．正确答案是：品种和强度等级
13．正确答案是：气干状态
14．正确答案是：和易性
15．正确答案是：混凝土拌合物的稀稠程度及充满模板的能力
16．正确答案是：坍落度是保水性的指标
17．正确答案是：每立方米混凝土中砂的质量和砂石的总质量之比
18．正确答案是：水泥石与粗骨料的结合面先发生破坏
19．正确答案是：早强剂
20．正确答案是：水灰比、砂率、单位用水量'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, "：")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 10判断
    panduan_length=10
    danxuanti_length=20
    duoxuanti_length=0
    dxAnswer = '''判断题01．对”。
判断题02．错”。
判断题03．“错”。
判断题04．对”。
判断题05．错”。
判断题06．对”。
判断题07．错”。
判断题08．错”。
判断题09．错”。
判断题10．“对”。'''

    pdAnswer = panduanAutoAnswerFix(dxAnswer, "”。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEqualsPanDuan(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    # 6个富文本
    line = browser.page_source
    frameId = line.split(":31_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":31_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "细度是指水泥颗粒总体的粗细程度。水泥颗粒越细，与水发生反应的表面积越大，因而水化反应速度较快，而且较完全，早期强度也越高，但在空气中硬化收缩性较大，成本也较高。如水泥颗粒过粗则不利于水泥活性的发挥。一般认为水泥颗粒小于40μm（0.04mm）时，才具有较高的活性，大于100μm（0.1mm）活性就很小了。硅酸盐水泥和普通硅酸盐水泥细度用比表面积表示。比表面积是水泥单位质量的总表面积")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":32_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":32_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "水泥的初凝时间是指从水泥加水拌合起至水泥浆开始失去可塑性所需的时间的时间，这个时间对施工影响较大，为了保证有足够的时间在初凝之前完成混凝土的搅拌、运输和浇捣及砂浆的粉刷、砌筑等施工工序，初凝时间不宜过短，为此，国家标准规定硅酸盐水泥的初凝时间不早于45分。短于这个时间很容易导致混凝土还来不及施工就已经失去了塑性。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":33_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":33_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "砂、石有专门的试验方法，通过不同孔径的筛子进行筛分细算。不同孔径筛子上的筛余量有一定的范围。如果其各个筛的筛余量在标准规定的范围内，那么就称其为连续级配。连续级配对混凝土和易性（尤其是流动性），对强度也有帮助。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":34_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":34_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1、严格控制水灰比，保证足够的水泥用量；2、合理选择水泥品种；3、选用较好砂、石骨料，并尽量采用合理砂率；4、掺引气剂、减水剂等外加剂；5、掺入高效活性矿物掺料；6、施工中搅拌均匀、振捣密实、加强养护、增加混凝土密实度、提高混凝土质量。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":35_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":35_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "质量吸水率:《建筑材料》形成性考核册答案 w. m, x10 m 29002500/2500 x0 \\frac{29002500}{2500}xI0 2500×1006169 2.密度:《建筑材料》形成性考核册答案 p= fn/J  50/18.5- 2m7 3.体积密度:《建筑材料》形成性考核册答案 R po Vo m/y0  -24-x21vI05-0\\times5-3 2119 4.孔隙率:《建筑材料》形成性考核册答案 PD-×100 2.7-1.71 2.7x1OB363%")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "施工每立方混凝土各种材料用量：水泥C = 286Kg砂子S = 286×2.28（1 + 0.03）=672Kg石子G = 286×4.47（1 + 0.01）=1291Kg水W = 286×0.64 - 286×2.28×0.03 - 286×4.47×0.01 = 151Kg施工配合比：（286 / 286）：（672 / 286）：（1291 / 286）：（151 / 286）=1: 2.35:4.51: 0.53")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum > 3:
        return
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
    for value in mapmulAnswer:
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
    for value in mapmulAnswer:
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



def wait3AndCloseTab(browser):
    time.sleep(2)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(3.5)


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473559'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473560'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473561'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473562'

zhangjie2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473238'
zhangjie3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473252'
zhangjie4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473283'
zhangjie5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473313'
zhangjie6 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473356'
zhangjie7 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473382'
zhangjie8 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473401'
zhangjie9 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473439'
zhangjie10 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473455'
zhangjie11= 'http://hubei.ouchn.cn/mod/quiz/view.php?id=473492'

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
    #
    #     enterTest(browser, xingkao2)
    #     if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #         writeAnswer2(browser)
    #     wait3AndCloseTab(browser)
    #
    #     enterTest(browser, xingkao3)
    #     if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #         writeAnswer3(browser)
    #     wait3AndCloseTab(browser)
    #
    #     enterTest(browser, xingkao4)
    #     if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
    #         writeAnswer4(browser)
    #     wait3AndCloseTab(browser)

    #开始做各章节的考试
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_2(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_3(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_4(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_5(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_6(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_7(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_8(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_9(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_10(browser)
    wait3AndCloseTab(browser)
    enterTest(browser, zhangjie2)
    if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
        writeAnswer_11(browser)
    wait3AndCloseTab(browser)


    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(2)
