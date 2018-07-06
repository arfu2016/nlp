"""
@Project   : aiball
@Module    : settings_common.py
@Author    : Steven [steven@cubee.com]
@Created   : 22/03/2018 10:29 AM
@Desc      : 
"""
import os
import queue

####################
# CORE             #
####################

DEBUG = False

# 项目根目录(.gitignore所在目录)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))

###########
# LOGGING #
###########
# For PUBSUB channel
LOGGING_REDIS_CHANNEL = 'AIBALL_USER_QUESTION_LOG_CHANNEL'
# For list
LOGGING_REDIS_LIST = 'AIBALL_USER_QUESTION_LOG_LIST'

LOGGING_QUEUE_REDIS = queue.Queue(-1)
# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Default logging for aiball. Depending on DEBUG, all log records are either
# sent to the console (DEBUG=True) or discarded (DEBUG=False) by means of the
# require_debug_true filter.
LOGGING = {
    'version': 1,
    # All below are optional.
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'aiball.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'aiball.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s',
        },
        'time_rotating_file': {
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s',
        },
        'redis': {
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s',
        },
        'mongodb': {
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'time_rotating_file': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'formatter': 'time_rotating_file',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR + '/aiball.log',
            'when': 'midnight',
        },
        'queue_redis': {
            'level': 'INFO',
            'class': 'logging.handlers.QueueHandler',
            'filters': ['require_debug_false'],
            'formatter': 'redis',
            'queue': LOGGING_QUEUE_REDIS,
        },
    },
    'loggers': {
        'aiball': {
            'handlers': ['console', 'time_rotating_file'],
            'level': 'DEBUG',
        },
        'aiball.server': {
            'handlers': ['queue_redis'],
            'level': 'INFO',
            # If set to false, logging messages are not passed to the handlers
            #  of ancestor loggers.
            # Here we want don't want that. So we set it to True.
            'propagate': True,
        },
    },
}

REDIS_CHANNEL = {
    'log': 'CUBEGIRL_USER_QUESTION_LOG_LIST',
    'buffer': 'CUBEGIRL_REDIS_BUFFER',
    'receive': 'GATEWAY_TO_ROBOT_DATA',
    'event': 'CHANNEL_MATCH_EVENT',
    'send': 'GATEWAY_TO_ROBOT_DATA',
    'command': 'CUBE_GIRL_CHANNEL_COMMAND_FROM_ADMIN'  # 管理后发布命令通道
}

# 配置redis中每个db的用处
REDIS_DB = {
    # 脚本
    'script': {
        'br_match_list': 12,
        'br_match_event': 13,
    },
    # server
    'server': {
        'match_list': 15,  # 当前时间向前推2小时，向后推10分钟的所有比赛列表
        'server_user': 16,  # 当前server进程和用户对应关系
        'intent': 14,  # 意图识别上下文
        'match': 14,  # 比赛相关
        'user': 14,  # user
    }
}

CACHE_TTL = {
    'intent': 1 * 10 * 60,  # 意图识别上下文过期时间（秒)
    'match': 3 * 60 * 60,  # 比赛过期时间（秒）
}

PLATFORM_SDK = ['mofang', 'ssports']

PLATFORM_CLIENT = {
    'no_screen': ['dingdong', 'tianmao', 'mi', 'mi_brain']
}

NEWS = {
    'index': 'http://h5.pre.aiball.ai/#/newsList/index',
    'detail': 'http://h5.dev.aiball.ai/#/detail/',
}

HELP = {
    'url': 'http://app.aiball.ai/help',
    'msg': '主人您好！我是您的英超私人助理小美！点击技能包，可以更深入的了解小美哦。',
    'sdk_msg': '主人您好！我是您的英超私人助理小美！点击技能包或者弹幕区问号，'
               '可以更深入的了解小美哦。'
}
