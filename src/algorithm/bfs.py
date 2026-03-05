"""
BFS算法实现
功能：实现二度人脉查询和社交距离计算
"""

from collections import deque


class BFSAlgorithm:
    """BFS算法类"""

    def __init__(self, graph):
        """
        初始化
        :param graph: AdjacencyList实例
        """
        self.graph = graph

    def find_second_degree(self, user_id):
        """
        查询二度人脉（好友的好友）
        时间复杂度：O(V+E)，V为节点数，E为边数
        """
        try:
            user_id = int(user_id)
        except:
            return {}, "用户ID格式错误"

        if not self.graph.has_user(user_id):
            return {}, f"用户 {user_id} 不存在"

        # 获取一度人脉
        first_degree = self.graph.get_friends(user_id)

        # BFS找二度人脉
        second_degree = {}  # 存储二度人脉及其连接路径
        visited = {user_id}  # 已访问集合
        visited.update(first_degree)  # 一度人脉也标记为已访问

        # 对于每个一度人脉，找其好友
        for friend in first_degree:
            friend_friends = self.graph.get_friends(friend)
            for potential in friend_friends:
                if potential not in visited:
                    # 找到二度人脉
                    visited.add(potential)
                    # 记录路径
                    second_degree[potential] = {
                        'path': f"{user_id} → {friend} → {potential}",
                        'via': friend
                    }

        if second_degree:
            return second_degree, f"找到 {len(second_degree)} 个二度人脉"
        else:
            return {}, "没有找到二度人脉"

    def find_shortest_path(self, start_id, end_id):
        """
        计算最短社交距离（最少好友中转次数）
        返回：(距离, 路径, 消息)
        """
        try:
            start_id = int(start_id)
            end_id = int(end_id)
        except:
            return -1, [], "用户ID格式错误"

        # 异常检查
        if not self.graph.has_user(start_id):
            return -1, [], f"起始用户 {start_id} 不存在"
        if not self.graph.has_user(end_id):
            return -1, [], f"目标用户 {end_id} 不存在"
        if start_id == end_id:
            return 0, [start_id], "同一用户"

        # BFS搜索最短路径
        visited = {start_id}
        queue = deque([(start_id, [start_id])])  # (当前节点, 路径)

        while queue:
            current, path = queue.popleft()

            # 遍历当前用户的所有好友
            for friend in self.graph.get_friends(current):
                if friend not in visited:
                    visited.add(friend)
                    new_path = path + [friend]

                    if friend == end_id:
                        # 找到目标
                        distance = len(new_path) - 1
                        return distance, new_path, f"社交距离: {distance}"

                    queue.append((friend, new_path))

        return -1, [], "无社交关联"

    def find_multi_degree(self, user_id, degree):
        """
        查询多度人脉（扩展功能）
        :param degree: 查询深度
        """
        try:
            user_id = int(user_id)
            degree = int(degree)
        except:
            return {}, "参数格式错误"

        if not self.graph.has_user(user_id):
            return {}, f"用户 {user_id} 不存在"

        if degree < 1:
            return {}, "度数必须大于等于1"

        # BFS层序遍历
        result = {}  # 存储{用户ID: (度数, 路径)}
        visited = {user_id}
        queue = deque([(user_id, [user_id], 0)])  # (当前节点, 路径, 当前度数)

        while queue:
            current, path, current_degree = queue.popleft()

            if 0 < current_degree <= degree:
                # 记录该度数的节点
                result[current] = {
                    'degree': current_degree,
                    'path': ' → '.join(map(str, path))
                }

            if current_degree < degree:
                # 继续BFS
                for friend in self.graph.get_friends(current):
                    if friend not in visited:
                        visited.add(friend)
                        new_path = path + [friend]
                        queue.append((friend, new_path, current_degree + 1))

        # 按度数排序
        sorted_result = dict(sorted(
            result.items(),
            key=lambda x: (x[1]['degree'], x[0])
        ))

        if sorted_result:
            return sorted_result, f"找到 {len(sorted_result)} 个多度人脉"
        else:
            return {}, f"没有找到 {degree} 度内的人脉"