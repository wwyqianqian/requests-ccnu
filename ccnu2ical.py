#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Copyright © 2018 - wwyqianqian <wwyqianqian@whres.net>
# Source code: https://github.com/wwyqianqian/requests-ccnu/blob/master/ccnu2ical.py
# RFC: https://tools.ietf.org/html/rfc5545

import requests
import json
import os
import random
import re


def getData():
    cookies = {
        'x': 'x',
        'x': 'x',
    }
    headers = {
        'Origin': 'http://xk.ccnu.edu.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-HK;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'http://xk.ccnu.edu.cn//kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default&su=2016xxxxxx',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    params = (
        ('gnmkdm', 'N2151'),
    )
    data = [
        ('xnm', '2018'),
        ('xqm', '3'),
    ]
    response = requests.post('http://xk.ccnu.edu.cn/kbcx/xskbcx_cxXsKb.html', headers=headers, params=params, cookies=cookies, data=data)
    data = json.loads(response.text)
    return data

def printHeader():
    with open('/Users/qianqian/Desktop/cal.ics', 'w', encoding='utf-8') as f:
        print('BEGIN:VCALENDAR\nPRODID:-//wwyqianqian//CCNU2ICAL Calendar 0.0001//CN\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:Courses\nX-WR-TIMEZONE:Asia/Shanghai\nBEGIN:VTIMEZONE\nTZID:Asia/Shanghai\nX-LIC-LOCATION:Asia/Shanghai\nBEGIN:STANDARD\nTZOFFSETFROM:+0800\nTZOFFSETTO:+0800\nTZNAME:CST\nDTSTART:19700101T000000\nEND:STANDARD\nEND:VTIMEZONE\n', file=f)

def printEvents():
    data = getData()
        for i in range(len(data["kbList"])):
        new_data = data["kbList"][i]      


        description = new_data["xm"] + " " + new_data["jxbmc"] + "课堂"
        location = new_data["cdmc"]
        summary = new_data["kcmc"]
        date_stamp = "20180625T000000Z"
        created = "20180620T000000Z"
        last_modified = "20180625T000000Z"
        status = "CONFIRMED"
        uid = date_stamp + "-" + str(i) + str(random.random()) + "wwyqianqian@whres.net"

        start2End = new_data["jcor"]
        re_start2End = re.findall(r"\d+", start2End)
        TIME_DICT = {
            '1': [0, 00, 0, 45],
            '2': [0, 55, 1, 40],
            '3': [2, 0, 2, 45],
            '4': [2, 55, 3, 40],
            '5': [4, 0, 4, 45],
            '6': [4, 55, 5, 40],
            '7': [6, 0, 6, 45],
            '8': [6, 55, 7, 40],
            '9': [8, 0, 8, 45],
            '10': [8, 55, 9, 40],
            '11': [10, 0, 10, 45],
            '12': [10, 55, 11, 40],
            '13': [12, 0, 12, 45],
            '14': [12, 55, 13, 40],
        };  
        for key in TIME_DICT:
            if key == re_start2End[0]:
                course_start_time = time2str(str(TIME_DICT[key][0])) + time2str(str(TIME_DICT[key][1])) + "00Z"
            elif key == re_start2End[1]:
                course_end_time = time2str(str(TIME_DICT[key][2])) + time2str(str(TIME_DICT[key][3])) + "00Z"     
      
        weeks = new_data["zcd"]
        re_weeks = re.findall(r"\d+", weeks)
        weeks_cycle = int(re_weeks[1]) - int(re_weeks[0]) + 1
        rrule = "FREQ=WEEKLY;COUNT=" + str(weeks_cycle)

        dayInWeek = new_data["xqjmc"]
        defineSunday = "20180902"
        DAY_DICT = {
            "星期日": 0,
            "星期一": 1,
            "星期二": 2,
            "星期三": 3,
            "星期四": 4,
            "星期五": 5,
            "星期六": 6,   
        };
        for key in DAY_DICT:
            if key == dayInWeek:
                course_start_date = int(defineSunday) + int(DAY_DICT[key])
                

        with open('/Users/qianqian/Desktop/cal.ics', 'a', encoding='utf-8') as f:
            print('BEGIN:VEVENT', file=f)
            print('DTSTART:' + str(course_start_date) + 'T' + str(course_start_time), file=f)
            print('DTEND:' + str(course_start_date) + 'T' + str(course_end_time), file=f)
            print('DTSTAMP:' + str(date_stamp), file=f)
            print('UID:' + str(uid), file=f)
            print('CREATED:' + str(created), file=f)
            print('DESCRIPTION:' + str(description), file=f)
            print('LAST-MODIFIED:' + str(last_modified), file=f)
            print('LOCATION:' + str(location) , file=f)
            print('STATUS:' + str(status), file=f)
            print('SUMMARY:' + str(summary) ,file=f)
            print('RRULE:' + rrule, file=f)
            print('END:VEVENT', file=f)
            print('END:VCALENDAR', file=f)

def time2str(i):    
    if int(i) < 10:
        return "0" + str(i)
    else:
        return str(i)
  

def main():   
    printHeader()
    printEvents()

main()    
