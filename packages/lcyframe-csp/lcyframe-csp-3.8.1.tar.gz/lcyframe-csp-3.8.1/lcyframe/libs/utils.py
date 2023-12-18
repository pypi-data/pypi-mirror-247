# coding=utf-8
import os
import logging
import hmac
import base64
import random
import time
from pathlib import Path
from datetime import timedelta, datetime, date
from string import ascii_letters
import zlib
import hashlib, string
import json
from bson.objectid import ObjectId
import operator
import re
import traceback, ipaddress
import socket, requests
from contextlib import suppress
from urllib.parse import urlparse, urljoin
from requests.utils import requote_uri
try:
    from JWT import JwtToken
    from Rsa import RSA
    from aes import AES
except: pass

_chars = string.printable[:87] + '_' + string.printable[90:95]
to_ObjectId = lambda a: ObjectId(a) if type(a) != ObjectId else a
to_python = lambda s: json.loads(s)
to_json = lambda obj: json.dumps(obj, ensure_ascii=False, sort_keys=True)
fix_path = lambda path: Path(path).as_posix()
traceback = traceback

num_or_alpha = re.compile("^(?!\d+$)[\da-zA-Z_]{5,10}$")  # 仅数字和字母组合，不允许纯数字,长度5~10
startwith_alpha = re.compile("^[a-zA-Z]{5,10}")  # 仅允许以字母开头,长度5~10
lllegal_char = re.compile('^[_a-zA-Z0-9\u4e00-\u9fa5]+$')  # 仅允许中文、英文、数字,_下划线。但不允许非法字符
email_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")  # 是否是邮箱
phone_re = re.compile("^(0|86|17951)?(13|14|15|16|17|18)[0-9]{9}$")  # 11位手机号
password_normal = re.compile("^(?:(?=.*)(?=.*[a-z])(?=.*[0-9])).{6,12}$")  # 一般密码 密码必须包含字母，数字,任意字符，长度6~12
password_strong = re.compile("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{6,12}$")  # 强密码 密码必须包含大小写，数字,任意字符，长度6~12


def random_int(length=6):
    """生成随机的int 长度为length"""
    return ("%0" + str(length) + "d") % random.randint(int("1" + "0" * (length - 1)), int("9" * length))


def gen_random_str(length=6, chars=_chars):
    return ''.join(random.choice(chars) for i in range(length))


def gen_random_sint(length=6):
    """
    获取字符串加数字的随机值
    :param length:
    :return:
    """
    return "".join(random.choice(string.hexdigits) for i in range(length))


def random_string(length=6):
    """生成随机字符串"""
    return ''.join(random.choice(ascii_letters) for i in range(length))


def gen_hmac_key():
    """随机生成长度32位密文"""
    s = str(ObjectId())
    k = gen_random_str()
    key = hmac.HMAC(k, s).hexdigest()
    return key


def enbase64(s):
    """
    编码
    :param s:
    :return:
    """
    if type(s) == bytes:
        return base64.b64encode(s)
    else:
        s = s.encode('utf-8')
        return base64.b64encode(s).decode('utf-8')


def debase64(s):
    """
    解码
    :param s:
    :return:
    """
    bytes_types = (bytes, bytearray)
    return base64.b64decode(s) if isinstance(s, bytes_types) else base64.b64decode(s).decode()


def check_params_date_value(datestr):
    if " " in datestr:
        ymd, hms = datestr.split(" ")
    else:
        ymd, hms = datestr, ""

    seqstr1 = ""
    seqstr2 = ""
    for i in ["-", "/", " ", ":"]:
        if i in ymd:
            seqstr1 = i
        if i in hms:
            seqstr2 = i
    ymd_fmt = []
    hms_fmt = []
    for index, i in enumerate(ymd.split(seqstr1)):
        ymd_fmt.append(["%Y", "%m", "%d"][index])
    for index, i in enumerate(hms.split(seqstr2)):
        hms_fmt.append(["%H", "%M", "%S"][index])
    fmt = ""
    if ymd_fmt:
        fmt += seqstr1.join(ymd_fmt)
    if hms_fmt:
        fmt += " " + seqstr2.join(hms_fmt)
    return string2datetime(datestr, fmt)


