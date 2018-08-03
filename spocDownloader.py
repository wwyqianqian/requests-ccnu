import requests
import json
import re

def spocLogin(account, password):
    headers = {
        'Origin': 'http://spoc.ccnu.edu.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://spoc.ccnu.edu.cn/starmoocHomepage',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = [
    ('loginName', account),
    ('password', password),
    ]

    s = requests.Session()
    s.get('http://spoc.ccnu.edu.cn/')
    print("初始化 s.cookies.get_dict()：", s.cookies.get_dict())

    r = s.post('http://spoc.ccnu.edu.cn/userLoginController/checkLogin', headers=headers, data=data)
    print(r.text)
    data = json.loads(r.text)
    if data['code'] == 0:
        print("登录成功!")

        getUserProRes = s.post('http://spoc.ccnu.edu.cn/userLoginController/getUserProfile', headers=headers, data=data)
        print("getUserProRes.headers", getUserProRes.headers)
        print("getUserProRes.request.headers", getUserProRes.request.headers)

        mysession = s.cookies.get_dict()

        userLoginRes = requests.post('http://spoc.ccnu.edu.cn/userLoginController/userLogin', headers=headers, data=data, cookies=mysession)
        print("userLoginRes.headers", userLoginRes.headers)
        print("userLoginRes.request.headers", userLoginRes.request.headers)

        newcookie = userLoginRes.headers['Set-Cookie']
        splitSetCookie = re.split(r'\s+', newcookie)[0]
        mysessioncookie = splitSetCookie[8:-1]
        print(mysessioncookie)
        thiscookie = {
            "SESSION": mysessioncookie,
        }

        homeRes = requests.get('http://spoc.ccnu.edu.cn/studentHomepage', headers=headers, cookies=thiscookie)
        print(homeRes.status_code)
        print(homeRes.headers)
        print(homeRes.request.headers)


        # {'JSESSIONID': 'D0C5560B6215AE18AE2C3DD150712D37',
        #  'SESSION': '5ac5e3d8-ce7b-499b-8d9c-c23b5223185f'}
        # responseSession = requests.post('http://spoc.ccnu.edu.cn/userLoginController/getUserProfile', headers=headers, data=data)
        # print(responseSession.headers)
        # setCookie = responseSession.headers['Set-Cookie']
        # print("这是服务端返回的cookie：", setCookie)
        #
        # splitSetCookie = re.split(r'\s+', setCookie)
        # myCookie = splitSetCookie[0][11:-1]
        # print("您的 JSESSIONID 为：", myCookie)
        #
        # s = requests.Session()
        # s.get('http://spoc.ccnu.edu.cn/')
        # resptest = s.post('http://spoc.ccnu.edu.cn/userLoginController/getUserProfile', headers=headers, data=data)
        # print(s.cookies.get_dict())

def getSiteResourceTree(siteID):
    data = [
    ('siteId', siteID),
    ]

    thisCookie = {
        'JSESSIONID': resCookies,
    }

    thisHeaders = {
        'Origin': 'http://spoc.ccnu.edu.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://spoc.ccnu.edu.cn/studentHomepage/studentCourseCenter?siteId=' + siteID,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    response = requests.post('http://spoc.ccnu.edu.cn/siteResource/getSiteResourceTree', headers=thisHeaders, cookies=thisCookie, data=data)
    print(response.text)


if __name__ == "__main__":
    account = input('输入账号：')
    password = input('输入密码：')
    resCookies = spocLogin(account, password)
    siteID = input('输入您想要下载资源的网页 URL http://spoc.ccnu.edu.cn/studentHomepage/studentCourseCenter?siteId= 后面的字符串\n')
    getSiteResourceTree(siteID)
