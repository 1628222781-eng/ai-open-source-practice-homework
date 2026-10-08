# AI 开源实践课程 · 本次作业提交包

> 主题：旅游攻略智能体（阿里云百炼 Flowagent）
>
> 👉 **第一次看这个包，先读《04-从零到提交-详细操作步骤.md》**，里面是从注册百炼到提交仓库的逐步操作手册（含本机环境适配命令与截图清单）。

## 提交清单（对应作业表各列）

| 作业项 | 完成方式 | 对应文件 |
| --- | --- | --- |
| **E** 在阿里云百炼上创建智能体（先看 11.md，即 Flowagent） | 按 11.md 使用百炼「智能体编排」模式，创建「旅游攻略规划师」，配置高德地图 MCP 工具 | 《01-百炼智能体搭建指南.md》（含可直接粘贴的系统提示词） |
| **F** 发布智能体并在本地生成一个 Streamlit 网页来调用它 | 百炼发布后拿 APP ID + API-KEY，本地 `streamlit run app.py` 调用 Application API | 《02-streamlit-app/app.py》《02-streamlit-app/README.md》 |
| **G** 通过 ai-agent-book 说明该智能体设计符合什么思想 | 用「Agent = LLM + 上下文 + 工具」公式 + ReAct + MCP + 上下文工程 + 规划模式逐条论证 | 《03-设计思想说明-ai-agent-book.md》 |
| **H** 实现视频中的代码 | 视频演示的即"本地代码调用百炼已发布应用"：DashScope Application Call API + 多轮 session_id | 与 F 共用 app.py，代码要点见《02-streamlit-app/README.md》第 5 节 |

## 需要你自己动手完成的部分（平台操作无法代劳）

1. 登录 <https://bailian.console.aliyun.com/> 创建智能体（照《01》一步步做，约 15 分钟）
2. 发布应用，拿到 **APP ID** 和 **API-KEY**
3. 本地运行：
   ```bash
   cd 02-streamlit-app
   pip install -r requirements.txt
   streamlit run app.py   # 在左侧边栏填入 KEY 和 APP ID
   ```
4. 测试成功后截图（智能体对话截图 + Streamlit 网页截图）
5. 把作业包提交到课程 Git 仓库，得到提交链接填入 **I 列**

## 建议的仓库目录结构

```
ai-open-source-practice-course/
└── homework/
    └── travel-agent/
        ├── README.md                 ← 本文件
        ├── 01-百炼智能体搭建指南.md
        ├── 02-streamlit-app/
        │   ├── app.py
        │   ├── requirements.txt
        │   └── README.md
        ├── 03-设计思想说明-ai-agent-book.md
        └── screenshots/              ← 你的百炼截图、Streamlit 运行截图
```
