"""
@Project   : CubeGirl
@Module    : tree_vector.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/14/17 11:26 AM
@Desc      : 
"""

from pydtk.tree import Tree
from pydtk.dtk import DT
from pydtk.operation import fast_shuffled_convolution

tree = Tree(string="(HED (SBV VOB))")
# tree = Tree(string="(喜欢 (PERSON 车 (什么)))")
# tree = Tree(string="('A' ('B' 'C'))")
# tree = Tree(string="('A'   (('B')  ('C')))")
# tree = Tree(string="(A (B C))")
# tree = Tree(string="{A: {B: {}, C:{}}}")
dtCalculator = DT(dimension=1024, LAMBDA=0.6,
                  operation=fast_shuffled_convolution)

distributedTree = dtCalculator.dt(tree)
print(type(distributedTree), len(distributedTree), distributedTree)
print(distributedTree.shape)
