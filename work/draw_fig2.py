import numpy as np
import matplotlib.pyplot as plt

# 数据
categories = ['VGG16 \n@Big Xbar', 'VGG16 \n@Small Xbar', 'ResNet18 \n@Big Xbar', 'ResNet18 \n@Small Xbar', 'miniYOLOv3 \n@Big Xbar', 'miniYOLOv3 \n@Small Xbar']
concat = [300208.5, 264960.625, 84376.75, 74123.125, 704937, 591267.75]  # 第一个量
noconcat = [244697.125, 178763.25, 64415.75, 53268.25, 505923.375, 414486.25]  # 第二个量

y3 = [1]*len(concat)
y2 = [2.672268907, 3.35, 2.9556962, 3.98224852, 1.65671, 2.6319018]
y1 = [5,7,7,10,3,5]

bwidth = 1.5

# 设置柱子宽度
bar_width = 0.2

# 计算每个柱子的位置
bar_positions1 = np.arange(len(categories))
bar_positions2 = bar_positions1 + bar_width
bar_positions3 = bar_positions1 + 2*bar_width

plt.figure(figsize=(8.2, 4))  # 设置图形的宽度为10，高度为6

# 创建柱状图
plt.bar(bar_positions1, y1, width=bar_width, label='Max Buffer Number @Conventional Method', edgecolor='black', color='#f8b12c', linewidth=bwidth)
plt.bar(bar_positions2, y2, width=bar_width, label='Average Buffer Number @Conventional Method', edgecolor='black', color='#bb3121', linewidth=bwidth)
plt.bar(bar_positions3, y3, width=bar_width, label='Buffer Number @Our Novel Method', edgecolor='black', color='#212968', linewidth=bwidth)

# 添加标签和标题
# plt.xlabel('Categories')
plt.ylabel('Local Port Buffer Number')
# plt.title('Comparison of Quantity 1 and Quantity 2')

# 设置 x 轴刻度标签
plt.xticks(bar_positions1 + bar_width / 2, categories)

# 设置外部边框宽度
ax = plt.gca()  # 获取当前坐标轴
ax.spines['top'].set_linewidth(bwidth)    # 顶部边框宽度
ax.spines['right'].set_linewidth(bwidth)  # 右侧边框宽度
ax.spines['bottom'].set_linewidth(bwidth) # 底部边框宽度
ax.spines['left'].set_linewidth(bwidth)   # 左侧边框宽度

# 添加图例
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=2)
plt.tick_params(axis='both', width=bwidth)
plt.tight_layout()
# 展示图形
plt.savefig('./fig2.png',dpi=300)
plt.show()
