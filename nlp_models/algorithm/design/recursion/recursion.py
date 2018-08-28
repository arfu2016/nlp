def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)
# 此处的递归，参数递减，在参数小到一定程度时，给一个返回值
# 重要的是递归的思维模式

