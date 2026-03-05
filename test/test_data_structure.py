import os
import sys
import tkinter as tk

# 动态锁定路径，确保能找到 src 目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir])

# 现在可以使用绝对导入
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

    # 数据持久化读取
    success, message = load_data(u_p, f_p, cache, adj)
    if success:
        root = tk.Tk()
        root.title("社交网络系统 - 2024级课程设计")
        app = SocialGui(root, adj, cache)
        root.mainloop()
    else:
        # 异常提示
        print(f"致命错误：{message}")
        print(f"请确保数据文件存在于：{os.path.dirname(u_p)}")


if __name__ == "__main__":
    main()