#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from kombu import Exchange, Queue
from kombu import serialization
# https://www.cnblogs.com/yunlongaimeng/p/11121294.html

# lcyframe框架下推荐使用celery=4.4.7。若不同版本的celery服务连接到同一个redis后端时，可能会引起冲突，work启动失败
# redis://:yourpassword@localhost:6379/0
redis_config = os.environ.app_config["redis_config"]
host = redis_config['host']
port = redis_config['port']
db = redis_config['db']
BROKER_URL = f"redis://{host}:{port}/{db}"
CELERY_RESULT_BACKEND = f"redis://{host}:{port}/{db}"

# serialization.registry._decoders.pop("application/x-python-serialize")
CELERY_TASK_SERIALIZER = 'json'     # pickle
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
# if os.name != "nt":
#     # Mac and Centos
#     CELERY_ACCEPT_CONTENT = ['application/json', ]
#     CELERY_TASK_SERIALIZER = 'json'
#     CELERY_RESULT_SERIALIZER = 'json'
# else:
#     # windows
#     CELERY_ACCEPT_CONTENT = ['pickle', ]
#     CELERY_TASK_SERIALIZER = 'pickle'
#     CELERY_RESULT_SERIALIZER = 'pickle'

# 任务失败或超时自动确认，默认为True
CELERY_ACKS_ON_FAILURE_OR_TIMEOUT = False

# 任务完成之后再确认
CELERY_ACKS_LATE = True

# worker进程崩掉之后拒绝确认
CELERY_REJECT_ON_WORKER_LOST = True

# 设置默认不存结果(保存在redis内),如果需要保持结果，请在任务中单独指定。@app.task(ignore_result=False)
CELERY_IGNORE_RESULT = True

# 设置结果的保存时间
CELERY_TASK_RESULT_EXPIRES = 24 * 3600

# worker执行任务以后不会自动释放内存，需要设置每个进程执行固定次数后销毁
CELERYD_MAX_TASKS_PER_CHILD = 10  # 每个worker执行了多少任务就会死掉，防止OOM

# 队列路由规则：routing_key、queue的名字规则
CELERY_QUEUES = (
    Queue("default", Exchange("default", type='direct'), routing_key="default"),
    Queue("celery", Exchange("celery", type='direct'), routing_key="celery"),
    Queue("for_task_A", Exchange("for_task_A", type='direct'), routing_key="for_task_A"),
    Queue("for_task_B", Exchange("for_task_B", type='direct'), routing_key="for_task_B")
)

# 批量设置文件内的所有事件的队列名称
CELERY_ROUTES = {
    'tasks.task_x': {"queue": "celery"},
    'tasks.taskA': {"queue": "for_task_A", "routing_key": "for_task_A"},
    'tasks.taskB': {"queue": "for_task_B", "routing_key": "for_task_B"}
}

# 新增加的定时任务部分：celery默认时区为世界标准时间，比东八区慢8小时
# https://www.cnblogs.com/belingud/p/11716303.html
CELERY_TIMEZONE = 'Asia/Shanghai'

# CELERYBEAT_SCHEDULE = {
#     'taskA_schedule' : {
#         'task':'tasks.taskA',
#         'schedule':2,
#         'args':(5,6)
#     },
#     'taskB_scheduler' : {
#         'task':"tasks.taskB",
#         "schedule":10,
#         "args":(10,20,30)
#     },
#     'add_schedule': {
#         "task":"tasks.add",
#         "schedule":5,
#         "args":(1,2)
#     }
# }
