#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Copyright © 2018 - wwyqianqian <wwyqianqian@whres.net>
# Source Code: https://github.com/wwyqianqian/requests-ccnu/blob/master/spocDownloader.py
# Version Number: v0.5.0
# Last Modified: 2018.8.5


import requests
import json
import sys
import getpass


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
    return dataTree


def tree_dict(d, need, attachmentList):
    for k, v in d.items():
        if k == need:
            attachmentList.append(v)
        if isinstance(v, dict) and v:
            tree_dict(v, need, attachmentList)
        elif isinstance(v, list) and v:
            tree_list(v, need, attachmentList)


def tree_list(l, need, attachmentList):
    for item in l:
        if isinstance(item, dict) and item:
            tree_dict(item, need, attachmentList)
        elif isinstance(item, list) and item:
            tree_list(item, need, attachmentList)


def printSource(name, infoID):
    source = len(name)
    print("云课堂上，本网站有 {} 个资源可供下载".format(source))
    for i in range(source):
        print("{0}. {1}".format(i + 1, name[i]))
        print("下面是本课件下载链接，请根据个人需求点击链接、重命名、并下载：")
        print("http://spoc.ccnu.edu.cn:80/getFileStream/" + infoID[i])
        print("---------------------------------------------------------------------------------")


if __name__ == "__main__":
    account = input('输入账号：')
    password = getpass.getpass('输入密码：(为了安全，您密码的输入不会显示在屏幕上，密码输入完毕请按回车键)')
    resCookies = spocLogin(account, password)
    siteID = input('输入您想要下载资源的网页 URL 后面的字符串 http://spoc.ccnu.edu.cn/studentHomepage/studentCourseCenter?siteId= \n')
    bigConstTree = getSiteResourceTree(siteID)
    attachmentNameList = []
    attachmentInfoIdList = []
    tree_dict(bigConstTree, "attachmentName", attachmentNameList)
    tree_dict(bigConstTree, "attachmentInfoId", attachmentInfoIdList)
    printSource(attachmentNameList, attachmentInfoIdList)