class TypeConvert(object):
    """类型转换类, 处理参数"""
    MAP = {int: int,
           float: float,
           list: list,
           bool: bool,
           str: str}

    STR2TYPE = {"int": int,
                "integer": int,
                "string": str,
                "str": str,
                "bool": bool,
                "float": float,
                "list": list,
                "dict": dict,
                "json": json.loads,
                "datetime": check_params_date_value}

    @classmethod
    def apply(cls, obj, raw):
        try:
            tp = type(obj)
            if tp in TypeConvert.MAP:
                return TypeConvert.MAP[tp](raw)
            return obj(raw)
        except Exception as e:
            logging.error("in TypeConvert.apply %s, obj: %s, raw: %s" % (e, obj, raw))
            return None

    @classmethod
    def convert_params(cls, _type, value):
        if _type in ["int", "integer"] and not value:
            value = 0
        try:
            tp = TypeConvert.STR2TYPE[_type]
            return tp(value)
        except Exception as e:
            raise e


def calculate_age(ts):
    """计算年龄"""
    if ts == -1:
        return -1
    born = datetime.fromtimestamp(ts)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def now():
    return int(time.time())


def oid_to_date(oid):
    return int_to_date_string(int(str(oid)[:8], 16))


def int_to_date_string(ts, fm=False):
    # fm = fm if fm else "%Y-%m-%d %H:%M:%S.%f"
    fm = fm if fm else "%Y-%m-%d %H:%M:%S"
    try:
        if not ts:
            ts = 0
        return datetime.fromtimestamp(ts).strftime(fm)
    except:
        return datetime.fromtimestamp(time.time()).strftime(fm)


def str2timestamp(date_string, fm=False):
    fm = fm if fm else "%Y-%m-%d"
    return int(time.mktime(time.strptime(date_string, fm)))
    # return int(time.mktime(datetime.strptime(date_string, format).timetuple()))


def timestamp2str(ts, fm=False):
    return int_to_date_string(ts, fm)


def datetime2string(date, fmt="%Y-%m-%d %H:%M:%S"):
    """
     datetime(2020,12,12 12:12:12) ==> 2020-12-12 12:12:12
    """
    return date.strftime(fmt)


def string2datetime(datestr, fmt="%Y-%m-%d %H:%M:%S"):
    """
    datestr: 2022-06-29 14:58:27.047955
    fmt: %Y-%m-%d %H:%M:%S
    2020-12-12 12:12:12 ==> datetime(2020,12,12 12:12:12)

    datestr: 2022-06-29 14:58:27.047955
    fmt: "%Y-%m-%d %H:%M:%S.%f
    datetime(2022-06-29 14:58:27.047955)
    """
    return datetime.strptime(datestr, fmt)


def get_yesterday_midnight():
    # 获取昨天的午夜时间戳
    return get_today_midnight() - 86400


def get_today_midnight():
    # 获取今天的午夜时间戳
    now = int(time.time())
    return now - now % 86400 - 3600 * 8 - 86400


def get_today_lasttime():
    # 获取今天最后一秒时间戳
    now = int(time.time())
    return now - now % 86400 - 3600 * 8 + 24 * 3600 - 1


def get_delta_day(day=0, is_zoo=False, return_fmt="date"):
    """
    获取-n~n天的时间
    datetime.datetime.fromordinal(datetime.datetime.today().toordinal()) + datetime.timedelta(days=-1)
    :param day:
    :param is_zoo: 是否需要0点时间
    :return:

    s1 = get_delta_day(day=1)
    s2 = get_delta_day(return_fmt=int)
    s3 = get_delta_day(return_fmt="string")
    s4 = get_delta_day(return_fmt=datetime)
    s5 = get_delta_day(return_fmt="%Y-%m-%d")
    s6 = get_delta_day(is_zoo=True)
    """

    if is_zoo:
        now = datetime.fromordinal(datetime.today().toordinal())
    else:
        now = datetime.now()

    if day == 0:
        delta_day = now
    else:
        # +-n天后
        delta_day = (now + timedelta(days=int(day)))

    # 返回格式
    if return_fmt == int:
        return int(time.mktime(delta_day.timetuple()))
    elif return_fmt in ["date", datetime]:
        return delta_day
    elif return_fmt in ["string"]:
        return delta_day.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return delta_day.strftime(return_fmt)


