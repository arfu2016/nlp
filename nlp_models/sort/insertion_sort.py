"""
@Project   : text-classification-cnn-rnn
@Module    : insertion_sort.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/22/18 1:10 PM
@Desc      : https://zhuanlan.zhihu.com/p/31645345
插入排序的原理非常简单，就像码扑克牌一样，让N个待排序的元素中的k个元素成为有序的序列，
然后将第k+1个元素插入到这k个元素中，如此反复从k=1直至n个元素全部有序。
用python实现代码如下，写了比较详细的代码注释，没用过Python的朋友应该也能看懂。
另外，列表在Python中属于可变对象，实际上不写返回值也可以达到排序的目的。
"""
"""
Created on Thu Feb  2 12:26:27 2017

@author: liuzimu
"""


# # 插入排序算法
# 首先排好一个子集，直至整个序列排好，排好整个序列的同时，也就找到了最小值和最大值
# 插入排序在集合中已经比较有序的情况下表现较好，如果在最坏情况下，时间复杂度依然是O(n^2)

# 1 自定义插入排序函数
def insertion_sort(A):
    l = len(A)
    for i in range(1,l): #遍历列表，注意在python中第一个元素是A[0]
        key = A[i] #key用于传递数据，起中间人的角色
		# 只要i不变，key就是固定的, key要往前面的有序数组里插
		# 开始前面的数组里只有一个数，必然是有序的
        j = i-1 #A[j]代表A[i]左侧的第一个元素
        while A[j] > key and j>=0: #遍历A[i]左侧的元素，j为负会导致计算错误
		# 如果某个值比key小，那么到此为止，它之前的也比key小
		# 如果找到最前面还没找到比key小的，说明key最小，也不能再往前插了，循环到此为止
            A[j+1] = A[j] #交换数据的位置，j位置上的往后挪
            A[j] = key #交换数据的位置，j位置被key占据
            j = j-1
    return A #返回排序后的列表A


# 2 对插入排序函数进行测试
x = [8,3,-9,11,6,5,6]
x = insertion_sort(x)
print(x)
