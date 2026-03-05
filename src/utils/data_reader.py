"""
数据读取模块
支持从CSV/TXT文件加载用户信息和好友关系
"""

import csv
import os
import sys

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from data_structure.hash_table import UserInfo


def load_users(filepath, cache):
    """
    加载用户信息
    支持CSV格式：用户ID,姓名,兴趣标签
    """
    users_loaded = 0

    if not os.path.exists(filepath):
        return False, f"用户文件不存在: {filepath}"

    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader)  # 跳过表头

            for row_num, row in enumerate(reader, start=2):
                if not row or len(row) < 2:
                    continue

                try:
                    user_id = int(row[0].strip())
                    name = row[1].strip()
                    interests = row[2].strip() if len(row) > 2 else ""

                    user_info = UserInfo(user_id, name, interests)
                    success, msg = cache.insert(user_id, user_info)
                    if success:
                        users_loaded += 1

                except ValueError as e:
                    print(f"警告: 第{row_num}行数据格式错误 - {str(e)}")
                except Exception as e:
                    print(f"警告: 第{row_num}行处理出错 - {str(e)}")

        return True, f"成功加载 {users_loaded} 个用户"

    except Exception as e:
        return False, f"读取用户文件失败: {str(e)}"


def load_relations(filepath, graph, cache):
    """
    加载好友关系
    支持TXT格式：用户ID1,用户ID2
    """
    relations_loaded = 0
    skipped = 0

    if not os.path.exists(filepath):
        return False, f"关系文件不存在: {filepath}"

    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split(',')
                if len(parts) != 2:
                    skipped += 1
                    continue

                try:
                    user1 = int(parts[0].strip())
                    user2 = int(parts[1].strip())

                    # 检查用户是否存在
                    if not cache.contains(user1) or not cache.contains(user2):
                        skipped += 1
                        continue

                    # 添加用户到图（如果尚未添加）
                    graph.add_user(user1)
                    graph.add_user(user2)

                    # 添加好友关系
                    success, msg = graph.add_friend(user1, user2)
                    if success:
                        relations_loaded += 1
                    else:
                        skipped += 1

                except ValueError:
                    skipped += 1
                except Exception as e:
                    skipped += 1
                    print(f"警告: 第{line_num}行处理出错 - {str(e)}")

        return True, f"成功加载 {relations_loaded} 条好友关系 (跳过 {skipped} 条无效数据)"

    except Exception as e:
        return False, f"读取关系文件失败: {str(e)}"


def load_data(user_file, relation_file, cache, graph):
    """
    加载所有数据的便捷函数
    """
    # 先加载用户
    user_success, user_msg = load_users(user_file, cache)
    if not user_success:
        return False, user_msg

    # 确保所有用户在图中存在
    for user_info in cache.get_all():
        graph.add_user(user_info.user_id)

    # 再加载关系
    rel_success, rel_msg = load_relations(relation_file, graph, cache)
    if not rel_success:
        return False, rel_msg

    return True, f"数据加载完成\n{user_msg}\n{rel_msg}"