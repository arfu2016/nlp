"""
@Project   : CubeGirl
@Module    : timeit_in_python.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/8/18 4:34 PM
@Desc      : 
"""

import timeit


def wrapper(func, *args, **kwargs):
    """
    一个装饰器，用来把有参数的函数转换为没有参数的函数
    :param func: func
    :param args: list
    :param kwargs: dict
    :return: func
    """
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


iterations = 10
wrapped_time = wrapper(lambda x: x+1, 2)
print('Time cost: {} s'.format(
      timeit.timeit(wrapped_time, number=iterations) / iterations))
