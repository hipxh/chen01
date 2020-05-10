import requests


class FangWen:
    def __init__(self):
        self.cookies = requests.cookies.RequestsCookieJar()

    def go(self, url, method, post_data, headers):
        response = requests.request(method, url
                                    , data=post_data
                                    , headers=headers
                                    , cookies=self.cookies)  # 传递cookie

        self.cookies.update(response.cookies)  # 保存cookie
