from typing import List, Dict, Optional
import time
from src.agents.family_agent import FamilyAgent
from src.utils.api_client import call_deepseek_api

class DebateSystem:
    """辩论系统，管理多智能体对话流程"""
    
    def __init__(self, topic: str, agents: List[FamilyAgent], max_turns: int = 10, gui=None):
        self.topic = topic
        self.agents = agents
        self.history: List[Dict[str, str]] = []  # 存储辩论历史
        self.max_turns = max_turns
        self.current_turn = 0
        self.gui = gui  # GUI引用
        self.running = False  # 控制辩论是否运行

    def get_agent_by_name(self, name: str) -> Optional[FamilyAgent]:
        """通过名字查找智能体"""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def build_prompt(self, agent: FamilyAgent) -> str:
        """为智能体构建对话提示词"""
        # 角色信息
        role_info = (
            f"你现在扮演{agent.name}，{agent.age}岁，身份是{agent.role}。\n"
            f"你的背景：{agent.background}。\n"
            f"你对“{self.topic}”的初始立场是：{agent.stance}。\n"
        )

        # 记忆信息
        memory_info = "你记得之前的讨论：\n" if agent.memory else "之前没有相关讨论记忆。\n"
        for mem in agent.memory:
            memory_info += f"- {mem}\n"

        # 历史对话
        history_info = "当前对话历史：\n"
        for h in self.history:
            history_info += f"{h['name']}：{h['content']}\n"

        # 辩论指导
        debate_guide = (
            "请你基于自己的身份、背景和立场，对当前讨论做出回应。\n"
            "要求：\n"
            "1. 紧扣主题，不要偏离“是否给7岁孙子报补习班”；\n"
            "2. 可以支持/反驳他人观点（如果记得之前的发言）；\n"
            "3. 语言符合你的年龄和身份（比如爷爷可能更传统，妈妈可能更关注升学）；\n"
            "4. 回复简洁（1-3句话），不要冗长。\n"
            "你的回复："
        )

        return role_info + memory_info + history_info + debate_guide

    def run(self) -> None:
        """运行辩论流程"""
        self.running = True
        if self.gui:
            self.gui.update_status("辩论开始...")
            self.gui.update_controls(state="disabled")

        try:
            while self.current_turn < self.max_turns and self.running:
                for agent in self.agents:
                    if not self.running:
                        break
                        
                    self.current_turn += 1
                    if self.current_turn > self.max_turns:
                        break

                    # 更新状态
                    if self.gui:
                        self.gui.update_status(f"当前轮次：{self.current_turn}/{self.max_turns}，{agent.name}正在思考...")
                    
                    # 构建提示词并获取回复
                    prompt = self.build_prompt(agent)
                    reply = call_deepseek_api(prompt, agent.name)

                    # 记录对话历史
                    self.history.append({
                        "name": agent.name,
                        "content": reply
                    })

                    # 其他智能体记录该发言
                    for other_agent in self.agents:
                        if other_agent != agent:
                            other_agent.add_memory(agent.name, reply)

                    # 更新GUI
                    if self.gui:
                        self.gui.add_message(agent.name, reply)
                    
                    time.sleep(1)  # 避免API请求过于频繁

            # 辩论结束
            if self.gui:
                self.gui.update_status("辩论结束")
                self.gui.update_controls(state="normal")
                
        except Exception as e:
            if self.gui:
                from tkinter import messagebox
                messagebox.showerror("错误", f"辩论过程中发生错误：{str(e)}")
                self.gui.update_status(f"发生错误：{str(e)}")
                self.gui.update_controls(state="normal")
        finally:
            self.running = False

    def stop(self) -> None:
        """停止辩论"""
        self.running = False