def calculate_time_difference(start, end):
    """
    计算2个时间差
    # 示例用法
    start_time = 1635590400  # 时间戳形式的起始时间
    end_time = 16356176800  # 时间戳形式的结束时间
    time_difference = calculate_time_difference(start_time, end_time)
    """

    # 将时间戳转换为datetime对象
    if isinstance(start, int):
        start = datetime.fromtimestamp(start)
    if isinstance(end, int):
        end = datetime.fromtimestamp(end)

    # 计算时间差
    diff = end - start

    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds // 60) % 60
    seconds = diff.seconds % 60

    # 返回时间差
    return f"{days}天{hours}时{minutes}分{seconds}秒"

def get_ts_from_object(s):
    if len(s) == 24:
        return int(s[:8], 16)
    return 0


def compress_obj(dict_obj, compress=True):
    """数据压缩"""
    dict_obj = {"$_key_$": dict_obj} if not isinstance(dict_obj, dict) else dict_obj
    if compress:
        return zlib.compress(to_json(dict_obj).encode("utf-8"))
    return to_json(dict_obj)


def uncompress_obj(binary_string, compress=True):
    """数据解压"""
    if compress:
        dict_obj = to_python(zlib.decompress(binary_string).decode("utf-8"))
    else:
        dict_obj = to_python(binary_string)

    if "$_key_$" in dict_obj:
        return dict_obj["$_key_$"]
    else:
        return dict_obj


def get_mod(uid, mod=10):
    return int(uid) % mod


def gen_salt(len=6):
    return ''.join(random.sample(string.ascii_letters + string.digits, len))


def gen_salt_pwd(salt, pwd):
    return hashlib.md5((str(salt) + str(pwd)).encode("utf-8")).hexdigest()


def md5(s):
    s = s if isinstance(s, bytes) else str(s).encode("utf-8")
    return hashlib.md5(s).hexdigest()

def md5_hex(s):
    """
    md5，输出16进制字节格式
    """
    return md5(s)

def md5_bin(s):
    """
    md5，输出二进制字节格式
    """
    s = s if isinstance(s, bytes) else str(s).encode("utf-8")
    return hashlib.md5(s).digest()

def base64_hmac_sha256(key, message):
    key_bytes = key.encode('utf-8')
    message_bytes = message.encode('utf-8')
    hmac_sha256 = hmac.new(key_bytes, message_bytes, hashlib.sha256)
    hmac_sha256_result = hmac_sha256.digest()
    base64_result = base64.b64encode(hmac_sha256_result)
    return base64_result

def pparams(request, params=None):
    print_params = {}
    if params == None:
        params = request.arguments
        params.update(request.body_arguments)
        if hasattr(request, "body_json_arguments"):
            params.update(request.body_json_arguments)

    for k, v in params.items():
        if k not in request.files:
            print_params[k] = v
        else:
            try:
                if "body" in v:
                    tmp = {}
                    tmp.update(v)
                    tmp["body"] = "%d bytes" % len(v["body"])
                    print_params[k] = tmp
                else:
                    print_params[k] = v
            except Exception as e:
                print_params[k] = {}

    return print_params


def version_cmp(version1, version2):
    """比较系统版本号
    v1 > v2 1
    v1 = v2 0
    v1 < v2 -1
    v1: 用户使用的版本
    v2：最新上线的版本
    """

    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    return operator.gt(normalize(version2), normalize(version1))


def _find_option_with_arg(argv, short_opts=None, long_opts=None):
    """Search argv for options specifying short and longopt alternatives.

    Returns:
        str: value for option found
    Raises:
        KeyError: if option not found.

    Example：
        config_name = _find_option_with_arg(short_opts="-F", long_opts="--config")
    """
    for i, arg in enumerate(argv):
        if arg.startswith('-'):
            if long_opts and arg.startswith('--'):
                name, sep, val = arg.partition('=')
                if name in long_opts:
                    return val if sep else argv[i + 1]
            if short_opts and arg in short_opts:
                return argv[i + 1]
    raise KeyError('|'.join(short_opts or [] + long_opts or []))


