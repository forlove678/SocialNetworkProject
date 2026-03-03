def recommend_by_interest(user_id, user_cache, adj_list, top_k=3):
    """基于兴趣标签推荐不在好友列表中的人"""
    target_user = user_cache.get(user_id)
    if not target_user: return []

    target_interests = set(target_user['兴趣标签'].split(';'))
    my_friends = set(adj_list.get_neighbors(user_id))

    recommendations = []
    # 遍历所有用户
    # 假设我们能获取所有 ID
    for other_id in range(1, 100):  # 示例范围
        oid = str(other_id)
        if oid == user_id or oid in my_friends: continue

        other_user = user_cache.get(oid)
        if other_user:
            other_interests = set(other_user['兴趣标签'].split(';'))
            common = target_interests.intersection(other_interests)
            if common:
                recommendations.append((oid, other_user['姓名'], len(common)))

    # 按共同兴趣数量排序
    recommendations.sort(key=lambda x: x[2], reverse=True)
    return recommendations[:top_k]