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
    for ele in elements:#or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text:
            return ele
def getAnswerElementEqualsBefore(elements, neirong, i, meidaotiyouduoshaogexuanxiang,y):
    elements = elements[i * meidaotiyouduoshaogexuanxiang+y:(i + 1) * meidaotiyouduoshaogexuanxiang+y]
    for ele in elements:#or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text:
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
    result = []
    split = answer.split("\n")
    for i in split:
        if len(i)<3:
            continue
        result.append(i.strip().split(reg)[1])
    return result
def panduanAutoAnswerFix(answer, reg):
    result = []
    split = answer.split("\n")
    for i in split:
        i = i.split(reg)[0]
        result.append(i.strip()[-1])
    return result

def duoxuanAutoAnswerFix(answer, reg, reg2,reg3):
    # map={}
    # split = answer.split("\n")
    # for i in split:
    #     map[i.split(reg)[0].strip()] = i.split(reg)[-1].split(reg2)
    # return map
    # 2019年11月18日11:44:49惊人发现,Python的map在mac下有序,在win下无序
    listList = []
    split = answer.split("\n")
    for i in split:
        if len(i)<6 or "窗体" in i:
            continue
        listList.append(i.split(reg)[-1].split(reg2)[0].split(reg3))
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
    time.sleep(0.3)


