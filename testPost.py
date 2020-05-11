import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
import time


# 将列表按指定长度切割多份
def list_of_groups(list_info, per_list_len):
    '''
    :param list_info:   列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) * per_list_len)
    end_list = [list(i) for i in list_of_group]  # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count != 0 else end_list
    return end_list


# 将单选题答案处理成list返回
def parseSingle2List(single_answer):
    single_list = []
    answers = single_answer.split("\n")
    for answer in answers:
        if len(answer.strip()) > 1:
            single_list.append(answer.strip())
    return single_list


# 处理单选题
def handleSingle(single_timu, single_answer, shijuan_html):
    single_list = []
    for single in single_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        single_list.append(choice_content.string)
    single_groups = list_of_groups(single_list, 4)
    parse_single_list = parseSingle2List(single_answer)
    right_answer = []
    i = 0
    for answer in parse_single_list:
        if "." in answer:
            answer = answer.split(".")[1]
        for answers in single_groups[i]:
            if answer in answers:
                right_answer.append(answers)
        i += 1
    label_list = []
    right_id_list = []
    for single in single_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        label_list.append(choice_content)
    for r_an in right_answer:
        for label in label_list:
            if r_an == label.string:
                right_id_list.append(label['for'])
    right_answers_map = {}
    for id in right_id_list:
        right_answers_map[id[0:-1]] = id[-1]
    single_auto_save_data = ""
    for k, v in right_answers_map.items():
        temp = (k + "=" + v + "&" + k[0:-6]+":flagged=0&"+(k[0:-6]+":flagged=0&")+(k[0:-6]+":sequencecheck=1&"))
        single_auto_save_data += temp
    return single_auto_save_data


# 处理autoSave接口的其它必填参数
def hanle_auto_save_param(sesskey,attempt,timu_num):
    other_params_auto_save_data = ""
    other_params = {}
    other_params['next'] = '结束答题…'
    other_params['attempt'] = attempt
    other_params['thispage'] = '0'
    other_params['nextpage'] = '-1'
    other_params['timeup'] = '0'
    other_params['sesskey'] = sesskey
    other_params['scrollpos'] = ''
    slots = []
    for i in range(timu_num):
        slots.append(str(i+1))
    other_params['slots'] = ",".join(slots)
    for k, v in other_params.items():
        temp = (k + "=" + v + "&")
        other_params_auto_save_data += temp
    return other_params_auto_save_data[0:-1]


# 解析试题页
def parseMulti2List(multi_answer):
    multi_list = []
    answers = multi_answer.split("\n")
    for answer in answers:
        if len(answer.strip()) > 1:
            multi_row_answers = []
            if "." in answer:
                answer = answer.split(".")[1]
            for an in answer.split("；"):
                multi_row_answers.append(an.strip())
            multi_list.append(multi_row_answers)
    return multi_list


def handleMulti(multi_timu, multi_answer, shijuan_html):
    multi_list = []
    for single in multi_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        multi_list.append(choice_content.string)
    multi_groups = list_of_groups(multi_list, 4)
    parse_multi_list = parseMulti2List(multi_answer)
    right_answer = []
    i = 0
    for multi_row_answers in parse_multi_list:
        for an in multi_row_answers:
            for xuanxiang in multi_groups[i]:
                if an in xuanxiang:
                    right_answer.append(xuanxiang)
        i += 1

    label_list = []
    right_id_list = []
    for single in multi_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        label_list.append(choice_content)
    for r_an in right_answer:
        for label in label_list:
            if r_an == label.string:
                right_id_list.append(label['for'])
    right_answers_map = {}
    for id in right_id_list:
        right_answers_map[id] = "1"
    single_auto_save_data = ""
    for k, v in right_answers_map.items():
        temp = (k + "=" + v + "&" + k[0:-7] + ":flagged=0&" + (k[0:-7] + ":flagged=0&") + (
                    k[0:-7] + ":sequencecheck=1&"))
        single_auto_save_data += temp
    return single_auto_save_data


def parseShiTi(shijuan_html,attempt,sesskey):
    single_answer = '''
    1.加密
    2.用于提供高速文件传输服务
    3.用户
    4.数据传输、资源共享
    5.网络覆盖范围
    6.总线型
    7.数据传输前不需要建立一条端到端的通路
    8.语法、语义和同步
    9.物理层
    10.发送方从上层向下层传输数据，每经过一层附加协议控制信息
    11.ICMP
    12.SMTP
    13.IEEE802.3u
    14.10BaseT
    15.高数据速率，小范围，低误码率
    16.无规则的拓扑结构
    17.数据链路层
    18.光纤同轴混合网（HFC） 
    19.无线局域网
    20.无线电波
        '''
    multi_answer = '''
    21.计算机系统；共享的资源；传输介质
