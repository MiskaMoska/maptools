import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, CirclePolygon
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import random


W = 8
H = 8
L = 5
R = 0.5
L_S1 = 8
LW = 5

# 创建图形和坐标轴
fig, ax = plt.subplots()
ax.axis('off')


heat_values = {}
for x in range(W):
    for y in range(H-1):
        edge1 = ((x, y), (x, y+1))
        edge2 = ((x, y+1), (x, y))
        heat_values[edge1] = random.randint(1, 100)
        heat_values[edge2] = random.randint(1, 100)

for y in range(H):
    for x in range(W-1):
        edge1 = ((x, y), (x+1, y))
        edge2 = ((x+1, y), (x, y))
        heat_values[edge1] = random.randint(1, 100)
        heat_values[edge2] = random.randint(1, 100)

# 调整图形边距
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  
cmap = plt.cm.get_cmap('coolwarm')

min_value = min(heat_values.values())
max_value = max(heat_values.values())

# 创建颜色映射规范化器
norm = colors.Normalize(vmin=min_value, vmax=max_value)

# 为每个元素赋予颜色
colored_heat_values = {}
for element, value in heat_values.items():
    color = cmap(norm(value))
    colored_heat_values[element] = color

# 设置坐标轴范围
ax.set_xlim(-2, (W-1)*L+2)
ax.set_ylim(-(H-1)*L-2, 2)
ax.set_aspect('equal')

link_dict = {}

# vertical links
for x in range(W):
    for y in range(H-1):
        edge1 = ((x, y), (x, y+1))
        edge2 = ((x, y+1), (x, y))
        src = (x*L, -y*L)
        dst = (x*L, (-y-1)*L)
        ctrl1 = (x*L-L/L_S1, -y*L-L/2)
        ctrl2 = (x*L+L/L_S1, -y*L-L/2)
        v1 = [src, ctrl1, dst]
        v2 = [src, ctrl2, dst]
        c = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path1 = Path(v1, c)
        path2 = Path(v2, c)
        patch1 = PathPatch(path1, facecolor='none', edgecolor=colored_heat_values[edge1], linewidth=LW)
        patch2 = PathPatch(path2, facecolor='none', edgecolor=colored_heat_values[edge2], linewidth=LW)
        link_dict[edge1] = patch1
        link_dict[edge2] = patch2
        ax.add_patch(patch1)
        ax.add_patch(patch2)

# # horizontal links
for y in range(H):
    for x in range(W-1):
        edge1 = ((x, y), (x+1, y))
        edge2 = ((x+1, y), (x, y))
        src = (x*L, -y*L)
        dst = ((x+1)*L, -y*L)
        ctrl1 = (x*L+L/2, -y*L-L/L_S1)
        ctrl2 = (x*L+L/2, -y*L+L/L_S1)
        v1 = [src, ctrl1, dst]
        v2 = [src, ctrl2, dst]
        c = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path1 = Path(v1, c)
        path2 = Path(v2, c)
        patch1 = PathPatch(path1, facecolor='none', edgecolor=colored_heat_values[edge1], linewidth=LW)
        patch2 = PathPatch(path2, facecolor='none', edgecolor=colored_heat_values[edge2], linewidth=LW)
        link_dict[edge1] = patch1
        link_dict[edge2] = patch2
        ax.add_patch(patch1)
        ax.add_patch(patch2)

for x in range(W):
    for y in range(H):
        node = CirclePolygon((x*L, -y*L), radius=R, facecolor='black', alpha=0.7)
        ax.add_patch(node)

# 显示图形

colorbar = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cbar = plt.colorbar(colorbar, ax=ax, shrink=0.8)

def format_func(value, tick_number):
    return f'{pow(2, value):.2e}'  # 将刻度值格式化为科学计数法

# 设置颜色卡的刻度标签映射
cbar.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_func(x, pos)))
plt.show()