# start to answer.
def getJudgeAnswers(pdAnswer,reg):
    ans=[]
    for pd  in pdAnswer.split("\n"):
        ans.append(pd.split(reg)[0][-1])
    return ans

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

    # 20判断
    pdAnswer = '''在霍桑试验的基础上,梅奥于1933年出版了《工业文明中的人的问题》一书,系统地阐述了与古典管理理论截然不同的一些观点（对）。
阿吉里斯在《个性与组织》一书中提出了“不成熟—成熟理论”（对）。
斯蒂格利茨由于在决策理论研究方面的贡献而荣获1978年诺贝尔经济学奖（错）。
马斯洛在其代表性著作《人类动机的理论》和《激励与个人》中,提出了著名的公平理论（错）。
美国学者巴纳德在1938年出版的《经理人员的职能》这本书中,系统地提出了动态平衡组织理论（对）。
社会系统组织理论的创始者为美国著名的社会学家罗森茨韦克（对）。
邓肯将组织环境分为内部环境和外部环境（对）。
.卡斯特和罗森茨韦克将影响一切组织的一般环境特征划分为文化特征、技术特征、教育特征、政治特征、法制特征、自然资源特征、人口特征、社会特征、经济特征等几个方面（对）。
组织界限以内与组织的个体决策行为直接相关的自然和社会因素被称为组织的内部环境（对）。
组织界限之外与组织内个体决策直接相关的自然和社会因素被称为组织的外部环境（对）。
组织”一词,源自希腊文,1873年,哲学家斯宾塞用“组织”来指涉“已经组合的系统或社会”（对）。
与个别行政组织的决策转换过程相关联的更具体的力量被称为行政组织的工作环境（错）。
以明文规定的形式确立下来,成员具有正式分工关系的组织为非正式组织（错）。
以镇压、暴力等控制手段作为控制和管理下属的主要方式,此种类型的组织为规范性组织（错）。
以组织的参与者或成员为主要的受惠对象,组织的目的在于维护及促进组织成员所追求的利益,此种类型的组织为互利性组织（对）。
规范地讲,行政组织是追求行政权力的组织（对）。
韦伯是科学管理运动的先驱者,被誉为“科学管理之父”（错）。
1911年,泰勒发表了《科学管理原理》一书,掀起了一场科学管理的革命（对）。
行政管理学派的代表人物法约尔,被誉为“管理理论之父”（对）。
德国著名的社会学家韦伯在《高级管理人员的职能》一书中,提出了理想型官僚组织理论（错）。'''
    pdAnswer = getJudgeAnswers(pdAnswer,"）。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    mulAnswer = '''美国行为科学家赫茨伯格在其《工作的推力》和《工作与人性》等著作中,提出影响人的积极性的因素主要有（保健因素、激励因素）。
西蒙指出,决策有两种极端的类型_（程序化决策、非程序化决策）。
里格斯指出,“棱柱型社会”具有以下三个基本特征_（重叠性、形式主义、异质性）。
里格斯在他创立的“棱柱模式理论”中,将社会形态划分_（棱柱社会、信息社会、工业社会）。
巴纳德认为,组织不论其级别高低和规模大小,都包含三个基本要素（共同的目标、协作的意愿、信息的联系）。
邓肯将组织环境分为（外部环境、内部环境）。
邓肯从组织环境的___两个维度对影响组织的环境因素进行了深入的分析（静态与动态、简单与复杂）。
依据学者们的研究,组织的环境分析过程主要包括____等基本阶段（全选）。
伯恩斯和斯塔克将组织结构划分为（有机式组织结构、机械式组织结构）。
行政组织环境的基本特点为__（全选）。
窗体顶端
学者们从不同的角度和方法去透视组织，给予不同的定义，目前学界对组织界定的取向，主要有以下几种（全选）。
窗体底端
依据邓肯的环境模式理论，从简单与复杂、静态与动态两个维度，组织存在的环境状态分别是（全选）。
按组织内部是否有正式的分工关系，人们把组织分为（正式组织、非正式组织）。
窗体底端
窗体顶端
美国学者艾桑尼以组织中人员对上级服从程度、上级对下级权力运用的关系，将组织划分为（规范性组织、强制性组织、功利性组织）。
窗体底端
窗体顶端
美国著名社会学家、交换学派的代表布劳及史考特，根据组织目标和受益者的关系，把组织划分为（全选）。
窗体底端
 窗体顶端
从系统论的角度来看，任何一种社会组织大体都发挥三种功能（“转换”功能、“聚合”功能）。
窗体底端
窗体顶端
窗体顶端
组织是一个纵横交错的权责体系，构成组织权责体系的三大要素为（职权、职责）。
世界银行在其1997年的《世界发展报告》中指出，以下几项基础性的任务处于每个政府使命的核心地位，这些使命包括（保持非扭曲的政策环境、保护环境、投资于基本的社会服务与基础设施）。
古典组织理论的主要代表人物有（韦伯、法约尔、泰勒）。
韦伯对行政组织理论的建构是从权力分析开始的，认为存在着下列纯粹形态的合法权力，它们是（超凡的权力、传统的权力、理性--法律的权力）。'''
    dxindex = 0
    howManyLabelBefore=40#前面有二十道判断,所以前面共40个label
    listmulAnswer = duoxuanAutoAnswerFix(mulAnswer, "（", "）","、")
    for value in listmulAnswer:
        for v in value:
            if "全选"==v.strip():
                #把当前题的所有label都选上
                for i in range(4):
                    elements1[dxindex*4+howManyLabelBefore+i].find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
            else:
                anEle = getAnswerElementEqualsBefore(elements1, v.strip(), dxindex, 4,howManyLabelBefore)  # 找到指定的那个label选项
                if anEle is not None:
                    anEle.find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
        dxindex += 1



    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.3)
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
    time.sleep(4)  # 保证富文本框加载完毕

    # 20判断
    pdAnswer = '''我国地方各级政府是各级国家权力机关的执行机关（对）。
省级政府每届任期4年（错）。
中国当前的城市，在行政级别上分为4个层次（对）。
市级政府对上一级国家行政机关负责并报告工作，并接受国务院的统一领导（对）。
民族自治地方分为自治区、自治县和民族乡三级（错）。
在影响组织的各种因素中，信息的因素是最为重要的（对）。
人的行为首先是在一一定的刺激下产生内在的愿望与冲动，即产生需要（对）。
赫茨伯格的双因素包括保健因素和激励因素（对）。
期望理论中的激励力量取决于目标价值和期望概率的综合作用（对）。
决策是领导者的最基本职责（对）。
组织结构垂直分化的结果与表现形式为组织结构的层级化（对）。
领导者通过及时调整各种关系，使各项工作、各个部门、各种人员之间能够和谐地配合，顺利完成组织任务，达成组织目标，这是领导者在履行其监督职能（错）。
行政组织结构横向分化的结果与表现形式为组织结构的分部化（对）。
领导机关或管理人员能够直接有效地管理和控制下属人员或单位的数目称之为管理级别（错）。
在单位和人数不变的情况下，管理层次和管理幅度的关系为正比例关系（错）。
在一个组织结构体系中，为完成定的任务或使命，设置不同的上下层级机关或部门，使其在各自职权范围内独立自主处理事务，不受上级机关干涉的组织结构体系为分权制（对）。
在一一个组织结构体系中，上级机关 或单位完全掌握组织的决策权和控制权，下级或派出机关处理事务须完全秉承上级或中枢机关的意志行事的组织结构体系为集权制（对）。
国务院是由全国人大组织产生（错）。
国务院是最高国家权力机关（错）。
秦朝的郡县制奠定了以中央集权为特征的行政建制（对）。'''
    pdAnswer = getJudgeAnswers(pdAnswer,"）。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    mulAnswer = '''21.社会组织的结构与其他生物的和机械的系统的结构都具有如下共同的特点（全选）。
22.组织结构的构成要素可划分为___两大类（组织的“显结构”；组织的“潜结构”）。
23.组织结构的“潜结构”的构成要素包括（全选）。
24.组织结构分化的方式和途径为（全选）。
25.促进组织活动一体化的手段和途径主要有（全选）。
26.组织设计中应注意组织设计的程序问题（归纳设计；演绎设计；）。
27.国务院是最高国家行政机关，它（由国家最高权力机关产生；在国家行政系统中处于最高地位）。
28.我国省级政府包括（全选）。
29.乡级政府行使的职权有（行政管理权；行政执行权；行政保护权）。
30.我国特别行政区享有（独立的司法权和终审权；1；立法权；独立的地方财政权）。 
31组织管理心理主要由组成（个体心理；组织心理；群体心理）。
32.人的行为机制主要包括（全选）。
33.下列因素中属于赫茨伯格双因素理论中的激励因素的是（工作富有成就；工作本身的重要性）。
34.推行目标激励理论的主要困难是（目标的公平合理；目标量化；目标难度的确定）。
35.群体发展大致经历的阶段有（全选）。
36.群体意识主要包括（群体归属意识；群体促进意识；群体认同意识）。
37.行政组织领导的特点是（全选）。
38.权力性影响力主要源于（全选）。
39.非权力性影响力主要源于（全选）。
40.勒温将领导者的作风分为___等类型（专制；民主V；放任）。'''
    dxindex = 0
    howManyLabelBefore=40#前面有二十道判断,所以前面共40个label
    listmulAnswer = duoxuanAutoAnswerFix(mulAnswer, "（", "）","；")
    for value in listmulAnswer:
        for v in value:
            if "全选"==v.strip():
                #把当前题的所有label都选上
                for i in range(4):
                    elements1[dxindex*4+howManyLabelBefore+i].find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
            else:
                anEle = getAnswerElementEqualsBefore(elements1, v.strip(), dxindex, 4,howManyLabelBefore)  # 找到指定的那个label选项
                if anEle is not None:
                    anEle.find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
        dxindex += 1



    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.3)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    time.sleep(2)
    browser.find_element_by_id("id_subject").send_keys("广场舞引发的矛盾")
    time.sleep(6)
    browser.switch_to.frame("id_message_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "在公共利益面前，“小团体”的自由必须受到约束。城市管理应该改变相关法律法规缺失、执行者缺位的现状，加强对群众性娱乐活动的管理和引导，帮助参与者提高文明素质和公德意识，为公众创造安宁和谐的城市生活环境。目前我国大多数城市对居民区附近的广场舞活动，没有针对性的管理措施。而且，即使少数地区出台了管理办法，也面临着执行难困境。噪声处罚需要专业人员到现场监测并出具证据，管理广场舞执法成本高，落实难。同时，对广场舞的管理还面临管理者缺位问题，小区物业往往左右为难，城管人员又无此权限。广场舞噪声扰民问题，实际上是一个是否尊重他人权益及公共利益的问题。长期的噪音干扰，无疑侵犯了一些小区居民的休息权。这看似是个不大的问题，但如果居民的合法权益长期被忽视、被侵犯，最后的后果就可能很严重。武汉发生了“泼粪”事件，无独有偶，前不久北京也发生了一起由广场舞噪音引发的严重事件。北京市昌平检察院以涉嫌非法持有枪支罪批捕一名男子，该男子因广场舞噪音过大与邻居发生争执，并拿出私藏猎枪朝天鸣枪，随后又将三条藏獒放出来冲进跳舞人群，所幸未造成人员伤亡。这起事件具有犯罪的恶性，与武汉广场舞纠纷的性质不可同日而语，但两者的诱因却都是广场舞噪音，须引起有关部门和广大居民的重视。应当认识到，一部分居民每天欢乐的几个小时，不应同时成为其他人的煎熬时间。发生在居民区的生活噪音污染，关系到居民生活的质量，关系到邻里关系的和谐，绝不是小问题。广场舞伴随城市发展而来，是文化现象，也是社会现象。广场舞曾经是精神文明建设的一个成果，是社会和谐的反映，但随着城市人口密度不断加大，以及公众对居住环境要求的提高，广场舞噪声已开始对居民生活和社区秩序造成较大影响。在公共利益面前，“小团体”的自由必须受到约束。城市管理应该改变相关法律法规缺失、执行者缺位的现状，加强对群众性娱乐活动的管理和引导，帮助参与者提高文明素质和公德意识，为公众创造安宁和谐的城市生活环境。")
    browser.switch_to.default_content()
    browser.find_element_by_id("id_submitbutton").click()
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

    # 20判断
    pdAnswer = '''行政组织决策的目的是为了实现社会的共同利益（对）。
行政组织决策是以行政权力为后盾（对）。
风险型决策的决策后果无法预测（错）。
确定目标是行政组织进行决策的起点（错）。
中枢系统是行政组织决策的中心（对）。
美国政治学家伊斯顿被认为是决策理论研究的开创者（错）。
在决策理论研究领域，杜鲁门提出了团体决策模型（对）。
现代观点认为，冲突既具有建设性又具有破坏性（对）。
组织中最佳的冲突状态是没有冲突（错）。
解决冲突的基本策略中具有“治本”性的是正视策略（对）。
合作意向都很高，宁可牺牲自身利益而使对方达到目的的冲突处理模式为协作型（错）。
通过组织明文规定的原则、渠道进行的信息传递和交流，是一-种正式沟通（对）。
信息的发讯者和受讯者以协商、会谈、讨论的方式进行信息的交流与意见反馈，直到双方共同了解为止，这种沟通形式为双向沟通（对）。
组织系统中处于相同层次的人、群体、职能部门之间进行的信息传递和交流为平行沟通（对）。
在组织管理中，书面沟通方式要优于口头沟通（错）。
作报告、发指示、下命令等属于单向沟通（对）。
20世纪90年代初陈国权开始研究组织学习和学习型组织，并提出了组织学习系统理论(OLST)（对）。
行政组织学习是一一种全员学习（错）。
知识的主要构成要素包括经验、事实、判断以及经验法则（对）。
行政组织学习不是组织内部成员个人学习的简单相加，而是一个社会过程（对）。'''
    pdAnswer = getJudgeAnswers(pdAnswer,"）。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    mulAnswer = '''根据决策所具有的条件的可靠程度的不同，决策可分为（不确定型决策；风险型决策；确定型决策）。
正确的决策目标应该具备的条件是（ 定量化；要明确责任；有一定的时间限制）。
西蒙的决策过程包括（全选）。 
冲突的特性有（客观性；主观性；程度性）。 
符合现代冲突观点的是（冲突本身没有好坏之分；有些冲突对组织具有破坏性；有些冲突对组织具有建设性）。
根据冲突发生的方向，可将冲突分为（横向冲突；直线/职能冲突；纵向冲突）。 
回避策略中，解决冲突的方法包括（限制；忽视；分离）。  
减少冲突的策略主要有（全选）。 
从组织沟通的-般模式和组成要素来看，组织沟通具有以下几个特点（全选）。
以组织结构及其运行程序为依据和标准，组织信息沟通的形式和类型可划分为以下几种（上行沟通；下 行沟通；平行沟通）。 
根据沟通是否需要第三者中介传递，我们可将沟通划分为以下两种类型（间接沟通；直接沟通）。
信息传递的过程中，会形成和出现不同的沟通结构形式，这便是沟通的网络，-般来讲，组织沟通网络可分为两大类（非正式沟通网络；正式沟通网络）。
戴维斯在《管理沟通与小道消息》一文中指出，口头传播方式的非正式信息交流渠道或形式主要有（全选）。
在组织沟通中，由信息传递的媒介形式引起的障碍主要有（语言障碍；沟通方式不当引起的障碍）。
组织沟通中存在的客观性障碍主要有（信息过量引起的障碍；空间距离所引起的障碍；组织机构引起的障碍）。 
组织学习的内容包括三个方面的改变，分别是（组织体系的改变；组织成员认知的改变；行为的改变）。
行政组织学习的类型可分为（三环学习；双环学；单环学习）。 
行政组织学习的途径包括（全选）。
行政组织学习途径之一的试验，可分为（示范性试验；持续性试验）。
行政组织学习过程中领导人应该作为（教师；公仆；设计师）。'''
    dxindex = 0
    howManyLabelBefore=40#前面有二十道判断,所以前面共40个label
    listmulAnswer = duoxuanAutoAnswerFix(mulAnswer, "（", "）","；")
    for value in listmulAnswer:
        for v in value:
            if "全选"==v.strip():
                #把当前题的所有label都选上
                for i in range(4):
                    elements1[dxindex*4+howManyLabelBefore+i].find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
            else:
                anEle = getAnswerElementEqualsBefore(elements1, v.strip(), dxindex, 4,howManyLabelBefore)  # 找到指定的那个label选项
                if anEle is not None:
                    anEle.find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
        dxindex += 1



    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.3)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer5(browser):
    canTakeWrongNum = 0
    #单多选在同一页混的时候,标记下单选题的数量
    danxuanLength=9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0
    time.sleep(4)  # 保证富文本框加载完毕

    # 20判断
    pdAnswer = '''根据行政组织文化产生的时间，行政组织文化可以分为传统行政组织文化和当代行政组织文化（对）。
行政组织文化具有多种功能，它能把组织成员个人目标与组织目标有机结合起来，引导组织成员的行为，我们把这种功能称为控制功能（错）。
行政组织文化相比于正式的组织规章制度的控制作用，它具有软约束性的特性（对）。
行政组织文化是一-种群体文化，是一一种无形的管理方式（对）。
行政组织绩效就是指的行政组织活动的成果（错）。
经济性指标一般指行政组织投入到管理中的资源，其关心的是行政组织的投入（对）。
效果通常是指公共服务符合政策目标的程度，其关心的是手段（对）。
效率就是指投入与产出之间的比例，力求以最少的投入获得最大的产出，其关心的是手段问题（对）。
组织变革不是一一个持续循环与发展的过程，因为要考虑到组织的稳定（错）。
组织发展起源于20世纪50年代初的调查反馈方法和实验室培训运动。它的先驱是法国心理学家烈文（对）。
1957年麦格雷戈应邀到联合碳化公司与公司人事部门联合成立顾问小组，把实验室训练的术系统地在公司使用。这个小组后被称之为“T训练小组”（错）。
作为一套极有系统的组织发展方案，格道式发展模式的目的在于使组织达到一一种最佳状态。此模式创立者为布菜克和默顿（对）。
系统变革模式认为，组织是一个系统，是由技术、结构、人员和任务四个因素构成，任何一一个因素的变化都会牵动和引起系统的变化。系统变革模式的创始人为利维特（对）。
美国心理学家埃德加●薛恩在其《组织心理学》一书中提出了系统变革模式（错）。
罗宾●斯特克兹认为，组织变革的方式取决于组织成员的技术能力和人际关系能力的组合，提出了渐进式变革模式（错）。
管理学大师德鲁克在《后资本主义社会》一书中指出:“世界 上没有贫穷的国家，只有无知的国家”（对）。
知识经济与传统经济相比，知识成为组织根本的生产要素（对）。
组织理论家卡斯特和罗森茨韦克认为，未来的组织将更趋向于动态和灵活（对）。
战略管理的核心是问题管理（错）。
随着信息技术的发展，将信息科技运用于行政组织的管理，建立“节约型政府”已经成为各国的一个普遍趋势（错）。'''
    pdAnswer = getJudgeAnswers(pdAnswer,"）。")
    dxindex = 0
    for pd in pdAnswer:
        anEle = getAnswerElementEquals(elements1, pd, dxindex, 2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.3)
        dxindex += 1

    mulAnswer = '''根据其在行政组织中所占有的地位，行政组织文化可以分为（ 主文化；亚文化）。
我国行政组织文化正在向方向迈进（全选）。
行政组织绩效的外延，除了内部的管理绩效，主要还包括（经济绩效；社会绩效；政治绩效）。
一个有效的绩效管理系统必须具备以下构成要件（全选）。
绩效指标包括的要素有（考评标度；考评标志；考评要素）。 
在选择绩效评估指标时应遵循的原则是（全选）。
组织变革并非凭空产生，它是有原因的。组织变革的动因是多种多样的，我们可以把组织变革的动因分为两大类:（内部环境因素；外部环境因素）。 
对组织管理和变革发生影响的外部环境包括（般环境因素；特殊工作环境）。 
美国斯坦福大学管理心理学教授利维特认为，组织是一个系统，是由相互影响、相互作用的因素构成的动态系统，这些因素有（全选）。
哈佛大学教授格雷纳967年在《组织变革模式》一书中，提出了一一种按权力来划分的组织变革模式。他认为，一般组织的权力分配情况可分成三种（分权；独权；授权）。
罗宾●斯特克兹于972年提出情境变革模式。他认为，组织变革的方式取决于组织成员的技术能力和人际关系能力的组合。根据这种不同组合，他提出了以下几种不同的变革型态（全选）。
组织变革要取得预期的成效，必须遵循科学的、合理的变革步骤或程序。美国学者凯利认为，组织变革需经过以下步骤或程序（诊断；执行；评估）。 
心理学家勒温(K. Lewin)从人的心理机制的变革角度，认为人的心理和行为的变革大致要经历以下几个阶段:（“ 改变；“解冻；“再冻结”）。
根据现代心理学和行为科学的研究，组织变革阻力产生的原因为（全选）。
以资料为基础的组织发展技术包括（职位期望技术；调查反馈法）。
组织中的工作和绩效，都要通过人的行为来完成。以行为为中心的组织发展技术主要有以下几种（全选）。
工作再设计就是通过对工作进行重新调整和再设计，使工作更有趣并富有挑战性，以此增强员工的工作满意度，激发员工的工作热情，提高组织工作的效率。工作再设计的途径和方案为:（工作扩大化；工作轮换；工作丰富化）。 
由于团队建设的内容和要求不同，故可以通过不同的方式来实现。比较常用的团队建设的方式或模式有（全选）。
组织诊断是组织变革的重要步骤和必要环节。组织诊断一般着眼于以下几个层面的问题（全选）。
知识管理的主要活动包括（全选）。'''
    dxindex = 0
    howManyLabelBefore=40#前面有二十道判断,所以前面共40个label
    listmulAnswer = duoxuanAutoAnswerFix(mulAnswer, "（", "）","；")
    for value in listmulAnswer:
        for v in value:
            if "全选"==v.strip():
                #把当前题的所有label都选上
                for i in range(4):
                    elements1[dxindex*4+howManyLabelBefore+i].find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
            else:
                anEle = getAnswerElementEqualsBefore(elements1, v.strip(), dxindex, 4,howManyLabelBefore)  # 找到指定的那个label选项
                if anEle is not None:
                    anEle.find_element_by_xpath("./../input[last()]").click()
                    time.sleep(0.3)
        dxindex += 1



    # end answer
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.3)
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
            time.sleep(0.3)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.3)

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
                time.sleep(0.3)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)

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
    time.sleep(0.3)
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
            time.sleep(0.3)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.3)

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
                time.sleep(0.3)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)

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
    time.sleep(0.3)
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
            time.sleep(0.3)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.3)

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
                time.sleep(0.3)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)

    pdAnswer = '''从实质上看，直接工资的工资率差异属于价格差异。（对）
    全面成本控制原则就是要求进行全过程控制。（错）
    缺货成本是简单条件下的经济批量控制必须考虑的相关成本之一。（错）
    在标准成本控制系统中，成本超支差应记入成本差异账户的贷方。（错）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 3, 2, 0)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 4, 2, 1)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.3)
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
            time.sleep(0.3)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.3)

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
                time.sleep(0.3)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)

    pdAnswer = '''利润或投资中心之间相互提供产品或劳务，最好以市场价格作为内部转移价格。（对）
剩余收益指标的优点是可以使投资中心的业绩评价与企业目标协调一致。（对）
一般来讲，成本中心之间相互提供产品或劳务，最好以“实际成本”作为内部转移价格。（错）
因利润中心实际发生的利润数大于预算数而形成的差异是不利差异。（错）
责任会计制度的最大优点是可以精确计算产品成本。（对）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 3, 2, 0)
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 4, 2, 1)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(0.3)
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
            time.sleep(0.3)
    # if (judgeQueTitle(elements1p, "生产需要甲材料，年需要量为100千克，如果自制，单位变动成本20")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "保本点升高，利润减少", 1)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input").click()
    #     time.sleep(0.3)

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
                time.sleep(0.3)

    # if (judgeQueTitle(elements1p, "从保本图得知（")):
    #     rightAnswer = getAnswerElementEquals4(elements1, "在其他因素不变的情况，保本点越低，盈利面积越大",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)
    #     rightAnswer = getAnswerElementEquals4(elements1, "实际销售量超过保本点销售量部分即是安全边际",2)
    #     rightAnswer.find_element_by_xpath("./..").find_element_by_xpath("./input[last()]").click()
    #     time.sleep(0.3)

    pdAnswer = '''在作业成本法下，成本动因是导致成本发生的诱因，是成本分配的依据。（对）
经济增加值与会计利润的主要区别在于会计利润扣除债务利息，而经济增加值扣除了股权资本费用，而不不扣除债务利息。（错）'''
    pdUtil5(pdAutoAnswer(pdAnswer, []), elements1p, ratios, 2, 1, 0)

    # end answer
    browser.find_element_by_xpath('//input[@type="submit"]').click()
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
    time.sleep(2)
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
    time.sleep(1.5)


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=469745'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=469746'
xingkao3 = 'http://hubei.ouchn.cn/mod/forum/view.php?id=518134'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=469747'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=469748'

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
        if readyToTestForum(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
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
