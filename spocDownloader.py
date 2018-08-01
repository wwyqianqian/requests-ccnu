import requests
import json


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

    r = requests.post('http://spoc.ccnu.edu.cn/userLoginController/checkLogin', headers=headers, data=data)
    print(r.text)
    data = json.loads(r.text)
    if data['code'] == 0:
        print("wow! 迫真登录成功了")


    resTest = requests.get('http://spoc.ccnu.edu.cn/studentHomepage', headers=headers, data=data)
    mycookies = resTest.cookies.get_dict()
    print("这是您的 cookie: ", mycookies)
    return mycookies


def getSiteResourceTree(siteID):
    data = [
    ('siteId', siteID),
    ]

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
    # print(thisHeaders['Referer'])
    # print(siteID)
    # print(resCookies)

    response = requests.post('http://spoc.ccnu.edu.cn/siteResource/getSiteResourceTree', headers=thisHeaders, cookies=resCookies, data=data)
    print(response.text)


if __name__ == "__main__":
    account = input('输入账号：')
    password = input('输入密码：')
    resCookies = spocLogin(account, password)
    siteID = input('输入您想要下载资源的网页 URL http://spoc.ccnu.edu.cn/studentHomepage/studentCourseCenter?siteId= 后面的字符串\n')
    getSiteResourceTree(siteID)
