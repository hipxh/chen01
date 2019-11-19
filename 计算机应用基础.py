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
        result.append(i.strip().split(reg)[1])
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
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0


    # 20单
    dxAnswer = '''1.微处理器
2.第一台
3.第一台
4.硬件系统与软件系统
5.操作系统
6.应用软件
7.控制和管理系统资源的使用
8.计算机硬件
9.运算器
10.显示器
11.微处理器
12.CPU
13.只读光盘
14.水产捕捞
15.激光式打印机
16.检查计算机是否感染病毒，消除部分已感染病毒
17.1024KB
18.（75）8
19.将网络资源集中管理和调度，并以虚拟化方式为用户提供服务的
20.通过信息传感设备将物品与互联网相连接，以实现对物品进行智能化管理的网络'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后label重新拿

    # 20填空

    dxAnswer = '''21.一
22.逻辑元件
23.工具
24.计算机辅助教学
25.控制器
26.存储器
27.所有指令
28.CPU
29.快
30.100
31.输入设备
32.显示器
33.系统软件
34.多种媒体信息
35.信息
36.病毒
37.音
38.基本
39.倍数
40.二进制'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿

    # 20单
    dxAnswer = '''41.单用户/多任务
42.开始
43.剪贴板
44.关闭计算机
45.拖拽
46.标题栏
47.标题栏
48.右
49.控制面板
50.所有子文件夹及其所有文件
51.Shift
52.右击
53.<Ctrl>+<空格>
54.工具
55.Ctrl
56.组织
57.可以显示在屏幕任一边
58.延长显示屏使用寿命
59.进行文件清理并释放磁盘空间
60.出现鼠标停滞/键盘无法输入等现象'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后label重新拿

    # 20填空

    dxAnswer = '''61.应用程序
62.关闭
63.玻璃图案
64.剪贴板
65.首先
66.拖拽
67.快捷
68.窗口结构
69.活动
70.非活动窗口
71.充满
72.对话框
73.可执行
74.箭头
75.资源管理器
76.展开
77.*
78.纯文本
79.系统还原
80.跳转列表'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//label')  # 下一页后label重新拿,这一页有单选有填空
    elements1t = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后label重新拿,这一页有单选有填空

    dxAnswer = '''81.3
82.共享软/硬件和数据资源
83.飞机
84.调制解调器
85.广域网
86.保证上网和打电话两不误
87.接入的计算机距离和范围
88.网卡
89.@
90.通信/日程/任务管理'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    dxAnswer = '''91.调制解调器
92.移动化
93.The Internet of Things
94.有限
95.资源子网
96.拓扑结构
97.代理商
98.E-Mail
99.WWW
100.通讯簿'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1t[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1


    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()


