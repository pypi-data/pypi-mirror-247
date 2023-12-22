from celery import Celery
from django.apps import apps

# 创建celery app
app = Celery("sobase")

# 从单独的配置模块中加载配置
app.config_from_object("celery_tasks.CeleryConfig", namespace="CELERY")
# 设置app自动加载任务
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
# app.config_from_object(dict(result_extended=True))
# 解决时区问题，定时任务启动就循环输出
# app.now = timezone.now

# 配置定时任务
app.conf.beat_schedule = {

}
