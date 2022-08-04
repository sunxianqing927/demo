# Python实用宝典
# 2021/11/13
import json
import hashlib
import base64
import hmac
import time
#from tracemalloc import start
#from webbrowser import get
import requests
from urllib.parse import quote_plus

from get_bin_files import *

dd_token="dd_token",
dd_secret="dd_secret"

class Messenger:
    def __init__(self, token=dd_token, secret=dd_secret):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json;charset=utf-8'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}
 
    def send_text(self, content):
        """
        发送文本
        @param content: str, 文本内容
        """
        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

#    m = Messenger(dd_token,dd_secret)
#    m.send_text("your msg")
