import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
from src.agents.family_agent import FamilyAgent
from src.core.debate_system import DebateSystem

class DebateGUI:
    """辩论系统的图形用户界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("家庭辩论系统 - 是否给7岁孙子报补习班")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("Header.TLabel", font=("SimHei", 12, "bold"))
        self.style.configure("Status.TLabel", font=("SimHei", 9), foreground="#666666")

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        self.title_label = ttk.Label(
            self.main_frame, 
            text="家庭辩论系统", 
            style="Header.TLabel"
        )
        self.title_label.pack(pady=(0, 10))

        # 辩论主题
        self.topic_frame = ttk.Frame(self.main_frame)
        self.topic_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.topic_frame, text="辩论主题：", style="Header.TLabel").pack(side=tk.LEFT)
        self.topic_var = tk.StringVar(value="是否给7岁孙子报补习班")
        ttk.Label(
            self.topic_frame, 
            textvariable=self.topic_var, 
            style="Header.TLabel",
            foreground="#2c3e50"
        ).pack(side=tk.LEFT, padx=5)

        # 辩论区域
        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 对话历史
        self.chat_history = scrolledtext.ScrolledText(
            self.chat_frame, 
            wrap=tk.WORD, 
            font=("SimHei", 10),
            bg="white",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)

        # 状态区域
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="准备就绪")
        ttk.Label(
            self.status_frame, 
            textvariable=self.status_var, 
            style="Status.TLabel",
            anchor=tk.W
        ).pack(fill=tk.X)

        # 控制区域
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=(0, 5))

        # 轮次设置
        ttk.Label(self.control_frame, text="最大轮次：").pack(side=tk.LEFT, padx=(0, 5))
        self.max_turns_var = tk.IntVar(value=15)
        turns_spinbox = ttk.Spinbox(
            self.control_frame,
            from_=5,
            to=50,
            increment=5,
            textvariable=self.max_turns_var,
            width=5
        )
        turns_spinbox.pack(side=tk.LEFT, padx=(0, 20))

        # 控制按钮
        self.start_btn = ttk.Button(
            self.control_frame, 
            text="开始辩论", 
            command=self.start_debate
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(
            self.control_frame, 
            text="停止辩论", 
            command=self.stop_debate,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(
            self.control_frame, 
            text="清空记录", 
            command=self.clear_history
        )
        self.clear_btn.pack(side=tk.RIGHT, padx=5)

        # 参与者信息区域
        self.participants_frame = ttk.LabelFrame(self.main_frame, text="参与成员")
        self.participants_frame.pack(fill=tk.X, pady=(10, 0))

        # 初始化辩论系统
        self.debate_system = None
        self.agents = self.init_agents()

    def init_agents(self) -> list[FamilyAgent]:
        """初始化家庭成员智能体并显示信息"""
        agents = [
            FamilyAgent(
                name="爷爷",
                role="退休教师",
                age=68,
                background="教了40年书，认为童年应该自由成长，反对过度补习",
                stance="反对报补习班，觉得7岁孩子应该多玩"
            ),
            FamilyAgent(
                name="奶奶",
                role="家庭主妇",
                age=65,
                background="周围邻居的孙子都在上补习班，担心自家孩子落后",
                stance="支持报补习班，怕孙子跟不上同龄人"
            ),
            FamilyAgent(
                name="爸爸",
                role="程序员",
                age=35,
                background="985大学毕业，相信科学教育，认为适当补习有用但不盲目",
                stance="中立，想先了解补习班的内容再决定"
            ),
            FamilyAgent(
                name="妈妈",
                role="公司经理",
                age=33,
                background="职场竞争激烈，认为早期教育能提升竞争力",
                stance="支持报补习班，尤其是英语和数学"
            ),
            FamilyAgent(
                name="姑姑",
                role="小学老师",
                age=28,
                background="现任小学班主任，见过太多因过度补习厌学的孩子",
                stance="反对报学术类补习班，可考虑兴趣班"
            )
        ]

        # 显示参与者信息
        for i, agent in enumerate(agents):
            frame = ttk.Frame(self.participants_frame)
            frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky=tk.W)
            
            ttk.Label(
                frame, 
                text=f"{agent.name} ({agent.role}, {agent.age}岁)",
                font=("SimHei", 10, "bold")
            ).pack(anchor=tk.W)
            
            ttk.Label(
                frame, 
                text=f"立场：{agent.stance}",
                font=("SimHei", 9)
            ).pack(anchor=tk.W)

        # 调整网格权重
        self.participants_frame.grid_columnconfigure(0, weight=1)
        self.participants_frame.grid_columnconfigure(1, weight=1)
        
        return agents

    def start_debate(self) -> None:
        """开始辩论"""
        max_turns = self.max_turns_var.get()
        self.debate_system = DebateSystem(
            topic=self.topic_var.get(),
            agents=self.agents,
            max_turns=max_turns,
            gui=self
        )
        
        # 在新线程中运行辩论，避免UI冻结
        threading.Thread(target=self.debate_system.run, daemon=True).start()

    def stop_debate(self) -> None:
        """停止辩论"""
        if self.debate_system:
            self.debate_system.stop()
            self.update_status("辩论已停止")
            self.update_controls(state="normal")

    def clear_history(self) -> None:
        """清空对话历史"""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.update_status("记录已清空，准备就绪")

    def add_message(self, name: str, content: str) -> None:
        """添加消息到对话历史"""
        self.chat_history.config(state=tk.NORMAL)
        
        # 根据发言者设置不同颜色
        colors = {
            "爷爷": "#2c3e50",
            "奶奶": "#e74c3c",
            "爸爸": "#3498db",
            "妈妈": "#9b59b6",
            "姑姑": "#1abc9c"
        }
        
        # 插入发言者
        self.chat_history.insert(tk.END, f"{name}：", name)
        # 插入内容
        self.chat_history.insert(tk.END, f"{content}\n\n")
        
        # 配置标签颜色
        self.chat_history.tag_config(name, foreground=colors.get(name, "#000000"), font=("SimHei", 10, "bold"))
        
        self.chat_history.config(state=tk.DISABLED)
        # 滚动到底部
        self.chat_history.see(tk.END)

    def update_status(self, message: str) -> None:
        """更新状态信息"""
        self.status_var.set(message)

    def update_controls(self, state: str) -> None:
        """更新控制按钮状态"""
        self.start_btn.config(state=state)
        self.stop_btn.config(state="normal" if state == "disabled" else "disabled")
        self.clear_btn.config(state=state)