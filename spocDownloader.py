import requests
import json
import re
import sys


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

    session = requests.Session()

    resCheck = session.post('http://spoc.ccnu.edu.cn/userLoginController/checkLogin', headers=headers, data=data)
    # print(resCheck.text)
    dataload = json.loads(resCheck.text)
    if dataload['code'] == 0:
        print("登录成功!")
    elif dataload['code'] == 1:
        sys.exit("密码错误! 请重新登录")
    elif dataload['code'] == 2:
        sys.exit("用户名不存在!(学号错误)! 请重新登录")
    elif dataload['code'] == 99:
        sys.exit("用户验证失败！未知错误，请重新登录")
    else:
        print("未知登录状况，请谨慎后续操作。")

    resGup = session.post('http://spoc.ccnu.edu.cn/userLoginController/getUserProfile', headers=headers, data=data)
    # print('resGup.headers\n', resGup.headers)
    # print('resGup.requests.headers\n', resGup.request.headers)
    # print('resGup.text\n', resGup.text)
    # print('resGup.status_code\n', resGup.status_code)

    return session.cookies.get_dict()


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

    resGetTree = requests.post('http://spoc.ccnu.edu.cn/siteResource/getSiteResourceTree', headers=thisHeaders, cookies=resCookies, data=data)
    dataTree = json.loads(resGetTree.text)
    constTree = dataTree['data'][0]['child'][0]
    return constTree


def getChild(inputTree, i):


    lenTree = len(bigConstTree['child'])
    print("长度：", lenTree)


    if i < lenTree:
        if inputTree['child'][i]['attachment'] == []:
            childChild(inputTree['child'][i]['child'][0], i)

        else:
            print(inputTree['attachment'][0]['attachment']['attachmentName'])
            print("先的")
    else:
        return ("hhhhhhh")





def childChild (childTree, i):

    if childTree['attachment'] == []:
        childTree = childTree['child'][0]

        childChild(childTree, i)

    else:
        print(childTree['attachment'][0]['attachment']['attachmentName'])
        print("后的\n")
        getChild(bigConstTree, i+1)



    # print(constTree['child'][0]['child'][0]['child'][0]['child'][0]['child'][0]['attachment'][0]['attachment']['attachmentName'])
    # source_url = constTree['child'][0]['child'][0]['child'][0]['child'][0]['child'][0]['attachment'][0]['attachmentInfoId']
    # print('http://spoc.ccnu.edu.cn:80/getFileStream/' + source_url)


if __name__ == "__main__":
    account = input('输入账号：')
    password = input('输入密码：')
    resCookies = spocLogin(account, password)
    siteID = input('输入您想要下载资源的网页 URL http://spoc.ccnu.edu.cn/studentHomepage/studentCourseCenter?siteId= 后面的字符串\n')
    bigConstTree = getSiteResourceTree(siteID)
    getChild(bigConstTree, 0)

