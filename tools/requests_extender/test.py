# Name: Test RequestsExtender
# Date: 2022-09-20
# Author: Ais
# Desc: None


import requests
from requests_extender import RequestsExtender


# 加载扩展
RequestsExtender.load({
    "req": [
        RequestsExtender.disp()
    ],
    "res": [
        RequestsExtender.dataflow(),
        RequestsExtender.exporter()
    ]
})


# 测试请求
res = requests.post(
    url = "https://fanyi.baidu.com/v2transapi",
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Acs-Token': '1663657391773_1663685106731_3j/Ng0BVqZkaO9cQk19lZCAtySa0LyzRGB9sa2MFtKIQf4IiSaNnChNooaFKMficIw6SVLVaH4YY64FNKdLkZ29EPDUKPXVsZ8puw5ddydVti/OuapJTTXer6Od3wcoTsZAdmCH+VxrbNpZ1up9+DraiINXjtZoWB6ZtPJC0bJIUXAZAH9kR5Q3tr/tVZVtjG+Bv6A0Pmm6ex9urLB23zrKik5XcfZgqSg3nwbX7D3bnAoWl+VSqGfGLZzEwJ77jgl2eTBPTkuwvzfaI8lUHVOL7qBA+xoi8BXX4QVwRnY8=',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://fanyi.baidu.com',
        'Referer': 'https://fanyi.baidu.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    },
    cookies = {
        'BIDUPSID': '9BBB68671D64E71189A7B56AD61A75A8',
        'PSTM': '1659446564',
        'BAIDUID': '9BBB68671D64E711DEF0C17F260BE7C1:FG=1',
        'APPGUIDE_10_0_2': '1',
        'SOUND_SPD_SWITCH': '1',
        'SOUND_PREFER_SWITCH': '1',
        'REALTIME_TRANS_SWITCH': '1',
        'HISTORY_SWITCH': '1',
        'FANYI_WORD_SWITCH': '1',
        'MCITY': '-%3A',
        'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
        'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1663549917,1663579371,1663596106,1663640111',
        'H_PS_PSSID': '26350',
        'BAIDUID_BFESS': '9BBB68671D64E711DEF0C17F260BE7C1:FG=1',
        'delPer': '0',
        'BA_HECTOR': '0h20ag04ag2h218g8h0gb6j11hiiffp18',
        'ZFY': '8GEyvUvPoPZxsV6gdv:BaP4hkOLTQMxRK0YQJuGjvUag:C',
        'BDRCVFR[QZ3_UL1MfH_]': 'mk3SLVN4HKm',
        'ariaDefaultTheme': 'undefined',
        'RT': '"z=1&dm=baidu.com&si=0pq6d1m423y&ss=l8a0j9tq&sl=3&tt=6bn&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1lcu&ul=27fp&hd=27g7"',
        'PSINO': '6',
        'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1663685098',
        'ab_sr': '1.0.1_NWNhM2M1NmIyOTU1NmVhMDVlMGNiZDgyMmNmODI5NDI5NzliNDZjZjIzNDkzODQxMGVkYWExYTIxOGJiNzIxYmVhZmNmYmMwMGMzZjkxNmQxODQyMzYzMGEwYjEwNDM5MDkzMWVmOGI2Nzk1NmY3ZTI2ODUyYmQ1MjcxOWU2ZmJjY2MyZjRlMzUxYTNhYTkxOWM3ZjcwNDhiZGZiMmI3NA==',
    },
    params = {
        'from': 'en',
        'to': 'zh',
    },
    data = {
        'from': 'en',
        'to': 'zh',
        'query': 'test',
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': '431039.159886',
        'token': '9b264c989222dec8ee4b1a1f9e8565f7',
        'domain': 'common',
    }
)

res1 = requests.get(
    url = "https://fanyi.baidu.com/",
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    },
    cookies = {
        'BIDUPSID': '9BBB68671D64E71189A7B56AD61A75A8',
        'PSTM': '1659446564',
        'BAIDUID': '9BBB68671D64E711DEF0C17F260BE7C1:FG=1',
        'APPGUIDE_10_0_2': '1',
        'SOUND_SPD_SWITCH': '1',
        'SOUND_PREFER_SWITCH': '1',
        'REALTIME_TRANS_SWITCH': '1',
        'HISTORY_SWITCH': '1',
        'FANYI_WORD_SWITCH': '1',
        'MCITY': '-%3A',
        'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
        'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1663549917,1663579371,1663596106,1663640111',
        'H_PS_PSSID': '26350',
        'BAIDUID_BFESS': '9BBB68671D64E711DEF0C17F260BE7C1:FG=1',
        'delPer': '0',
        'BA_HECTOR': '0h20ag04ag2h218g8h0gb6j11hiiffp18',
        'ZFY': '8GEyvUvPoPZxsV6gdv:BaP4hkOLTQMxRK0YQJuGjvUag:C',
        'BDRCVFR[QZ3_UL1MfH_]': 'mk3SLVN4HKm',
        'ariaDefaultTheme': 'undefined',
        'RT': '"z=1&dm=baidu.com&si=0pq6d1m423y&ss=l8a0j9tq&sl=3&tt=6bn&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1lcu&ul=27fp&hd=27g7"',
        'PSINO': '6',
        'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1663685098',
        'ab_sr': '1.0.1_NWNhM2M1NmIyOTU1NmVhMDVlMGNiZDgyMmNmODI5NDI5NzliNDZjZjIzNDkzODQxMGVkYWExYTIxOGJiNzIxYmVhZmNmYmMwMGMzZjkxNmQxODQyMzYzMGEwYjEwNDM5MDkzMWVmOGI2Nzk1NmY3ZTI2ODUyYmQ1MjcxOWU2ZmJjY2MyZjRlMzUxYTNhYTkxOWM3ZjcwNDhiZGZiMmI3NA==',
    },
)

res2 = requests.get(
    url = "https://fanyiapp.cdn.bcebos.com/cms/image/480f948019d284081745a58783076905.png",
)


