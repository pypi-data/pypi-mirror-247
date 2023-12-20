#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：sobase 
@File    ：TM.py
@Author  ：cx
@Date    ：2023/12/19 7:04 下午 
@Desc    ：任务管理辅助类
'''
import time, json
from core_base.system import models
import httpx
import re
import os, django, uuid, sys
from pathlib import Path
import time, json
import os, django, uuid, random
import asyncio
import httpx
import ast


class ExecuteRequestTask():

    def __init__(self, nid, **kw):
        self.nid = nid

    def request(self, client, infos):
        urls = infos.get("urls", [])
        rType = infos.get("rType", "GET")
        data = infos.get("data", {})
        for url in urls:
            client.verify = True if "https://" in url else False
            resp = client.request(rType, url, data=data)
            print(resp.status_code)

    def executeTask(self):
        task_management = models.TaskManagement.objects.filter(periodic_task__id=self.nid, task_status=True).first()
        if task_management is None:
            return f"error={self.nid}"
        urls = task_management.urls
        rType = str(task_management.reqmethod).upper()
        print(urls)
        # 100个请求发送一次
        limits = httpx.Limits(max_keepalive_connections=0, max_connections=100)

        with httpx.Client(limits=limits, timeout=5,
                          headers=ast.literal_eval(
                              task_management.reqheaders if task_management.reqheaders else "{}")) as client:
            infos = {'rType': rType, "urls": urls,
                     "data": ast.literal_eval(task_management.payload if task_management.payload else "{}")}
            self.request(client, infos)

    def run(self):
        start = time.time()
        self.executeTask()
        end = time.time()
        return end - start
