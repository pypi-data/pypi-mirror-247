# coding=utf-8
import os, re
import logging
import random
import time
from datetime import datetime, date
import zlib, hmac
from bson import BSON, ObjectId
from functools import wraps
from lcyframe.libs import utils, funts, cprint, JWT, aes, Rsa, errors
from utils import errors, keys


def get_excel_url(host, img, path=None):
    """excel"""
    if path is None:
        path = "/data/excel"

    if "http" in host and host.startswith("http"):
        pass
    else:
        host = "http://" + host

    p = host + path
    p = os.path.join(p, img)
    return p


def get_imge_url(host, img, path=None):
    """******"""
    if path is None:
        path = "/data"

    if "http" in host and host.startswith("http"):
        pass
    else:
        host = "http://" + host

    p = os.path.join(host, path, img)
    return p


def save_filedata(data, base_path, **kwargs):
    """保存文件"""
    if not data:
        return "", ""

    filename = gen_filename(data, **kwargs)
    save_path = gen_filepath(base_path, filename)

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    if not os.path.exists(save_path):
        with open(save_path, "wb") as f:
            body = data["body"] if isinstance(data["body"], bytes) else data["body"].encode("u8")
            f.write(body)

    return filename, save_path


def gen_filepath(base_path, filename=None):
    if not os.path.exists("%s" % base_path):
        os.makedirs("%s" % base_path)

    save_path = "%s/%s" % (base_path, filename)
    return save_path


def gen_filename(file_data, prefix="", suffix="", name_type="unique", require_format=[], require_size=0):
    """
    生成文件名
    根据数据md5对文件去重
    :param body:
    :param name_type: unique名称按数据去重，date 按时间格式命名 random 随机命名
    :return:

    """

    metadata = get_fileinfo(file_data, require_format=require_format, require_size=require_size)

    if name_type == "unique":
        filename = metadata["unique_name"]
    elif name_type == "date":
        filename = "%s-%s" % (datetime.now().strftime("%Y%m%d%H%M%S"), str(utils.random_int(4)))
    elif name_type == "random":
        filename = str(utils.gen_random_sint(16))
    else:
        filename = metadata["name"]

    if metadata["format"]:
        return "%s%s%s.%s" % (prefix, filename, suffix, metadata["format"])
    else:
        return "%s%s%s" % (prefix, filename, suffix)


def get_fileinfo(file_data=None, file_path=None, require_format=[], require_size=0):
    """
    读取文件基本信息
    :param file_data:
    :return:
    """
    if file_data:
        if not isinstance(file_data, dict):
            file_data = {
                "body": file_data,
                "filename": "default"
            }
        body = file_data["body"]
        filename = file_data["filename"]
        unique_name = utils.md5(body if isinstance(body, bytes) else body.encode("u8"))
        name, format = file_data["filename"].rsplit(".", 1) if "." in file_data["filename"] else (file_data["filename"], "")
        # TODO Fix 包含有以下几种符号的文件名，会导致系统解压命令失败：'('、')'。如需在线调用系统命令解压，请打开注释.
        #  推荐使用python的Patool库进行统一加解压，可避免此问题
        # if format in ["rar", "zip", "pkg", "gz", "tar", "jar", "7z"]:
        #     if name.find("(") or name.find(")"):
        #         name = name.replace("(", "（").replace(")", "）")
        #
        #     filename = name + "." + format if format else name

        size = len(body)
    elif file_path and os.path.exists(file_path):
        with open(file_path, "r") as p:
            body = p.read()
            unique_name = utils.md5(body)
            name, format = file_data.split("/")[-1].split(".")
            size = len(body)
    else:
        raise

    if require_format and format.lower() not in require_format:
        raise errors.UploadError("请上传指定格式：" + ",".join(require_format))
    if require_size and size > require_size:
        raise errors.UploadError("大小不能超过%sM" % int(require_size/1024/1024))

    return {
        "filename": filename,
        "name": name,
        "format": format.lower(),
        "size": size,
        "unique_name": unique_name,
        "unique_filename": ("%s.%s" % (unique_name, format)) if format else unique_name
    }


