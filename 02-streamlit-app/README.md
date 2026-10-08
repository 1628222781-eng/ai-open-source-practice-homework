# 本地运行 Streamlit 网页调用百炼智能体

> 对应作业表 **F 列**（发布智能体并本地 Streamlit 调用）和 **H 列**（实现视频中的代码）

## 1. 前提

- 已按《01-百炼智能体搭建指南.md》在百炼创建并 **发布** 了「旅游攻略规划师」智能体
- 已拿到两个值：
  - **API-KEY**（百炼控制台右上角 → API-KEY 管理）
  - **APP ID**（应用详情 → 应用调用页面）

## 2. 安装依赖

```bash
cd 02-streamlit-app
pip install -r requirements.txt
```

## 3. 配置密钥（二选一）

方式一：启动后在页面左侧边栏直接粘贴 API Key 和 APP ID（推荐，最简单）

方式二：设置环境变量后再启动

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY="sk-xxxxxxxx"
$env:DASHSCOPE_APP_ID="你的APPID"
streamlit run app.py

# macOS / Linux
export DASHSCOPE_API_KEY=sk-xxxxxxxx
export DASHSCOPE_APP_ID=你的APPID
streamlit run app.py
```

## 4. 启动

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`：

- 🟢 已配置密钥：输入旅游需求 → 真实调用百炼智能体 → 返回带天气、地图数据的逐日攻略
- 🟡 未配置密钥：演示模式，可先看界面效果再配置

## 5. 代码要点（对应视频教学内容）

1. **Application Call API**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`，
   请求头带 `Authorization: Bearer <API-KEY>`，请求体 `{"input": {"prompt": "..."}}`
2. **多轮会话**：百炼返回 `output.session_id`，下次请求把它放进
   `input.session_id` 传回，服务端即可记住上下文——这就是
   ai-agent-book 第 2 章讲的"上下文"在平台侧的实现
3. **错误处理**：对 HTTP 401（KEY 错误/欠费）、超时等做了兜底提示
4. **Streamlit 状态管理**：`st.session_state` 保存历史消息与 session_id，
   `st.chat_message / st.chat_input` 构建聊天界面

## 6. 常见报错

| 现象 | 原因 |
| --- | --- |
| HTTP 401 | API-KEY 无效或账户欠费 |
| HTTP 404 | APP ID 填错，或应用未发布 |
| 一直转圈 | 网络问题，或智能体在高德 MCP 工具上卡住，可在百炼控制台「调用明细」排查 |
