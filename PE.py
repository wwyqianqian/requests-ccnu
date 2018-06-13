import json


def printList(PElist):
    tplt = "{0:<20}\t{1:<35}\t{2:<5}\t{3:<8}\t{4:<8}\t{5:<20}"
#   print(tplt.format("教授", " 课程id", "人数", "体育课", "是否本校", "上课时间", chr(12288)))
    for i in range(0,len(PElist)):
        pe = PElist[i]
        with open('/Users/qianqian/Desktop/physical.txt', 'a', encoding='utf-8') as f:
            print(i+1, tplt.format(pe['jsxx'], pe['jxb_id'], pe['jxbrs'], pe['jxdd'], pe['jxms'], pe['sksj']), file=f) 

def main():
    with open('/Users/qianqian/Desktop/ccnu.txt', 'r') as f:
        data = f.read()
    PE = json.loads(data) 
    printList(PE)

main()
