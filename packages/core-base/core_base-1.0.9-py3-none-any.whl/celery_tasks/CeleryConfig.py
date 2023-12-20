import os
from django.conf import settings
from celery.schedules import crontab
# 为celery设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'sobase.settings')
import django
django.setup()
from sobase import settings

from django.db import close_old_connections
close_old_connections()
imports = ("celery_tasks.tasks")
# 设置结果存储
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BROKER_URL = f'{settings.REDIS_URL}/8'
# 设置结果存储
CELERY_RESULT_BACKEND = 'django-db'
#CELERY_RESULT_BACKEND = f'{settings.REDIS_URL}/9'

# 设置代理人broker
# CELERY_BROKER_URL = config.REDIS_URL
# celery 的启动工作数量设置
CELERY_WORKER_CONCURRENCY = 20
# 任务预取功能，就是每个工作的进程／线程在获取任务的时候，会尽量多拿 n 个，以保证获取的通讯成本可以压缩。
CELERY_PREFETCH_MULTIPLIER = 20
# 非常重要,有些情况下可以防止死锁
CELERY_FORCE_EXECV = True
# celery 的 worker 执行多少个任务后进行重启操作
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100
# 禁用所有速度限制，如果网络资源有限，不建议开足马力。
worker_disable_rate_limits = True
# celery beat配置

CELERY_ENABLE_UTC = False
enable_utc = False
timezone = 'Asia/Shanghai'
CELERY_DJANGO_CELERY_BEAT_TZ_AWARE = False

# # SCHEDULER 定时任务保存数据库
# 将任务调度器设为DatabaseScheduler
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
# CELERY_TASK_TIME_LIMIT = 5
# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除。
# 设为0，存储结果永不过期
# CELERY_RESULT_EXPIRES = xx
CELERY_TASK_RESULT_EXPIRES = 60*60*24  # 后端存储的任务超过一天时，自动删除数据库中的任务数据，单位秒
CELERY_MAX_TASKS_PER_CHILD = 1000  # 每个worker执行1000次任务后，自动重启worker，防止任务占用太多内存导致内存泄漏
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
DJANGO_CELERY_BEAT_TZ_AWARE = False
# https://github.com/celery/django-celery-results/issues/326#issuecomment-1181580646
CELERY_RESULT_EXTENDED = True
BEAT_SCHEDULE = {
    "check": {
        "task": "celery_tasks.tasks.check",  #执行的函数
        "schedule": crontab(minute="*/1"),   # every minute 每分钟执行
        "args": ()  # # 任务函数参数
    }
}