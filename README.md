# requests-ccnu
本仓库是 CCNUer 日常生活必备的小脚本集合。多是利用 py3 的 requests 库写出的，模拟登录学校网站后，进行您想要的查询和**适度**的爬取。实现很简单，点子更重要，欢迎校友提 PR。

现已完成：

* [ccnu2ical.py](https://github.com/wwyqianqian/requests-ccnu/blob/master/ccnu2ical.py), [ccnu2ical.js](https://github.com/wwyqianqian/requests-ccnu/blob/master/ccnu2ical.js) 前者通过处理 JSON、后者通过爬取 HTML 结构来获取学生课程表，并按照 RFC 文档把课表改写为```.ics``` 格式的日历文件。同学们可自行导入谷歌日历或 iCloud 等等支持 .ics 格式的系统日历，从此告别每学期一度的手动输入。当前版本号：v0.5.0。
* [courses.py](https://github.com/wwyqianqian/requests-ccnu/blob/master/courses.py) 选课脚本，现阶段由于教务处取消了「抢课」环节，故失效，剩余部分代码结构仅供学习参考。
* [spocDownloader.py](https://github.com/wwyqianqian/requests-ccnu/blob/master/spocDownloader.py) 云课堂下载器。学校新版云课堂前端没有给出「下载」按钮，同学们无法直接下载 PPT、论文等课件，而之前的旧版云课堂有这个功能，很多同学产生了依赖，于是这是个比较大的需求。目前此脚本通过模拟登录 spoc 网站，发送请求获取后端数据，拿到了特征，最后通过 URL 拼接，找到了文件真正的下载链接。这个脚本可以爬取到指定课程的所有文件，同学们可以按照个人需求手动下载。当前版本号：v0.5.0。
* [spocFriends.py](https://github.com/wwyqianqian/requests-ccnu/blob/master/spocFriends.py) 学校开放的搜索好友平台。目前支持输入学号范围，批量查询同学姓名。照片由于属于隐私范畴，遂不做。

---

