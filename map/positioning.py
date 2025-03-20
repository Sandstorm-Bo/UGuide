import json

# 解析道路文件
with open('map\北邮道路.geojson', 'r',encoding='utf-8') as f:
    roads_data = json.load(f)

# 解析景点文件
with open('map\北邮景点.geojson', 'r',encoding='utf-8') as f:
    attractions_data = json.load(f)

# 提取景点坐标
attractions = [feature['geometry']['coordinates'] for feature in attractions_data['features']]

import networkx as nx

# 创建图
G = nx.Graph()

# 遍历道路数据，添加边
for feature in roads_data['features']:
    geometry = feature['geometry']
    if geometry['type'] == 'MultiLineString':
        for line in geometry['coordinates']:
            for i in range(len(line) - 1):
                G.add_edge(tuple(line[i]), tuple(line[i + 1]))

# 假设我们要从第一个景点到第二个景点
start_point = attractions[0]
end_point = attractions[1]

# 使用Dijkstra算法找到最短路径
shortest_path = nx.dijkstra_path(G, tuple(start_point), tuple(end_point))

print("最短路径:", shortest_path)

import matplotlib.pyplot as plt

# 绘制所有道路
for feature in roads_data['features']:
    geometry = feature['geometry']
    if geometry['type'] == 'MultiLineString':
        for line in geometry['coordinates']:
            x, y = zip(*line)
            plt.plot(x, y, 'b-')

# 绘制最短路径
x, y = zip(*shortest_path)
plt.plot(x, y, 'r-', linewidth=2)

# 绘制景点
for attraction in attractions:
    plt.plot(attraction[0], attraction[1], 'go')  # 绿色圆点表示景点

plt.show()