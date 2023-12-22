# 启动
# 参考资料
# https://www.jianshu.com/p/15e02fea4263
# https://github.com/hongjinquan/django-schedule-celery
# https://www.shuzhiduo.com/A/8Bz8woOxdx/

# 启动需要运行两句
# 第一句

# 主机器启动beat，分发任务
# 1. celery -A sobase beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler -f logs/celery.log
# 从机启动worker
# 2. celery -A sobase worker -l info
# 用于开发环境 同时启动 执行beat 和 worker
# 3. 一步到位  celery -A sobase worker -B --loglevel=info -f logs/celery.log

# celery -A sobase worker -l info -P eventlet # 不带日志启动
# celery -A sobase worker --pool=solo -l info -f logs/celery.log # 带日志启动

# 修改tasks 类必须重启 否则无法生效滴
# celery -A sobase worker -B --loglevel=info

from celery import shared_task
from celery_tasks.CeleryApp import app
import telnetlib
from datetime import datetime
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from core_base.system.models import TaskManagement
import time, json
from celery_tasks.utils import ExecuteTask


# 健康检查
@app.task()
def check(*args, **kwargs):
    print(args)
    print(kwargs)
    print("ok")
    return datetime.now()


@app.task()
def send_url(*args, **kwargs):
    task_name = args[0]
    print(f"task_name={task_name}")
    periodic_task = PeriodicTask.objects.filter(name=task_name).first()
    if periodic_task is None:
        return f"none task,task_name={task_name}"
    execute_request_task = ExecuteTask.ExecuteRequestTask(periodic_task.id)
    return execute_request_task.run()
