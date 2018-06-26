"""
@Project   : text-classification-cnn-rnn
@Module    : print_table.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/25/18 6:17 PM
@Desc      : 
"""

for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    # Note use of 'end' on previous line
    print(repr(x*x*x).rjust(4))

for x in range(1, 11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))
