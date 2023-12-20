#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：sobase 
@File    ：task_management.py
@Author  ：cx
@Date    ：2023/12/19 11:21 上午 
@Desc    ：任务管理
'''
from core_base.system.models import TaskManagement
from core_base.utils.json_response import SuccessResponse, ErrorResponse, DetailResponse
from core_base.utils.serializers import CustomModelSerializer
from core_base.utils.viewset import CustomModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django.db import transaction
from django.utils import timezone
import uuid, json


class TaskManagementSerializer(CustomModelSerializer):
    class Meta:
        model = TaskManagement
        fields = "__all__"
        read_only_fields = ["id"]
        depth = 1


class TaskManagementViewSet(CustomModelViewSet):
    """
    任务管理
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = TaskManagement.objects.all()
    serializer_class = TaskManagementSerializer
    extra_filter_backends = []

    def create(self, request, *args, **kwargs):
        copy_data = request.data
        task_uuid = uuid.uuid4().hex
        crontab, interval = None, None
        with transaction.atomic():
            task_type = copy_data.get('task_type', 0)
            if task_type == 0:
                cron_list = copy_data.get('cron_list', "")
                # 创建周期性任务
                crontab = CrontabSchedule.objects.create(minute=cron_list[1],
                                                         hour=cron_list[2],
                                                         day_of_week=cron_list[3],
                                                         day_of_month=cron_list[4],
                                                         month_of_year=cron_list[5])
            else:
                every = copy_data.get('every', 0)  # 定时任务
                period = copy_data.get('period', 'SECONDS')  # 秒
                interval = IntervalSchedule.objects.create(every=every, period=period)
            periodic_task = PeriodicTask.objects.create(name=task_uuid, task="celery_tasks.tasks.send_url",
                                                        args=json.dumps([task_uuid]),
                                                        crontab=crontab,
                                                        interval=interval)
            copy_data.update({"periodic_task_id": periodic_task.id})
            copy_data.pop("cron_list")
            copy_data.pop("every")
            copy_data.pop("period")
            TaskManagement.objects.create(**copy_data)
            return DetailResponse(msg="创建成功")

    # 手动验证定时任务
    @action(methods=['post'], detail=False)
    def CheckTask(self, request, *args, **kwargs):
        task_name = request.data.get("task_name")
        periodic_task = PeriodicTask.objects.filter(name=task_name).first()
        from celery_tasks.utils import ExecuteTask
        execute_request_task = ExecuteTask.ExecuteRequestTask(periodic_task.id)
        msg = execute_request_task.run()
        return DetailResponse(msg=f"运行成功,耗时(秒)：{msg}")
