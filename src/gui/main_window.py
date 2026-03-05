"""
主界面模块
实现社交网络系统的图形用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from src.algorithm.bfs import BFSAlgorithm
from src.algorithm.recommendation import RecommendationSystem


class SocialGui:
    """社交网络系统主界面"""

    def __init__(self, root, graph, cache):
        self.root = root
        self.graph = graph
        self.cache = cache
        self.bfs = BFSAlgorithm(graph)
        self.recommender = RecommendationSystem(graph, cache)

        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.create_menu()
        self.create_main_frames()
        self.create_status_bar()

        # 初始化显示
        self.update_status("系统就绪")
        self.update_stats_display()

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="刷新数据", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)

        # 查看菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="查看", menu=view_menu)
        view_menu.add_command(label="网络统计", command=self.show_statistics)
        view_menu.add_command(label="所有用户", command=self.show_all_users)

        # 扩展功能菜单
        extend_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="扩展功能", menu=extend_menu)
        extend_menu.add_command(label="多度人脉查询", command=self.show_multi_degree_dialog)
        extend_menu.add_command(label="智能推荐", command=self.show_recommend_dialog)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)

    def create_main_frames(self):
        """创建主界面框架"""
        # 主容器
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧控制面板
        left_frame = ttk.Frame(main_container, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        # 右侧结果显示面板
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_control_panel(left_frame)
        self.create_result_panel(right_frame)

    def create_control_panel(self, parent):
        """创建左侧控制面板"""
        # 标题
        title = ttk.Label(parent, text="社交网络分析系统",
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)

        # 数据统计信息
        self.stats_frame = ttk.LabelFrame(parent, text="数据统计", padding=5)
        self.stats_frame.pack(fill=tk.X, pady=5)

        self.user_count_label = ttk.Label(self.stats_frame, text="用户数: 0")
        self.user_count_label.pack(anchor=tk.W)

        self.rel_count_label = ttk.Label(self.stats_frame, text="关系数: 0")
        self.rel_count_label.pack(anchor=tk.W)

        # 一度人脉查询
        degree1_frame = ttk.LabelFrame(parent, text="一度人脉查询", padding=5)
        degree1_frame.pack(fill=tk.X, pady=5)

        ttk.Label(degree1_frame, text="用户ID:").grid(row=0, column=0, padx=5, pady=5)
        self.degree1_entry = ttk.Entry(degree1_frame, width=15)
        self.degree1_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(degree1_frame, text="查询",
                  command=self.query_first_degree).grid(row=0, column=2, padx=5, pady=5)

        # 二度人脉查询
        degree2_frame = ttk.LabelFrame(parent, text="二度人脉查询", padding=5)
        degree2_frame.pack(fill=tk.X, pady=5)

        ttk.Label(degree2_frame, text="用户ID:").grid(row=0, column=0, padx=5, pady=5)
        self.degree2_entry = ttk.Entry(degree2_frame, width=15)
        self.degree2_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(degree2_frame, text="查询",
                  command=self.query_second_degree).grid(row=0, column=2, padx=5, pady=5)

        # 社交距离计算
        distance_frame = ttk.LabelFrame(parent, text="社交距离计算", padding=5)
        distance_frame.pack(fill=tk.X, pady=5)

        ttk.Label(distance_frame, text="起始用户:").grid(row=0, column=0, padx=5, pady=5)
        self.start_entry = ttk.Entry(distance_frame, width=10)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(distance_frame, text="目标用户:").grid(row=1, column=0, padx=5, pady=5)
        self.end_entry = ttk.Entry(distance_frame, width=10)
        self.end_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(distance_frame, text="计算",
                  command=self.calculate_distance).grid(row=1, column=2, padx=5, pady=5)

        # 用户信息查询
        info_frame = ttk.LabelFrame(parent, text="用户信息查询", padding=5)
        info_frame.pack(fill=tk.X, pady=5)

        ttk.Label(info_frame, text="用户ID:").grid(row=0, column=0, padx=5, pady=5)
        self.info_entry = ttk.Entry(info_frame, width=15)
        self.info_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(info_frame, text="查询",
                  command=self.query_user_info).grid(row=0, column=2, padx=5, pady=5)

        # 刷新按钮
        ttk.Button(parent, text="刷新统计",
                  command=self.update_stats_display).pack(fill=tk.X, pady=10)

    def create_result_panel(self, parent):
        """创建右侧结果显示面板"""
        # 创建选项卡
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 查询结果选项卡
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="查询结果")

        self.result_text = ScrolledText(self.result_frame, wrap=tk.WORD,
                                        font=('Arial', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 路径显示选项卡
        self.path_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.path_frame, text="路径显示")

        self.path_text = ScrolledText(self.path_frame, wrap=tk.WORD,
                                      font=('Arial', 10))
        self.path_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 设置文本标签样式
        self.result_text.tag_configure("title", font=('Arial', 12, 'bold'))
        self.result_text.tag_configure("error", foreground="red", font=('Arial', 10, 'bold'))
        self.result_text.tag_configure("success", foreground="green", font=('Arial', 10, 'bold'))
        self.result_text.tag_configure("highlight", foreground="blue", font=('Arial', 10, 'bold'))

        self.path_text.tag_configure("title", font=('Arial', 12, 'bold'))
        self.path_text.tag_configure("path", foreground="blue", font=('Arial', 10))

    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = ttk.Label(self.status_bar, text="就绪",
                                      relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_status(self, message):
        """更新状态栏"""
        self.status_label.config(text=message)
        self.root.update()

    def update_stats_display(self):
        """更新统计显示"""
        user_count = len(self.graph.get_all_users())
        rel_count = self.graph.get_edge_count()

        self.user_count_label.config(text=f"用户数: {user_count}")
        self.rel_count_label.config(text=f"关系数: {rel_count}")

    def query_first_degree(self):
        """查询一度人脉"""
        user_id = self.degree1_entry.get().strip()

        if not user_id:
            messagebox.showwarning("输入错误", "请输入用户ID")
            return

        try:
            user_id = int(user_id)
        except:
            messagebox.showerror("输入错误", "用户ID必须是数字")
            return

        self.update_status(f"正在查询用户 {user_id} 的一度人脉...")

        if not self.graph.has_user(user_id):
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"❌ 用户 {user_id} 不存在\n", "error")
            self.update_status("查询失败：用户不存在")
            return

        friends = self.graph.get_friends(user_id)

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"👥 用户 {user_id} 的一度人脉\n", "title")
        self.result_text.insert(tk.END, "="*40 + "\n\n")

        if friends:
            self.result_text.insert(tk.END, f"共找到 {len(friends)} 个好友:\n\n", "highlight")

            for i, friend_id in enumerate(sorted(friends), 1):
                user_info = self.cache.get(friend_id)
                name = user_info.name if user_info else f"用户{friend_id}"

                self.result_text.insert(tk.END, f"{i:2d}. ID: {friend_id}\n")
                self.result_text.insert(tk.END, f"    姓名: {name}\n\n")
        else:
            self.result_text.insert(tk.END, "该用户暂无好友\n")

        self.notebook.select(0)
        self.update_status("查询完成")

    def query_second_degree(self):
        """查询二度人脉"""
        user_id = self.degree2_entry.get().strip()

        if not user_id:
            messagebox.showwarning("输入错误", "请输入用户ID")
            return

        try:
            user_id = int(user_id)
        except:
            messagebox.showerror("输入错误", "用户ID必须是数字")
            return

        self.update_status(f"正在查询用户 {user_id} 的二度人脉...")

        second_degree, message = self.bfs.find_second_degree(user_id)

        self.result_text.delete(1.0, tk.END)

        if second_degree:
            self.result_text.insert(tk.END, f"🔄 用户 {user_id} 的二度人脉\n", "title")
            self.result_text.insert(tk.END, "="*40 + "\n\n")
            self.result_text.insert(tk.END, f"共找到 {len(second_degree)} 个二度人脉:\n\n", "highlight")

            for i, (friend_id, info) in enumerate(sorted(second_degree.items()), 1):
                user_info = self.cache.get(friend_id)
                name = user_info.name if user_info else f"用户{friend_id}"

                self.result_text.insert(tk.END, f"{i:2d}. {name} (ID: {friend_id})\n")
                self.result_text.insert(tk.END, f"    路径: {info['path']}\n\n")
        else:
            self.result_text.insert(tk.END, message + "\n", "error" if "不存在" in message else "normal")

        self.notebook.select(0)
        self.update_status(message)

    def calculate_distance(self):
        """计算社交距离"""
        start_id = self.start_entry.get().strip()
        end_id = self.end_entry.get().strip()

        if not start_id or not end_id:
            messagebox.showwarning("输入错误", "请输入起始用户ID和目标用户ID")
            return

        try:
            start_id = int(start_id)
            end_id = int(end_id)
        except:
            messagebox.showerror("输入错误", "用户ID必须是数字")
            return

        self.update_status(f"正在计算 {start_id} 到 {end_id} 的社交距离...")

        distance, path, message = self.bfs.find_shortest_path(start_id, end_id)

        self.result_text.delete(1.0, tk.END)
        self.path_text.delete(1.0, tk.END)

        if distance >= 0:
            self.result_text.insert(tk.END, f"📏 社交距离计算结果\n", "title")
            self.result_text.insert(tk.END, "="*40 + "\n\n")
            self.result_text.insert(tk.END, f"起始用户: {start_id}\n")
            self.result_text.insert(tk.END, f"目标用户: {end_id}\n")
            self.result_text.insert(tk.END, f"社交距离: {distance} 次中转\n\n", "highlight")

            # 显示路径
            self.path_text.insert(tk.END, f"🛣️ 详细路径\n", "title")
            self.path_text.insert(tk.END, "="*40 + "\n\n")

            path_str = " → ".join(map(str, path))
            self.path_text.insert(tk.END, path_str + "\n", "path")

            # 显示路径详情
            self.path_text.insert(tk.END, "\n路径详情:\n", "highlight")
            for i in range(len(path) - 1):
                current = path[i]
                next_user = path[i + 1]
                current_info = self.cache.get(current)
                next_info = self.cache.get(next_user)

                current_name = current_info.name if current_info else f"用户{current}"
                next_name = next_info.name if next_info else f"用户{next_user}"

                self.path_text.insert(tk.END, f"  {current_name} → {next_name}\n")
        else:
            self.result_text.insert(tk.END, f"❌ {message}\n", "error")
            self.path_text.insert(tk.END, message + "\n")

        self.result_text.insert(tk.END, f"\n{message}")
        self.notebook.select(1) if distance >= 0 else self.notebook.select(0)
        self.update_status(message)

    def query_user_info(self):
        """查询用户信息"""
        user_id = self.info_entry.get().strip()

        if not user_id:
            messagebox.showwarning("输入错误", "请输入用户ID")
            return

        try:
            user_id = int(user_id)
        except:
            messagebox.showerror("输入错误", "用户ID必须是数字")
            return

        user_info = self.cache.get(user_id)

        self.result_text.delete(1.0, tk.END)

        if user_info:
            self.result_text.insert(tk.END, f"👤 用户信息 (ID: {user_id})\n", "title")
            self.result_text.insert(tk.END, "="*40 + "\n\n")
            self.result_text.insert(tk.END, f"姓名: {user_info.name}\n")
            self.result_text.insert(tk.END, f"兴趣标签: {user_info.interests if user_info.interests else '未设置'}\n\n")

            # 好友统计
            friends = self.graph.get_friends(user_id)
            self.result_text.insert(tk.END, f"好友数量: {len(friends)}\n", "highlight")

            # 好友列表
            if friends:
                self.result_text.insert(tk.END, "\n好友列表:\n")
                for i, friend_id in enumerate(sorted(friends), 1):
                    friend_info = self.cache.get(friend_id)
                    friend_name = friend_info.name if friend_info else f"用户{friend_id}"
                    self.result_text.insert(tk.END, f"  {i}. {friend_name} (ID: {friend_id})\n")
        else:
            self.result_text.insert(tk.END, f"❌ 用户 {user_id} 不存在\n", "error")

        self.notebook.select(0)

    def show_multi_degree_dialog(self):
        """显示多度人脉查询对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("多度人脉查询")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="用户ID:").grid(row=0, column=0, padx=10, pady=10)
        user_entry = ttk.Entry(dialog, width=15)
        user_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="度数(1-5):").grid(row=1, column=0, padx=10, pady=10)
        degree_entry = ttk.Entry(dialog, width=15)
        degree_entry.grid(row=1, column=1, padx=10, pady=10)

        def query():
            try:
                user_id = int(user_entry.get())
                degree = int(degree_entry.get())
                if degree < 1 or degree > 5:
                    messagebox.showerror("错误", "度数必须在1-5之间")
                    return
                dialog.destroy()
                self.query_multi_degree(user_id, degree)
            except:
                messagebox.showerror("错误", "请输入有效的数字")

        ttk.Button(dialog, text="查询", command=query).grid(row=2, column=0, columnspan=2, pady=10)

    def query_multi_degree(self, user_id, degree):
        """查询多度人脉"""
        self.update_status(f"正在查询用户 {user_id} 的 {degree} 度人脉...")

        result, message = self.bfs.find_multi_degree(user_id, degree)

        self.result_text.delete(1.0, tk.END)

        if result:
            self.result_text.insert(tk.END, f"🔄 用户 {user_id} 的 {degree} 度人脉\n", "title")
            self.result_text.insert(tk.END, "="*40 + "\n\n")
            self.result_text.insert(tk.END, f"共找到 {len(result)} 个好友:\n\n", "highlight")

            # 按度数分组显示
            by_degree = {}
            for uid, info in result.items():
                d = info['degree']
                if d not in by_degree:
                    by_degree[d] = []
                by_degree[d].append((uid, info))

            for d in range(1, degree + 1):
                if d in by_degree:
                    self.result_text.insert(tk.END, f"\n📌 {d}度人脉 ({len(by_degree[d])}人):\n")
                    for uid, info in sorted(by_degree[d]):
                        user = self.cache.get(uid)
                        name = user.name if user else f"用户{uid}"
                        self.result_text.insert(tk.END, f"  • {name} (ID: {uid})\n")
                        self.result_text.insert(tk.END, f"    路径: {info['path']}\n\n")
        else:
            self.result_text.insert(tk.END, message + "\n")

        self.update_status(message)
        self.notebook.select(0)

    def show_recommend_dialog(self):
        """显示智能推荐对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("智能推荐")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="为用户ID:").grid(row=0, column=0, padx=10, pady=10)
        user_entry = ttk.Entry(dialog, width=15)
        user_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="推荐数量:").grid(row=1, column=0, padx=10, pady=10)
        k_entry = ttk.Entry(dialog, width=15)
        k_entry.insert(0, "5")
        k_entry.grid(row=1, column=1, padx=10, pady=10)

        def recommend():
            try:
                user_id = int(user_entry.get())
                k = int(k_entry.get())
                if k < 1 or k > 20:
                    messagebox.showerror("错误", "推荐数量必须在1-20之间")
                    return
                dialog.destroy()
                self.smart_recommend(user_id, k)
            except:
                messagebox.showerror("错误", "请输入有效的数字")

        ttk.Button(dialog, text="推荐", command=recommend).grid(row=2, column=0, columnspan=2, pady=10)

    def smart_recommend(self, user_id, top_k):
        """智能推荐"""
        self.update_status(f"正在为用户 {user_id} 生成推荐...")

        # 使用混合推荐
        recommendations, message = self.recommender.hybrid_recommend(user_id, top_k)

        self.result_text.delete(1.0, tk.END)

        if recommendations:
            self.result_text.insert(tk.END, f"🎯 为您推荐的 {len(recommendations)} 个新朋友\n", "title")
            self.result_text.insert(tk.END, "="*40 + "\n\n")

            for i, rec in enumerate(recommendations, 1):
                self.result_text.insert(tk.END, f"{i:2d}. {rec['name']} (ID: {rec['user_id']})\n", "highlight")
                self.result_text.insert(tk.END, f"    推荐指数: {rec['score']:.2f}\n")
                self.result_text.insert(tk.END, f"    推荐理由: {rec['reason']}\n\n")
        else:
            self.result_text.insert(tk.END, message + "\n")

        self.update_status(message)
        self.notebook.select(0)

    def refresh_data(self):
        """刷新数据显示"""
        self.update_stats_display()
        self.result_text.delete(1.0, tk.END)
        self.path_text.delete(1.0, tk.END)
        self.update_status("数据已刷新")
        messagebox.showinfo("刷新完成", "数据统计已更新")

    def show_statistics(self):
        """显示网络统计"""
        self.result_text.delete(1.0, tk.END)

        users = self.graph.get_all_users()
        if not users:
            self.result_text.insert(tk.END, "暂无数据\n")
            return

        user_count = len(users)
        rel_count = self.graph.get_edge_count()

        self.result_text.insert(tk.END, "📊 社交网络统计\n", "title")
        self.result_text.insert(tk.END, "="*40 + "\n\n")
        self.result_text.insert(tk.END, f"用户总数: {user_count}\n")
        self.result_text.insert(tk.END, f"关系总数: {rel_count}\n")

        if user_count > 0:
            avg_degree = (2 * rel_count) / user_count
            self.result_text.insert(tk.END, f"平均度数: {avg_degree:.2f}\n\n")

        # 度数分布
        self.result_text.insert(tk.END, "度数分布:\n", "highlight")
        degree_dist = {}
        for user_id in users:
            degree = len(self.graph.get_friends(user_id))
            degree_dist[degree] = degree_dist.get(degree, 0) + 1

        for degree in sorted(degree_dist.keys()):
            count = degree_dist[degree]
            percentage = (count / user_count) * 100
            self.result_text.insert(tk.END, f"  度数 {degree:2d}: {count:3d}人 ({percentage:5.1f}%)\n")

        # 孤岛节点
        isolated = [uid for uid in users if len(self.graph.get_friends(uid)) == 0]
        if isolated:
            self.result_text.insert(tk.END, f"\n孤岛节点 ({len(isolated)}人):\n", "highlight")
            for uid in isolated[:10]:
                user = self.cache.get(uid)
                name = user.name if user else f"用户{uid}"
                self.result_text.insert(tk.END, f"  {name} (ID: {uid})\n")

        self.notebook.select(0)

    def show_all_users(self):
        """显示所有用户"""
        self.result_text.delete(1.0, tk.END)

        users = self.cache.get_all()
        if not users:
            self.result_text.insert(tk.END, "暂无用户数据\n")
            return

        self.result_text.insert(tk.END, f"📋 所有用户 (共{len(users)}人)\n", "title")
        self.result_text.insert(tk.END, "="*40 + "\n\n")

        for user in sorted(users, key=lambda x: x.user_id):
            self.result_text.insert(tk.END, f"ID: {user.user_id:3d} | {user.name}\n")
            if user.interests:
                self.result_text.insert(tk.END, f"    兴趣: {user.interests}\n")

        self.notebook.select(0)

    def show_help(self):
        """显示帮助信息"""
        help_text = """
