# -*- coding: utf-8 -*-
import random, time
from lcyframe.libs.beanstalk_route import BsRoute
from base import BaseModel

"""
目前仅支持监听default tube；所有任务都在此通道
self.beanstalk.DemoEvents.event({"DemoEvents": 1})
"""

@BsRoute.tasks
class DemoEvents(BaseModel):
    tube = "default"

    @classmethod
    def event(cls, job):
        """
        返回False：job不会删除
        返回非False：job会被删除
        :param x:
        :return:
        """
        print(job)
        return True
