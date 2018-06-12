import requests


cookies = {
    'BIGipServerpool_jwc_xk': 'xxx',
    'JSESSIONID': 'xxx',
}

headers = {
    'Origin': 'http://xk.ccnu.edu.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://xk.ccnu.edu.cn//xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=xxxxxxxxxx',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = (
    ('gnmkdm', 'N253512'),
    ('su', 'xxxxxxxxxx'),
)

data = [
  ('jxb_ids', 'xxxxxxxxxxDF474FE0531Dxxxxxxxxxx'),
  ('kch_id', '3300xxxx'),
  ('xsbxfs', '0'),
  ('rwlx', '2'),
  ('rlkz', '0'),
  ('rlzlkz', '0'),
  ('sxbj', '0'),
  ('xxkbj', '0'),
  ('qz', '0'),
  ('cxbj', '0'),
  ('xkkz_id', '6DEFC870CF6C2041E0531D50A8C07F4F'),
  ('njdm_id', '2017'),
  ('zyh_id', '220'),
  ('kklxdm', '10'),
  ('xklc', '1'),
  ('xkxnm', '2018'),
  ('xkxqm', '3'),
]

response = requests.post('http://xk.ccnu.edu.cn/xsxk/zzxkyzb_xkBcZyZzxkYzb.html', headers=headers, params=params, cookies=cookies, data=data)

print(response)
