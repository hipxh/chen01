#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from threading import Thread

import timeunit
import bs4
from selenium import webdriver
import os

studyName = os.path.basename(__file__).split('.')[0]

#其中一张试卷全部为富文本提交
def getAnswerElement(elements, neirong, i):
    for ele in elements:
        if neirong in ele.text:
            return ele

def getAnswerElementEquals(elements, neirong,i,meidaotiyouduoshaogexuanxiang):
    elements = elements[i*meidaotiyouduoshaogexuanxiang:(i+1)*meidaotiyouduoshaogexuanxiang]
    for ele in elements:
        if neirong == ele.text or "A. " + neirong == ele.text or "B. " + neirong == ele.text or "C. " + neirong == ele.text or "D. " + neirong == ele.text or "E. " + neirong == ele.text or "a. " + neirong == ele.text or "b. " + neirong == ele.text or "c. " + neirong == ele.text or "d. " + neirong == ele.text or "e. " + neirong == ele.text :
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

rightTiGan=[]

def judgeQueTitle(elements1p, title):
    if isinstance(elements1p, list):
        for ele in elements1p:
            if title+"（" in ele.text:
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

def danxuanAutoAnswerFix(answer,reg):
    result=[]
    split = answer.split("\n")
    for i in split:
        result.append(i.strip().split(reg)[1])
    return result
def duoxuanAutoAnswerFix(answer, reg, reg2):
    map={}
    split = answer.split("\n")
    for i in split:
        map[i.split(reg)[0].strip()] = i.split(reg)[-1].split(reg2)
    return map

def duoxuanAutoAnswer(answer, map):
    split = answer.split("")
    for i in split:
        if len(i) < 2:
            continue
        i_split = i.split("（")#2019年11月17日14:25:30bug,如果选项里有括号,则报错,此处应取第一个左括号的前面和最后一个右括号的右边,怕耽误速度,暂不处理
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
        if (judgeQueTitle(elements1p[titleIndex], timu)):#如果题干在错的list里,就点击错误
            a = 0
            ratios[danxuantiLength * 4 + panduanIndex * 2 + 1].click()
            break
    if a == 1:  # 如果把错题都走了一遍仍然为1,则该判断题是对的
        ratios[danxuantiLength * 4 + panduanIndex * 2].click()
    time.sleep(0.1)


