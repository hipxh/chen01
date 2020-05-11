import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
import time
import os
from important_info import important_info


def parseShiTi(shijuan_html, attempt, sesskey, info):
    print(time.strftime('%Y-%m-%d %H:%M:%S',
                        time.localtime(time.time())) + "####### 即将解析: " + shijuan_html.title.string)
    single_answer = info.single_answer
    multi_answer = info.multi_answer
    single_timu = shijuan_html.find_all('input',
                                        attrs={'type': 'radio'})  # ('input',class_=re.compile('questionflagpostdata '))
    slots_num1 = shijuan_html.find_all('a', attrs={'data-quiz-page': '0'})
    slots_num2 = shijuan_html.find_all('a', attrs={'data-quiz-page': '1'})
    slots_num3 = shijuan_html.find_all('a', attrs={'data-quiz-page': '2'})
    slots_num4 = shijuan_html.find_all('a', attrs={'data-quiz-page': '3'})
    slots_num5 = shijuan_html.find_all('a', attrs={'data-quiz-page': '4'})
    multi_timu = []
    for multi in shijuan_html.find_all('input', attrs={'type': 'checkbox'}):
        if "choice" in multi["name"]:
            multi_timu.append(multi)
    single_data = handleSingle(single_timu, single_answer, shijuan_html)
    multi_data = handleMulti(multi_timu, multi_answer, shijuan_html)
    other_param_data = hanle_auto_save_param(sesskey, attempt,
                                             len(slots_num1) + len(slots_num2) + len(slots_num3) + len(
                                                 slots_num4) + len(slots_num5))
    param_data = single_data + multi_data + other_param_data
    return param_data


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
        temp = (k + "=" + v + "&" + k[0:-6] + ":flagged=0&" + (k[0:-6] + ":flagged=0&") + (
                    k[0:-6] + ":sequencecheck=1&"))
        single_auto_save_data += temp
    return single_auto_save_data


# 处理多选题
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


# 处理autoSave接口的其它必填参数
def hanle_auto_save_param(sesskey, attempt, timu_num):
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
        slots.append(str(i + 1))
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


# python取指定前后字符中间
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


# 从科目名txt取账号构成字典
def getAcounts(course_name):
    acounts = {}
    file = open(course_name + '.txt')
    keys = []
    for line in file.readlines():
        keys.append(line.strip())

    for key in keys:
        username = key.split("\t")[0]
        password = key.split("\t")[1]
        acounts[username] = password
    return acounts


# 从带数字的科目名txt中取出所有完成形考obj
def getImportantInfo(course_name):
    infos = []
    curdir = os.path.curdir
    filenames = os.listdir(curdir)
    tiku_files = []
    for filename in filenames:
        if ".txt" in filename and course_name in filename and len(filename) > len(course_name + ".txt"):
            tiku_files.append(filename)
    for tiku_name in tiku_files:
        file = open(tiku_name)
        info = important_info("", "", "", "")
        single_flag = False
        multi_flag = False
        judge_flag = False
        single_answer = ""
        multi_answer = ""
        judge_answer = ""
        for line in file.readlines():
            if line.strip() == "":
                single_flag = False
                multi_flag = False
                judge_flag = False
            elif "quiz/view" in line:
                info.cmid = line.split("id=")[1].strip()
            elif "单选题" in line or "单向选择题" in line:
                single_flag = True
            elif "多选题" in line or "多向选择题" in line:
                multi_flag = True
            elif "判断题" in line:
                judge_flag = True
            elif single_flag:
                single_answer += line
            elif multi_flag:
                multi_answer += line
            elif judge_flag:
                judge_answer += line
        info.single_answer = single_answer
        info.multi_answer = multi_answer
        info.judge_answer = judge_answer
        infos.append(info)
    return infos


