"""
社交网络图谱分析及智能推荐系统
主程序入口
"""

import os
import sys
import tkinter as tk

# 动态锁定路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir])

from data_structure.adjacency_list import AdjacencyList
from data_structure.hash_table import HashTable
from utils.data_reader import load_data
from gui.main_window import SocialGui


def main():
    adj = AdjacencyList()
    cache = HashTable()

    # 路径拼接：指向根目录下的 data
    u_p = os.path.join(parent_dir, 'data', 'user_sample.csv')
    f_p = os.path.join(parent_dir, 'data', 'friend_sample.txt')

    print(f"正在加载数据...")
    print(f"用户文件: {u_p}")
    print(f"关系文件: {f_p}")

    # 数据持久化读取
    success, message = load_data(u_p, f_p, cache, adj)
    if success:
        print(message)
        root = tk.Tk()
        root.title("社交网络系统 - 2024级课程设计")
        app = SocialGui(root, adj, cache)
        root.mainloop()
    else:
        print(f"致命错误：{message}")
        print(f"请确保数据文件存在于：{os.path.dirname(u_p)}")
        input("按回车键退出...")


if __name__ == "__main__":
    main()