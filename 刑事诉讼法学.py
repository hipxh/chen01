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
        if "\n" in ele.text:
            if neirong == ele.text or "A.\n" + neirong == ele.text or "B.\n" + neirong == ele.text or "C.\n" + neirong == ele.text or "D.\n" + neirong == ele.text or "E.\n" + neirong == ele.text or "a.\n" + neirong == ele.text or "b.\n" + neirong == ele.text or "c.\n" + neirong == ele.text or "d.\n" + neirong == ele.text or "e.\n" + neirong == ele.text or "1.\n" + neirong == ele.text or "2.\n" + neirong == ele.text or "3.\n" + neirong == ele.text or "4.\n" + neirong == ele.text:
                return ele
        else:
            if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text or "1. " + neirong == ele.text or "2. " + neirong == ele.text or "3. " + neirong == ele.text or "4. " + neirong == ele.text:
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
        result.append(i.strip().split(reg,1)[1])
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
        listList.append(i.split(reg,1)[-1].split(reg2))
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
    time.sleep(0.3)


# start to answer.
def writeAnswer1(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')

    dxAnswer = '''1.刑事诉讼
    2.人民法院对刑事案件进行的审判活动
    3.监督与被监督
    4.监督职能
    5.正在被执行刑罚的人
    6.司法机关在必要的时候可以指定证人
    7.辨认证据
    8.要求解除强制措施
    9.机关、团体.企事业单位的保卫部门
    10.外国人犯罪的案件
    11.职能管辖
    12.非法拘禁犯罪
    13.受理
    14.中国公民对外国人犯罪的案件
    15.某侦查人员接受过另一当事人的吃请
    16.李某应否回避需提交检察院检察长决定
    17.可以口头方式提出
    18.杨某的母亲
    19.公诉案件自案件移送审查起诉之日起
    20.可以为其指定辩护人'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(6)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''21.纠问式; 控告式; 混合式
    22.保证刑法的正确实施; 保障国家安全和社会公共安全; 维护社会主义社会秩序; 惩罚犯罪保护人民
    23.对公安机关提请批准的案件，进行审查; 对直接受理的案件进行侦查; 对公安机关的侦查活动，依法实行监督
    24.要求同被告人和解; 请求撤回自诉; 请求以调解结案
    25.对被告人负有保护责任的村长; 被告人的养父; 被告人的母亲
    26.如果对不起诉决定不服，可以直接向人民法院起诉; 认为公安机关应当立案侦查而不立案时，可以要求人民检察院督促立案; 有权委托诉讼代理人
    27.必须在法律规定和被代理人授权范围内为代理行为; 只要不超越代理权限，其行为有一定自主性; 其行动如果没有被代理人的授权或同意，不具有法律效力
    28.提供法律咨询; 代理申诉、控告; 为被逮捕的犯罪嫌疑人申请取保候审
    29.宣告无罪; 终止审理; 不起诉; 撤销案件
    30.有关国家秘密的案件; 有关公民个人隐私的案件; 未成年人犯罪的案件
    31.贪污贿赂犯罪; 国家机关工作人员利用职权实施的侵犯公民民主权利的犯罪; 国家机关工作人员利用职权实施的非法拘禁犯罪
    32.告诉才处理的案件; 被害人有证据证明的轻微刑事案件
    33.危害国家安全案件; 判处无期徒刑的案件; 判处死刑的案件
    34.鉴定人员; 书记员
    35.审判长; 书记员; 翻译人员; 人民陪审员
    36.在本案中担任证人; 接受当事人委托的人的请客送礼
    37.被告人; 未成年被告人的法定代理人
    38.被告人是聋哑人的; 被告人是盲人的; 被告人是未成年人的
    39.律师; 被告人的朋友
    40.公诉案件的被害人; 附带民事诉讼的当事人; 公诉案件被害人的近亲属'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.3)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer2(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')


    dxAnswer = '''1.公诉机关
2.被害人陈述
3.被告人供述
4.证人关于被告人实施犯罪情况的证言
5.证人听到被害人喊叫的证言
6.犯罪嫌疑人
7.24
8.3日
9.进行侦查实验
10.公安机关
11.原始证据.间接证据
12.李某在这次抢劫前还杀了赵某
13.物证
14.信件是书证，字条是物证
15.甲乙二人没有通谋，各自埋伏，几乎同时向丙开枪，后查明丙身中一弹，甲乙对各自犯罪行为供认不讳，但收集到的证据无法查明这一枪到底是谁打中的
16.既属物证，又属书证
17.蔺某
18.在侦查.审查起诉阶段，被害人提出赔偿要求经记录在案的，公安机关.检察院可以对民事赔偿部分进行调解
19.原告人，自公诉人提起公诉起，有权提起附带民事诉讼
20.六个月'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(6)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''21.被毁财物的复制品; 鉴定结论的抄件
22.甲吃、喝、嫖、赌，道德品质败坏; 甲在10年以前曾采用过与本案相同的手段实施过杀人行为(未遂，被判过刑)
23.被撬坏的门锁; 现场发现的烟头; 赃款; 沾有被害人血迹的衣服
24.不利于被告人的证据; 直接证据
25.被告人的个人情况和犯罪后的表现; 犯罪事实是否发生; 构成犯罪事件的各种情节
26.小颖盗窃的事实; 小颖犯罪后的表现; 小颖的年龄
27.有能力履行保证义务; 享有政治权利，人身自由未受到限制; 有固定的住所和收入; 与本案无牵连
28.责令具结悔过，重新交纳保证金; 予以逮捕; 监视居住
29.通缉在案的; 越狱逃跑的; 正在实行犯罪的; 正在被追捕的
30.人民检察院; 被害人; 被害人的法定代理人
31.刑事被告人的法定代理人; 刑事被告人; 对被告人的行为负有赔偿责任的组织
32.甲住院期间的误工费用; 甲住院期间的陪护费用; 甲医治精神恍惚支付的费用; 甲因住院支付的费用
33.留置送达的程序中无须见证人到场; 在找不到收件人，同时也找不到代收人时，才能采用留置送达
34.二审法院发回重审的; 公诉案件改变管辖的; 补充侦查完毕又起诉的
35.该女婴已因溺水而死亡; 郑某的行为系故意; 郑某作案时已满18周岁'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(6)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    # 富文本
    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "答：（1）可对江某采取取得候审措施。因为江某罪行不重，采取取得候审措施后的社会危害性基本不存在。（2）公安机关不同意江某之弟做保证人的做法正确。因为保证人的住址不固定，行踪不稳定，不利于监管嫌疑人。（3）如果江某无法提供别的保证人，他可以通过提供保证金的形式被取保候审。")
    browser.switch_to.default_content()

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.3)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')

    dxAnswer = '''1.一个月
2.被害人委托的人
3.2
4.直接向人民法院起诉
5.公诉人
6.公诉机关
7.认为有犯罪事实需要追究刑事责任
8.控告
9.应当在对犯罪现场进行初步勘验后立即立案
10.将报案材料整理后，移送公安机关，由公安机关采取措施
11.在收到通知书后7日内书面答复检察院
12.甲省检察院可以决定通缉
13.为了进行辨认，必要时见证人可以在场
14.丁也被逮捕，在羁押过程中因急病突发死亡，公安机关未经检察机关批准，直接撤销案件
15.物证检验应当制作笔录，参加检验的侦查人员.鉴定人和见证人均应签名或者盖章
16.检察院对黄某作出附条件不起诉决定、对吴某作出不起诉决定时，可要求他们向赵某赔礼道歉、赔偿损失
17.被害人提出申诉后又撤回的，仍可向法院起诉
18.某乙有权向上一级检察院申诉
19.被告人是否提出反诉
20.法院应在张某起诉之日起15天内作出是否立案的决定'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(6)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''21.犯罪已过追诉时效的; 经特赦令免除刑罚
22.犯罪嫌疑人; 被害人
23.搜查; 鉴定; 勘验、检查
24.不起诉; 撤销案件; 提起公诉
25.写出起诉意见书，送同级人民检察院审查决定; 撤销案件
26.撤销案件; 不起诉; 提起公诉
27.人民检察院自行补充侦查; 人民检察院退回公安机关补充侦查
28.向上一级人民检察院申诉; 直接向人民法院起诉
29.是否有明确的指控犯罪事实; 是否附有证人名单; 是否有主要证据的复印件或照片; 是否附有证据目录
30.应当由A地公安机关以外的侦查机关侦查; 辩护律师因涉嫌伪证罪需追究刑事责任的，应当及时通知其所在的律师事务所或者所属的律师协会
31.危害国家安全犯罪; 恐怖活动犯罪; 重大毒品犯罪; 黑社会性质的组织犯罪
32.对于复杂、疑难案件，期限届满仍有必要继续采取技术侦查措施的，经过有权机关批准，有效期可以延长，但最多不超过两个月; 对于复杂、疑难案件，期限届满仍有必要继续采取技术侦查措施的，经过有权机关批准，有效期可以延长，每次自批准之日起三个月以内有效; 批准技术侦查的决定自签发第二日起三个月内有效; 对于复杂、疑难案件，期限届满仍有必要继续采取技术侦查措施的，经过上一级侦查机关批准，有效期可以延长
33.对采取技术侦查措施获取的与案件无关的材料，必须及时销毁; 采取技术侦查措施获取的材料，只能用于对犯罪的侦查、起诉和审判，不得用于其他用途; 侦查人员对采取技术侦查措施过程中知悉的国家秘密、商业秘密和个人隐私，应当保密
34.王某与某甲约定交货时间，到县城一宾馆内与老板（侦查人员）交易。当王某带甲前往交易时，被侦查人员人赃俱获，此即为控制下交付; 本案中王某的侦查方式属于诱惑侦查，是不可行的; 隐匿身份对农民甲实施侦查，需经过公安机关负责人决定
35.必要的时候，可以由审判人员在庭外对证据进行核实; 如果使用该证据可能危及有关人员的人身安全，人民法院可以采取不暴露有关人员身份的措施; 对乙采用技术侦查措施收集的证据，可以作为证据使用'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.3)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer4(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')

    dxAnswer = '''1.公安机关