def check__forestall_brute(app, key):
    """
    防止暴力破解密码登录
    登录前判断
    """
    if not hasattr(app, "forestall_brute_mapping"):
        return True
    else:
        logs = app.forestall_brute_mapping.get(key, {"count": 0, "ts": 0})
        if logs and logs["count"] >= 10 and logs.get("expire") > utils.now():
            raise errors.ErrorInvalid("你的操作已被系统判定为攻击行为")
        else:
            return True

def add_forestall_brute(app, key):
    """
    防止暴力破解密码登录
    当密码错误后，将key加入规则
    如次数得到指定值，将限定一段时间内不能登录
    """
    if not hasattr(app, "forestall_brute_mapping"):
        setattr(app, "forestall_brute_mapping", {})
    logs = app.forestall_brute_mapping.get(key, {"count": 0, "ts": 0})
    logs["count"] += 1
    logs["ts"] = utils.now()
    if logs["count"] >= 10:
        logs["expire"] = utils.now() + 15*60
    app.forestall_brute_mapping[key] = logs

def remove_forestall_brute(app, key):
    """
    防止暴力破解密码登录,以下操作后，移除key
    登陆成功后
    修改密码后
    """
    if hasattr(app, "forestall_brute_mapping"):
        app.forestall_brute_mapping.pop(key, False)

def get_excel_path(root_path, file_name=None):
    if not file_name:
        file_name = "%s.xlsx" % (datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(0, 99)))

    path = datetime.now().strftime("%Y%m%d")

    base_path = 'data/excel'
    if not os.path.exists("%s/%s/%s" % (root_path, base_path, path)):
        os.makedirs("%s/%s/%s" % (root_path, base_path, path))

    save_path = "%s/%s/%s/%s" % (root_path, base_path, path, file_name)

    file_name = '%s/%s' % (path, file_name)

    return save_path, file_name


def get_now_time_tuple(ts):
    d = utils.int_to_date_string(ts, fm="%d")
    m = utils.int_to_date_string(ts, fm="%m")
    y = utils.int_to_date_string(ts, fm="%Y")
    return y, m, d


def pc_or_mobile(ua):
    """
    判断客户端PC还是手机端
    :param ua: ******User-Agent******
    :return:
    """
    factor = ua
    is_mobile = False
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp' \
                    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)' \
                    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)' \
                     r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)' \
                     r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw' \
                     r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8' \
                     r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit' \
                     r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)' \
                     r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji' \
                     r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx' \
                     r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi' \
                     r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)' \
                     r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg' \
                     r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21' \
                     r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-' \
                     r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it' \
                     r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)' \
                     r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)' \
                     r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit' \
                     r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'

    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(factor) != None:
        is_mobile = True
    user_agent = factor[0:4]
    if _short_matches.search(user_agent) != None:
        is_mobile = True

    return is_mobile

def tts():
    return time.time() * 1000

def get_argument(self):
    """
    ******
    :param self:
    :return:
    """
    argument = {}
    try:
        keys = self.params.keys()
        for key in keys:
            if key == "secret_key":
                continue
            argument[key] = self.get_argument(key)
    except:
        argument = {k: v[0] for k, v in self.request.body_arguments.items() or self.request.arguments.items()}

    return argument


