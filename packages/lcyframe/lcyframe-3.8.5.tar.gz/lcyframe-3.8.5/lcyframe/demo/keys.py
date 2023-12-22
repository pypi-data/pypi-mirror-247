#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
redis Keys
"""
TOKEN_MARK = "token:%s"    # 登陆标记
NONCE_MARK = "nonce:%s"    # 重复请求标记

imagecode_key = "imagecode:%s"
imagecode_exp = 1 * 60

# 短信验证码每个账号每天最多只能收到10条
# 短信验证码每个IP每天最多只能收到500条
sms_times = 10
smscode_interval = "smsinterval:%s"     # 间隔1分钟
smscode_times = "smstimes:%s"           # 每天发送最多10条
smscode_key = "smscode:%s"              # 验证码
smscode_exp = 5 * 60                    # 有效期