2.虐待案件
3.被告人的上诉
4.被害人因受强制.威吓无法告诉的
5.开庭审判
6.合议庭
7.由高级人民法院复核同意后再报请最高人民法院核准
8.撤销案件
9.判决宣告赵某无罪
10.二审法院撤销一审法院事实不清，证据不足的判决
11.市检察分院检察长
12.人民法院对人民检察院的书面纠正意见没有重新组织合议庭进行审理
13.警告制止，如果不听制止，可以强行带出法庭
14.告知张某，应当另行起诉
15.最高人民法院审理一审案件所作的判决和裁定
16.人民检察院应当写出书面理由，将案卷退回公安机关处理
17.认为原判刑罚太重，不同意判处死缓，直接改判有期徒刑15年
18.对王某的取保候审应由国家安全机关执行
19.该人民法院院长
20.人民法院按照审判监督程序审判的案件，应当决定中止原判决.裁定的执行'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(6)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    mulAnswer = '''21.是否附有证据目录; 是否有主要证据的复印件或照片; 是否有明确的指控犯罪事实; 是否附有证人名单
22.辩护人; 诉讼代理人; 被害人
23.检查; 冻结; 查询; 扣押
24.拘留; 罚款; 强行带出法庭; 警告制止
25.需要通知新的证人到庭的; 需调取新的物证的; 需要重新鉴定和勘验的
26.被告人死亡的; 犯罪已过追诉时效期间的
27.案件事实清楚，情节简单.无需侦查; 有明确的被告和原告; 犯罪后果轻微，社会危害性不大
28.自诉人可在判决宣告以前撤回自诉; 被告人可提出反诉; 人民法院对自诉案件可以进行调解
29.简易程序可以变更为第一审普通程序; 审判员一人独任审判; 公诉案件检察人员可以不出庭
30.开庭审理; 调查询问式审理
31.只有被告人上诉的案件; 只有被告人的近亲属上诉的案件
32.第二审人民法院不公开审理的公诉案件; 人民检察院抗诉的案件; 第二审人民法院开庭审理的公诉案件
33.高级人民法院核准的死刑缓期二年执行判决; 终审的判决和裁定; 最高人民法院核准的死刑判决; 已过法定期限没有上诉.抗诉的判决和裁定
34.二审法院可以不开庭审理; 因本案存在抗诉，二审法院对甲和乙都不受上诉不加刑原则的限制; 因上诉和抗诉都不是针对原审事实认定，二审法院对本案不能以事实不清为由撤销原判，发回重审
35.诉讼代理人; 辩护人; 提起公诉的检察院; 当事人'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(6)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    # 富文本
    line = browser.page_source
    frameId = line.split(":36_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":36_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "答:（1）李某可以书面或者口头的形式，直接向二审人民法院提出上诉，也可以通过原审人民法院提出上诉。（2）人民检察院可以提起抗诉。抗诉的程序是：一是抗诉的提出。抗诉的提出是指哪一级别的人民检察院对哪一级别的人民法院已经发生法律效力的判决、裁定，可以向哪一级别的人民法院提出的抗诉。根据我国民事诉讼法的规定，最高人民检察院对各级人民法院已经发生法律效力的判决、裁定，上级人民检察院对下级人民法院已经发生法律效力的判决、裁定，可以提出抗诉；地方各级人民检察院对同级人民法院已发生法律效力的判决、裁定，不得直接提出抗诉，只能提请上级人民检察院提出抗诉。二是抗诉的方式。抗诉的方式是指人民检察院对人民法院的生效裁判提出抗诉采取的方式。人民检察院决定对人民法院的生效裁判提出抗诉的，应当制作抗诉书。抗诉书是人民检察院对人民法院的生效裁判提出抗诉的法律文书，也是人民检察院行使检察监督权引起对抗诉案件再行审理的法律文书。抗诉书中应载明：提出抗诉的人民检察院和接受抗诉的人民法院；抗诉案件的原审法院对案件的编号及其发生法律效力的判决、裁定；抗诉的事实和理由；提出抗诉的时间。有证据的，人民检察院向人民法院提交抗诉书的同时，可以向人民法院提供证据，或者提供证据来源。人民检察院提出抗诉的案件，人民法院应当再审，即只要人民检察院提出抗诉，人民法院就应当直接进行再审，并不需要院长提交审判委员会讨论。（3）二审法院的做法合法。刑诉法第二百二十五条第（一）项规定，原判决认定事实和适用法律正确、量刑适当的，二审法院应当裁定驳回上诉，维持原判；本案中，虽然原审人民法院在认定盗窃数额时与实际不符，少认定2110元，但案件基本事实和适用法律均无错误，故二审法院裁定驳回李某上诉，维持原判是正确的。（4）做法是错误的。依照《刑事诉讼法》第二百四十三条第一款的规定，各级人民法院院长对本院已经发生法律效力的判决和裁定，如果发现在认定事实上或者在适用法律上确有错误，必须提交审判委员会处理。因此，二审法院院长认为此案在认定事实上确有错误，必须提交审判委员会处理。院长本人不能以院长名义撤销本院对此案的裁定，不能自行决定零星组成合议庭审理此案。所以，本案院长的做法显然是错误的。（5）不违反“上诉不加刑”原则。因为刑诉法规定人民检察院提出抗诉的，不受规定的限制，本案中，在检察机关提出抗诉的情况下，二审法院可直接改判加重被告人李某的刑罚，不违反“上诉不加刑”原则。")
    browser.switch_to.default_content()


    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.3)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer5(browser):
    time.sleep(2)
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')

    dxAnswer = '''1.被害人
2.A市中级法院
3.人民法院指派的审判人员指挥
4.先依法裁定减刑，然后对所犯罪另行审判
5.作出生劳判决的法院
6.某甲
7.本人财产为
8.附带民事诉讼原告人和检察院都可以申请法院采取保全措施
9.省检察院对该案向省高院提出抗诉
10.由市中级人民法院院长提交本院审判委员会处理
11.由再审法院裁定中止执行原判决
12.中止审理
13.人民法院负责无罪、免除处罚、罚金、没收财产及死刑立即执行判决的执行
14.裁定维持一审判决
15.由省高级人民法院院长提交本院审判委员会处理
16.省检察院对该案向省高级人民法院提出抗诉
17.接受抗诉的人民法院应当进行审查以决定是否重新审理
18.区人民检察院
19.法院审理结束后，为了刘某的健康成长，决定不公开宣告判决
20.某甲不符合法定的应当指定的情形，人民法院可不为其指定辩护人'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(6)

    mulAnswer = '''21.有新的证据证明原判决、裁定认定的事实确有错误，可能影响定罪量刑的; 据以定罪量刑的证据不确实、不充分，依法应当予以排除的; 审判人员在审理该案件时有贪污受贿、枉法裁判行为的; 违反法律规定的诉讼程序，可能影响公正审判的; 原判决、裁定适用法律确有错误的'''
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿
    elements1 = elements1[:6]
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 5)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
        dxindex += 1

    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿
    elements1 = elements1[5:]

    mulAnswer = '''22.按照第二审程序审理的案件，认为必须判处被告人死刑立即执行的，直接改判后，应当报请最高人民法院核准; 撤销原判，用判决予以改判
