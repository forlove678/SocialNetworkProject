import tkinter as tk
import os
from data_structure.adjacency_list import AdjacencyList
from data_structure.hash_table import HashTable
from utils.data_reader import DataReader
from gui.main_window import SocialNetworkApp


def main():
    adj_list = AdjacencyList()
    user_cache = HashTable()

    # 获取项目根目录路径（处理 src 运行时的路径问题）
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    user_path = os.path.join(base_dir, "data", "user_sample.csv")
    friend_path = os.path.join(base_dir, "data", "friend_sample.txt")

    try:
        DataReader.load_users(user_path, user_cache)
        DataReader.load_relations(friend_path, adj_list)
    except FileNotFoundError:
        print("警告：未找到数据文件，请检查 data/ 目录。")

    root = tk.Tk()
    app = SocialNetworkApp(root, adj_list, user_cache)
    root.mainloop()


if __name__ == "__main__":
    main()