# start to answer.
def writeAnswer1(browser):
    canTakeWrongNum=0

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''错错错对错
错错对对错
错错对对错
错对对错错'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    # 保证进来的是第一页
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    dxindex=0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an,dxindex,4)#找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex+=1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    browser.find_element_by_xpath('//input[@name="previous"]')
    elements1 = browser.find_elements_by_xpath('//label')#下一页后label重新拿


    mulAnswer = '''16.生产力  社会化大生产
17.人际关系角色  信息传递角色  决策制定角色
18.技术技能 人际技能  概念技能
19.宏观环境  产业环境
20.人是“社会人”而不是“经济人”  企业中存在着非正式组织  生产效率主要取决于工人的士气
21.传统的权力  超凡的权力  理性----合法的权力
22.系统思考  改变心智模式  超越自我  建立共同愿景
23.产品设计 产品质量  厂容厂貌  员工服饰
24.制定计划  执行计划  检查计划执行情况
25.战略计划  作业计划
26.高利润  提高市场占有率  提高员工福利待遇
27.收益  成本  期限  风险
28.定性预测  定量预测
29.多重性  层次性  单一性  变动性
30.尽可能量化企业目标  把目标控制在五个以内  目标期限应以长期目标为主  期限适中'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".","  ")
    for key, value in mapmulAnswer.items():
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex,4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    pdAnswer = '''31.对
     32.错 
     33.对
      34.错 
      35.错
       36.对
        37.错
         38.对 
         39.错
          40.对'''

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    browser.find_element_by_xpath('//input[@name="previous"]')
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    listpdanswer = danxuanAutoAnswerFix(pdAnswer, ".")

    dxindex = 0
    for an in listpdanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex,2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    #富文本
    line = browser.page_source
    frameId = line.split(":45_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId+":45_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1.银华公司是怎样认识到企业文化的作用的? 随着经济体制改革的深化，银华公司的管理和发展出现了困难。通过调查分析，认为必须引入先进的管理理念，即企业文化。 2.银华公司在企业文化建设上做了哪些工作? （ 从机制方面，银华公司建立和完善了考核机制、监督机制、分配制度、人才选拔机制等。 从教育方面，银华公司注重引导和规范职工的日常行为；定期组织员工学习。等等。 加强投入，包括人、财、物的投入。 3.怎样认识企业文化的本质和作用? 企业文化是指一定历史条件下，企业在生产经营和管理活动中所创造的具有本企业特色的精神财富及其物质形态。它包括三个部分：精神文化、制度文化和物质文化。 优秀的企业文化对外可以促进形成独特的企业形象定位，产生品牌效应，拓展市场和增加产品附加值；对内则形成强大的凝聚力，起到学习、维系和激励的功能，引导、协调并约束员工行为，在较高程度上实现员工个人目标与企业目标的一致，促进企业和个人的共同成长。")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum>3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer2(browser):
    canTakeWrongNum=0

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''1.全局性
2.编制具体的行动计划
3.密集型发展战略
4.关联多元化
5.程序化决策
6.头脑风暴法
7.1100
8.丙
9.组织结构
10.责权利对等
11.矩阵制结构
12.矩阵制组织结构
13.量才使用
14.自我考评
15.职务轮换'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    # 保证进来的是第一页
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    dxindex=0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an,dxindex,4)#找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex+=1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    browser.find_element_by_xpath('//input[@name="previous"]')
    elements1 = browser.find_elements_by_xpath('//label')#下一页后label重新拿


    mulAnswer = '''16.科学  艺术
