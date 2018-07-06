"""
@Project   : aiball
@Module    : decorators.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/13 17:05
@Desc      : 常用的装饰器
"""


def singleton(cls):
    """
    定义singleton装饰器，用于装饰类，构成单例类
    :param cls: 需要被装饰的类
    :return:
    """
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
