#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from selenium import webdriver
import os



studyName = os.path.basename(__file__).split('.')[0]


# 其中一张试卷全部为富文本提交
def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele


def getAnswerElementEquals(elements, neirong, key,i, meidaotiyouduoshaogexuanxiang):
    for ele in elements:
        _key = ele.text.replace(' ', '')
        _key = _key.replace(' ', '')
        if key in _key:
            return ele
    return None

# 单选和多选在一页
def getAnswerElementEqualsdanxuanduoxuaninOnePage(elements, neirong, i, meidaotiyouduoshaogexuanxiang,
                                                  danxuanLabelLength):
    elements = elements[danxuanLabelLength + i * meidaotiyouduoshaogexuanxiang:(
                                                                                       i + 1) * meidaotiyouduoshaogexuanxiang + danxuanLabelLength]
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
        i = i.split("题目：")[1]
        result[i.strip().split(reg)[0].strip()] = i.strip().split(reg)[1].strip()
    return result

#111
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
#20道填空,30道单多选混搭
def getAnswerElementEqualsDanDuoXuan(elements, neirong, key,i, meidaotiyouduoshaogexuanxiang):
    for ele in elements:
        if key in ele.text.replace(' ',''):
            return ele
    return None


def getDanxuanAnswerRatio(value, anEle):
    _ratios = anEle.find_elements_by_xpath("./..//label")
    for r in _ratios:
        if value in r.text:
            return r.find_element_by_xpath('./../input[last()]')


def getDuoxuanAnswerRatio(value, anEle):
    rightRatios = []
    _ratios = anEle.find_elements_by_xpath("./..//label")
    for v in value.split("; "):
        for r in _ratios:
            if v in r.text:
                rightRatios.append(r.find_element_by_xpath('./../input[last()]'))
                break
    return rightRatios

