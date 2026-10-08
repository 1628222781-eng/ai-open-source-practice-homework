# -*- coding: utf-8 -*-
"""
旅游攻略智能体 - Streamlit 网页客户端
对应作业表 F 列：发布智能体并在本地生成一个 Streamlit 网页来调用它
对应作业表 H 列：实现视频中的代码（通过 DashScope Application API 调用百炼已发布应用）

运行方式：
    pip install -r requirements.txt
    streamlit run app.py

配置方式（二选一）：
    1. 在左侧边栏直接输入 API-KEY 和 APP ID
    2. 设置环境变量 DASHSCOPE_API_KEY / DASHSCOPE_APP_ID
未配置时页面会以"演示模式"运行，方便先看界面效果。
"""

import os

import requests
import streamlit as st

st.set_page_config(page_title="旅游攻略智能体", page_icon="🧳", layout="wide")

DASHSCOPE_APP_URL = "https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion"


# ---------------------------------------------------------------- #
# 页面状态初始化
# ---------------------------------------------------------------- #
def init_state():
    st.session_state.setdefault("messages", [])  # 历史消息 [{"role":..., "content":...}]
    st.session_state.setdefault("bailian_session_id", None)  # 百炼侧会话 ID，用于多轮记忆
    st.session_state.setdefault("api_key", os.getenv("DASHSCOPE_API_KEY", ""))
    st.session_state.setdefault("app_id", os.getenv("DASHSCOPE_APP_ID", ""))


# ---------------------------------------------------------------- #
# 核心逻辑：调用百炼已发布的智能体应用（Application Call API）
# ---------------------------------------------------------------- #
def call_bailian_agent(prompt: str, api_key: str, app_id: str, session_id: str | None):
    """调用百炼 Application API。

    文档：https://help.aliyun.com/zh/model-studio/application-call-api
    请求：POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion
    携带上一次返回的 session_id 即可实现多轮对话记忆（上下文工程）。
    """
    url = DASHSCOPE_APP_URL.format(app_id=app_id)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": {"prompt": prompt},
        "parameters": {},
        "debug": {},
    }
    if session_id:
        payload["input"]["session_id"] = session_id

    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    data = resp.json()

    status = data.get("status_code") or data.get("output", {}).get("finish_reason")
    if data.get("status_code") not in (200, None) and "output" not in data:
        raise RuntimeError(f"百炼返回异常：{data}")

    output = data.get("output", {})
    text = output.get("text", "")
    new_session_id = output.get("session_id", session_id)
    return text, new_session_id


# ---------------------------------------------------------------- #
# 演示模式：未配置 KEY 时给一段固定示例，保证页面可运行、可截图
# ---------------------------------------------------------------- #
DEMO_REPLY = """🌤️ **【演示模式】未配置 API-KEY / APP ID，以下为示例输出**

配置后即可实时调用你在百炼上发布的「旅游攻略规划师」智能体。

### 📅 示例：成都 3 日行程（节选）

| 时间段 | 安排 | 地点 | 交通 | 预算参考 |
| --- | --- | --- | --- | --- |
| D1 上午 | 抵达 + 宽窄巷子 | 宽窄巷子 | 地铁4号线 | 门票免费 |
| D1 下午 | 人民公园喝茶 | 鹤鸣茶社 | 步行 10 分钟 | ¥30/人 |
| D1 晚上 | 火锅初体验 | 小龙坎（春熙路店） | 地铁2号线 | ¥120/人 |
| D2 全天 | 熊猫基地 + 文殊院 | 大熊猫繁育研究基地 | 景区直通车 | ¥55 门票 |

💡 实用贴士：熊猫基地建议早上 7:30 到，熊猫最活跃；提前在"成都大熊猫繁育研究基地"公众号预约门票。
"""


def get_reply(prompt: str):
    """统一入口：有配置走百炼真实调用，没配置走演示模式。"""
    api_key = st.session_state.api_key.strip()
    app_id = st.session_state.app_id.strip()
    if not api_key or not app_id:
        return DEMO_REPLY, None

    try:
        return call_bailian_agent(
            prompt, api_key, app_id, st.session_state.bailian_session_id
        )
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response is not None else "?"
        detail = e.response.text[:300] if e.response is not None else str(e)
        return f"❌ 调用失败（HTTP {code}）：{detail}", None
    except Exception as e:  # noqa: BLE001
        return f"❌ 调用失败：{e}", None


# ---------------------------------------------------------------- #
# 页面 UI
# ---------------------------------------------------------------- #
def render_sidebar():
    with st.sidebar:
        st.header("⚙️ 百炼应用配置")
        st.markdown(
            "在 [百炼控制台](https://bailian.console.aliyun.com/) "
            "发布智能体后，于「应用调用」页获取 **APP ID**；"
            "API-KEY 在右上角头像 → API-KEY 管理中创建。"
        )
        st.session_state.api_key = st.text_input(
            "API Key（DASHSCOPE_API_KEY）",
            value=st.session_state.api_key,
            type="password",
        )
        st.session_state.app_id = st.text_input(
            "应用 APP ID", value=st.session_state.app_id
        )
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.session_state.bailian_session_id = None
            st.rerun()

        st.divider()
        status = (
            "🟢 已连接百炼（真实调用）"
            if st.session_state.api_key.strip() and st.session_state.app_id.strip()
            else "🟡 演示模式（未配置密钥）"
        )
        st.caption(status)


def render_chat():
    st.title("🧳 旅游攻略智能体")
    st.caption("基于阿里云百炼智能体编排 + 高德地图 MCP ｜ 输入目的地即可生成逐日攻略")

    # 渲染历史消息
    for msg in st.session_state.messages:
        avatar = "🙋" if msg["role"] == "user" else "🧳"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 快捷示例
    if not st.session_state.messages:
        st.markdown("#### 🎯 试试这样问")
        cols = st.columns(2)
        examples = [
            "我想去成都玩 3 天，2 大 1 小，预算 5000 元，喜欢美食和熊猫",
            "十一打算去西安 4 天，两个人，喜欢历史和碳水，帮我做攻略",
            "月底去三亚，海边度假为主，帮我看看天气和行程",
            "杭州一日游，西湖周边，暴走路线，预算 300",
        ]
        for i, ex in enumerate(examples):
            if cols[i % 2].button(ex, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": ex})
                with st.chat_message("user", avatar="🙋"):
                    st.markdown(ex)
                with st.chat_message("assistant", avatar="🧳"):
                    with st.spinner("正在查询天气、规划路线…"):
                        reply, sid = get_reply(ex)
                    st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.bailian_session_id = sid
                st.rerun()

    # 用户输入
    if prompt := st.chat_input("例如：我想去成都玩 3 天，预算 5000，喜欢美食…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🧳"):
            with st.spinner("正在查询天气、搜索景点、规划路线…"):
                reply, sid = get_reply(prompt)
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.bailian_session_id = sid


def main():
    init_state()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()
