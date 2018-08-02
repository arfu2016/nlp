"""
@Project   : DuReader
@Module    : binary_search.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/16/18 10:50 AM
@Desc      : 
"""
from bisect import bisect_left


def index(a, x):
    """binary search: Locate the leftmost value exactly equal to x;
    search list a for x
The behavior of bisect can be fine-tuned in two ways.

First, a pair of optional arguments, lo and hi , allow narrowing the region in the sequence
to be searched when inserting. lo defaults to 0 and hi to the len() of the sequence.
Second, bisect is actually an alias for bisect_right , and there is a sister function called
bisect_left . Their difference is apparent only when the needle compares equal to an
item in the list: bisect_right returns an insertion point after the existing item, and
bisect_left returns the position of the existing item, so insertion would occur before it.

	"""
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
	"""i == len(a)其实是没找着，而且这时a[i]是不存在的"""
        return i
    raise ValueError("No {} in {}".format(x, a))

