"""
@Project   : CubeGirl
@Module    : apply_vec.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/23/17 11:17 PM
@Desc      : from json to PCA
"""

import json
import matplotlib.pyplot as plt
from sklearn import decomposition

import matplotlib
from matplotlib.font_manager import FontManager
import subprocess


with open('data/cube_vec.json') as vecFile:
    word2vec = json.load(vecFile)
for word, vector in word2vec.items():
    print(word, vector)

annotation, data_ori = zip(*word2vec.items())

pca = decomposition.PCA(n_components=2)
pca.fit(data_ori)
result = pca.transform(data_ori).tolist()
print(result)
# print(type(result))
x, y = zip(*result)
print(annotation)

fig, ax = plt.subplots()
ax.scatter(x, y)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print(matplotlib.matplotlib_fname())

fm = FontManager()
mat_fonts = set(f.name for f in fm.ttflist)
output = subprocess.check_output(
    'fc-list :lang=zh -f "%{family}\n"', shell=True)
print('Type of output:', type(output))
output = output.decode('utf-8')
# print('*' * 10, '系统可用的中文字体', '*' * 10)
# print(output)
zh_fonts = set(f.split(',', 1)[0] for f in output.split('\n'))
available = mat_fonts & zh_fonts
print('*' * 10, '可用的字体', '*' * 10)
for f in available:
    print(f)

for i, txt in enumerate(annotation):
    ax.annotate(txt, (x[i], y[i]))
plt.show()
