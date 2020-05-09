import requests

if __name__ == '__main__':

    login_url = "http://sso.ouchn.cn/Passport/AjaxLogin?lu=1842001400086&lp=19931210&ru=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLoginCallback&to=20200509&ip=%3A%3Affff%3A172.16.4.87&aid=11&lou=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLogout&sf=e57e97bdb5c64b7a&_=1588910077684"
    result1 = requests.get(url=login_url)
    print(result1.cookies)
    login_url = "http://shome.ouchn.cn/home/index"
    result2 = requests.get(url=login_url,cookies=result1.cookies)

    pass
    #
    # login_url = "http://passport.ouchn.cn/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dstudentspace%26redirect_uri%3Dhttp%253A%252F%252Fstudent.ouchn.cn%252F%2523%252Fsignin-oidc%2523%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520ouchnuser%2520ouchnstudentspaceapi%26state%3D5c8efc8a48a64ebba80e3de03fb0bc32%26nonce%3Dd110bb2d7e664134a05d5530513793af"
    # result = get(url=login_url)
    #
    #
    # params = {'username': '1842001400086', 'password': '19931210', 'button': 'login', '__RequestVerificationToken': 'CfDJ8AF1CiN3kJ5Eq1qyIMytci5AiYlf8z8d6Csb3UMKZ3WNWnx5qSQEkT4S2RU0II8Lnm7Kj5GWJbePF299NGPEwygeup5l4wEYAY_qckTq_ZzQ35PI4Nmp2pXF6giHirG7UkMpTltU6gYaTMLSnPG - ve4','RememberLogin':'false'}
    # post_url = "http://passport.ouchn.cn/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dstudentspace%26redirect_uri%3Dhttp%253A%252F%252Fstudent.ouchn.cn%252F%2523%252Fsignin-oidc%2523%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520ouchnuser%2520ouchnstudentspaceapi%26state%3D5c8efc8a48a64ebba80e3de03fb0bc32%26nonce%3Dd110bb2d7e664134a05d5530513793af"
    # result = post(url=post_url, params=params)
    # # access_token = result['access_token']
    # print(result)
