#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from lcyframe import route
from base import BaseHandler, helper

@route("/imagecode")
class ImageCodeHandler(BaseHandler):
    """
    图片验证码
    """
    @helper.admin(0)
    def get(self):
        """
        获取验证码


        Request extra query params:
        - uuid # 随机串 type: str


        :return:
        :rtype:
        """
        code, code_data = self.model.BasicsModel.send_imagecode(self.params["uuid"])
        self.write_success(data={
            "code_data": code_data,
            "uuid": self.params["uuid"]
        })

    @helper.admin(0)
    def post(self):
        """
        校验图形验证码
        
        
        Request extra query params:
        - stype # 类型 type: int
        - uuid # 随机串 type: str
        - imgcode # 图形验证码 type: str
        

        :return:
        :rtype:
        """
        
        code = self.params["code"]
        uuid = self.params["uuid"]
        if not self.model.BasicsModel.vaild_imagecode(uuid, code):
            raise self.api_error.ErrorCommon("验证码错误")
        self.write_success()



@route("/smscode")
class SMSCodeHandler(BaseHandler):
    """
    短信验证码
    """
    @helper.admin(0)
    def get(self):
        """
        获取短信验证码
        
        
        Request extra query params:
        - stype # 类型,预留 type: int
        - uuid # 随机串,预留 type: str
        - mobile # 随机串 type: str
        

        :return:
        :rtype:
        """
        sms_code = self.model.BasicsModel.send_smscode(
            self.params["uuid"],
            self.params["mobile"],
            self.params["stype"]
        )
        self.write_success(data={"code": sms_code, "uuid": self.params["uuid"]})

    @helper.admin(0)
    def post(self):
        """
        短信验证码


        Request extra query params:
        - stype # 类型,预留 type: int
        - uuid # 随机串,预留 type: str
        - mobile # 随机串 type: str
        - smscode # 验证码 type: int


        :return:
        :rtype:
        """

        code = self.params["code"]
        uuid = self.params["uuid"]
        if not self.model.BasicsModel.vaild_smscode(uuid, code):
            raise self.api_error.ErrorCommon("验证码错误")
        self.write_success()

@route("/sendemail")
class SendEmailHandler(BaseHandler):
    @helper.admin(0)
    def get(self):
        """
        测试发送邮件
        """

        """
        发送试用申请通过通知
        :param company: 试用申请企业名,
        :param username: 用户名称
        :param account: 用户账号
        :param email: 接收邮箱
        :param password: 密码
        :param domain_name: 授权域名
        :param activate_url: 激活链接
        """
        raise
        args = ["商户", "用户名称", "用户账号", ["123220663@qq.com"], "密码", "授权域名", "激活链接"]
        self.model.ActivateModel.email_avtivate_link(*args,
                                                     license="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTM2MTI4MDAsImlhdCI6MTY2MjExNDMyMywiZGF0YSI6eyJhdXRob3JpemF0aW9uIjo2OSwiY29tcGFueSI6MjcsInNlcnZpY2VfbGlmZSI6MzAsInByb2R1Y3RfaWQiOjcsInByb2R1Y3RfbmFtZSI6Ilx1NjgwN1x1NTFjNlx1NGVhN1x1NTRjMSIsInByb2R1Y3RfdHlwZSI6MSwiYXV0aF9zdGF0ZSI6MCwidmVyc2lvbiI6MS4wLCJhY3RpdmVfbW9kZSI6MCwiaXNzdWVkX2F0IjoiMjAyMi0wOS0wMiAxMDoyNToyMyIsImF1dGhfdmFsaWRfYXQiOiIyMDIzLTA5LTAyIDAwOjAwOjAwIn19.D0NnyvK7323o50bEFW5PPuTX4Pz7oFw80cN1Do_2Bw8",
                                                     tryapply=True
                                                     )

        # 发送邮件激活
        # args = ["商户", ["123220663@qq.com"]]
        # self.model.ActivateModel.email_avtivate_link(*args, license="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTM2MTI4MDAsImlhdCI6MTY2MjExNDMyMywiZGF0YSI6eyJhdXRob3JpemF0aW9uIjo2OSwiY29tcGFueSI6MjcsInNlcnZpY2VfbGlmZSI6MzAsInByb2R1Y3RfaWQiOjcsInByb2R1Y3RfbmFtZSI6Ilx1NjgwN1x1NTFjNlx1NGVhN1x1NTRjMSIsInByb2R1Y3RfdHlwZSI6MSwiYXV0aF9zdGF0ZSI6MCwidmVyc2lvbiI6MS4wLCJhY3RpdmVfbW9kZSI6MCwiaXNzdWVkX2F0IjoiMjAyMi0wOS0wMiAxMDoyNToyMyIsImF1dGhfdmFsaWRfYXQiOiIyMDIzLTA5LTAyIDAwOjAwOjAwIn19.D0NnyvK7323o50bEFW5PPuTX4Pz7oFw80cN1Do_2Bw8")
        return self.write_success()



@route("/download")
class DownloadHandler(BaseHandler):
    @helper.admin(0)
    def get(self):
        """
        下载文件
        stype: 1授权文件

        """
        filepath = {
            1: self.app_config["data_config"]["authorizedoc"],
            2: self.app_config["data_config"]["followup"]
        }[self.params["stype"]]
        file_id = self.params["name"]
        path = os.path.join(self.app_config["data_config"]["data_base"], filepath, file_id)
        if not os.path.exists(path):
            raise self.api_error.ErrorCommon("不数据不存在")

        with open(os.path.join(self.app_config["data_config"]["data_base"], filepath, file_id), "rb") as p:
            # while True:
            data = p.read()

            self.set_header("charset", 'UTF-8')
            # self.set_header("content_type", 'application/download')
            self.set_header("Content_Type", 'application/octet-stream')
            self.set_header("Content_Disposition", f'attachment; filename="{file_id}"')
            # super(BaseHandler, self).write(base64.b64encode(data).decode())
            super(BaseHandler, self).write(data)
