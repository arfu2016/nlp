"""
@Project   : text-classification-cnn-rnn
@Module    : cache_simple.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/20/18 5:48 PM
@Desc      : 
Besides making silly recursive algorithms viable, lru_cache really shines in applications that need to fetch information from the Web.

functools.lru_cache(maxsize=128, typed=False)

For optimal performance, maxsize should be a power of 2
The typed argument, if set to True , stores results of different argument
types separately, i.e., distinguishing between float and integer arguments that are normally considered equal, like 1 and 1.0 . By the way, because lru_cache uses a dict to store the results, and the keys are made from the positional and keyword arguments used in the calls, all the arguments taken by the decorated function must be hashable.
"""
import time
import datetime

from cachetools import cached, TTLCache
# 1 - let's import the "cached" decorator and the "TTLCache" object from cachetools
cache = TTLCache(maxsize=100, ttl=300)  # 2 - let's create the cache object.


@cached(cache)  # 3 - it's time to decorate the method to use our cache system!
def get_candy_price(candy_id):
    # let's use a sleep to simulate the time your function spends trying to connect to
    # the web service, 5 seconds will be enough.
    time.sleep(5)

    # let's pretend that the price returned by the web service is $1 for candies with a
    # odd candy_id and $1,5 for candies with a even candy_id

    price = 1.5 if candy_id % 2 == 0 else 1

    return datetime.datetime.now().strftime("%c"), price


if __name__ == '__main__':
    # now, let's simulate 20 customers in your show.
    # They are asking for candy with id 2 and candy with id 3...
    for i in range(0, 20):
        print(get_candy_price(2))
        print(get_candy_price(3))
