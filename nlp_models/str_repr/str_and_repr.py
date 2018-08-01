"""
@Project   : text-classification-cnn-rnn
@Module    : str_and_repr.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/25/18 6:08 PM
@Desc      :
The str() function is meant to return representations of values which are
fairly human-readable, while repr() is meant to generate representations
which can be read by the interpreter (or will force a SyntaxError if there is
no equivalent syntax). For objects which don’t have a particular representation
for human consumption, str() will return the same value as repr().
Many values, such as numbers or structures like lists and dictionaries, have
the same representation using either function. Strings, in particular,
have two distinct representations.
"""

s = 'Hello, world.'
a = str(s)
b = repr(s)

if __name__ == '__main__':
    print('a:', a)
    print('b:', b)
    print('eval of b:', eval(b))
    try:
        print('eval of a:', eval(a))
    except Exception as e:
        print('exception for a:', e)

a_string = 'bar'
print(str(a_string))
print(repr(a_string))
print(json.dumps(a_string))
print(pickle.dumps(a_string))
print(a_string.encode('utf-8'))

print(a_string)
print(eval(repr(a_string)))
print(json.loads(json.dumps(a_string)))
print(pickle.loads(pickle.dumps(a_string)))
print(a_string.encode('utf-8').decode('utf-8'))

print(isinstance(str(a_string), str))
print(isinstance(repr(a_string), str))
print(isinstance(json.dumps(a_string), str))
print(isinstance(pickle.dumps(a_string), bytes))
print(isinstance(a_string.encode('utf-8'), bytes))

