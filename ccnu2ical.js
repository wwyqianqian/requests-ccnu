// Copyright © 2018 Sumi Makito
// Source code: https://gist.github.com/SumiMakito/754eb2fcfdaf81ab16b319dda59a28f2/#file-ccnu2ical-js  


(function() {
    // 设置开学第一天的[[前一天]] 
    // 也就是学期第一周星期一前的[[星期日]]的日期
    var FIRST_DAY = new Date("2018-08-26");
    // 有的教务会把菜单放在外围, 然后课程表千在 iframe 中显示
    // 如果是这样的话, 需要把下面的设置为 true 否则可能取到的是空的
    var TIMETABLE_IN_IFRAME = false;

    var DAY_MAPPING = {
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "日": 0,
    };
    var TIME_MAPPING = {
        1: [8, 0, 8, 45],
        2: [8, 55, 9, 40],
        3: [10, 0, 10, 45],
        4: [10, 55, 11, 40],
        5: [12, 0, 12, 45],
        6: [12, 55, 13, 40],
        7: [14, 0, 14, 45],
        8: [14, 55, 15, 40],
        9: [16, 0, 16, 45],
        10: [16, 55, 17, 40],
        11: [18, 0, 18, 45],
        12: [18, 55, 19, 40],
        13: [20, 0, 20, 45],
        14: [20, 55, 21, 40],
    };
    var ID = new Date().getTime();
    var VCAL_HEADER = "BEGIN:VCALENDAR\nPRODID:-//Makito//ZFN2VCAL Calendar 0.0002//CN\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:Courses" + ID + "\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:\nBEGIN:VTIMEZONE\nTZID:Asia/Shanghai\nX-LIC-LOCATION:Asia/Shanghai\nBEGIN:STANDARD\nTZOFFSETFROM:+0800\nTZOFFSETTO:+0800\nTZNAME:CST\nDTSTART:19700101T000000\nEND:STANDARD\nEND:VTIMEZONE\n";
    var VCAL_TAIL = "END:VCALENDAR";

    function getVEvent(course, weekId, beginTime, endTime) {
        return "BEGIN:VEVENT\n" +
            "DTSTART:" + date2tstr(beginTime) + "\n" +
            "DTEND:" + date2tstr(endTime) + "\n" +
            "DTSTAMP:" + date2tstr(beginTime) + "\n" +
            "UID:" + escape(course.name) + "@Week" + weekId + "+" + Math.random() + "\n " +
            "CREATED:20180101T000000Z\n" +
            "DESCRIPTION:教师: " + course.teacher + ", 教学班: " + course.class + "\n" +
            "LAST-MODIFIED:20180101T000000Z\n" +
            "LOCATION:" + course.place + "\n" +
            "STATUS:CONFIRMED\n" +
            "SUMMARY:" + course.name + "\n" +
            "END:VEVENT\n";
    }

    function ito2wstr(i) {
        return (i < 10 ? "0" : "") + i;
    }

    function date2tstr(date) {
        return date.getFullYear() + ito2wstr(date.getMonth() + 1) + ito2wstr(date.getDate()) + "T" +
            ito2wstr(date.getHours()) + ito2wstr(date.getMinutes()) + ito2wstr(date.getSeconds()) + "Z";
    }

    function stratoia(stra) {
        var ia = [];
        for (var n = 0; n < stra.length; n++) {
            ia.push(Number.parseInt(stra[n]));
        }
        return ia;
    }

    function exploitCourses(root) {
        var exploited = [];
        var cells = root.querySelectorAll("#kbgrid_table_0 td");
        for (var i = 0; i < cells.length; i++) {
            var cell = cells[i];
            if (cell.id == undefined || cell.id.trim() == "") continue;
            var fontSlots = cell.querySelectorAll("div.timetable_con font");
            if (fontSlots.length != 9) continue;
            var courseDay = cell.id.split("-")[0];
            var courseName = fontSlots[0].innerText.trim().replace("\n", "");
            var courseTime = fontSlots[2].innerText.trim().replace("\n", "");
            var coursePlace = fontSlots[4].innerText.trim().replace("\n", "");
            var courseTeacher = fontSlots[6].innerText.trim().replace("\n", "");
            var courseClass = fontSlots[8].innerText.trim().replace("\n", "");

            var timeRegexp = /\((\d+)\-(\d+)节\)(\d+)\-(\d+)周/g;
            var timeMatch = timeRegexp.exec(courseTime);
            if (timeMatch == null || timeMatch.length != 5) continue;
            exploited.push({
                name: courseName,
                day: Number.parseInt(courseDay) % 7,
                time: stratoia([timeMatch[1], timeMatch[2]]),
                period: stratoia([timeMatch[3], timeMatch[4]]),
                teacher: courseTeacher,
                place: coursePlace,
                class: courseClass,
            });
        }
        return exploited;
    }

    var courses = [];
    if (TIMETABLE_IN_IFRAME) {
        document.querySelectorAll('iframe').forEach(item => {
            courses = courses.concat(exploitCourses(item.contentWindow.document));
        });
    } else {
        courses = courses.concat(exploitCourses(document));
    }
    var vCal = VCAL_HEADER;
    for (var m = 0; m < courses.length; m++) {
        var course = courses[m];
        for (var week = course.period[0]; week <= course.period[1]; week++) {
            if (course.period[0] > week && course.period[1] < week) continue;
            var beginTime = new Date();
            var endTime = new Date();
            var tzOffset = beginTime.getTimezoneOffset() * 60 * 1000;
            var tsOffset = (week - 1) * 7 * 24 * 60 * 60 * 1000 + course.day * 24 * 60 * 60 * 1000;
            beginTime.setTime(FIRST_DAY.getTime() + tsOffset);
            endTime.setTime(FIRST_DAY.getTime() + tsOffset);
            beginTime.setHours(TIME_MAPPING[course.time[0]][0], TIME_MAPPING[course.time[0]][1]);
            endTime.setHours(TIME_MAPPING[course.time[1]][2], TIME_MAPPING[course.time[1]][3]);
            beginTime.setTime(beginTime.getTime() + tzOffset);
            endTime.setTime(endTime.getTime() + tzOffset);
            // console.log(JSON.stringify(course));
            // console.log(date2tstr(beginTime) + ", " + date2tstr(endTime));
            vCal += getVEvent(course, week, beginTime, endTime);
        }
    }
    vCal += VCAL_TAIL;
    console.log("ZFN2VCAL by Makito (CCNU special)");
    if (courses.length <= 0) {
        console.error("Got zero courses. Please take a look at the config section.");
        return;
    }
    console.info("No errors have been found yet.");
    console.log("Courses in JSON format:");
    console.log(JSON.stringify(courses));
    console.log("Saving iCal file ...");
    var blob = new Blob([vCal], { type: 'text/calendar' }),
        anchor = document.createElement('a');
    anchor.download = "Courses" + ID;
    anchor.href = (window.webkitURL || window.URL).createObjectURL(blob);
    anchor.dataset.downloadurl = ['text/calendar', anchor.download, anchor.href].join(':');
    anchor.click();
    console.log("Workflow finished.");
})();