17.狭窄  空泛
18.该产业是否具有吸引力  公司是否拥有优势资源  该产业的盈利能力
19.稳定型战略  收缩型战略  发展型战略
20.无关联多元化  复合多元化
21.生产系统  产品的核心技术  顾客基础  销售渠道
22.业务性决策  日常管理决策
23.德尔菲法  头脑风暴法  哥顿法
24.函询  反馈
25.组织的部门机构  职责的规定  职位的安排
26.M型结构  多部门结构  产品部式结构
27.保持了集中统一指挥的特点  分工非常细密  注重专业化管理
28.有知识的人  有能力的人  对组织忠诚的人
29.组织现有的规模和岗位  管理人员的流动率  组织发展的需要
30.调动内部成员的工作积极性  吸收外部人才  保证选聘工作的准确性  被聘者可以迅速展开工作'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".","  ")
    for key, value in mapmulAnswer.items():
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex,4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    pdAnswer = '''31.错 
32.对
 33.错
  34.错
   35.对
    36.对
     37.错
      38.对
       39.对
        40.对'''

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    browser.find_element_by_xpath('//input[@name="previous"]')
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    listpdanswer = danxuanAutoAnswerFix(pdAnswer, ".")

    dxindex = 0
    for an in listpdanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex,2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    #富文本
    line = browser.page_source
    frameId = line.split(":45_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId+":45_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1．决策包括哪些基本活动过程?其中的关键步骤是什么?决策过程：识别问题--确定决策目标--拟订可行方案—分析评价方案--选择方案--实施方案关键步骤是选择方案。2．案例中两家企业形成鲜明对比的原因是什么?决策的正确与否是两家企业的发展形成反差的原因。3．科学决策需要注意哪些问题?科学性的决策，要求决策者准确认识事物的发展变化规律，并采取科学的程序和方法，做出符合事物发展规律的决策。")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum>3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    canTakeWrongNum=0

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判
    elements1 = browser.find_elements_by_xpath('//label')
    dxAnswer = '''1.自身影响力              
    2.1-9型
3.转移法                  
4.需要层次理论
5.消极强化                
6.激励或影响人的行为
7.书面沟通
8.地位差异
9.选择性知觉
10.反馈
11.前馈控制
12.实物标准
13.可行性
14.直接监督或巡查
15.运营能力'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    # 保证进来的是第一页
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    dxindex=0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an,dxindex,4)#找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex+=1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    browser.find_element_by_xpath('//input[@name="previous"]')
    elements1 = browser.find_elements_by_xpath('//label')#下一页后label重新拿


    mulAnswer = '''16.法定权力  奖励权力  处罚权力
17.职位权力  任务结构  上下级关系
18.情感能力  行为能力  意志能力  认知能力
19.积极进取的措施  消极防范的措施
20.生活要得到基本保障  避免人身伤害，失业保障  年老时有所依靠
21.要给职工提供适当的工资和安全保障  要改善他们的工作环境和条件  对职工的监督要能为他们所接受
22.积极强化  消极强化  惩罚  自然消退
23.信息的传递  对信息的理解
24.口头沟通和书面沟通  非语言方式沟通和电子媒介沟通
25.正式沟通  非正式沟通
26.企业高层管理人员  企业中层管理人员  企业基层管理人员
27.较高素质的管理者  下属人员的积极参与和配合  适当的授权
28.销售额  成本总额  工资总额
29.目标明确原则  控制关键点原则  及时性、经济性原则
30.质量 成本 采购'''
    dxindex = 0
    mapmulAnswer = duoxuanAutoAnswerFix(mulAnswer, ".","  ")
    for key, value in mapmulAnswer.items():
        for v in value:
            anEle = getAnswerElementEquals(elements1, v.strip(), dxindex,4)  # 找到指定的那个label选项
            if anEle is not None:
                anEle.find_element_by_xpath("./../input[last()]").click()
                time.sleep(0.1)
        dxindex += 1

    pdAnswer = '''31.错 
    32.错 
    33.对
     34.对 
     35.对
      36.错 
      37.错
       38.错
        39.对
        40.错'''

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    browser.find_element_by_xpath('//input[@name="previous"]')
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    listpdanswer = danxuanAutoAnswerFix(pdAnswer, ".")

    dxindex = 0
    for an in listpdanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex,2)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    #富文本
    line = browser.page_source
    frameId = line.split(":45_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId+":45_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "1．孟教授讲的领导应发扬民主，给员工决策权的说法对吗?为什么? 从以下两个角度中的任何一个来回答均可： （1）个人决策与群体决策的关系。 （2）领导风格与民主管理。 2．真正的民主管理应具备哪些条件? 该工段具备这些条件吗? 根据领导权变理论，领导方式必须随着被领导者的特点和环境的变化而变化。实行民主管理要求员工既有工作热情，又有必需的知识与能力。 该工段不具备这些条件。")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum>3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer4(browser):
    canTakeWrongNum=0

    # 试卷题目固定布局

    # 单选多选混合,根据题库判断单选还是多选,进行相应的点击,,,规律-前4单,中3多,后3判

    time.sleep(4)
    browser.find_element_by_xpath('//input[@type="submit"]')




    #富文本
    line = browser.page_source
    frameId = line.split(":2_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId+":2_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "（1）管理是管理者为有效地达到组织目标，对组织资源和组织活动有意识、有组织、不断地进行的协调活动。（2）技术技能，是指管理者从事自己管理范围内的工作所需要的技术和能力。（3）人际技能，又称人际关系技能，是指成功地与人打交道并与别人沟通的能力。（4）概念技能，是指管理者对事物的洞察、分析、判断、抽象和概括的能力。（5）经济环境：是指一个组织所在的国家或地区的总体经济状况，包括生产力发展水平、产业结构状况、通货膨胀状况、收入和消费水平，市场的供求状况以及经济体制等。（6）技术环境：它对组织的发展有至关重要的影响。伴随着社会信息化和知识经济时代的到来，科学技术对组织的影响更为显著，技术的变革正在从根本上影响着组织模式的变革和管理者的管理方式。（7）决策，是指为了达到一定的目标，采用一定的科学方法和手段，从两个以上的可行方案中选择一个满意方案的分析判断过程。（8）所谓激励，是指人类活动的一种内心状态。它具有加强和激发动机，推动并引导行为朝向预定目标的作用。（9）控制：为保证组织目标以及为实现目标所制定的计划得以实现，要求管理者必须对计划的执行过程进行监督、检查，如果发现偏差，还要及时采取纠偏措施。（10）企业战略就是指组织为了实现长期生存和发展，在综合分析组织内部条件和外部环境的基础上做出的一系列带有全局性和长远性的谋划。")
    browser.switch_to.default_content()

    line = browser.page_source
    frameId = line.split(":4_answer_id_ifr")[0][-15:].split("id=\"")[1]
    browser.switch_to.frame(frameId + ":4_answer_id_ifr")
    browser.find_element_by_id("tinymce").send_keys(
        "答：管理学分为总论、决策与计划、组织、领导、控制、创新六篇，每一篇都有特定的目标主旨。而计划作为管理学理论的基础，让我有了许多很深的体会。在为群体中一起工作的人们设计环境，使每个人有效地完成任务时，管理人员最主要的任务，就是努力使每个人理解群体的使命和目标以及实现目标的方法。如果要使群体的努力有成效，其成员一定要明白期望他们完成的是什么，这就是计划工作的职能，而这项职能在所有管理职能中是最基本的。计划包括确定使命和目标以及完成使命和目标的行动；这需要指定决策，即从各种可供选择的方案中确定行动步骤。计划制订分为如下步骤：寻找机会→确定目标→拟订前提条件→确定备选方案→评估备选方案→选择方案→制定衍生计划→用预算量化计划。计划制订的步骤可以用于大多数需要的场合，例如许多大学生准备出国留学，那就可以根据这些计划步骤来为自己做准备。首先，我们需要认识到出国读书的机会以及因此所带来的机遇等，然后，我们就需要设定各方面的目标，如选择国家以及就读的专业领域等。???我们还需要假设是否能在留学过程中获得奖学金以及是否能够在外兼职打工，无论哪种情况，都有几个需要仔细平衡的选择方案。因此，学生们可以就申请不同的学校利弊进行评价，选择适合自己的留学国家和学校。在成功收到入取通知书后和申请到签证后，我们就需要开始指定衍生计划，包括选择住处、搬到一个新的地址，或在学校附近找一份工作。然后，我们需要将一切计划转换成预算，包括学费、生活费等等。这些步骤都是一个计划的体现。???无论是企业还是个人，一个好的完善的计划必定能够帮助我们更快更有效的确定行动方向，从而能达到事半功倍的效果。例如许多著名品牌都制定了其长远的营销战略：可口可乐公司的长远目标宗旨就是?:“我们致力于长期为公司的股东创造价值，不断改变世界。通过生产高质量的饮料为公司、产品包装伙伴以及客户创造价值，进而实现我们的目标。”?ＡＴＴ则是：“我们立志成为全球最受推崇和最具价值的公司。我们的目标是丰富顾客的生活，通过提供新鲜有效的通信服务帮助顾客在商业上取得更大成功，并同时提升股东价值综上所述，一个学期的管理学带给我很多心得体会，我也将会应用于今后的实践中，取得了跟多的收获。")
    browser.switch_to.default_content()

    # end answer
    if canTakeWrongNum>3:
        return
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
    if len(windowstabs)>1:#如果没找到课程,至少别报错
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


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=506598'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=506599'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=506600'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=506601'


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

    enterTest(browser, xingkao1)
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


    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(2)
