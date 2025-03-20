import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义一个函数来捕捉（snap）接近的点
def snap_points(coordinates, tolerance=0.00005):
    """
    将距离非常近的点合并为同一个点
    
    参数:
    coordinates: 所有坐标点的列表
    tolerance: 容差，如果两点距离小于此值，则被视为同一点
    
    返回:
    snapped_coords: 每个原始点对应的捕捉后的点的字典
    """
    # 创建KD树来进行快速近邻搜索
    tree = cKDTree(coordinates)
    
    # 为每个点找到邻近的点
    groups = {}
    visited = set()
    
    for i, point in enumerate(coordinates):
        if i in visited:
            continue
            
        # 找到所有在容差范围内的点
        indices = tree.query_ball_point(point, tolerance)
        
        # 将这些点分组
        representative = tuple(coordinates[indices[0]])  # 使用组内第一个点作为代表
        group = [indices[0]]
        
        for idx in indices[1:]:
            if idx not in visited:
                group.append(idx)
                
        # 标记所有这些点为已访问
        visited.update(indices)
        
        # 保存这个组
        groups[representative] = group
    
    # 创建原始点到捕捉点的映射
    snapped_coords = {}
    for rep, group in groups.items():
        for idx in group:
            snapped_coords[tuple(coordinates[idx])] = rep
            
    return snapped_coords

def line_intersection(p1, p2, p3, p4):
    """
    计算两条线段的交点
    返回: 如果相交返回交点坐标，否则返回None
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:  # 平行或重合
        return None
        
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
    
    # 检查交点是否在两条线段上
    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    return None

def find_intersections(roads_data):
    """
    查找所有道路的交点并添加到道路数据中
    """
    intersections = []
    modified_features = []
    
    # 遍历所有可能的道路对
    for i, feature1 in enumerate(roads_data['features']):
        if feature1['geometry']['type'] != 'MultiLineString':
            continue
            
        new_lines1 = []
        for line1 in feature1['geometry']['coordinates']:
            current_line = []
            for j in range(len(line1) - 1):
                current_line.append(line1[j])
                
                # 检查与其他所有线段的交点
                for feature2 in roads_data['features'][i+1:]:
                    if feature2['geometry']['type'] != 'MultiLineString':
                        continue
                        
                    for line2 in feature2['geometry']['coordinates']:
                        for k in range(len(line2) - 1):
                            intersection = line_intersection(
                                line1[j], line1[j+1],
                                line2[k], line2[k+1]
                            )
                            
                            if intersection:
                                # 将交点转换为元组并四舍五入到6位小数
                                intersection = tuple(round(x, 6) for x in intersection)
                                if intersection not in intersections:
                                    intersections.append(intersection)
                                    current_line.append(list(intersection))
                                    
            current_line.append(line1[-1])
            new_lines1.append(current_line)
            
        # 更新当前要素的坐标
        feature1['geometry']['coordinates'] = new_lines1
        modified_features.append(feature1)
    
    # 更新道路数据
    roads_data['features'] = modified_features
    return roads_data, intersections

# 主程序代码
def main():
    # 解析道路文件
    with open('map/北邮道路.geojson', 'r', encoding='utf-8') as f:
        roads_data = json.load(f)

    # 解析景点文件
    with open('map/北邮地点.geojson', 'r', encoding='utf-8') as f:
        attractions_data = json.load(f)

    # 提取景点坐标
    attractions = [feature['geometry']['coordinates'] for feature in attractions_data['features']]

    # 在创建图之前，先处理交点
    roads_data, intersections = find_intersections(roads_data)
    
    # 收集所有坐标点（包括交点）
    all_points = []
    for feature in roads_data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'MultiLineString':
            for line in geometry['coordinates']:
                for point in line:
                    all_points.append(point)

    # 添加景点坐标
    for attraction in attractions:
        all_points.append(attraction)

    # 将所有点转换为numpy数组以便处理
    all_points_array = np.array(all_points)

    # 捕捉接近的点
    snapped_points = snap_points(all_points_array)

    # 创建图
    G = nx.Graph()

    # 遍历道路数据，添加边
    for feature in roads_data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'MultiLineString':
            for line in geometry['coordinates']:
                for i in range(len(line) - 1):
                    # 使用捕捉后的点作为节点
                    start = snapped_points[tuple(line[i])]
                    end = snapped_points[tuple(line[i + 1])]
                    
                    # 计算边的权重（距离）
                    weight = np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
                    
                    # 添加边到图中
                    if start != end:  # 避免自环
                        G.add_edge(start, end, weight=weight)

    # 捕捉起点和终点
    start_point = snapped_points[tuple(attractions[-8])]
    end_point = snapped_points[tuple(attractions[8])]

    # 使用Dijkstra算法找到最短路径
    shortest_path = nx.dijkstra_path(G, start_point, end_point, weight='weight')

    print("最短路径:", shortest_path)

    # 绘制所有道路
    plt.figure(figsize=(10, 8))
    for feature in roads_data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'MultiLineString':
            for line in geometry['coordinates']:
                # 使用原始坐标绘制道路
                x, y = zip(*line)
                plt.plot(x, y, 'b-', alpha=0.5)

    # 绘制最短路径
    x, y = zip(*shortest_path)
    plt.plot(x, y, 'r-', linewidth=2)

    # 绘制景点
    for attraction in attractions:
        plt.plot(attraction[0], attraction[1], 'go', markersize=8)

    # 绘制捕捉后的点
    unique_snapped = set(snapped_points.values())
    snapped_x, snapped_y = zip(*unique_snapped)
    plt.plot(snapped_x, snapped_y, 'rx', markersize=3)

    # 在绘图部分添加交点的显示
    plt.title('北邮校园导航路径')
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.grid(True)
    plt.show()

# 确保在作为脚本运行时才执行main函数
if __name__ == "__main__":
    main()