def check2json(data):
    if isinstance(data, (list, tuple)):
        for index, item in enumerate(data):
            data[index] = check2json(item)
        return data
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = check2json(value)
        return data
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    elif data == None:
        return ""
    else:
        return data

def service_kill(name):
    import subprocess
    def cmdprocess(cmdline):
        pipe = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        output, stderr = pipe.communicate()
        return_code = pipe.returncode
        stderr = stderr.decode(errors='replace')
        output = output.decode(errors='replace')
        return output, stderr, return_code
    try:
        cmdline = "ps -ef | grep "+str(name)+" | grep -v grep | awk '{print $2}'"
        output, stderr, return_code = cmdprocess(cmdline)
        if return_code != 0:
            return
        pids = output.splitlines()
        for pid in pids:
            kill_cmdline = f"kill -9 {pid}"
            cmdprocess(kill_cmdline)
    except Exception as e:
        logging.error(f'杀死进程{name}失败:{e}')

def get_ip(address):
    """
    address：www.xxx.com
    返回ip
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        with suppress(Exception):
            s.connect((address, 1))
            return s.getsockname()[0]
    return None

def ping(address, port):
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if test_socket.connect_ex((address, port)) == 0:
        return True
    else:
        return False

def check_dns(dns_host):
    """
    检测DNS服务器是否可用
    """
    is_enable = False
    msg = b'\x5c\x6d\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x05baidu\x03com\x00\x00\x01\x00\x01'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    for i in range(3):
        sock.sendto(msg, (dns_host, 53))
        try:
            sock.recv(4096)
            is_enable = True
            break
        except socket.timeout as e:
            logging.error('{dns} 该dns服务器不可用'.format(dns=dns_host))

    return is_enable

def ip_into_int(ip):
    from functools import reduce
    return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))

def check_internal_ip(ip):
    """
    内网IP 局域网IP
    """
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    net_d = ip_into_int('127.0.0.0') >> 24
    net_e = ip_into_int('0.0.0.0') >> 24
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c or ip >> 24 == net_d or ip >> 24 == net_e

def check_ssrf_url(url):
    """
    提取有效url，防止SSRF攻击
    URL为内网IP或域名，攻击者通过SSRF漏洞扫描内网漏洞获取权限
    URL中包含端口，攻击者可以扫描发现内网其他机器的服务进行利用
    当请求方法允许其他协议的时候，将可能利用gophar、file等协议进行第三方服务利用，如利用内网的redis获取权限、利用fastcgi进行getshell等
    http://123.123.123.123@10.0.0.1:8888/
    http://10.0.0.1#123.123.123.123
    当request.get(url)时，实际请求10.0.0.1，存在安全隐患
    """
    schema = urlparse(url).scheme or None
    hostname = urlparse(url).hostname or url
    try:
        if not verify_domain(url):
            return ""
        # ip_address = socket.getaddrinfo(hostname, schema)[0][4][0]
        ip_address = ""
        AddressFamily = ""
        for item in socket.getaddrinfo(hostname, schema):
            AddressFamily = item[0]
            if AddressFamily == socket.AddressFamily.AF_INET:
                ip_address = item[4][0]
                break

        if AddressFamily == socket.AddressFamily.AF_INET:
            if check_internal_ip(ip_address):
                return ""
        return (schema or "http") + "://" + hostname
    except Exception as e:
        return ""

def safe_request_url(url, **kwargs):
    """
    安全请求外部url，防止SSRF攻击
    1、通过内网ip攻击
    2、通过30x状态码跳转攻击
    3、通过误导访问不知名url攻击
    """
    def _request_check_location(r, *args, **kwargs):
        if not r.is_redirect:
            return
        url = r.headers['location']

        parsed = urlparse(url)
        url = parsed.geturl()

        # Facilitate relative 'location' headers, as allowed by RFC 7231.
        # (e.g. '/path/to/resource' instead of 'http://domain.tld/path/to/resource')
        # Compliant with RFC3986, we percent encode the url.
        if not parsed.netloc:
            url = urljoin(r.url, requote_uri(url))
        else:
            url = requote_uri(url)

        safe_url = check_ssrf_url(url)
        if not safe_url:
            raise requests.exceptions.InvalidURL("SSRF Attack: %s" % (url, ))

    safe_url = check_ssrf_url(url)
    if not safe_url:
        raise requests.exceptions.InvalidURL("SSRF Attack: %s" % (url,))

    all_hooks = kwargs.get('hooks', dict())
    if 'response' in all_hooks:
        if hasattr(all_hooks['response'], '__call__'):
            r_hooks = [all_hooks['response']]
        else:
            r_hooks = all_hooks['response']

        r_hooks.append(_request_check_location)
    else:
        r_hooks = [_request_check_location]

    all_hooks['response'] = r_hooks
    kwargs['hooks'] = all_hooks
    return requests.get(safe_url, **kwargs)

def verify_username(username, min: int = 4, max: int = 10):
    """
    校验用户名
    :param username: 待验证用户名
    :param min: 最小长度
    :param max: 最大长度
    :return:
    """
    re_str1 = re.compile("^[a-zA-Z](?!\d+$)[\da-zA-Z_]")  # 非数字开头
    re_str2 = re.compile("^(?!\d+$)[\da-zA-Z_]{%d,%d}$" % (min, max))  # 非数字开头，字母与数字组合，长度4~10

    return re.search(re_str1, username) and re.search(re_str2, username)


def verify_nickname(nickname, min: int = 4, max: int = 10):
    """
    校验昵称
    :param nickname: 待验证昵称
    :param min: 最小长度
    :param max: 最大长度
    :return:
    """
    # 允许中文、字母、数字组合，禁止非法字符,长度4~10
    lllegal_char = re.compile('^[_a-zA-Z0-9\u4e00-\u9fa5]{%d,%d}$' % (min, max))
    return re.search(lllegal_char, nickname)


def verify_password(password, min: int = 4, max: int = 10, strong_level=1):
    """
    校验密码
    :param password: 待验证密码
    :param min: 最小长度
    :param max: 最大长度
    :param strong: 密码强度等级
            以下所有规则下的密码都禁止包含空格、表情、汉字
            1、一般密码：符合长度且不能是重复或者连续的数字
            2、正常密码：必须包含字母、数字
            3、强密码：必须包含字母（含大写或小写）、数字
            4、强密码：必须包含字母、数字、特殊英文字符
            5、史上最强密码：必须包含字母（含大小写）、数字、特殊英文字符

    :return:
    """
    password_normal = re.compile(
        "^(?:(?=.*)(?=.*[A-Za-z])(?=.*[0-9])).{%d,%d}$" % (min, max))  # 一般密码 密码必须包含字母(大写或小写)，数字，长度6~12
    password_strong = re.compile(
        "^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{%d,%d}$" % (min, max))  # 强密码 密码必须含字母（含大写），数字，任意字符，长度6~12
    special_char = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "|", ".", ",", "?", "{", "}",
                    "[", "]", ":"]

    if strong_level == 1:
        if len(password) < min or len(password) > max:
            result = False
        elif is_simple(password) == True:
            result = False
        else:
            result = True
    elif strong_level == 2:
        result = re.search(password_normal, password)
    elif strong_level == 3:
        result = re.search(password_strong, password)
    elif strong_level == 4:
        result = re.search(password_normal, password)
        if result:
            result = any(c in special_char for c in password)
    elif strong_level == 5:
        result = re.search(password_strong, password)
        if result:
            result = any(c in special_char for c in password)
    else:
        result = False

    if not result:
        return False

    # 禁止中文、标签
    if extract_chinese(password):
        return False

    # 禁止非法全角字符
    if extract_illegal_char(password):
        return False

    # 是否含表情
    if password != replace_emoji(password):
        return False

    return True


def verify_phone(phone):
    """
    校验手机号
    :param phone: 待验证phone
    :param min: 最小长度
    :param max: 最大长度

    :return:
    """
    phone_re = re.compile("^(0|86|17951)?(13|14|15|16|17|18)[0-9]{9}$")  # 11位手机号
    return re.search(phone_re, phone)


def verify_email(email, min: int = 7, max: int = 50):
    """
    校验邮箱
    :param phone: 待验证邮箱
    :param min: 最小长度
    :param max: 最大长度

    :return:
    """
    # 是否是邮箱,且长度在7~50之间
    email_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?){%d,%d}$" % (min, max))
    return re.search(email_re, email)

def verify_email2(email):
    """
    此方法稍慢
    """
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError as e:
        return False

def extract_domain_ip(url):
    """
    提取url中的ip地址
    1、http://www.xxx.com/a   >> 12.34.56.89
    2、http://12.34.56.78/a   >> 12.34.56.89
    2、http://12.34.56.78:8080/a   >> 12.34.56.89
    """
    parts = url.split('/')
    if url.startswith("http"):
        if len(parts) > 2:
            domain = parts[2]
            domain = domain.split(":")[0]
        else:
            domain = parts[0]
    else:
        domain = parts[0]

    try:
        ipaddress.ip_address(domain)
        ip = domain
    except ValueError:  # {ValueError}'http://www.baidu.com/page' does not appear to be an IPv4 or IPv6 address
        try:
            # answer = tools.dns_query_a(domain)
            # ips = [item.address for item in answer]
            # ip = ",".join(ips)
            domain = extract_domain(url).registered_domain
            ip = socket.gethostbyname(domain)
        except Exception as e:
            ip = ""
    except Exception as e:
        ip = ""
    finally:
        return ip

def verify_ip(address):
    """
    校验IP
    支持ipv4\ipv6
    :return:
    # 示例用法
    ipv4 = '192.168.0.1'
    ipv6 = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'

    print(is_valid_ip(ipv4))  # 输出：True
    print(is_valid_ip(ipv6))  # 输出：True
    """
    # 使用正则表达式匹配IPv4和IPv6地址的格式
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, address):
        try:
            # 验证IPv4地址的有效性
            ip = ipaddress.IPv4Address(address)
            return True
        except ValueError:
            return False
    else:
        try:
            # 验证IPv6地址的有效性
            ip = ipaddress.IPv6Address(address)
            return True
        except ValueError:
            return False

def _get_protocol(domain):
    if domain.startswith("https://"):
        protocol = "https://"
    elif domain.startswith("http://"):
        protocol = "http://"
    else:
        protocol = ""
    return protocol

def verify_domain(domain, mtype=1):
    """
    校验域名
    mtype:
        1判断是否为合法域名；
        2提取域名有效部分：https://7w.7.wx.baidu.com >> 7w.7.wx.baidu.com
    :return:
    """
    protocol = _get_protocol(domain)
    domain_re = r'\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b'
    result = re.search(domain_re, domain, re.I)
    if result:
        if mtype == 1:
            return result.group() == domain.replace(protocol, "")
        else:
            return result.group()
    else:
        return False

def extract_domain(domain):
    """
    提取顶级域名
    domain: http://news.baidu.com
    tld = extract_domain(domain)
        >>> ExtractResult(subdomain='news', domain='baidu', suffix='com')
        >>> tld[0] or tld.subdomain == "news"
        >>> tld[1] or tld.domain   == "baidu"
        >>> tld[2] or tld.suffix == "com"
        >>> tld.registered_domain == "baidu.com"

    """

    import tldextract
    tld = tldextract.extract(domain)
    return tld


def extract_domain2(domain):
    """
    提取域名协议，主域，端口,不包含path
    # urllib3.get_host(https://news.baidu.com)  # ('https', 'news.baidu.com', None)
    # urllib3.get_host(news.baidu.com:8888)     # ('http', 'news.baidu.com', 8888)
    # urllib3.get_host(news.baidu.com:9999/abc/123?a=1)     # ('http', 'news.baidu.com', 9999)
    # urllib3.get_host(news.baidu.com/:80:123/abc/123?a=1)     # ('http', 'news.baidu.com', 9999) 注意 path=':80:123/abc/123?a=1'

    protocol:默认http
    """
    import urllib3
    try:
        protocol, host, port = urllib3.get_host(domain)
        return protocol, host, port or ""
    except Exception as e:
        return False


def extract_chinese(str):
    """
    提取中文
    :param str:
    :return:
    """

    regex_str = ".*?([\u4E00-\u9FA5]+).*?"
    match_obj = re.findall(regex_str, str)
    return match_obj


def extract_illegal_char(str):
    """
    提取非法半角字符，空格
    :param str:
    :return:
    """
    regex_str = "([！￥……（）——，。、？；：【】「」《》“”‘'  ]+).*?"
    match_obj = re.findall(regex_str, str)
    return match_obj


def extract_illegal_char2(str):
    """
    性能较差
    判断是否含有特殊非法字符
    :param str:
    :return:
    """
    # 所有非法字符
    all_illegal_char = range(0x0, 0x10ffff)  # 总数110万个
    for s in str:
        if s in all_illegal_char:  # 判断一个字符大约需要20ms
            return False
    return True


def change_emoji(char_str):
    """
    将表情转为字符
    :param str: 123🆚456
    :param result: 123:VS_button:456

    :param str: 表情🏷
    :param result: 表情:label:

    :return:
    """
    import emoji
    return emoji.demojize(char_str)


def replace_emoji(char_str, rep_str=''):
    """
    将字符串中的表情替换为指定的字符，默认替换为空，即过滤表情
    常用语用户名、昵称注册等禁止表情的输入
    :param char_str:
    :param rep_str:
    :return:
    """
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(rep_str, char_str)


def is_simple(password):
    """
    判断字符串密码是否为简单重复或者纯数字或连续的数字
    若是，返回True
    若不是，返回False
    :param password:
    :return:
    """
    if password.isdigit():
        password = [int(n) for n in password]
        if len(set(password)) == 1:
            return True

        for index, a in enumerate(password[: -1]):
            b = password[index + 1]
            if (b - a) != 1:
                return False
        return True
    else:
        password = [n for n in password]
        if len(set(password)) == 1:
            return True
        else:
            return False

def is_letter(char_str):
    """
    字符串是否全部由字母组成
    str.isalpha(): abc、a是bc都返回真，不满足
    """
    return re.match(re.compile(r"[a-zA-Z]+$"), char_str)

def transfer_str(str):
    """
    mongo 正则匹配 转义
    :param str:
    :return:
    """
    new_str = ""
    special = ['/', '^', '$', '*', '+', '?', '.', '(', ')']
    for c in str:
        if c in special:
            new_str += '\\'
        new_str += c
    return new_str


def supper_format(filename, format_list):
    """
    判断文件是否在指定的格式内
    :param filename: abc.e.f.tar.gz
    :param format_list: ["rar", "tar", "tar.gz"]
    :return: True
    """
    return any(filter(lambda x: filename.lower().endswith(x.lower()), format_list))


def get_filename_format(filename, format_list):
    """
    截取文件名和格式名
    针对压缩包名称较为复杂的情况
    :param filename: abc.e.f.tar.gz
    :param format_list: ["rar", "tar", "tar.gz"]
    :return: abc.e.f
    """
    if "." not in filename:
        return filename, ""

    exists_format = False

    for i in format_list:
        if not i.startswith("."):
            suffix = "." + i
        else:
            suffix = i
        if filename.lower().endswith(i):
            name, format = filename.rsplit(suffix, 1)[0], i
            exists_format = True
            break

    if exists_format:
        return name, format
    else:
        return filename.rsplit(".", 1)


def auto_rename(name, uncompress_path, n=1):
    """
    指定一个解压位置，若有同名文件夹存在，则自动重命名
    :param name:
    :param uncompress_path:
    :param n:
    :return:
    """
    while n < 100:
        if n > 1:
            dst_path = os.path.join(uncompress_path, name + "-" + str(n))
        else:
            dst_path = os.path.join(uncompress_path, name)

        if os.path.exists(dst_path):
            n += 1
            return auto_rename(name, uncompress_path, n)
        else:
            if n > 1:
                return name + "-" + str(n), dst_path
            else:
                return name, dst_path
    raise


def undecompress(compress_path, uncompress_path):
    """
    解压包
    :param compress_path: 压缩包目前所在目录: /code/123.zip
    :param uncompress_path: 需要解压至该目录:/code/newname
    :param decompress_format: 支持的解压格式列表["zip", "rar", "7z", "tar", "tbz2", "tgz", "tar.bz2", "tar.gz", "tar.xz", "tar.Z"]
    :return:
    """
    import patoolib
    try:
        if not os.path.exists(uncompress_path): os.makedirs(uncompress_path)
        patoolib.extract_archive(compress_path, outdir=uncompress_path)
    except Exception as e:
        os.remove(uncompress_path)
        logging.error(str(e))
    else:
        return True


def pdf2img(pdf_path, to_path):
    '''
    # 将PDF转化为图片
    pdf_path pdf文件的路径
    to_path 保存文件夹目录
    zoom_x x方向的缩放系数
    zoom_y y方向的缩放系数
    rotation_angle 旋转角度
    '''
    try:
        import fitz
        doc = fitz.open(pdf_path)
        print("PDF转图片，任务文件：%s" % pdf_path)

        ts = now()
        for pg in range(doc.pageCount):
            print("\r共%s页,正在转换第%s/%s张" % (doc.pageCount, pg + 1, doc.pageCount), end="")
            page = doc[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为8，这将为我们生成分辨率提高64倍的图像。
            zoom_x = 6.0
            zoom_y = 6.0
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pm = page.get_pixmap(matrix=trans, alpha=False)
            save_name = '{:01}.png'.format(pg + 1)
            pm.save(os.path.join(to_path, save_name))
        print()
        print("耗时:%s秒" % str(now() - ts))
    except Exception as e:
        print(str(e))

def imagecode(stype=4, args_value=None, return_type=2, filename=None, **kwargs):
    """
    生成图形验证码
    stype: 验证码类型
    args_value： 指定生成参数；值可以是：指定的验证码，生成的长度；加减法符号
    return_type： 返回类型 1 返回字节码；2返回base64；3保存到指定文件
    filename： 保存路径/名称.png
    kwargs：生成参数
    dict(
        font_color_values=font_color_values,
        font_background_value='#87CEFF',
        draw_dots=True,
        dots_width=5,
        dots_count=200,
        draw_lines=True,
        lines_width=4,
        lines_count=10,
        lines_background_value="#ffffff",
    )

    例子：
    print(imagecode(1, "123456", return_type=2))
    print(imagecode(2, 6, return_type=2))
    print(imagecode(3, 6, return_type=3))
    print(imagecode(4, 6, return_type=3))
    print(imagecode(5, "+", return_type=3))

    """
    from .gvcode import VFCode
    default_kw = dict(
        font_background_value='#87CEFF',
        draw_dots=True,
        dots_width=5,
        dots_count=200,
        draw_lines=True,
        lines_width=4,
        lines_count=10,
        lines_background_value="#ffffff",
    )
    if kwargs:
        default_kw.update(kwargs)
    vc = VFCode(**default_kw)

    mp = {
        # 自定义验证码
        # vc.generate('abcd')
        1: vc.generate,

        # 数字验证码（默认5位）
        # vc.generate_digit()
        # vc.generate_digit(4)
        2: vc.generate_digit,

        # 字母验证码（默认5位）
        # vc.generate_alpha()
        # vc.generate_alpha(5)
        3: vc.generate_alpha,

        # 数字字母混合验证码（默认5位）
        # vc.generate_mix()
        # vc.generate_mix(6)
        4: vc.generate_mix,

        # 数字加减验证码（默认加法）
        # 数字加减验证码（加法）
        # vc.generate_op('+')
        # 数字加减验证码（减法）
        # vc.generate_op('-')
        # 数字乘法，字母x
        # vc.generate_op('x')
        5: vc.generate_op,
    }
    if stype not in [1, 2, 3, 4, 5]:
        raise Exception("类型错误")

    if args_value is not None:
        mp[stype](args_value)
    else:
        mp[stype]()

    code = vc.code
    if return_type == 1:    # 返回字节码
        code_data = vc.get_img_bytes()
    elif return_type == 2:
        code, code_data = vc.get_img_base64()
    else:
        vc.save(filename)
        code_data = filename

    return code, code_data

def get_string_size(string, encode_type="utf-8"):
    """
    获取字符串字节数
    """
    if isinstance(string, bytes):
        string = string.decode()
    return len(string.encode(encode_type))