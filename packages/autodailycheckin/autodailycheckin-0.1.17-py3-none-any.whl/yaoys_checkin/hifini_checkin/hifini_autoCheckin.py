# -*- coding: utf-8 -*-
# @FileName  :ableSci_checkin.py
# @Time      :2022/8/20 8:19
# @Author    :yaoys
# @Desc      :
import hashlib
import json
import os
import re
import time

import requests
from requests.cookies import cookiejar_from_dict

from yaoys_checkin.checkin_util.checkin_log import get_checkin_logger
from yaoys_checkin.checkin_util.logutil import log_info
from yaoys_checkin.model.all_class_parent import allClassParent

header = {
    # 'x-requested-with': 'XMLHttpRequest',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://www.hifini.com/sg_sign.htm',
    # 'origin': 'https://www.hifini.com',
    'Sec-Ch-Ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': 'Windows',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57'

}

UA_Header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Referer': 'https://www.hifini.com/sg_sign.htm',
    'Sec-Ch-Ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': 'Windows',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57'
}


class hifini(allClassParent):

    def __init__(self, **kwargs):
        super(hifini, self).__init__(**kwargs)

        self.session = None
        if self.logger is None:
            self.logger, log_config = get_checkin_logger(config_file=self.config_file, log_name=str(os.path.basename(__file__)).split('.')[0])

        self.checkin_message, self.is_success = self.hifini_sign()

    def __stringtoHex(self, acSTR):
        val = ""
        for i in range(len(acSTR) - 1):
            strr = acSTR[i]
            code = ord(strr)
            if isinstance(code, int):
                val += str(code + 1)
            else:
                val += str(int(code) + 1)
        return val

    def __md5encode(self, word):
        return hashlib.md5(word.encode()).hexdigest()

    def __hifini_checkin__(self):
        if self.cookie is None:
            raise Exception('The cookie is None')
        if self.cookie.startswith("cookie:"):
            self.cookie = self.cookie[len("cookie:"):]
        self.session = requests.sessions.session()
        cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in self.cookie.split("; ")}
        resp = self.session.get(url='https://www.hifini.com/sg_sign.htm', headers=header, verify=False,
                                cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True))

        if resp.status_code == 403 and 'sg_sign.htm' in resp.text:
            return "Cookie已经失效,请更新Cookie", False

        if resp.status_code != 200:
            return "签到失败,请联系管理员", False

        # if "今天已经签过" in resp.text:
        #     return "已经签到过，请勿重复签到", True
        # 需要进行人机验证
        if "slideBox" in resp.text:

            js_url = re.findall('<script type="text/javascript" src="(.*?)"></script>', resp.text)

            resp = self.session.get("https://www.hifini.com" + js_url[0],
                                    headers=UA_Header, verify=False, cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True))

            js_text = resp.text.replace("(", "")
            js_text = js_text.replace(")", "")

            key_value = re.findall('document.getElementById"bt-info",key="(.*?)",value="(.*?)";function stringtoHexacSTR', js_text)

            key = key_value[0][0]
            value = self.__md5encode(self.__stringtoHex(key_value[0][1]))
            resp = self.session.get("https://www.hifini.com/" + "a20be899_96a6_40b2_88ba_32f1f75f1552_yanzheng_huadong.php?type=ad82060c2e67cc7e2cc47552a4fc1242&key="
                                    + key + "&value=" + value,
                                    headers=UA_Header, verify=False, cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True))

            if resp.status_code != 200 or "slideBox" in resp.text:
                return "绕过人机验证失败,请手动签到", False

            resp = self.session.get(url='https://www.hifini.com/sg_sign.htm', headers=header, verify=False,
                                    cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True))

            resp = self.session.post(url='https://www.hifini.com/sg_sign.htm', headers=header, verify=False,
                                     cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True))

            if resp.status_code == 403 and 'sg_sign.htm' in resp.text:
                return "Cookie已经失效,请更新Cookie", False

            if resp.status_code != 200:
                return "签到失败,请联系管理员", False

        resp = resp.json()
        checkin_message = ''
        if 'message' in resp:
            checkin_message = resp['message']

        # 获取金币数量
        resp = self.session.get(url='https://www.hifini.com/my.htm', headers=header, verify=False,
                                cookies=cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True))
        if resp.status_code != 200:
            checkin_message += ', 获取每日金币数量失败'
            return checkin_message, True
        jinbi_count = re.findall(r'<span class="text-muted">(.*?)<em style="color: #f57e42;font-style: normal;font-weight: bolder;">(.*?)</em>', resp.text)
        if len(jinbi_count[0]) != 2:
            checkin_message = checkin_message + ', ' + '金币：查询失败'
        else:
            checkin_message = checkin_message + ', ' + jinbi_count[0][0] + jinbi_count[0][1]

        return checkin_message, True

    def hifini_checkin_main(self):
        if self.cookie is not None and len(self.cookie) > 0:
            account_checkin_message, success = self.__hifini_checkin__()
            # 存在账户签到信息，说明成功执行了签到
            if account_checkin_message is not None and len(account_checkin_message) > 0:
                log_info(f"[hifini_Account_{self.account_index}]:" + str(account_checkin_message), my_logger=self.logger)
        else:
            return '', False
        return f"[hifini_Account_{self.account_index}] " + str(account_checkin_message) + "      \n", success

    def hifini_sign(self):

        if self.checkin_verification is None or self.checkin_verification == '':
            return ''.join(self.checkin_message), False
        success = False
        try:
            # 科研通签到
            log_info('*******************************hifini checkin*******************************', my_logger=self.logger)
            if isinstance(self.checkin_verification, str) is True:
                self.cookie = self.checkin_verification
                self.account_index = 1
                message, success = self.hifini_checkin_main()
                self.checkin_message.append(message)
            elif isinstance(self.checkin_verification, list) is True:
                for i in range(0, len(self.checkin_verification)):
                    if isinstance(self.checkin_verification[i], dict) is True:
                        self.cookie = self.checkin_verification[i]['cookie']
                        self.account_index = i + 1
                        message, success = self.hifini_checkin_main()
                        self.checkin_message.append(message)
                    else:
                        log_info('hifini config error', my_logger=self.logger)
                        self.checkin_message.append('hifini config error')

                    if self.more_time_sleep > 0:
                        time.sleep(self.more_time_sleep)
            else:
                log_info('hifini config error' + '    \n', my_logger=self.logger)
                self.checkin_message.append('hifini config error' + '    \n')

            log_info('*******************************hifini checkin complete*******************************', my_logger=self.logger)
            return ''.join(self.checkin_message), success
        except Exception as e:
            self.checkin_message.append('main function: hifini checkin error, the error is ' + str(e) + '    \n')
            log_info('main function: hifini checkin error, the error is ' + str(e) + '    \n', my_logger=self.logger)
            log_info('*******************************hifini error*******************************', my_logger=self.logger)

        return ''.join(self.checkin_message), True
