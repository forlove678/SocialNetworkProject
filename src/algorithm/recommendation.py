"""
推荐算法实现（扩展功能）
功能：基于共同好友或共同兴趣的智能推荐
"""

from src.data_structure.heap import MaxHeap


class RecommendationSystem:
    """推荐系统类"""

    def __init__(self, graph, user_table):
        """
        初始化
        :param graph: AdjacencyList实例
        :param user_table: HashTable实例（存储用户信息）
        """
        self.graph = graph
        self.user_table = user_table

    def recommend_by_common_friends(self, user_id, top_k=5):
        """
        基于共同好友数量的推荐
        时间复杂度：O(V * d^2)，d为平均度数
        """
        try:
            user_id = int(user_id)
            top_k = int(top_k)
        except:
            return [], "参数格式错误"

        if not self.graph.has_user(user_id):
            return [], f"用户 {user_id} 不存在"

        # 获取用户的一度人脉
        direct_friends = self.graph.get_friends(user_id)

        # 计算每个非好友用户的共同好友数
        candidates = {}  # {用户ID: 共同好友数}

        # 遍历所有用户
        all_users = self.graph.get_all_users()
        for other in all_users:
            if other == user_id or other in direct_friends:
                continue  # 排除自己和现有人脉

            other_friends = self.graph.get_friends(other)
            # 计算共同好友数
            common = len(direct_friends & other_friends)
            if common > 0:
                candidates[other] = common

        # 获取Top-K
        return self._get_top_k(candidates, top_k)

    def recommend_by_interests(self, user_id, top_k=5):
        """
        基于共同兴趣的推荐
        需要用户信息中包含兴趣标签
        """
        try:
            user_id = int(user_id)
            top_k = int(top_k)
        except:
            return [], "参数格式错误"

        if not self.graph.has_user(user_id):
            return [], f"用户 {user_id} 不存在"

        # 获取当前用户的兴趣
        current_user = self.user_table.get(user_id)
        if not current_user:
            return [], "用户信息不存在"

        current_interests = set(current_user.interests.split(';')) if current_user.interests else set()
        if not current_interests:
            return [], "用户未设置兴趣标签"

        direct_friends = self.graph.get_friends(user_id)
        candidates = {}

        all_users = self.graph.get_all_users()
        for other in all_users:
            if other == user_id or other in direct_friends:
                continue

            other_user = self.user_table.get(other)
            if not other_user:
                continue

            other_interests = set(other_user.interests.split(';')) if other_user.interests else set()

            # 计算兴趣相似度（杰卡德相似系数）
            if current_interests and other_interests:
                intersection = len(current_interests & other_interests)
                union = len(current_interests | other_interests)
                similarity = intersection / union if union > 0 else 0

                if similarity > 0:
                    candidates[other] = {
                        'score': similarity,
                        'common_interests': list(current_interests & other_interests)
                    }

        # 按相似度排序
        sorted_candidates = sorted(
            candidates.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )[:top_k]

        result = []
        for user_id, info in sorted_candidates:
            user = self.user_table.get(user_id)
            result.append({
                'user_id': user_id,
                'name': user.name if user else f"用户{user_id}",
                'score': info['score'],
                'common_interests': info['common_interests'],
                'reason': f"共同兴趣: {', '.join(info['common_interests'])}"
            })

        return result, f"找到 {len(result)} 个推荐结果"

    def hybrid_recommend(self, user_id, top_k=5):
        """
        混合推荐算法
        综合考虑共同好友和共同兴趣
        """
        try:
            user_id = int(user_id)
            top_k = int(top_k)
        except:
            return [], "参数格式错误"

        if not self.graph.has_user(user_id):
            return [], f"用户 {user_id} 不存在"

        direct_friends = self.graph.get_friends(user_id)
        current_user = self.user_table.get(user_id)
        current_interests = set(current_user.interests.split(';')) if current_user and current_user.interests else set()

        candidates = {}
        all_users = self.graph.get_all_users()

        for other in all_users:
            if other == user_id or other in direct_friends:
                continue

            score = 0
            reason_parts = []

            # 共同好友得分（权重0.6）
            other_friends = self.graph.get_friends(other)
            common_friends = direct_friends & other_friends
            if common_friends:
                friend_score = len(common_friends) * 0.6
                score += friend_score
                reason_parts.append(f"共同好友{len(common_friends)}人")

            # 共同兴趣得分（权重0.4）
            if current_interests:
                other_user = self.user_table.get(other)
                if other_user and other_user.interests:
                    other_interests = set(other_user.interests.split(';'))
                    common_interests = current_interests & other_interests
                    if common_interests:
                        interest_score = len(common_interests) * 0.4
                        score += interest_score
                        reason_parts.append(f"共同兴趣{len(common_interests)}个")

            if score > 0:
                other_user_info = self.user_table.get(other)
                candidates[other] = {
                    'score': score,
                    'reason': '；'.join(reason_parts),
                    'name': other_user_info.name if other_user_info else f"用户{other}"
                }

        # 使用堆排序
        return self._get_top_k(candidates, top_k, value_key='score')

    def _get_top_k(self, candidates, k, value_key=None):
        """
        获取Top-K推荐结果
        使用堆排序优化
        """
        if not candidates:
            return [], "没有找到合适的推荐"

        # 转换为列表便于排序
        items = []
        for user_id, value in candidates.items():
            if value_key:
                score = value[value_key]
                items.append((score, user_id, value))
            else:
                items.append((value, user_id, {'score': value}))

        # 使用堆获取Top-K
        heap = MaxHeap(k + 1)
        for item in items:
            heap.push(item)

        # 提取结果
        result = []
        while not heap.is_empty() and len(result) < k:
            item = heap.pop()
            score, user_id, info = item
            user = self.user_table.get(user_id)

            result.append({
                'user_id': user_id,
                'name': info.get('name', user.name if user else f"用户{user_id}"),
                'score': score,
                'reason': info.get('reason', f'推荐指数: {score:.2f}')
            })

        return result, f"找到{len(result)}个推荐结果"