23.王某由作出一审判决的法院执行; 核准死刑立即执行的机关是最高人民法院
24.判决书认定的年龄错误，实际年龄未满18周岁; 提供一重大银行抢劫案线索，经查证属实; 发现关键定罪证据可能是刑讯逼供所得; 罪犯正在怀孕
25.被判处拘役的罪犯李某患有严重疾病需要保外就医; 被判处5年有期徒刑的妇女赵某，服刑时其宁正值哺乳期; 被判处无期徒刑的女罪犯张某，被发现服则时怀有身孕
26.不符合暂予监外执行条件的罪犯通过贿赂等非法手段被暂予监外执行的; 严重违反有关暂予监外执行监督管理规定的; 暂予监外执行的情形消失后，罪犯刑期未满的
27.被判处拘役的罪犯李某患有严重疾病需要保外就医; 被判处无期徒刑的女罪犯张某，被发现服刑时怀有身孕; 被判处有期徒刑10年的罪犯王某，在狱中自杀未遂，致使生活不能自理
28.对于被判处有期徒刑的罪犯，剩余刑期在六个月以下的，由看守所代为执行; 第一审人民法院判决被告人免除刑事处罚的，如果被告人在押，在判决生效后应当立即释放
29.二者的抗诉对象均是确有错误的判决、裁定; 二者均由抗诉的检察院向同级法院提起; 二者均可以由地方各级检察院提起; 二者均可以由各级检察院提起
30.最高人民检察院; 该省高级人民法院
31.被害人温某; 王某的父亲; 王某的成年胞兄
32.公安机关对羁押的未成年人应当与羁押的成年人分别看管; 16岁以上不满18岁未成年人犯罪的案件，一般不公开审理; 未成年人刑事案件，是指被告人实施被指控的犯罪时已满14周岁不满18周岁的案件
33.最高人民检察院; 省人民检察院
34.甲市中级人民法院有权决定提审; 省高级人民法院有权指令区人民法院再审
35.在押的未成年犯罪嫌疑人有认罪、悔罪表现的，检察人员可以安排其与法定代理人、近亲属等会见、通话; 应当听取辩护人的意见; 应当听取未成年被害人的法定代理人的意见; 应当听取未成年被害人的意见'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".", "; ")
    for value in mapmulAnswer:
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex, 4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.3)
        dxindex += 1

    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.3)
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


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=465688'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=465689'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=465690'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=465691'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=465692'

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