22.电路交换；报文交换；分组交换
23.A. 应用层；传输层；网际层
24.发送；接收
25.无线接入点；无线路由器；无线网卡
26.存储转发；直接转发
27.光源；光纤
28.透明传输；差错检测
29.点对点信道；广播信道
30.数字用户线接入复用器；用户线；用户设施
        '''
    single_timu = shijuan_html.find_all('input',attrs={'type': 'radio'})  # ('input',class_=re.compile('questionflagpostdata '))
    multi_timu = []
    for multi in shijuan_html.find_all('input', attrs={'type': 'checkbox'}):
        if "choice" in multi["name"]:
            multi_timu.append(multi)
    single_data = handleSingle(single_timu, single_answer, shijuan_html)
    multi_data = handleMulti(multi_timu, multi_answer, shijuan_html)
    other_param_data = hanle_auto_save_param(sesskey, attempt, 32)
    param_data = single_data + multi_data + other_param_data
    return param_data


def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


if __name__ == '__main__':
    # parseShiTi();

    cmid = '659661'         # 形考url的末尾id

    # 老平台登录后进新平台的第一个post所需header
    headers = {'Host': 'hubei.ouchn.cn',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Origin': 'http://shome.ouchn.cn',
               'Cookie': 'CheckCode=6SC8BtjY/n4=',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    headers2 = {'Host': 'hubei.ouchn.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://hubei.ouchn.cn',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9'}
    headers3 = {'Host': 'hubei.ouchn.cn',
                'Connection': 'keep-alive',
                'Origin': 'http://hubei.ouchn.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9'}

    # 取当前年月日时分秒14位字符串
    strftime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    # 登录,能拿到tokenId
    login_url = "http://sso.ouchn.cn/Passport/AjaxLogin?lu=1842001400086&lp=19931210&ru=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLoginCallback&to=20200509&ip=%3A%3Affff%3A172.16.4.87&aid=11&lou=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLogout&sf=e57e97bdb5c64b7a&_=1588910077684"
    result1 = requests.get(url=login_url)

    # 在html里拿认证的url
    login_url = "http://shome.ouchn.cn/Learn/Course/GetMoodleHub?site=http://hubei.ouchn.cn&rid=4&courseCode=01507&cid=c89531f3-ca83-4d78-810a-fe4755b85a66"
    result1 = requests.get(url=login_url, cookies=result1.cookies)
    html1 = BeautifulSoup(result1.text, "html.parser")
    find_all = html1.find_all('form', limit=1)
    sessKey_post_data = html1.find_all('input')[-1]
    value_ = sessKey_post_data['value']
    quote = urllib.parse.quote(value_)
    get_MoodleSession_url = find_all[0]['action']
    get_MoodleSession_url_final = (get_MoodleSession_url + "").split("Time=")[0] + "Time=" + strftime + \
                                  (get_MoodleSession_url + "").split("Time=")[1][14:]

    # 此处经常签名错误,故做报错重试机制
    retry_num = 0
    while(retry_num<3):
        retry_num+=1
        # 此处重定向是重头戏,python会自动调用最后个那个重定向后的接口
        chongdingxiang_result = requests.post(url=get_MoodleSession_url,
                                              data='CourseClass=' + quote,
                                              headers=headers)
        time.sleep(3)
        sesskey = getmidstring(chongdingxiang_result.text, "sesskey\":\"", "\",\"themerev")
        if sesskey is not None:
            break
        print("重定向请求出错,正在进行第"+str(retry_num)+"次尝试...")
    result_history = chongdingxiang_result.history
    get_attempt_url = "http://hubei.ouchn.cn/mod/quiz/startattempt.php"
    get_attempt_data = "cmid=" + cmid + "&sesskey=" + sesskey
    shijuan_result = requests.post(url=get_attempt_url, data=get_attempt_data, headers=headers2,
                                   cookies=result_history[0].cookies)
    time.sleep(3)
    shijuan_result_history = shijuan_result.history
    attempt = str(shijuan_result_history[0].headers['Location'])[-7:]
    shijuan_html = BeautifulSoup(shijuan_result.text, "html.parser")
    auto_save_data = parseShiTi(shijuan_html,attempt,sesskey)
    auto_save_urlEncode_data = urllib.parse.quote(auto_save_data)
    auto_save_urlEncode_data2 = auto_save_urlEncode_data.replace("%3D","=")
    auto_save_urlEncode_data3 = auto_save_urlEncode_data2.replace("%26","&")
    auto_save_url = "http://hubei.ouchn.cn/mod/quiz/autosave.ajax.php"
    auto_save_result = requests.post(url=auto_save_url, data=auto_save_urlEncode_data3, headers=headers3, cookies=result_history[0].cookies)
    time.sleep(2)

    #提交试卷
    submit_url = "http://hubei.ouchn.cn/mod/quiz/processattempt.php"
    requests.post(url=submit_url, data="attempt="+attempt+"&finishattempt=1&timeup=0&slots=&sesskey="+sesskey, headers=headers2,
                  cookies=result_history[0].cookies)




    # shijuan_url = "http://hubei.ouchn.cn/mod/quiz/attempt.php?attempt=6774580"
    # shijuan_result = requests.get(url=shijuan_url, cookies=result_history[0].cookies)