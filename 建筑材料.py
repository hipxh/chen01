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
        print(i)
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
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．造岩矿物是指答案：组成岩石的矿物　
2．由两种或两种以上矿物组成的岩石称为答案：多矿岩
3．由地球内部的岩浆上升到地表附近或喷出地表，冷却凝结而成的岩石称为答案：岩浆岩　
4．下列关于岩石性质说法有误的一项是答案：岩石是典型的塑性材料　
5．毛石指的是答案：由爆破直接获得的石块　
6．毛石按平整度可分为答案：平毛石和乱毛石　
7．料石（又称条石）是由答案：人工或机械开采出的较规则的六面体石块，略经加工凿琢而成的
8．料石按其加工后的外形规则程度，分为答案：毛料石、粗料石、半细料石和细料石　
9．下列关于天然花岗石说法有误的一项是答案：花岗石属碱性石材
10．下列关于天然大理石说法有误的一项是答案：绝大多数大理石板材只宜用于室外'''
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
def writeAnswer_4(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．石灰的主要成分是答案：氢氧化钙
2．通常所说的建筑消石灰粉其实就是答案：熟石灰粉
3．石灰（CaO加水之后水化为熟石灰[CaOH2]的过程，称为答案：石灰的熟化
4．生石灰水化的特点是体积增大答案：1-2.5倍
5．在内部，对强度增长起主导作用的是答案：结晶硬化
6．下列不作为评判生石灰质量好坏标准的一项是答案：水化过程中的放热量
7．熟石灰粉颗粒愈细，有效成分愈多，其品质答案：愈好
8．下列关于石灰技术性质说法有误的一项是答案：保水性较差
9．下列关于石灰应用说法有误的一项是答案：磨细生石灰粉在干燥条件下储存期一般不超过一年
10．建筑上常用的石膏，其主要生产原料是答案：生石灰
11．石膏的品种很多，虽然各品种的石膏在建筑中均有应用，但是用量最多、用途最广的是答案：建筑石膏
12．建筑石膏与适量的水混合后，起初形成均匀的石膏浆体，但紧接着石膏浆体失去塑性，成为坚硬的固体，其原因是答案：半水石膏遇水后，将重新水化生成二水石膏，并逐渐凝结硬化
13．建筑石膏凝结硬化的过程需要答案：放出热量
14．建筑石膏的技术要求主要有答案：细度、凝结时间和强度
15．建筑石膏呈洁白粉末状，密度约为答案：2.6-2.75 g/㎝3
16．下列关于石膏性质特点说法有误的一项是答案：与石灰等胶凝材料相比，耐水性、抗冻性好
17．建筑石膏容易受潮吸湿，凝结硬化快，因此在运输、贮存的过程中，应注意避免答案：受潮
18．水玻璃的最主要成分是答案：硅酸钠
19．水玻璃的化学通式为答案：R2O·nSiO2
20．下列关于水玻璃的硬化说法错误的是答案：水玻璃在自然条件下凝结与硬化速度非常快
21．下列环境条件最有利于水玻璃凝结硬化的是答案：温度高、湿度小
22．下列有关水玻璃的性质说法有误的一项是答案：硬化后的水玻璃，其主要成分为SiO2，所以它的耐碱性能很高
23．相对来讲，与水玻璃硬化后的强度关系最小的一项是答案：水玻璃的价格
24．下列有关水玻璃的应用说法有误的一项是答案：水玻璃可用来涂刷石膏制品表面，浸渍多孔性材料
25．以水玻璃为基料，加入二种或四种矾的水溶液，称为答案：二矾或四矾防水剂'''
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
def writeAnswer_5(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．通用硅酸盐水泥的生产原料主要是答案：石灰质原料和黏土质原料
2．为调整通用硅酸盐水泥的凝结时间，在生产的最后阶段还要加入答案：石膏
3．通用硅酸盐水泥的主要组分包括答案：硅酸盐水泥熟料、石膏和混合材料　
4．提高硅酸三钙的相对含量，就可以制得答案：高强水泥和早强水泥　
5．混合材料也是通用硅酸盐水泥中经常采用的重要组成材料，主要是指答案：为改善水泥性能，调节水泥强度等级而加入到水泥中的矿物质材料　
6．水泥经高温灼烧以后的质量损失率称为答案：烧失量　
7．从水泥加水拌和起到水泥浆开始失去塑性所需的时间称为答案：初凝试讲　
8．水泥凝结硬化过程中，体积变化是否均匀适当的性质称为答案：安定性　
9．水泥的抗压强度最高，一般是抗拉强度的答案：10~20倍　
10．为了便于识别，硅酸盐水泥和普通水泥包装袋上要求用答案：红字印刷
11．水泥存放期一般不应超过答案：3个月　
12．硅酸盐水泥的水化速度表现为 答案：早期快后期慢
13．硬化后的水泥浆体称为 答案：水泥石
14．水灰比是指水泥浆中水与水泥的答案：质量之比
15．水泥水化的临界温度为答案：0oC
15．自应力值大于2MPa的水泥称为答案：自应力水泥
15．相比较来讲，对于抢修工程或早期强度要求高的工程宜优先选用答案：铝酸盐水泥
15．从水泥加水拌和起到水泥浆开始失去塑性所需的时间称为答案：初凝时间
16．硅酸盐水泥的初凝时间不得早于答案：45min
17．硅酸盐水泥的细度其比表面积应不小于答案：300m2/kg
18．水泥石中引起腐蚀的组分主要是 答案：氢氧化钙和水化铝酸钙
19．下列关于防止水泥石腐蚀的说法有误的一项是答案：降低水泥石的密实度，可使水泥石的耐侵蚀性得到改善
20．预拌砂浆施工时，施工环境温度宜为 答案：5℃～35℃ 
21．下列关于预拌砂浆使用基本要求说法有误的一项是答案：不同品种、规格的预拌砂浆可以混合使用
22．当活性混合材料掺入硅酸盐水泥中与水拌合后，首先的反应是 答案：硅酸盐水泥熟料水化
23．下列被称为活性材料碱性激化剂的是答案：氢氧化钙
24．普通硅酸盐水泥，简称普通水泥，代号为答案：P·O
25．砂浆分层度试验时，通常以两次试验结果的算术平均值作为分层度值，其结果应精确至答案：1mm'''
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
def writeAnswer_6(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．下列关于混凝土性能特点说法有误的一项是答案：在硬化后有很强的塑性
2．混凝土的应用要求主要涉及的内容包括答案：强度、工作性、耐久性和经济性
3．钢筋和混凝土能共同工作，主要是因为答案：近乎相等的线膨胀系数
4．决定混凝土成本的最主要原料是答案：水泥
5．一般情况下水泥强度等级应为混凝土设计强度等级的答案：1.5~2.0倍
6．选用水泥时，主要考虑的因素是 答案：品种和强度等级
7．细骨料的粒径通常小于答案：4.75mm
8．天然砂分为河砂、湖砂、山砂和海砂，其中材质最差的是答案：山砂
9．在混凝土中，骨料的总表面积小，则胶凝材料用量答案：小
10．砂的筛分试验主要是用来测定答案：粗细程度及颗粒级配
11．砂在烘箱中烘干至恒重，达到内外均不含水的状态，称为答案：全干状态
12．下列关于含泥量、泥块含量和石粉含量说法有误的一项是答案：含泥量或泥块含量超量时，不得采用水洗的方法处理
13．下列关于砂中有害物质的说法有误的一项是答案：有机物可以加速水泥的凝结
14．通常将岩石颗粒粗骨料称为答案：石子
15．在用水量和水灰比固定不变的情况下，最大粒径加大，骨料表面包裹的水泥浆层加厚，混凝土拌合物的流动性将答案：提高
16．下列关于石子颗粒级配说法有误的一项是答案：间断级配的颗粒大小搭配连续合理，用其配置的混凝土拌合物工作性好，不易发生离析
17．压碎指标与石子强度关系说法正确的一项是答案：压碎指标越大，石子的强度越大
18．骨料颗粒在气候、外力及其它物理力学因素作用下抵抗碎裂的能力称为答案：坚固性
19．骨料颗粒的理想形状应为答案：立方体
20．海水只可用于拌制答案：素混凝土
21．下面关于拌合用水说法有误的一项是答案：地表水和地下水首次使用前无需按规定进行检测，可直接作为钢筋混凝土拌合用水使用
22．混凝土拌合物在一定的施工条件和环境下，是否易于各种施工工序的操作，以获得均匀密实混凝土的性能是指混凝土的答案：工作性
23．保水性反映了混凝土拌合物的答案：稳定性
24．坍落度试验时，坍落度筒提起后无稀浆或仅有少数稀浆自底部析出，则表示答案：保水性差
25．维勃稠度值大，说明混凝土拌合物的答案：保水性差
26．在相同用水量情况下，水泥越细，其答案：混凝土拌合物流动性小，但粘聚性及保水性较好。
27．大量试验证明，当水胶比在一定范围0.40～0.80内而其他条件不变时，混凝土拌合物的流动性只与单位用水量有关，这一现象称为答案：恒定用水量法则
28．当胶凝材料仅有水泥时，水胶比亦称答案：水灰比
29．砂率是答案：每立方米混凝土中砂和砂石总质量之比
30．下列关于砂率说法有误的一项是答案：合理砂率即在流动性不变的前提下，所需水泥浆总体积为最大的砂率
31．下列关于改善混凝土拌合物的工作性的措施说法有误的是答案：改善砂、石料的级配，一般情况下尽可能采用间断级配
32．拌制混凝土时，其他条件不变的前提下，加大砂石粒径，则答案：流动性提高，保水性降低
33．混凝土的强度有受压强度、受拉强度、受剪强度、疲劳强度等多种，其中最重要的是答案：受压强度
34．普通混凝土受压一般发生的破坏形式为答案：水泥石与粗骨料的结合面发生破坏
35．按照国家标准，立方体抗压强度试件的边长为答案：150mm
36．根据《普通混凝土力学性能试验方法标准》GB/T50081-2002规定，混凝土的轴心抗压强度采用的棱柱体标准试件的尺寸是答案：150mm×150mm×300mm
37．水泥水化需要的水分仅占水泥质量的答案：25%
38．水泥的水化是放热反应，维持较高的养护湿度，可答案：有效提高混凝土强度的发展速度
39．下列关于提高混凝土强度措施的方法说法有误的一项是答案：实践证明，混凝土的龄期在3-6个月时，强度较28d会提高50-100%
40．混凝土抵抗压力水渗透的性能称为混凝土的答案：抗渗性
41．下列关于混凝土抗冻性说法有误的一项是答案：在养护阶段，水泥的水化热高，会降低混凝土的抗冻性
42．下列关于混凝土碳化说法有误的一项是答案：混凝土的碳化可使混凝土表面的强度适度提高
43．下列主要用于改善混凝土拌合物流变性能的外加剂是答案：减水剂
44．减水剂是指答案：在保持混凝土拌合物流动性的条件下，能减少拌合水量的外加剂
45．下列关于减水剂作用效果说法有误的一项是答案：在保持流动性及水泥用量的条件下，使水灰比上升，从而提高混凝土的强度
46．早强剂按其化学组成分为答案：无机早强剂和有机早强剂
47．下列属于有机早强剂的是答案：乙酸盐早强剂
48．氯盐早强剂包括钙、钠、钾的氯化物，其中应用最广泛的为答案：氯化钙 
49．下列关于引气剂说法有误的一项是答案：引气剂也是一种亲水型表面活性剂
50．引气剂的活性作用主要是发生在答案：固-气界面
51．能延缓混凝土的凝结时间并对混凝土的后期强度发展无不利影响的外加剂是答案：缓凝剂
53．矿物掺合料分为答案：磨细矿渣、磨细粉煤灰、磨细天然沸石、硅灰
54．矿物外加剂与水泥混合材料的最大不同点是具有答案：更高的细度
55．下列关于矿物掺合料特性和机理说法有误的是答案：可改善混凝土耐久性
56．下列在大体积混凝土工程施工中，采用最多的外加剂是答案：泵送剂
57．道路、隧道、机场的修补、抢修工程的混凝土施工时，采用最多的外加剂是答案：速凝剂
58．下列关于混凝土外加剂使用注意事项说法有误的一项是答案：液态状外加剂，为保持作用的均匀性，采用直接倒入搅拌机的方法加入
59．粉状外加剂如有结块，经性能检验合格后应粉碎至全部通过筛子型号为答案：0.65mm
60．混凝土的配合比设计顺序正确的一项是 答案： 计算配合比--基准配合比--实验室配合比--施工配合比
61．通过对水胶比的微量调整，在满足设计强度的前提下，确定一水泥用量最节约的方案，从而进一步调整配合比，称为答案：实验室配合比
62．在进行混凝土的配合比设计前，需确定和了解混凝土的工作性涉及答案：强度等级
63．在进行混凝土的配合比设计前，需确定和了解的基本资料不包括答案：工程造价和投资人
64．混凝土水胶比的确定主要取决于混凝土的答案：坍落度指标
65．砂率的确定主要考虑的两个方面是答案：强度和耐久性
66．混凝土水胶比的确定主要取决于混凝土的答案：坍落度指标
67．砂率的确定主要考虑的两个方面是答案：强度和耐久性
68．进行初步计算配合比设计时，用来确定砂、石用量的体积法假定主要是指答案：假定混凝土拌合物的体积等于各组成材料的体积与拌合物中所含空气的体积之和
69．按计算配合比进行混凝土配合比的试配和调整,试拌采用机械搅拌时，其搅拌不应小于搅拌机公称容量的答案：1/4
70．下列关于混凝土生产的质量控制说法有误的一项是答案：采用天然水现场进行搅拌的混凝土，拌合用水的质量不需要进行检验
71．混凝土生产施工工艺的质量控制时，混凝土的运输、浇筑及间歇的全部时间不应超过混凝土的 答案：初凝时间 
72．混凝土质量合格性的指标通常是答案：抗压强度
73．当一次连续浇注的同配合比混凝土超过1000m3时，每200 m3取样不应少于答案：1次  
74．可在施工现场通过压力泵及输送管道进行浇注的混凝土称为答案：泵送混凝土
75．泵送混凝土的砂率要比普通混凝土大答案：8%～10% 
76．大体积混凝土应用最突出的特点是答案：降低混凝土硬化过程中胶凝材料的水化热以及养护过程中对混凝土进行温度控制 
77．下列混凝土工程不属于大体积混凝土的是答案：楼梯 
78．高性能混凝土是一种新型高技术混凝土，其最主要的指标是答案：耐久性  
79．为能得到很低的渗透性并使活性矿物掺合料充分发挥强度效应，高性能混凝土水胶比一般低于 答案： 0.4  
80．根据供销合同，由搅拌站统一生产的，以商品形式供应给施工单位的混凝土称为答案：商品混凝土 
81．下面关于商品混凝土说法有误的一项是答案：商品混凝土不利于保证混凝土的质量  
82．筛分试验不需要的实验仪器是答案：搅拌机  
83．筛分试验的主要目的是答案： 测定细集料（天然砂、人工砂、石屑）的颗粒级配及粗细程度
84．坍落度试验主要检测和确定混凝土拌合物的 答案：流动性 
85．坍落度试验主要检测和确定混凝土拌合物的 答案：流动性 
86．混凝土立方体抗压强度测定时，取样或拌制好的混凝土拌合物应至少用铁锨再来回拌和 答案：3次  
87．下列关于混凝土立方体抗压强度测定试验操作步骤不当的是 答案：当试件接近破坏开始急剧变形时，应加大调整试验机油门，直到破坏  
88．混凝土立方体抗压强度测定需要的仪器设备主要包括。答案：抗压强度试模、振动台、压力试验机 
89．在已选定设计强度等级的情况下，欲提高混凝土的强度保证率，可提高答案：配制强度'''
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
def writeAnswer_7(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．将砖、石、砌块等粘结成为砌体的砂浆称为答案：砌筑砂浆　
2．砌筑砂浆最常用的细骨料为答案：普通砂
3．砂浆的流动性也叫做稠度，是指答案：在自重或外力作用下流动的性能　
4．下列有关砂浆性质说法有误的一项是答案：砂浆的粘结强度、耐久性均随抗压强度的增大而降低　
5．下列关于砌筑砂浆配合比设计应满足的基本要求说法有误的一项是答案：经济上应合理，水泥及掺合料的用量越多越好　
6．水泥混合砂浆配合比计算时，第一步应答案：确定砂浆的试配强度　
7．下列关于砌筑砂浆验收说法有误的一项是答案：砂浆强度应以标准养护，龄期为21d的试块抗压试验结果为准
8．同一验收批砂浆试块抗压强度的最小一组的平均值必须大于或等于设计强度等级对应的立方体抗压强度的答案：0.75倍　
9．水泥砂浆宜用于砌筑潮湿环境以及强度要求较高的砌体答案：砌筑潮湿环境以及强度要求较高的砌体
10．下列关于砌筑砂浆应用说法有误的一项是答案：低层房屋或平房不可采用石灰砂浆
11．凡涂抹在建筑物或建筑构件表面的砂浆，统称为答案：抹面砂浆
12．下列关于普通抹面砂浆说法有误的一项是答案：普通抹面砂浆是建筑工程中用量最小的抹面砂浆
13．直接用于建筑物内外表面，以提高建筑物装饰艺术性为主要目的抹面砂浆指的是答案：装饰砂浆
14．下列关于特种砂浆说法有误的一项是答案：保温砂浆又称刚性砂浆
14．用于砌筑潮湿环境以及强度要求较高的砌体，宜用答案：水泥砂浆
15．下列关于预拌砂浆说法有误的一项是 答案：不同品种、规格的预拌砂浆可混合使用
16．预拌砂浆施工时，施工环境温度宜为 答案：5℃～35℃
17．下列关于预拌砂浆进场时的做法有误的是 答案：预拌散装干混砂浆进场时，需外观均匀，可有少量结块、受潮现象
18．下列关于湿拌砂浆储存容器使用不当的一项是答案：储存容器应密闭、吸水
19．砂浆稠度试验的试验目的是 答案：稠度试验用于确定砂浆配合比及施工中控制砂浆稠度，从而达到控制用水量的目的
20．砂浆稠度试验时，下列用不到的仪器设备是答案：烤箱
21．砂浆分层度试验的试验目的是 答案：用于测定砂浆拌合物在运输、停放、使用过程中的离析、泌水等内部组成的稳定性
22．砂浆分层度值的单位应是答案：mm'''
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
def writeAnswer_8(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．国家标准《烧结普通砖》GB5101—2003规定，凡以黏土、页岩、煤矸石、粉煤灰等为主要原料，经成型、焙烧而成的实心或孔洞率不大于15%的砖，称为答案：烧结普通砖　
2．泛霜也称起霜，是指答案：砖在使用过程中的盐析现象
3．烧结多孔砖是指答案：以粘土、页岩、煤矸石为主要原料，经焙烧而成的主要用于承重部位的多孔砖　
4．下列关于烧结多孔砖说法有误的一项是答案：烧结多孔砖因其强度较高，绝热性能较普通砖差　
5．蒸压灰砂砖简称灰砂砖是以答案：石灰和砂为主要原料，经坯料制备、压制成型，再经高压饱和蒸汽养护而成的砖　
6．下列关于蒸压灰砂砖和蒸压粉煤灰砖说法有误的一项是答案：灰砂砖可用于长期受热200℃以上、受急冷、急热或有酸性介质侵蚀的环境　
7．粉煤灰砌块又称答案：粉煤灰硅酸盐砌块
8．下列关于粉煤灰砌块说法有误的一项是答案：粉煤灰砌块宜用于经常处于高温的承重墙　
9．蒸压加气混凝土砌块的制作原料为答案：钙质材料和硅质材料
10．下列关于加气混凝土砌块的特点和应用说法有误的一项是答案：加气混凝土砌块适用于建筑物的基础和温度长期高于80℃的建筑部位　
11．混凝土小型空心砌块的空心率为答案：25%~50%
12．下列关于混凝土小型空心砌块说法有误的一项是答案：混凝土小型空心砌块用自然养护时，必须养护21天后方可使用
13．轻骨料混凝土小型空心砌块的体积密度不大于 答案：1400kg/m
14．下列关于轻骨料混凝土小型空心砌块的说法有误的一项是答案：轻骨料混凝土小型空心砌块的抗震性能较差
15．纤维增强低碱度水泥建筑平板的增强材料为 答案：温石棉、中碱玻璃纤维或抗碱玻璃纤维
16．下列关于纤维增强低碱度水泥平板说法有误的一项是答案：纤维增强低碱度水泥平板质量高、强度低
17．GRC轻质多孔隔墙条板的增强材料是答案：耐碱玻璃纤维
18．GRC轻质多孔隔墙条板是 答案：以耐碱玻璃纤维为增强材料，以硫铝酸盐水泥为主要原料的预制非承重轻质多孔内隔墙条板 
19．生产石膏空心条板的胶凝材料是答案：建筑石膏
20．下列关于石膏空心条板说法有误的一项是 答案：用石膏空心条板安装墙体时必须使用龙骨
21．彩钢夹芯板的芯材一般采用答案：隔热材料
22．下列关于彩钢夹芯板说法有误的一项是答案：彩钢夹芯板的芯材一般采用不可燃烧材料'''
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
def writeAnswer_9(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．根据脱氧程度不同，浇铸的钢锭可分为沸腾中脱氧程度最差的是答案：沸腾钢
2．钢是指答案：含碳量在2%以下，含有害杂质较少的铁—碳合金
3．钢按化学成分可分为答案：碳素钢和合金钢
4．在碳素钢中加入某些合金元用于改善钢的性能或使其获得某些特殊性能的钢称为答案：合金钢
5．建筑用钢的强度指标，通常用答案：屈服点和抗拉强度
6．钢材抵抗冲击荷载而不被破坏的能力称为答案：冲击韧性
7．钢材承受交变荷载反复作用时，可能在最大应力远低于屈服强度的情况下突然破坏，这种破坏称为答案：疲劳破坏
8．钢材随时间的延长，其强度提高，塑性和冲击韧性下降，这种现象称为答案：时效
9．冷弯性能是指答案：钢材在常温下承受弯曲变形的能力，是钢材的重要工艺性能
10．下列均是钢材重要的工艺性能的一组是答案：冷弯性和可焊性
11．钢材中最主要含有的化学元素是答案：铁和碳
12．下列均可改善钢材性能的的一组化学元素是答案：锰、钛、钒
13．下列关于钢材中含碳量说法有错误的一项是答案：钢材随含碳量的越高，强度和硬度越高
14．下列关于钢材有害元素氧、硫、磷说法有误的一项是答案：磷的偏析较严重，使钢材的冷脆性降低，可焊性降低
15．钢材经冷加工产生塑性变形，从而提高其屈服强度，这一过程称为答案：冷加工强化处理
16．冷加工是指答案：钢材在常温下进行的加工
17．将经过冷拉的钢筋于常温下存放15～20d，或加热到100～200℃并保持2h左右，这个过程称为答案：时效处理
18．因时效而导致钢材性能改变的程度称为答案：时效敏感性
19．屈服点为235MPa的A级沸腾纲表示表示为答案：Q235—A·F
20．低合金高强度结构钢是在碳素结构钢的基础上，添加少量的一种或几种合金元素的一种结构钢，通常其合金元素含量小于答案：5%
21．钢结构用型钢所用母材主要是答案：碳素结构钢及低合金高强度结构钢
22．冷弯薄壁型钢指答案：指用2～6mm厚的薄钢板或带钢经模压或冷弯各种断面形状的成品钢材
23．用加热钢坯轧成的条型成品钢筋，称为答案：热轧钢筋
24．下列关于钢结构用钢材说法有误的一项是答案：预应力混凝土用钢绞线，是以数根优质碳素结构钢钢丝的经过冷处理而制成
25．拉伸试验主要测定钢材的答案：抗拉强度、屈服点、断后伸长率
26．下列关于钢筋混凝土结构用钢检验要求说法有误的一项是答案：冷轧扭钢筋的检验时，每批不应大于50t
27．钢的表面与周围介质发生化学作用或电化学作用而遭到侵蚀破坏的过程，称为钢材的答案：锈蚀
2．根据锈蚀作用机理，钢材的锈蚀可分为答案：化学锈蚀和电化学锈蚀
28．下列关于钢材在使用中防止锈蚀说法有误的一项是答案：重要的预应力承重结构，可以掺用氯盐，并对原材料进行严格检验控制
29．在仓储中钢材锈蚀防止做法错误的一项是答案：金属材料在保管期间，必须按照规定的检查制度，每两年进行一次检查
30．钢筋试验时，一般要求室温的范围为答案：10~35℃
31．拉伸试验的两根试件中，如其中一根试件的屈服点、抗拉强度和伸长率三个指标中，有一个指标达不到标准中规定的数值，则应答案：再抽取双倍（4根）钢筋，制取双倍（4根）试件重做试验
32．下面关于拉伸试验说法有误的一项是答案：拉伸试验用钢筋试件可进行车削加工用两个小冲点或细划线标出试件原始标距
33．拉伸试验步骤的第一步是答案：调整试验机初始参数
34．下面关于钢筋冷弯试验说法有误的一项是答案：冷弯试验时，将试件安放好后，应快速地加荷
35．钢筋冷弯试验的目的是答案：通过冷弯试验，测定其弯曲塑性变形性能'''
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
def writeAnswer_10(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．高分子化合物聚合物是由千万个原子彼此以共价键连接的大分子化合物，其分子量一般在答案：104以上　
2．合成高分子化合物，常用的聚合方法有答案：加聚和缩聚
3．高分子化合物按其在热作用下所表现出来的性质的不同，可分为答案：热塑性聚合物和热固性聚合物　
4．在光、热、大气作用下，高分子化合物的组成和结构发生变化，致使其性质变化如失去弹性、出现裂纹、变硬、脆或变软、发粘失去原有的使用功能，这种现象称为答案：老化　
5．塑料的性质主要取决于答案：所用合成树脂的性质　
6．生产塑料时，着色剂的作用是答案：使塑料制品具有鲜艳的色彩和光泽　
7．下列关于塑料性质说法有误的一项是答案：塑料与钢铁等金属材料相比，强度和弹性模量较大，即刚度大
8．塑料得到热能力小，其导热能力为金属的答案：1/500～1/600　
9．聚乙烯软性好、耐低温性好，耐化学腐蚀和介电性能优良成型工度<50℃，耐老化差，其主要用于答案：防水材料、给排水管和绝缘材料等
10．下列关于建筑塑料制品说法有误的一项是答案：塑料装饰板材按原材料的不同可分为平板、波形板、实体异型断面板、中空异型断面板等
11．下列关于胶粘剂组成与分类说法错误的一项是答案：按强度特性不同，胶粘剂可分为有机类和无机类
12．热熔型胶粘剂的黏结原理是答案：通过加热熔融粘合，随后冷却、固化，发挥粘合力
13．下列关于胶粘剂使用注意事项说法有误的一项是答案：胶层越厚越好
14．选择胶粘剂的时应了解胶粘剂的价格和来源难易，其目的是答案：在满足使用性能要求的条件下，尽可能选用价廉的、来源容易的、通用性强的胶粘剂'''
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
def writeAnswer_11(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 5单
    dxAnswer = '''1．沥青按其在自然界中获取的方式，可分为答案：地沥青和焦油沥青
2．建筑工程中最常用的是答案：石油沥青和煤沥青
3．直接影响石油沥青的柔软性、抗裂性及施工难度的组分是答案：油分
4．石油沥青的黏结力和延伸性随树脂含量的增加而答案：减小
5．沥青质含量增加时，沥青的黏度和粘结力将答案：增加
6．沥青质含量增加时，沥青的硬度和软化点将答案：提高 
7．反映沥青材料内部阻碍其相对流动的特性是答案：黏滞性
8．用来表示石油沥青塑性的指标是答案：延度
8．石油沥青过于黏稠而需要稀释，一般采用答案：石油产品系统的轻质油
9．用来表示石油沥青黏滞性的指标是答案：针入度
10．用来表示石油沥青温度敏感性的指标是答案：软化点
11．石油沥青的塑性又称答案：延展性
12．石油沥青在热、阳光、氧气和潮湿等因素的长期综合作用下抵抗老化的性能是指答案：大气稳性性
14．下列关于道路沥青说法有误的一项是答案：北方寒冷地区宜选用高黏度的石油沥青
15．根据我国现行石油沥青标准，石油沥青主要分为答案：道路石油沥青、建筑石油沥青和普通石油沥青
16．用树脂改性石油沥青，可以改进沥青的答案：耐寒性、黏结性和不透气性
17．矿物填充料改性沥青时，掺入粉状填充料的合适掺量一般为沥青质量的答案：10%~25%
18．橡胶在阳光、热、空气答案：氧气和臭氧或机械力的反复作用下，表面会出现变色、变硬、龟裂、发黏，同时机械强度降低，这种现象称为答案：老化
19．应用最广、产量最多的合成橡胶为答案：丁苯橡胶
20．以合成树脂为主要成分的防水材料，称为答案：树脂型防水材料
21．聚氨酯密封膏作为防水材料，属于答案：树脂型防水材料
22．根据国家规范规定，石油沥青防水卷材仅适用于答案：Ⅲ级和Ⅳ级屋面
23．对于防水等级为Ⅲ级的屋面，应选用答案：三毡四油沥青卷材
24．以合成高分子聚合物改性沥青为涂盖层，纤维织物或纤维毡为胎体，粉状、粒状、片状或薄膜材料为覆面材料制成的可卷曲片状防水材料是答案：高聚物改性沥青防水卷材
25．下列关于高聚物改性沥青防水卷材说法有误的一项是答案：根据国家标准规定，高聚物改性沥青防水卷材仅适用于防水等级为Ⅰ级屋面防水工程
26．以合成高分子聚合物改性沥青为涂盖层，纤维织物或纤维毡为胎体，粉状、粒状、片状或薄膜材料为覆面材料制成的可卷曲片状防水材料是答案：高聚物改性沥青防水卷材
27．合成高分子防水卷材的铺设一般采用答案：单层铺设
28．防水涂料按液态类型可分为答案：溶剂型、水乳型和反应型三种
29．防水涂料在一定水压或动水压和一定时间内不出现渗漏的性能称为答案：不透水性
30．下列主要用作屋面、墙面、沟和槽的防水嵌缝材料的防水油膏是答案：沥青嵌缝油膏
31．丙烯酸类密封膏不适用于答案：水池接缝
32．下列关于防水粉说法错误的一项是答案：防水粉露天风力过大时施工容易，建筑节点处理简单等特点
33．针入度测定试验时，沥青试样加热时间不得超过答案：30min
34．针入度测定试验时，同一试样平行试验不得少于答案：3次
35．延度测定试验时，试样加热温度不得超过试样估计软化点答案：100oC
36．延度测定试验，测定结果应取答案：平行试验测定结果的算数平均值
37．软化点测定试验主要目的是答案：测定石油沥青的粘性和塑性随温度升高而变化的程度
38．软化点测定试验时，当试样软化点小于80℃时，重复性试验的允许差为答案：1℃'''
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

        # 开始做各章节的考试
        enterTest(browser, zhangjie2)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_2(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie3)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_3(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie4)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_4(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie5)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_5(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie6)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_6(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie7)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_7(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie8)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_8(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie9)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_9(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie10)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_10(browser)
        wait3AndCloseTab(browser)
        enterTest(browser, zhangjie11)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer_11(browser)
        wait3AndCloseTab(browser)


    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(6)
