import os
from loghelper import log
from request import http
import time

token = ''
if os.getenv('AutoMihoyoBBS_captcha_token') is not None:
    token = os.getenv('AutoMihoyoBBS_captcha_token')

def game_captcha(gt: str, challenge: str):
    response = geetest(gt, challenge, 'https://passport-api.mihoyo.com/account/ma-cn-passport/app/loginByPassword')
    # 失败返回None 成功返回validate
    if response is None:
        return response
    else:
        return response['validate']


def bbs_captcha(gt: str, challenge: str):
    response = geetest(gt, challenge,
                       "https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id"
                       "=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon")
    # 失败返回None 成功返回validate
    if response is None:
        return response
    else:
        return response['validate']


def geetest(gt: str, challenge: str, referer: str):
    print(gt)
    print(challenge)
    
    response = http.post('http://api.damagou.top/apiv1/jiyanRecognize.html', data={
        'userkey': token,
        'gt': gt,
        'challenge': challenge,
        'headers': {
            'Referer': referer
        }
    }, timeout=6000)
    data = response.json()
    if data['status'] == 0:
        return data["data"]
    else:
        log.warning(data['msg'])  # 打码失败输出错误信息
        return None
    