def admin(permission_bit=0):
    """
    认证：支持多个客户端同时访问
    1、验证是否登录：token
    2、验证是否合法请求：sign
    3、验证是否来自管理端请求（可指定其他端）
    :param permission_bit: 0 游客可访问
    :return:

    :::
    :::密码的加密流程：登录时需提交密码的密文格式
    1、前/后端均采用AES加密，输出十六进制字符串,参数详细如下（密钥写死在客户端）
        key: 82b0bfa746bdb72e310609070defa1cd
        iv: 3eddc41dd41239c8
        mode: ECB
        padding: zeropadding
    2、验签样例：
        密码明文：123456
        AES密文：016078ca0cbf7fa1655bc609418c576d

    ::: Token的生成流程：（登录后获得）
    1、后端讲提交的密码进行解密，得到明文，在通过md5(slat+password)与数据库进行对比
    2、如密码正确，则登陆成功，服务端将uid和当前时间戳组成dict={"uid": 100,"ts": 1636349973}
    3、用相同的秘钥（key=82b0bfa746bdb72e310609070defa1cd）通过JWT加密得到token，写入redis并返回给客户端
    4、客户端把uid和token放置在header里，发起后续请求

    Token的验证样例：
    加密前：{"uid": 100,"ts": 1636349973}
    JWT加密后："eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtZXNzYWdlIjp7InRzIjoxNjM2MzQ5OTczLCJ1aWQiOjEwMH0sImV4cCI6MTYzNjM1MzU3M30.h_eHntkiaTM9P4IQ_tDKuWo8ijdtH1Cwff9aM_3-N_M"

    ::: Sign数字签名生成流程（前端生成、后端验证。调用接口必须提供）
    1、客户端把uid和token放置在header里，每次调用接口时，服务端将在redis内重置该Token的有效期，如果key不存在，则提示客户端重新登陆
    2、在请求参数里新增timestamp、nonce参数；前者是当前请求的时间戳，后者是一个随机参数；
    3、利用&拼接在请求参数query_string里，服务端判断当前时间与提交的timestamp是否相差在1分钟内的接口，若是，正常请求，否则返回错误，防止重放攻击，防刷
    4、服务端每次收到请求后，都需要保存nonce到redis，过期时间1分钟，如果遇到重复的nonce，视为重复请求，返回错误，保证接口冥等性
    5、客户端把所有请求参数名按照首字母大到小（小写）方式进行排序（值为空的参数去掉），利用&拼接，得到待签名字符串str1
    6、将str1进行base64编码得到str2
    7、将token和str2拼接（token+str2），得到str3
    8、将str3进行md5加密（md5(str3)），输出十六进制字符串，得到sign
    9、验证：
        待加密参数：{"a": 1, "b": 2, "timestamp": 1634094357, "nonce": "tfbksz"}
        # p1 利用&拼接
        str1 = 'a=1&b=2&nonce=tfbksz&timestamp=1634094357'
        # p2 base64编码
        str2 = 'YT0xJmI9MiZub25jZT10ZmJrc3omdGltZXN0YW1wPTE2MzQwOTQzNTc='
        # p3 拼接token
        str3 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsImV4cCI6MTYzNDA5OTAxNn0.djsmWDtwBR2AGGF79HufFcN1ofD5NCW0QI9H59EMB-0YT0xJmI9MiZub25jZT10ZmJrc3omdGltZXN0YW1wPTE2MzQwOTQzNTc='
        # p4 md5加密 输出32位小写字符串
        sign = '990b897e66a59a976498ad0a5e29d9fd'

    """

    def wrap(method):
        @wraps(method)
        def has_role(self, *args, **kwargs):
            self.user_id = self.request.headers.get("uid", 0)
            if type(self.user_id) != int and self.user_id.isdigit():
                self.user_id = int(self.user_id)
            self.token = self.request.headers.get("token", "")
            if permission_bit:
                # 是否合法访问
                _check_token(self, permission_bit)

                # sign
                # _verifi_sign(self, self.token)

                # 只有超管账号允许访问系统端
                _check_admin(self)

            self.params = funts.get_params(self)

            # 对已登录的用户进行权限拦截
            _check_permissions(self, permission_bit)

            if self.app_config.get("logging_config", {}).get("level", "debug") == "debug":
                logging.debug(
                    "请求参数: " + (utils.to_json(utils.check2json(utils.pparams(self.request, params=self.params)))
                                if hasattr(self, "params") else str(utils.pparams(self.request) or {})))

            return method(self, *args, **kwargs)

        return has_role

    return wrap