# time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
if __name__ == '__main__':
    # parseShiTi();
    course_name = "网络实用技术基础"
    infos = getImportantInfo(course_name)
    # 先拿到账号字典
    acounts = getAcounts(course_name)

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

    # 所有账号分别登录
    acount_i = 0
    for k, v in acounts.items():
        acount_i += 1
        print(time.strftime('%Y-%m-%d %H:%M:%S',
                            time.localtime(time.time())) + "####### 程序即将处理第[" + acount_i + "]个账号: " + k)
        # 一个账号只用登录一次便可完成该科目所有形考
        student_name = ""
        # 登录,能拿到tokenId
        login_url = "http://sso.ouchn.cn/Passport/AjaxLogin?lu=" + k + "&lp=" + v + "&ru=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLoginCallback&to=20200509&ip=%3A%3Affff%3A172.16.4.87&aid=11&lou=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLogout&sf=e57e97bdb5c64b7a&_=1588910077684"
        result1 = requests.get(url=login_url)

        # 在html里拿认证的url
        login_url = "http://shome.ouchn.cn/Learn/Course/GetMoodleHub?site=http://hubei.ouchn.cn&rid=4&courseCode=01507&cid=c89531f3-ca83-4d78-810a-fe4755b85a66"
        result1 = requests.get(url=login_url, cookies=result1.cookies)
        html1 = BeautifulSoup(result1.text, "html.parser")
        find_all = html1.find_all('form', limit=1)
        get_MoodleSession_url = find_all[0]['action']
        # 取当前年月日时分秒14位字符串
        strftime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        get_MoodleSession_url_final = (get_MoodleSession_url + "").split("Time=")[0] + "Time=" + strftime + \
                                      (get_MoodleSession_url + "").split("Time=")[1][14:]
        # 此处经常签名错误,故做报错重试机制
        retry_num = 0
        while (retry_num < 3):
            retry_num += 1
            # 此处重定向是重头戏,python会自动调用最后个那个重定向后的接口
            chongdingxiang_result = requests.post(url=get_MoodleSession_url_final,
                                                  data='CourseClass=%5B%7B%22OrganizationCode%22%3A%224200201%22%2C%22CourseClassCode%22%3A%224200201_AUTO200%22%2C%22CourseClassName%22%3A%22%E8%8D%86%E5%B7%9E%E7%94%B5%E5%A4%A7%E6%A0%A1%E6%9C%AC%E9%83%A8_2020%E5%B9%B4%E6%98%A5%E5%AD%A3%E4%B8%80%E9%94%AE%E5%88%86%E7%8F%AD%22%7D%5D',
                                                  headers=headers)
            time.sleep(3)
            sesskey = getmidstring(chongdingxiang_result.text, "sesskey\":\"", "\",\"themerev")
            if sesskey is not None:
                student_name = getmidstring(chongdingxiang_result.text, '查看个人资料">', '<')
                print(time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.localtime(time.time())) + "####### " + student_name + " 已登录")
                break
            print("重定向请求出错,正在进行第" + str(retry_num) + "次尝试...")
        result_history = chongdingxiang_result.history
        # 一个账号考完所有形考
        for info in infos:
            cmid = info.cmid  # 形考url的末尾id
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time())) + "####### " + student_name + " 即将处理形考id: " + cmid)
            # 判断下这个人是否已经考过该形考,且得分百分之八十以上则跳过
            before_kao_url = "http://hubei.ouchn.cn/mod/quiz/view.php?id=" + cmid
            before_kao_result = requests.get(url=before_kao_url, headers=headers2, cookies=result_history[0].cookies)
            top_score = getmidstring(before_kao_result.text, '最高分:', '<')
            if top_score is not None and len(top_score) > 1:
                score_split = top_score.split("/")
                if (float(score_split[0].strip()) / float(score_split[1].strip()) > 0.8):
                    print(time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.localtime(
                                            time.time())) + "####### " + student_name + " 该形考最高得分已满足要求(80%),跳过该形考.")
                    continue

            get_attempt_url = "http://hubei.ouchn.cn/mod/quiz/startattempt.php"
            get_attempt_data = "cmid=" + cmid + "&sesskey=" + sesskey
            shijuan_result = requests.post(url=get_attempt_url, data=get_attempt_data, headers=headers2,
                                           cookies=result_history[0].cookies)
            time.sleep(3)
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    time.time())) + "####### " + student_name + " 已进入试卷,即将根据题库得出  [题干不变,选项乱序] 试卷的单选和多选的正确答案")
            shijuan_result_history = shijuan_result.history
            attempt = str(shijuan_result_history[0].headers['Location'])[-7:]
            shijuan_html = BeautifulSoup(shijuan_result.text, "html.parser")
            auto_save_data = parseShiTi(shijuan_html, attempt, sesskey, info)
            auto_save_urlEncode_data = urllib.parse.quote(auto_save_data)
            auto_save_urlEncode_data2 = auto_save_urlEncode_data.replace("%3D", "=")
            auto_save_urlEncode_data3 = auto_save_urlEncode_data2.replace("%26", "&")
            auto_save_url = "http://hubei.ouchn.cn/mod/quiz/autosave.ajax.php"
            auto_save_result = requests.post(url=auto_save_url, data=auto_save_urlEncode_data3, headers=headers3,
                                             cookies=result_history[0].cookies)
            time.sleep(2)
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    time.time())) + "####### " + student_name + " 已保存答案,即将提交...")
            # 提交试卷
            submit_url = "http://hubei.ouchn.cn/mod/quiz/processattempt.php"
            requests.post(url=submit_url,
                          data="attempt=" + attempt + "&finishattempt=1&timeup=0&slots=&sesskey=" + sesskey,
                          headers=headers2,
                          cookies=result_history[0].cookies)

            before_kao_url = "http://hubei.ouchn.cn/mod/quiz/view.php?id=" + cmid
            before_kao_result = requests.get(url=before_kao_url, headers=headers2, cookies=result_history[0].cookies)
            top_score = getmidstring(before_kao_result.text, '最高分:', '<')
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    time.time())) + "####### " + student_name + " 已提交! 该形考得分:" + top_score)
