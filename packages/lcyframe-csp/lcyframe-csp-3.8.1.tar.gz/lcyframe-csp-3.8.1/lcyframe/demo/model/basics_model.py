#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseModel
from model.schema.basics_schema import BasicsSchema

class BasicsModel(BaseModel, BasicsSchema):

    @classmethod
    def _parse_data(cls, doc, **kwargs):
        """
        组装、修正单条记录
        该方法若存在，框架会自动使用
        若不存在，则模式使用框架内置方法
        :param doc: 单条数据
        :param kwargs:
        :return:
        """
        if not doc:
            return {}

        if "_id" in doc:
            doc["basics_id"] = doc.pop("_id", "")

        return doc

    @classmethod
    def send_smscode(cls, uuid, mobile, stype, **kwargs):
        """
        发送短信验证码
        :return:
        :rtype:
        """
        minute_flag = cls.redis.get(cls.keys.smscode_interval % mobile) or 0
        if minute_flag:
            raise cls.api_error.ErrorCommon("发送太频繁，请稍后在尝试")

        day_times = cls.redis.get(cls.keys.smscode_times % mobile) or b'0'
        if int(day_times.decode()) >= cls.keys.sms_times:
            raise cls.api_error.ErrorCommon("短信验证码每个账号每天最多只能收到10条")

        sms_code = cls.utils.random_int(4)
        if stype == 1:
            content = f"【XXXX】您的短信验证码为：{sms_code}，有效期为5分钟；请勿泄露给他人，如非本人操作，请忽略此信息。"
        else:
            content = ""
        result = cls.helper.smscode(mobile, content, 4)
        if result.status_code == 200 and cls.utils.to_python(result.content)["code"] == 100:
            cls.redis.setex(cls.keys.smscode_key % uuid, cls.keys.smscode_exp, sms_code)
            cls.redis.setex(cls.keys.smscode_interval % mobile, 60, sms_code)
            cls.redis.incr(cls.keys.smscode_times % mobile)
            cls.redis.expire(cls.keys.smscode_times % mobile, cls.utils.get_today_lasttime()-cls.utils.now())
            return sms_code
        raise cls.api_error.ErrorCommon("发送失败")

    @classmethod
    def vaild_smscode(cls, uuid, code, **kwargs):
        """
        校验短信验证码
        :return:
        :rtype:
        """
        sms_code = cls.redis.get(cls.keys.smscode_key % uuid)
        sms_code = sms_code.decode() if sms_code else ""
        if code == sms_code:
            cls.redis.delete(cls.keys.smscode_key % uuid)
        return code == sms_code

    @classmethod
    def send_imagecode(cls, uuid, **kwargs):
        """
        生成图形验证码
        :return:
        :rtype:
        """
        image_code, code_data = cls.utils.imagecode(**{"lines_count": 8, "lines_width": 1, "dots_count": 100})
        cls.redis.setex(cls.keys.imagecode_key % uuid, cls.keys.imagecode_exp, image_code)
        return image_code, code_data

    @classmethod
    def vaild_imagecode(cls, uuid, code, **kwargs):
        """
        校验图形验证码
        :return:
        :rtype:
        """
        image_code = cls.redis.get(cls.keys.imagecode_exp % uuid)
        image_code = image_code.decode() if image_code else ""
        if code == image_code:
            cls.redis.delete(cls.keys.imagecode_key % uuid)
        return code == image_code


    @classmethod
    def get_basics_list_by_last_id(cls, last_id, count, **kwargs):
        """
        前端列表
        :return:
        :rtype:
        """
        spec = {}
        spec.update(kwargs.get("spec", {}))
        data_list, last_id = cls.find_list_by_last_id(spec,
                                                      count,
                                                      sort=[("create_at", -1), ],
                                                      fields=kwargs.get("fields", None),
                                                      last_id_field=False)
        return data_list, last_id

    @classmethod
    def get_basics_list_by_page(cls, page, count, **kwargs):
        """
        后台列表
        :return:
        :rtype:
        """
        spec = {}
        spec.update(kwargs.get("spec", {}))
        data_list, pages, counts = cls.find_list_by_page(spec,
                                                         page,
                                                         count,
                                                         sort=[("create_at", -1), ],
                                                         fields=kwargs.get("fields", None))
        return data_list, pages, counts

    @classmethod
    def create_basics(cls, *args, **kwargs):
        """
        创建
        :return:
        :rtype:
        """
        pass

    @classmethod
    def modify_basics(cls, *args, **kwargs):
        """
        修改
        :return:
        :rtype:
        """
        pass

    @classmethod
    def delete_basics(cls, basics_id, **kwargs):
        """
        删除
        :return:
        :rtype:
        """
        return cls.update({"_id": basics_id}, {"state": -1})