def _check_token(self, permission_bit):
    token_debug = self.token_config.get("debug", False)
    if not token_debug:
        if permission_bit != 0:
            if not self.user_id or not self.token:
                raise errors.ErrorTokenInvalid

            jwt = JWT.JwtToken(self.token_config["secret"], self.token_config["expire"])
            try:
                if jwt.is_expire(self.token):
                    raise errors.ErrorTokenExpireInvalid

                if not jwt.is_validate(self.token):
                    raise errors.ErrorTokenInvalid

                payload = jwt.decode(self.token)
                if payload and payload["user_id"] != self.user_id:
                    raise errors.ErrorTokenInvalid

                self.set_header("Token", jwt.refresh_token(self.token))
            except Exception as e:
                raise errors.ErrorTokenInvalid


def _verifi_sign(self, token):
    """
    验签
    :param self:
    :param token:
    :param secret_key:
    :return:
    """

    def source_argument():
        """
        获取原始参数值
        """
        argument = {}
        try:
            keys = self.params.keys()
            for key in keys:
                if key == "secret_key":
                    continue
                argument[key] = self.get_argument(key)
        except:
            argument = {k: v[0] for k, v in self.request.body_arguments.items() or self.request.arguments.items()}

        return argument

    argument = source_argument()
    argument["timestamp"] = int(self.get_argument("timestamp", 0))
    argument["nonce"] = self.get_argument("nonce", "")
    sign = self.get_argument("sign", "")

    if not argument["timestamp"] or not argument["nonce"]:
        raise errors.ErrorMissingArgument("Missing timestamp, nonce")

    new_sign = gen_sign(token, **argument)

    if new_sign != sign:
        raise errors.ErrorTokenInvalid

    # ExpireQuery
    expire_query = int(self.token_config.get("expire_query", 0))
    if expire_query != 0:
        if utils.now() - argument["timestamp"] > expire_query:
            raise errors.ErrorExpireQuery

    # DuplicateQuery
    duplicate_query = int(self.token_config.get("duplicate_query", 0))
    if duplicate_query != 0:
        if self.redis.exists(keys.NONCE_MARK % argument["nonce"]):
            raise errors.ErrorDuplicateQuery

        self.redis.setex(keys.NONCE_MARK % argument["nonce"], duplicate_query, 1)


def _check_admin(self):
    self.is_admin = True

    self.member = self.model.AdminModel.get_admin(self.user_id)
    if not self.member:
        raise errors.ErrorUserNotFound
    if self.member["company_id"] != 1:
        raise errors.ErrorNoRolePermission("无权访问")

    # self.gid = self.member["gid"]


def _check_permissions(self, permission_bit):
    """
    验证权限
    """
    if permission_bit and self.request.path not in ["/permission/enable"]:
        has_perm, msg = self.model.RBACPermissionModel.has_permission(self)
        if not has_perm:
            raise errors.ErrorNoApiPermission


def verifi_ip(self, ip_list):
    """
    验证白名单
    :param self:
    :param ip_list:
    :return:
    """
    if not self.application.app_config["security"]["verifi_ip"]:
        return

    ip_list = [ip.encode("u8") for ip in ip_list]
    remote_ip = self.request.remote_ip.encode("u8")
    s = "*" in ip_list or remote_ip in ip_list
    if not s:
        raise errors.ErrorTranIpError


def gen_sign(token, **kwargs):
    """
    验签 3.0
    :param sign:
    :param kwargs:
    :return:
    """
    str1 = gen_sign_str(kwargs)
    str2 = utils.enbase64(str1)
    sign = utils.gen_salt_pwd(token, str2)
    return sign


def gen_sign_str(params):
    """
    ******
    :param params:
    :return:
    """
    keys = [k for k, v in params.items() if v != "" and k != "sign"]
    keys.sort()
    sign_str = "&".join(["%s=%s" % (k, str(params[k])) for k in keys])

    return sign_str

def sort_query_string(query_string):
    """
    参数按照key小写，从小到大排序；并用&拼接；
    注意：不适用于过滤value=空字符串的情况

    """
    t = query_string.split("&")
    t.sort()
    return "&".join(t)