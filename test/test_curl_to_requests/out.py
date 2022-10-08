import requests

# test request A
res = requests.get(
    url = "https://music.163.com/song",
    headers = {
        'authority': 'music.163.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://music.163.com/',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    },
    cookies = {
        'WNMCID': 'hlgusj.1644759482271.01.0',
        'WEVNSM': '1.0.0',
        'NMTID': '00OBSN_WyfQmFxackvJguBWDNsu1gUAAAF-804A_w',
        'WM_TID': '4budwMXm409FBVQQQVZq%2BLofYfgFCmf3',
        '_ntes_nnid': 'd31642e9dcbb099fbc815d926fbfe7bb,1660056866048',
        '_ntes_nuid': 'd31642e9dcbb099fbc815d926fbfe7bb',
        '_iuqxldmzr_': '32',
        'JSESSIONID-WYYY': '2nZviTJAnaQUrOkSgeUPKK0cjP7cXtRwn5cel4c9t%2BO%5CMncSnGyiAproqKzczb7p27t%2BTe0AjjJ%2FpVt7u1PTDHQiqoKg8PEliS0lKRyCJJw4FRrXNUVldVb2irdf8oSm7sogWROQYJzUs%2FX33kKAFxINom%2Frd1wbKxxwGyA4K%2Bt8IhYK%3A1663254094494',
        'WM_NI': 'CtHJVI3pH6WIhLGZk%2Bnc5%2Bb6249qD%2B4sylbaJygS7AADxqfX9YbdoR4ZITbgRGAZ8yfx3r6UIQ%2F5%2Bu72%2FD6bQIlfsG%2FM3W6si0ZmUmkGeDh4kNjaMnHfmELU397KySvOODY%3D',
        'WM_NIKE': '9ca17ae2e6ffcda170e2e6eeb6e8549c868e87ec80ab8e8eb6c44a868e9a87c450ba9f8888d33eb3888f92cb2af0fea7c3b92a81ac88abd543f1b088d7d643ac9489bbea21aebdfbcce13ef2ecf792c721f8adb78de16b8aa7a9b4b64b839cb892e554fb87ae85ee5af88687b5e16d92998fbbbb73a6a8fd93b55f8b8fe1d6aa7ff5eee1a5b56a9397a487f24ded93fdb8b579abf0968ed867a999aba5eb40a992a682d0668cbaa3a6cf5ff1e7f9acfc59b69181a5dc37e2a3',
    },
    params = {
        'id': '1925052534',
    },
)


# test request B
res1 = requests.post(
    url = "https://fanyi.baidu.com/v2transapi",
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Acs-Token': '1663225385326_1663259610544_gDkRoDh4Yx6E2NR5K/14+q/i/Y6X4SYFepqWvQ3hdEQsnjhr1ujNAU129rKW6peObqN2e5o1M5bDuc4E68SXIKyp1K3Qalnk4/7QIkTYH0MjmD1OrvozdmTT2aog6T7P1oejp3PYGccfhoEiaZdRERg83hvOs9VQRKuX6/tjeISMoCSfr0ha82tK8FGLFsvKsFVwl7kB3OqJ/Th7boLehDqsZ5K8xUDafAPw0ND+AGpP4GwZAc1PHRmS+590+XDegfO6zKSjorIhWvzB4LH/wbEPShTJv3OGCs1shog7KJZtU6AZK1yPW8RiDJ1oTaAXwOvSDCklRIBULvg/AXzxKw==',
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
        'BA_HECTOR': '0galah2ga1a50g2k2g0h3eik1hi5jrg19',
        'ZFY': '8GEyvUvPoPZxsV6gdv:BaP4hkOLTQMxRK0YQJuGjvUag:C',
        'BAIDUID_BFESS': '9BBB68671D64E711DEF0C17F260BE7C1:FG=1',
        'ariaDefaultTheme': 'undefined',
        'RT': '"z=1&dm=baidu.com&si=outaaskggf&ss=l82pug1n&sl=4&tt=5hz&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1x01&ul=2b24&hd=2b2j"',
        'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1663030343,1663122188,1663206092,1663258116',
        'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1663258116',
        'ab_sr': '1.0.1_ZDFjYzhhNjEzMzk0NDFlZWQ3OTk4YzI1MDk4NzMyNzU5ZGRkZDcyMjdiMjdkNjgyMTE0Y2QzMmE1ZjFjYzA3OWZiYjQxODQ5YzI4ZWU2NGE2YzM5NjUzZDNhNWFhOGE5NjJiNWY4YjE0MmEzY2YyYWIwOTQxZDQ3NmJlYzJjZDcyNWM5ZDhhYjQwNGZjNDU1ZDcyMDE3NzVjNjYxMjhlYQ==',
        'BDRCVFR[QZ3_UL1MfH_]': 'mk3SLVN4HKm',
        'delPer': '0',
        'PSINO': '6',
        'H_PS_PSSID': '26350',
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


