from typing import List

class FamilyAgent:
    """家庭成员智能体类，存储身份信息和立场"""
    
    def __init__(self, name: str, role: str, age: int, background: str, stance: str):
        self.name = name
        self.role = role
        self.age = age
        self.background = background
        self.stance = stance
        self.memory = []  # 存储其他成员的观点

    def add_memory(self, speaker: str, opinion: str) -> None:
        """记录其他成员的观点到记忆中"""
        self.memory.append(f"{speaker}说：{opinion}")
    
    def __repr__(self) -> str:
        return f"FamilyAgent(name={self.name}, role={self.role}, age={self.age})"