def writeAnswer1(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    dxindex = 0

    # 5单
    dxAnswer = '''题目：即良好的治理，它是治理所应追求的目标。	答案：善治
题目：是奴隶制和封建制国家的典型政体形式。	答案：专制君主制
题目：是政治发展实现其他目标的前提。	答案：政治稳定
题目：被认为是近代西方政治科学的奠基人。	答案：马基雅维利
题目：指的是根据宪法、法律的规定公民享有参与公共社会生活的权利。	答案：公民权利
题目：和全能主义国家被视为中国国家与社会关系的基本模式。	答案：一元主义
题目：是指人们根据其政治正义观念来判定的政治秩序的合理性，其核心观念是人们对政治合作的理解。	答案：政治合法性
题目：主要是通过宪法和法律，来实现民主政治的政治形态或政治过程。	答案：宪政
题目：理论是现代民主的主流理论，也是现代通行的民主宪政制度的理论基础。	答案：代议制民主
题目：是监督的本质之所在。	答案：制约权力
题目：是全球化背景下的一种混合的政治主张和意识形态，或者更准确地说，它是一个政治口号。	答案：第三条道路
题目：而理性地妥协是良好社会中公民所应当具备的精神。	答案：宽容
题目：是政治共同体内全体成员共同利益的统称，它是全体社会成员在一定社会基础之上所形成的总体意志和要求的表达，是个人利益和团体利益上升到全社会范围内的利益意志的表现。答案：公共利益
题目：制度是近现代民主政治发展的产物，它强调政治权力的获得以及政治权力的运作必须遵从人们的政治正义观念。	答案：宪政
题目：建设是实现当代政治文明的基本路径。	答案：宪政
题目：是实现当代政治文明的基本路径。	答案：宪政建设
题目：是指一国政治体系的连续性和有序性，它包括国家政权体系的稳定、权力结构的稳定、政治过程的有序状态。	答案：政治稳定
题目：政治文化往往与独裁政治统治相伴随。	答案：顺从型
题目：方案政治设计的核心是寻求一个清官明君式的好人统治，这是“人治”社会的政治设计思路。	答案：理想主义
题目：就是坚信社会科学应该建立在可观察的人类行为基础之上、并只能就可量化的数据展开研究的观点。	答案：行为主义
题目：是一国国民长期形成的相对稳定的对于生活其中的政治体系和所承担政治角色的认知、情感和态度，它与政府、政治组织等制度性结构相对应，成为政治体系的主观要素。	答案：政治文化
题目：是指社会中人们依据基本的政治共识与法律制度展开政治实践的一种状态。	答案：政治秩序
题目：是自由主义的核心原则。	答案：个人主义
题目：是政治的核心，一切政治活动，都是围绕着这一核心展开和进行的。	答案：政治权力
题目：意味着两个方面的进展：建立现代民主制度，明确公民自由权利，并从政治、经济、法律、社会等多重角度，为之设立保护屏障。	答案：民主化
题目：与政治不分是儒家思想的特色。	答案：伦理
题目：原则主要是资本主义国家政府组织机构的设置原则。	答案：分权制衡
题目：19世纪，由于的发展、教育的普及、社会等级观念的淡化以及公民选举权的扩大，民主得到了真正开发的机会，从而在欧美发达国家实现了从理论向制度的转化。	答案：市场经济
题目：柏拉图在《理想国》一书中明确指出，政治的本质在于，一个“理想国”具有智慧、勇敢、节制和正义四种美德。	答案：公正
题目：从社会政治发展史来看，政府组织机构的设置原则主要有三类，即集权原则、分权制衡原则和。	答案：议行合一原则
题目：从政治参与的主体来看，政治参与是的政治行为。	答案：普通公民
题目：从中国的历史演变来看，与的高度一体化以及国家权力至高无上是中国政治结构的主要特点。	答案：国家社会
题目：道德政治观或伦理政治观认为政治是一种追求，是一种规范性的道德。	答案：社会价值
题目：道家的政治学说以“法自然”为思想核心，在统治手法上强调。	答案：无为而治
题目：法国启蒙思想家卢梭在“社会契约论”的基础上，进一步引出学说。	答案：人民主权
题目：封建地主阶级在进行政治统治时，在统治形式上采取的中央集权制。	答案：君主专制
题目：根据思想，可以通过对国家权力的功能划分，在分别执行国家各种权力的各个国家机关之间，建立以权力制约权力的监督制约机制。	答案：分权制衡
题目：根据马克思的理解，指的是统治阶级的思想观念。	答案：意识形态
题目：公共权力的来源和基础是。	答案：公共利益
题目：公共权力具有和至高无上性，公民权利具有神圣不可侵犯性。	答案：权威性
题目：古代社会治理的核心理念是。	答案：统治
题目：国家的三要素说，认为具有、土地、主权者即为国家。	答案：人民
题目：国家结构形式主要可以分为和复合制。	答案：单一制
题目：建设社会主义的基础就是党的领导、人民当家作主和依法治国的统一性，而宪政就是实现这三者统一的基本路径。	答案：政治文明
题目：经验事实表明，的滥用是社会动荡的根源。	答案：权力
题目：具有现代化和的政治领导人及执政党的存在，对于民主的和平转变具有重要意义。	答案：民主意识
题目：马克思主义的经济分析方法内含着唯物辩证法的思想，它将社会划分为经济基础、上层建筑和三大结构。	答案：意识形态
题目：马克思主义认为，问题是全部政治的基本问题，根本问题。	答案：国家政权
题目：马克斯·韦伯根据政治权威的建立和运行依据，把国家划分为国家、个人魅力型权威国家和法理型权威国家。	答案：传统型权威
题目：美国政治舞台一直由和共和党所把持。	答案：民主党
题目：孟德斯鸠认为一切有权力的人都容易，这是万古不易的一条经验。	答案：滥用权力
题目：民主的基础与前提是倡导和个人独立。	答案：宽容精神
题目：墨子的政治学说以、“非攻”为中心，主张以缓和社会矛盾来维持统治。	答案：兼爱
题目：权力制约原则在资本主义国家的宪法中主要表现为。	答案：分权原则
题目：儒家和法家的主张分别形成了中国历史上的王道和。	答案：霸道
题目：儒家政治学说的核心是，主张为政以德，修己治人。	答案：仁政
题目：我们把人民运用其直接对国家权力进行监督的监督机制称之为以权利制约权力的监督。	答案：民主权利
题目：西方现代政治学的经济学研究方法把政治生活中的个人看作是人，他们遵循着个人利益最大化原则进行政治活动。	答案：理性经济
题目：现代保守主义倡导最大可能的和最小可能的政府管制。	答案：经济自由
题目：现代民主宪政包含人民的统治和两方面的内容。	答案：对人民的保护
题目：现代社会科学把当作一种具有行动取向的信念体系，一种指导和激发政治行为的综合性的思想观念。	答案：意识形态
题目：现代意义的政治参与思想是源自于近代民主理论中有关的思想。	答案：人民权利
题目：宪法和被看成是民主宪政体制下约束政府权力的根本机制。	答案：个人权利
题目：宪政制度将选举制度、代议制度和结合起来，体现了当代人们心目中的政治正义观念。	答案：权力制约
题目：选举权和是民主得以保障和保存的基础性权利。	答案：罢免权
题目：亚里士多德把等同于“最高的善”，认为它是人相互间的一种道德性结合。	答案：国家
题目：一般而言，政治发展的方式可以分为两大类：和政治改革。	答案：政治革命
题目：一般说来，专制制度下的人民只能通过才能实现自己的政治权利。	答案：政治斗争
题目：与古代社会的选举活动相比，近代选举制度在形式上采用。	答案：普选制
题目：在权威主义和极权主义国家，政府官僚集团和往往是政府的重要支持力量。	答案：军人集团
题目：在我国，参与政治的社团一般称作，包括工会、共青团、妇联、工商联等。	答案：人民团体
题目：在我国，制度化的政治接触渠道是。	答案：信访
题目：在中国历史上，权力政治观的代表当属春秋战国时期的。	答案：法家
题目：早期现代化国家的政治发展经历了国家建设、民主化、三个阶段。	答案：福利化
题目：哲学家苏格拉底就被以危害国家安全罪而判处死刑，这一贯被看成是的典型。	答案：暴民统治
题目：政党的产生是现代政治发展的产物。	答案：议会民主
题目：政党的目标是通过竞取政府职位而赢得。	答案：政府权力
题目：政党就是指人们为了通过或其他手段赢得政府权力而组织的政治团体。	答案：选举
题目：政府的是国家的强制性和合法性的有机结合和集中体现。	答案：权威性
题目：政府的作用必须通过一定的程序和途径，在形式上或者实质上把自己的主张、制度、规则和政策等上升为对普遍的的诉求。	答案：公共利益
题目：政府以为基础，以暴力手段为后盾，具有凌驾于社会之上的普遍强制力。	答案：法律制度
题目：政治主要指政治秩序或体系丧失其合法性的情况。	答案：合法性危机
题目：政治是政治合法性的最根本的基础，它是人们评价政治体系的标准。	答案：正义观
题目：政治参与是普通公民通过各种参加政治生活，并影响政治体系的构成、运行方式、运行规则和政策过程的行为。	答案：合法方式
题目：政治合法性是指人们根据其政治正义观念来判定的的合理性，其核心观念是人们对政治合作的理解。	答案：政治秩序
题目：政治权力是一种支配力量，掌握了政治权力，也就掌握了社会的支配力量。掌握了社会的支配力量，也就意味着在社会分配中处于优势地位。	答案：价值和利益
题目：政治社团的功能在我国共青团、妇联、工会的作用中发挥得最为突出。	答案：提供信息
题目：政治文化具有延续性，它通过得以传播和沿袭。	答案：政治社会化
题目：政治学所研究的问题错综复杂，但归根结底，就是、社会、国家三者的关系问题。	答案：个人
题目：政治研究的科学化进程遇到的三个难题是数据问题、隐性价值问题、问题。	答案：价值中立
题目：政治制度化包括政治参与的制度化、的制度化两个基本方面的内容。	答案：政治管理
题目：政治秩序最关键的核心是或者说政治共识的存在。	答案：政治合法性
题目：直到的产生，才给“政治”一个较为准确而深刻的定义。	答案：马克思主义
题目：中国学说对政治的阐释，直接寄托了他们对于仁义礼智信的道德追求。	答案：儒家
题目：中国当前最重要的政治社团是、青年组织和妇女组织。	答案：工会
题目：中国人民是共产党和民主党派合作的主要场所。	答案：政治协商会议
题目：自秦汉到晚清，中国中央集权的政治延续2000多年。	答案：君主专制
题目：自由主义认识到一个人的自由可能会威胁他人的自由，所以，它倡导。	答案：法律下的自由
题目：作为一种制度，民主的最大特点在于，它以作为其政治合法性的基础，政治决策以公民的意见为最终依据。	答案：公民的意志
题目：作为政治理论，自由主义强调个人自由永远目的、始终是手段。	答案：国家权威'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        anEle = getAnswerElementEquals(elements1p[:25], value,key.replace(' ',''), dxindex, 3)  # 找到指定的那个label选项
        if anEle is not None:
            try:
                anEle.find_element_by_xpath("./../div[last()]/*/*/input[last()]").send_keys(value)
            except:
                browser.execute_script("arguments[0].click();", anEle.find_element_by_xpath("./../div[last()]/*/*/input[last()]"))
            time.sleep(0.2)
        dxindex += 1

    listAnswer2 = []
    dxindex = 0

    # 5单
    dxAnswer = '''题目：“第三条道路”，指的是一种既非资本主义也非社会主义的第三种选择的思想。它与所谓的（       ）思想有着密切的关系。	答案：新社会民主主义; 后社会主义
题目：（           ）精辟地论述道：“一切有权力的人都容易滥用权力，这是万古不易的一条经验。有权力的人们使用权力一直遇有界限的地方才休止。……..要防止滥用权力，就必须以权力约束权力。”	答案：孟德斯鸠
题目：（           ）是政治权力的潜在作用方式。	答案：规范方式
题目：（          ）是我国基本的政治制度。	答案：人民代表大会制度
题目：（       ）认为，处于当代这种深刻的理性多元主义的现实中，指望人们都持某一种综合性教义是不可能的，除非用国家力量来压迫民众。	答案：罗尔斯
题目：（       ）是实现政治稳定的根本途径。	答案：政治制度化
题目：（       ）是政治权力主观构成要素中最为基本的要素。	答案：理论与策略
题目：（       ）为政治文化研究提供了基本概念和理论框架，因此被认为是当代政治文化研究的经典之作。	答案：《公民文化》
题目：（       ）在《变化社会中的政治秩序》中认为“现代性孕育着稳定，而现代化过程却滋生着动乱”。	答案：亨廷顿
题目：（      ）的存在形成了对“公权”和“私权”进行划分的根本理由。	答案：利益
题目：（      ）的总统是由直接选举产生的。	答案：法国; 阿根廷
题目：（      ）观念意味着政府在治理过程中不是一个权威的身份参与治理，而是与其他团体、公民平等的身份去参与，与它们协商合作，共同治理。	答案：契约
题目：（      ）精神是现代政治文明的精神实质。	答案：宽容; 理性
题目：（      ）是多党制的典型。	答案：意大利; 法国
题目：（      ）是使市民社会与国家政治相联系的基本途径。	答案：选举
题目：（      ）是天生的民主派。	答案：中产阶级
题目：（      ）是西方国家的主流意识形态。	答案：自由主义
题目：（      ）是政府的灵魂。	答案：阶级性
题目：（      ）原则是现代宪法为国家组织规定的第一个基本原则，它主要阐明了国家权力的来源和归属的问题。	答案：人民主权原则
题目：（      ）政治观体现了人们对“政治”应然状态的追求。	答案：道德
题目：（      ）指出：在专制政府中国王便是法律，同样地，在自由国家中法律便应成为国王。	答案：潘恩
题目：（     ）被认为是工业化国家的意识形态，至今有300多年的历史。它是封建主义走向衰亡、市场经济逐步发展的产物。	答案：自由主义
题目：（     ）方案是“法治”社会的政治设计思路。	答案：现实主义
题目：（     ）认为，在确立各种规则时，必须要征得参与者的同意，所谓“同意限定公正”。	答案：布坎南
题目：（     ）是一种对国家管理的最直接、最广泛的监督方式。	答案：公民监督
题目：（   ）途径可以把我们引向“民主就是人民的统治”，其实质就是“公民自治”的结论。	答案：理想主义
题目：1847年，马克思恩格斯创立了第一个国际性的工人阶级政党（      ）。	答案：共产主义者同盟
题目：1880年美国（        ）政治研究院的建立被视为现代政治科学建立的一个重要事件标志。	答案：哥伦比亚大学
题目：1949年—1978年，中国基本上实施（     ）的自下而上的集权式的政治发展策略。	答案：民众主义
题目：1970年代以后，（   ）的产生，使英美保守主义思想受到冲击。	答案：新右派
题目：1978年以后，随着改革开放的深化，中国基本上采用了（      ）的自上而下的相对分权主义的政治发展策略。	答案：精英主义
题目：20世纪现代自由主义的主要观点是（      ）。	答案：福利改革; 经济干预
题目：八大民主党派在中国共产党的领导下，本着（       ）的方针，实行参政议政，参与民主政治生活。	答案：互相监督; 长期共存; 荣辱与共; 肝胆相照
题目：保守思想和观念大体出现在18世纪末19世纪初期。它的产生是对以（     ）为标志的经济和政治急剧变迁的反动。	答案：法国革命
题目：参政权是指公民参与社会政治生活的权利，主要包括(          )。	答案：创制权; 选举权; 复决权; 罢免权
题目：抽象地看，实现政治稳定的途径包括（       ）。	答案：政治制度化; 减少政治参与
题目：传统的中国被认为是一个高度“政治化”的社会，具体表现在于（     ）。	答案：官本位; 权力本位; “皇权主义”和政治全能主义; 政治经济文化结构高度合一  
题目：从广义上看，政治文明主要是指公共领域里的（      ），它意味着人们之间的普遍合作。	答案：政治秩序
题目：从历史的角度看，第一代“权利”指传统的（       ）。	答案：公民权; 自由权
题目：从全球化的发展过程来看，推动着全球化的主要动力有（      ）。	答案：跨国公司; 技术革命; 各国的制度变革
题目：从社会主义的发展历史来看，具有典型意义的政体形式主要有（    ）。	答案：人民代表大会政权形式; 巴黎公社政权形式; 苏维埃政权形式
题目：从学科发展角度来看，中国古代社会政治研究与（       ）研究高度结合，因此，一直没有形成独立的政治学科。	答案：社会伦理
题目：从政府政治体系的角度来说，政治民主化主要表现为（     ）的民主化改造。	答案：政府体制
题目：从政治参与的本质上看，政治参与是公民对于国家的（      ）关系。	答案：权利; 责任; 义务
题目：从总体上而言，善治在精神上仍有相统一之处，这种精神就是（      ）。	答案：效率精神; 契约观念
题目：当代政治共识的建立途径更多地是通过（      ）的形式来实现的。	答案：重叠共识
题目：当今世界上，大多数国家都实行（       ）。	答案：多党制
题目：道家的政治学说以（      ）为思想核心。	答案：法自然
题目：第三次民主化过程中发展中国家和地区政治发展的现实显示，民主的和平转变需要具备的基本条件是（     ）	答案：文化世俗化; 政治文明化; 政治领导人和执政党开明化; 经济市场化
题目：多元民主理论认同（     ）主义的民主观，但在某些具体问题上持有不同观点。	答案：精英
题目：概括而言，政党的功能和作用主要体现在（      ）。段	答案：实现利益聚集和表达的途径; 实现社会化和政治动员的途径; 形成和培养政治精英的渠道; 组织政府的手段
题目：各国宪法和法律规定的公民民主权利主要体现在公民的（      ）上。	答案：参政权
题目：根据（     ）的观点，人是一种政治的动物，人的本性就是要过一种社会集体生活。	答案：亚里士多德
题目：公民权利首先表现为（          ）。	答案：政治权利
题目：公民委托出去的只是国家的治权，而始终掌握着国家的主权。因为公民可以利用（       ）制约手段监督和影响政府的行为。	答案：撤销决定; 否决议案; 选举权利; 制止行为
题目：共产党组织被认为是（     ）政党的典型。	答案：单位化
题目：关于权力的来源和基础，西方历史上曾经盛行（       ）。	答案：君权神授论
题目：怀疑人类的理性能力，使保守主义信奉（      ），反对任何宏大的社会设计和改造方案。	答案：实用主义
题目：基于个人才能和工作愿望各不相同这样的事实，自由主义并不同意（    ）这样的观念。	答案：社会平等; 收入平等
题目：加强基层民主建设，实行（       ），是确保公民基本民主权利的最基本的途径。	答案：村民自治
题目：经济发展创造了一个庞大的（       ），这是民主的基础之一。答案：中产阶级
题目：精英民主理论所指的精英是指（     ）上最优秀的人物，他们是与普通大众相对应的一个群体。	答案：道德; 政治
题目：就当今世界来看，具有典型意义的主要国家宪法和法律规定的公民政治权利主要包括（        ）。	答案：生存权; 自由权; 民主权
题目：就研究内容而言，从居于主导地位的儒家思想来看，中国传统政治研究特点可以概括为（     ）。	答案：伦理政治学
题目：理想主义途径认为民主的价值在于（        ）。	答案：平等; 自治; 权威
题目：理想主义途径认为民主的首要价值在于（     ）	答案：自治
题目：两党制以（      ）最为典型。	答案：美国; 英国
题目：马克思主义创立的（          ）是人类思想发展史上的革命，也为人们科学认识和把握政治的含义提供了方法论基础。	答案：辩证唯物主义; 历史唯物主义
题目：马克思主义对于（      ）问题十分重视，把它作为工人阶级取得政权之后实现民主的重要标志。	答案：政治参与
题目：马克思主义认为，国家是（      ）的产物。	答案：私有制; 分工
题目：马克思主义认为，社会的（     ）决定政治权力的分配。	答案：经济秩序
题目：马克思主义认为（          ）是凝聚社会力量的核心。	答案：利益
题目：马克思主义认为（      ）是奴隶制和封建制国家的典型政体形式。	答案：专制君主制
题目：马克思主义政治观的基本内容，概括起来认为政治主要是（    ）。	答案：一种具有公共性的社会关系; 根本问题是政治权力; 有规律的社会现象，是科学，也是艺术; 经济的集中体现
题目：美国政治学家（       ）认为，没有自治组织的存在，就不可能实现国家层面上的民主。	答案：达尔
题目：美国政治学家（       ）认为政治是对于社会价值的权威性分配的决策活动。这一定义在当今西方社会得到广泛认同和引用。	答案：戴维·伊斯顿
题目：民主的限度包括（       ）。	答案：以不产生多数人对少数人的暴政为限度
题目：民主化成为一种世界性的进程是在（       ）。	答案：20世纪
题目：目前，现代国家一般都采用（     ）民主制。	答案：代议制; 直接参与; 精英
题目：契约观念的首要条件就是（      ），它是人们缔约的起点。	答案：自愿
题目：全球化对国家政治产生的深刻影响是（      ）。	答案：使国家主权受到一定的制约; 对后发展国家的政治文化造成了双重影响; 推动世界范围内的民主化; 对政府的治理提出了更高的要求
题目：人们把古希腊（     ）的“哲学王”思想看作是精英主义的最早表述。	答案：柏拉图
题目：儒家政治学说的主要内容是（       ）。	答案：礼治; 德治
题目：善治的实质在于建立在对（     ）认同之上的合作。	答案：市场原则; 公共利益
题目：善治是一个上下互动的管理过程，它主要通过（       ）方式实施对公共事务的管理。	答案：伙伴关系; 确立认同和共同的目标; 协商; 合作
题目：善治提倡有效率的治理，具体而言包括（       ）。	答案：回应性; 管理效率; 制度效率
题目：社会主义将（      ）确定为其宪政规则。	答案：议行合一
题目：市民社会是在国家权力体系外自发形成的一种自治社会，以其（       ）为特点。	答案：独立性; 制度化
题目：虽然解决矛盾或危机的方法很多，但在民主政治制度中，（      ）则是最根本的民主途径。	答案：选举
题目：孙中山先生是（        ）政治观的代表人物。	答案：管理
题目：完善人民代表大会制度需要（        ）。	答案：完善人大的罢免制度;  完善人大的质询制度; 厘清宪法与党的领导之间的关系; 完善人大的选举制度
题目：为了防止政府滥用公权，侵害公民自由权利，代议制民主理论家提出（      ）等原则，限制公共权力，还主张通过分权与制衡，实现公共权力部门之间的相互制约。	答案：法治政府; 有限政府; 高效政府
题目：为了有效消除执政者的欲望，防止执政偏向，亚里士多德提出了（     ）等一系列的权力制约方法。	答案：选举; 监督; 限任
题目：我国公民享有的民主权利主要包括（         ）。	答案：批评和建议权; 监督权; 选举权和被选举权; 申诉和控告权
题目：西方传统政党最早出现于（      ）。	答案：英国
题目：西方国家政治社团发挥功能和作用的途径主要有（     ）。	答案：大众传媒; 政党和议会党团; 超国家机构; 立法机关
题目：下列关于改良社会主义的观点，表述正确的是（      ）。	答案：反对暴力革命; 按照道德原则分配财富
题目：下列组织属于邦联制的是（      ）。	答案：东南亚国家联盟; 独联体; 欧洲共同体
题目：现代国家的选举原则主要有（       ）。	答案：直接选举原则; 普遍选举原则; 间接选举原则; 平等选举原则
题目：现代国家政权建构的基本原则中（         ）是国家产生的逻辑起点。	答案：人民主权原则
题目：现代化容易出现政治不稳定的原因有（      ）。	答案：利益冲突加剧; 政府的执行危机; 新旧价值观念的冲突; 人们的社会期望以及参与意识的提高
题目：现代政治文明并不要求宗教、思想和的统一，而要求（      ）的合法性得到承认，能够在公民中取得统一。	答案：政治秩序
题目：现代政治文明遵循的基本原则有（      ）。	答案：宽容和理性精神; 平等原则; 秩序原则; 自由原则
题目：现代自由主义以认同和支持（    ）为特点。	答案：国家干预
题目：宪政的核心是（     ）。	答案：民主政治
题目：宪政建设的根本意义在于它的（     ）正义。	答案：程序
题目：宪政制度于17世纪在（      ）确立以来，到今天已经发展形成了稳定和完备的制度体系。	答案：英国
题目：新右派产生于20世纪70年代后期，它的理论具体表述就是（      ）。	答案：强国家; 自由经济
题目：行为主义政治学要求用研究（     ）的态度、手段和方法来研究政治现象，由此出发，主张以政治行为作为政治学的研究对象。	答案：自然科学
题目：行为主义政治学着重研究（        ）的活动，以期发现政治过程中个人和团体实际行为一致性的范围和性质。	答案：利益集团; 政党; 选民; 政府
题目：亚里斯多德认为政治的最高形式就是（          ）。	答案：国家
题目：一般来讲，（      ）只有在民主社会和宪政国家中才能存在和实现。	答案：社会监督
题目：一般来说，政治参与的制度化要求（      ）。	答案：政治参与渠道的通畅; 有效的利益整合机制
题目：以毛泽东为代表的中国共产党人，把马克思主义政治观运用于中国革命实践，他所撰写的（        ）等著作成为具有中国特色的马克思主义政治学说的主要代表作。	答案：《论人民民主专政》; 《论联合政府》; 《中国社会各阶级分析》; 《新民主主义论》
题目：议行合一原则是（            ）国家政府组织设置的基本原则。	答案：社会主义
题目：意大利马克思主义政治理论家（       ）在分析西方资本主义国家特点的时候指出，国家统治＝暴力＋文化领导权，其中，拥有文化领导权使其政治统治合理化。	答案：葛兰西
题目：英国政府一直在（      ）的轮流执掌之下。	答案：工党; 保守党
题目：舆论监督以其（     ）而对政治权力主体具有强大的威慑力，曾经被马克思形象地称为“另一个法庭――社会舆论的法庭”。	答案：及时性; 公开性; 评价性; 广泛性
题目：在2000多年的历史演变中，（      ）学说成为与中央集权的君主专制体制最相匹配的政治意识形态。	答案：儒家
题目：在当代，政治发展主要指政治的（      ）过程。	答案：现代化
题目：在分类研究中，社会成员如何看待政治生活中不同党派、团体和个人之间的（   ）是区分传统政治文化与现代政治文化的一个重要指标。	答案：竞争; 冲突
题目：在市场经济条件下，（         ）是最为基本的社会资源配置机制。	答案：市场; 政府
题目：在西方发达国家。社团发挥其作用的非常规方式有（      ）。	答案：恐怖活动; 政变; 示威抗议; 司法诉讼
题目：在现代法治社会，（       ）监督已经成为公众参与监督的最重要的形式，也是遏制官僚主义、以权谋私等腐败现象滋生蔓延的有力武器。	答案：新闻舆论
题目：在现代社会中，（      ）制度已成为调整国家权力活动的基本途径。	答案：选举
题目：在现实生活中，人们一般把社会主义和（     ）看成是两种对立的意识形态。	答案：自由主义
题目：在众多政治设计思路中，具有明显对比性的是理想主义与现实主义方案，二者具有明显的差异。这种差异根源于人们对（      ）的认识和评价的截然不同。	答案：公共权力; 人性
题目：针对政治制度的合法性危机，有可能出现的政治行动主要是（        ）。	答案：政治改革
题目：政党形成于19世纪初期，它的产生是现代（       ）政治发展的产物。	答案：议会民主
题目：政府必须建立在“被统治者”同意的基础上，这种观念使自由主义者更加支持（   ）。	答案：民主制; 代议制
题目：政治参与的作用主要表现在（      ）。	答案：有助于经济发展; 有助于促进政治民主发展; 有助于实现社会公平
题目：政治参与实际上乃是公民行使以（     ）为核心的公民权利的过程。	答案：普选权
题目：政治合法性的核心观念是人们对（        ）的理解。	答案：政治合作
题目：政治权力具有（   ）的特性。	答案：扩张性; 支配性; 排他性; 权威性和强制性
题目：政治文明意味着人类合作的稳定性和有序性，它的根本原则就是	答案：秩序
题目：政治稳定是指一国政治体系的连续性和有序性，它包括（      ）。	答案：权力结构的稳定; 国家政权体系的稳定; 政治过程的有序状态
题目：政治学名著《理想国》的作者是（        ）	答案：柏拉图
题目：政治学名著《政治学》的作者是（         ）	答案：亚里士多德
题目：政治学研究内容可以分为（      ）。	答案：政治科学研究; 政治哲学研究
题目：政治学研究最常见、最传统的方法是（          ）。	答案：权力研究途径
题目：政治研究科学化进程遇到的难题是（      ）。	答案：数据问题; 隐性价值问题; 价值中立问题
题目：治理方法的单一从根本上说是古代治理中缺乏（       ）精神的结果。	答案：平等协商
题目：中国共产党领导的多党合作制中的民主党派属于（      ）。	答案：参政党
题目：中国古代的法家主张，政治之道在于（     ），即政治权力的获取、保持和运用。	答案：势; 法; 术
题目：中国古代关于政治的研究主要围绕君主的（          ）而展开。	答案：治国之道
题目：综合现代国家宪法的内容及其精神实质来看，宪法对国家政权组织建构提出了如下原则要求(        )。	答案：权力制约原则; 法治原则; 人民主权原则
题目：纵观各国的宪法，以下的（       ）体现了法治原则。	答案：法律面前人人平等; 各国家机关的权力必须由宪法和法律授予; 国家制定的法律必须是良法; 司法独立
题目：最先提出政治合法性概念的是（     ）。	答案：马克斯·韦伯
题目：作为1787年美国宪法主要起草人的（     ）指出，一个国家的统治者和被统治者都不是天使而是人，因而防止把某些权力逐渐集中于同一部门的最可靠办法，就是给予各部门的主管人抵制其他部门侵犯的必要法定手段和个人的主动。	答案：汉密尔顿
题目：作为社会（或市民社会）构成的主要角色，（      ）是现代政治生活中的重要政治现象，是现代政治体系的重要组成部分。	答案：社团; 政党'''
    mapdxanswer = danxuanAutoAnswerFix(dxAnswer, "答案：")
    for key, value in mapdxanswer.items():
        key = key.replace(' ', '')
        key = key.replace(' ', '')
        anEle = getAnswerElementEquals(elements1p[20:], value, key, dxindex, 3)  # 找到指定的那个label选项
        if anEle is not None:#找到后,根据value判断下是单选还是多选
            if "; " in value:
                rightRatios = getDuoxuanAnswerRatio(value,anEle)
                for r in rightRatios:
                    try:
                        r.click()
                    except:
                        browser.execute_script("arguments[0].click();",r)
                    time.sleep(0.2)
            else:
                rightRatio = getDanxuanAnswerRatio(value,anEle)
                try:
                    rightRatio.click()
                except:
                    browser.execute_script("arguments[0].click();",rightRatio)
                time.sleep(0.2)

        dxindex += 1



    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_element_by_xpath('//input[@name="next"]').click()
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
        time.sleep(1)
        browser.get(xkurl)  # 先考形1
    else:
        return 0


# 2.立即考试.判断一下,防止多次考试
def readyToTest(browser):
    time.sleep(2)
    readyTest = browser.find_element_by_xpath('//button[@type="submit"]')
    if '再次' not in readyTest.get_attribute("value"):
        if '再次' not in readyTest.text:
            if '现在' in readyTest.text or '继续' in readyTest.text:
                readyTest.click()
                time.sleep(2)
                return 1
        return 0
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


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=466597'
xingkao2 = 'http://hubei.ouchn.cn/mod/forum/view.php?id=466594'




option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
browser = webdriver.Chrome(chrome_options=option)
# browser.maximize_window()  #max_window

browser.get('http://student.ouchn.cn/')
browser.implicitly_wait(15)  # wait

file = open(studyName + '.txt')
keys = []
for line in file.readlines():
    keys.append(line.strip())


def writeAnswer2(browser):
    time.sleep(2)
    browser.find_element_by_id("id_subject").send_keys("此次国务院常务会议确定")
    time.sleep(6)
    browser.switch_to.frame("id_message_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "仇高擎表示，目前在中小企业贷款领域，银行还在很大程度上依赖担保公司的担保。为调动商业银行的积极性，国务院常务会议提出了三条支持信用担保公司发展的措施。即鼓励地方政府通过资本注入、风险补偿等多种方式增加对信用担保公司的支持；设立多层次中小企业贷款担保基金和担保机构，提高对中小企业贷款比重；对符合条件的中小企业信用担保机构免征营业税。仇高擎表示，目前担保公司实力较弱，并且分散，缺少比较强的担保公司，国务院的措施正是支持担保公司做强。如果担保公司资本金有限，所能担保的额度也有限，能支持的企业也有限，因此国务院此次强调要鼓励地方政府来对担保公司注资。国务院常务会议强调，要积极扩大住房、汽车和农村消费信贷市场。哈继铭认为，这是明确要求银行扩大消费贷款的发放。目前，中国的贷款主要发放给了企业，个人消费贷款仅占贷款总额的12%左右。为了扩大城市居民的消费需求，要求银行扩大住房、汽车贷款。此前“家电下乡”等扩大农村消费市场的措施正在采取，通过发放农村消费贷款可以有效扩大农村的消费能力。仇高擎表示，原来商业银行在核销不良贷款时，需要经过财政部门的批准，程序很慢，而且标准也很严格，不少需要核销的不良贷款不能及时核销。新政策可能会放松核销的标准和程序。此外，仇高擎还认为，对于商业银行对中小企业、三农以及灾区贷款，可能会在财税上给予商业银行一些优惠，从而保证商业银行的盈利。哈继铭也表示，对于商业银行对某些特定企业的贷款，可以给予财税优惠。在调动银行积极性的同时，此次国务院常务会议强调，要形成银行、证券、保险等多方面扩大融资、分散风险的合力。")
    browser.switch_to.default_content()
    browser.find_element_by_id("id_submitbutton").click()


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
            # saveTest2GetAnswer(browser, proxy)
        wait3AndCloseTab(browser)

        enterTest(browser, xingkao2)
        if readyToTestForum(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer2(browser)
        wait3AndCloseTab(browser)

    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(6)
