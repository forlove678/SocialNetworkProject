import tkinter as tk
from tkinter import messagebox
from algorithm.bfs import get_connections


class SocialNetworkApp:
    def __init__(self, root, adj_list, user_cache):
        self.root = root
        self.adj_list = adj_list
        self.user_cache = user_cache
        self.root.title("社交网络分析系统")

        tk.Label(root, text="输入用户ID:").pack(pady=5)
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        tk.Button(root, text="查询一度人脉", command=lambda: self.search(1)).pack(pady=5)
        tk.Button(root, text="查询二度人脉", command=lambda: self.search(2)).pack(pady=5)

        self.result_text = tk.Text(root, height=10, width=40)
        self.result_text.pack(pady=10)

    def search(self, deg):
        uid = self.entry.get()
        if not self.user_cache.get(uid):
            messagebox.showerror("错误", "用户不存在")
            return

        conns = get_connections(self.adj_list, uid, deg)
        self.result_text.delete(1.0, tk.END)
        for c in conns:
            info = self.user_cache.get(c)
            self.result_text.insert(tk.END, f"ID: {c}, 姓名: {info['姓名']}\n")