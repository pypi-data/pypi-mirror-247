import requests

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': '__51vcke__JxH1j8MO5hiukbBc=783944bb-1c94-50ba-a043-aa14dbaa1f49; __51vuft__JxH1j8MO5hiukbBc=1686534034566; tkik_2132_nofavfid=1; tkik_2132_smile=1D1; tkik_2132_onlineindex=1; tkik_2132_saltkey=Tn53Q5Cz; tkik_2132_lastvisit=1700552253; '
              'tkik_2132_auth=89527ZByyErIC6fddlfzgSCAON7U%2BM%2FT%2FT84uQbi%2B0JQGkR3iBUXESkyb0shirDbGoBxxfXZTTFWwa5QBPL6KeEzoQ; tkik_2132_lastcheckfeed=44779%7C1700555868; tkik_2132_forum_lastvisit=D_38_1702382386D_40_1702382620; tkik_2132_visitedfid=40D38D44D2D41; tkik_2132_sid=CcccaQ; '
              'tkik_2132_lip=123.178.214.209%2C1702382368; tkik_2132_ulastactivity=02c2McDt1qmQf4mR%2F5ylApMn1dnmqx37tyGpl17EyrE97WHCr173; __51uvsct__JxH1j8MO5hiukbBc=27; tkik_2132_onlineusernum=288; tkik_2132_sendmail=1; '
              '__vtins__JxH1j8MO5hiukbBc=%7B%22sid%22%3A%20%22c3e382e4-2fdd-5f2b-8587-f6293d5903f0%22%2C%20%22vd%22%3A%204%2C%20%22stt%22%3A%20680851%2C%20%22dr%22%3A%2015065%2C%20%22expires%22%3A%201702644109687%2C%20%22ct%22%3A%201702642309687%7D; tkik_2132_lastact=1702642318%09plugin.php%09; '
              'tkik_2132_creditbase=0D318D31D136D0D0D0D0D0; tkik_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; tkik_2132_creditnotice=0D1D0D0D0D0D0D0D0D44779; tkik_2132_misigntime=1702642318',
    'Host': 'legado.cn',
    'Referer': 'https://legado.cn/k_misign-sign.html',
    'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': 'Windows',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
}

data = requests.post(url='https://legado.cn/plugin.php?id=k_misign:sign&operation=qiandao&formhash=704fbad1&format=empty&inajax=1&ajaxtarget=',
                     headers=headers, verify=False)
print(data.text)