📖 使用说明

1. 系统启动时会自动加载 data 目录下的示例数据

2. 基础功能：
   - 一度人脉：输入用户ID，查询直接好友
   - 二度人脉：查询好友的好友（排除自身和直接好友）
   - 社交距离：计算两用户间的最短路径
   - 用户信息：查看用户详细资料

3. 扩展功能：
   - 多度人脉：在"扩展功能"菜单中查询1-5度人脉
   - 智能推荐：基于共同好友和共同兴趣的混合推荐

4. 数据格式：
   - 用户文件：ID,姓名,兴趣标签（可选）
   - 关系文件：每行一对用户ID，用逗号分隔

5. 注意事项：
   - 所有ID必须是数字
   - 关系文件中的用户必须在用户文件中存在
        """
        messagebox.showinfo("使用说明", help_text)

    def show_about(self):
        """显示关于信息"""
        about_text = """
社交网络图谱分析及智能推荐系统
版本：1.0

数据结构课程设计
计算机与人工智能学院
2024级计算机科学与技术专业

功能特点：
✓ 自主实现邻接表、哈希表
✓ BFS算法实现人脉查询
✓ 智能推荐系统
✓ 友好的图形界面

指导教师：彭玲 讲师
        """
        messagebox.showinfo("关于", about_text)