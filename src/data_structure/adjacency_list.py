"""
邻接表实现无向图
功能：存储用户好友关系，支持增删改查操作
"""

class AdjacencyList:
    """邻接表类 - 用于存储和管理用户好友关系"""

    def __init__(self):
        """初始化邻接表"""
        self.graph = {}  # 使用字典存储邻接表，键为用户ID，值为邻居集合
        self.user_count = 0

    def add_user(self, user_id):
        """
        添加新用户
        时间复杂度：O(1)
        """
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return False, "用户ID必须是有效的数字"

        if user_id in self.graph:
            return False, f"用户 {user_id} 已存在"

        self.graph[user_id] = set()
        self.user_count += 1
        return True, f"用户 {user_id} 添加成功"

    def remove_user(self, user_id):
        """
        删除用户及其所有好友关系
        时间复杂度：O(n)，n为好友数量
        """
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return False, "用户ID必须是有效的数字"

        if user_id not in self.graph:
            return False, f"用户 {user_id} 不存在"

        # 获取该用户的所有好友
        friends = list(self.graph[user_id])

        # 删除与该用户相关的所有好友关系
        for friend in friends:
            if friend in self.graph:
                self.graph[friend].discard(user_id)

        # 删除用户节点
        del self.graph[user_id]
        self.user_count -= 1
        return True, f"用户 {user_id} 删除成功"

    def add_friend(self, user1, user2):
        """
        添加好友关系（无向图，双向添加）
        时间复杂度：O(1)
        """
        try:
            user1 = int(user1)
            user2 = int(user2)
        except (ValueError, TypeError):
            return False, "用户ID必须是有效的数字"

        if user1 not in self.graph:
            return False, f"用户 {user1} 不存在"
        if user2 not in self.graph:
            return False, f"用户 {user2} 不存在"

        if user1 == user2:
            return False, "不能和自己成为好友"

        if user2 in self.graph[user1]:
            return False, "好友关系已存在"

        self.graph[user1].add(user2)
        self.graph[user2].add(user1)
        return True, "好友关系添加成功"

    def remove_friend(self, user1, user2):
        """
        删除好友关系
        时间复杂度：O(1)
        """
        try:
            user1 = int(user1)
            user2 = int(user2)
        except (ValueError, TypeError):
            return False, "用户ID必须是有效的数字"

        if user1 not in self.graph or user2 not in self.graph:
            return False, "用户不存在"

        if user2 in self.graph[user1]:
            self.graph[user1].remove(user2)
            self.graph[user2].remove(user1)
            return True, "好友关系删除成功"

        return False, "好友关系不存在"

    def get_friends(self, user_id):
        """
        获取用户的所有一度人脉
        时间复杂度：O(1)
        """
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return set()

        if user_id not in self.graph:
            return set()
        return self.graph[user_id].copy()

    def has_user(self, user_id):
        """检查用户是否存在"""
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return False
        return user_id in self.graph

    def has_friend(self, user1, user2):
        """检查两人是否为好友"""
        try:
            user1 = int(user1)
            user2 = int(user2)
        except (ValueError, TypeError):
            return False

        if user1 not in self.graph or user2 not in self.graph:
            return False
        return user2 in self.graph[user1]

    def get_all_users(self):
        """获取所有用户ID"""
        return list(self.graph.keys())

    def get_graph_size(self):
        """获取图中用户数量"""
        return len(self.graph)

    def get_edge_count(self):
        """获取好友关系数量"""
        count = 0
        for user in self.graph:
            count += len(self.graph[user])
        return count // 2  # 无向图每条边计算两次