def writeAnswer2(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 10单
    dxAnswer = '''1.不会
2.完全相同
3.docx
4.另存为
5.Ctrl
6.剪贴板
7.底纹
8.完全一致
9.插入
10.符号'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后label重新拿

    # 10填空

    dxAnswer = '''11.所见即所得
12.页面
13.控制
14.操作对象
15.四周
16.多
17.页面布局
18.页面布局
19.SmartArt
20.截取屏幕'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer3(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 10单
    dxAnswer = '''1.单元格在工作表中的位置
2.0 1/2
3.启动Excel后不能再新建空白工作簿
4.=IF（A5<60，"不及格"，"及格"）
5.# VALUE!
6.=$A$2*$B$1
7.不可以按单元格颜色进行排序
8.饼图
9.自动更新
10.单击“视图”→“工作簿视图”→“页面布局”选项'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后label重新拿

    # 10填空

    dxAnswer = '''11.不包括
12.单元格本身
12.绝对引用
13.30
13.40
14.TRUE
15.FALSE
15.最大值
16.最小值
16.所有数据
17.排序
18.条件格式
19.选中图表
20.当前工作表所有内容
20.设置打印区域'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer4(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 10单
    dxAnswer = '''1.显示幻灯片的方式
2.普通视图
3.为文本、图形预留位置
4.幻灯片之间的跳转
5.预定义的幻灯片样式和配色方案
6.文本和线条
7.幻灯片切换
8.动作设置
9.“视图”菜单的“幻灯片放映”命令
10.修改母版不会对演示文稿中任何一张幻灯片带来影响'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后label重新拿

    # 10填空

    dxAnswer = '''11.大纲视图
12.普通视图
13.幻灯片浏览视图
14.幻灯片视图
12.图表
13.图表
13.插入
14.幻灯片切换
15.动画效果
15.普通
15.动画方案
16.内容提示向导
16.设计模板
16.空演示文稿
17.人工
17.排练计时
18.动作设置
19.全部应用
20.幻灯片母版
20.讲义母版
20.备注母版
20.标题母版'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
    time.sleep(0.1)
    # save and submit
    browser.find_elements_by_xpath('//button[@type="submit"]')[1].click()
    browser.find_element_by_xpath('//input[@class="btn btn-primary m-r-1"]').click()
def writeAnswer5(browser):
    canTakeWrongNum = 0
    # 单多选在同一页混的时候,标记下单选题的数量
    danxuanLength = 9

    # 试卷题目固定布局
    ratios = browser.find_elements_by_xpath('//input[@type="radio"]')
    elements1p = browser.find_elements_by_xpath('//div[@class="qtext"]')
    browser.find_element_by_id("quiznavbutton1").click()
    browser.find_element_by_id("quiznavbutton1")
    elements1 = browser.find_elements_by_xpath('//label')
    dxindex = 0

    # 10单
    dxAnswer = '''1.建立在严格的数学理论，集合论和谓词演算公式的基础之上
2.可由一个或多个其值能唯一标识该关系模式中任何元组的属性组成
3.数据库管理员
4.数据库表
5.前后顺序可以任意颠倒，不影响库中的数据关系
6.可靠性
7.数据表既相对独立、又相互联系
8.数据库→数据表→记录→字段
9.选择
10.书号'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        anEle = getAnswerElementEquals(elements1, an, dxindex, 4)  # 找到指定的那个label选项
        if anEle is not None:
            anEle.find_element_by_xpath("./../input[last()]").click()
            time.sleep(0.1)
        dxindex += 1

    browser.find_element_by_xpath('//input[@name="next"]').click()
    time.sleep(4)
    elements1 = browser.find_elements_by_xpath('//input[@type="text"]')  # 下一页后label重新拿

    # 10填空

    dxAnswer = '''11.Office2010
12.数据库管理
12.记录或元组
13.字段或属性
13.一对一
14.一对多
15.多对多
14.操作
15.实体完整性
15.操作完整性
15.自定义完整性
16.数据结构
16.操纵及完整性约束
16.存储结构
17.唯一确定一条记录的字段
18.关系
19.一对多
20.查询
20.窗体'''
    listdxanswer = danxuanAutoAnswerFix(dxAnswer, ".")
    dxindex = 0
    for an in listdxanswer:
        elements1[dxindex].send_keys(an)
        time.sleep(0.2)
        dxindex += 1

    # end answer-翻页的情况下用的结束答题
    if canTakeWrongNum > 3:
        return
    browser.find_elements_by_xpath('//input[@type="submit"]')[1].click()
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


# 等待三秒,让我们看到卷子已经答题提交完成,然后关tab,切到第一个tab,再进学习
def wait3AndCloseTab(browser):
    time.sleep(2)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1.5)


xingkao1 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=457956'
xingkao2 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=457958'
xingkao3 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=457962'
xingkao4 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=457965'
xingkao5 = 'http://hubei.ouchn.cn/mod/quiz/view.php?id=457968'

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
        enterTest(browser, xingkao5)
        if readyToTest(browser) == 1:  # 除非没考过,否则就关闭tab,重进学习页面,考下一个形考
            writeAnswer5(browser)
        wait3AndCloseTab(browser)

    # 5个形考走完提交之后直接换账号
    browser.get("http://passport.ouchn.cn/Account/Logout?logoutId=student.ouchn.cn")
    time.sleep(2)
