# 家庭辩论系统

一个基于多智能体的家庭辩论模拟系统，模拟家庭成员就"是否给7岁孙子报补习班"这一话题进行辩论。

## 功能特点

- 模拟不同家庭成员的立场和观点
- 基于DeepSeek API实现智能对话生成
- 可视化界面展示辩论过程
- 可配置辩论轮次和查看辩论历史

## 如何使用

1. 克隆仓库
```bash
git clone <https://github.com/5ANADIUM509/family_debate.git>
cd family_debate
```


2. 创建并激活虚拟环境
```bash
# 创建虚拟环境
python -m venv .venv
# 激活虚拟环境
.venv\Scripts\activate
macOS/Linux 系统：
```

3. 安装依赖包
```bash
pip install -r requirements.txt
```
4. 配置 API 密钥
```bash
# 复制环境变量示例文件
cp .env.example .env
```
# 编辑.env文件，填入你的DeepSeek API密钥
