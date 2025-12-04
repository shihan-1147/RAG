import streamlit as st
import pandas as pd

# 假设您在 backend.py 中封装了 LLM 提取逻辑
# from backend import extract_disaster_info

st.title("社交媒体灾情提取系统 📊")

# --- 界面布局 (左右两栏) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("模拟灾情文本输入")
    # 文本域，允许输入多行文本
    text_input = st.text_area("粘贴社交媒体文本（每行一条）:",
                              height=300,
                              value="北京朝阳区积水严重，车辆无法通行。\n海淀发生轻微塌方，暂无人员伤亡。")

with col2:
    st.subheader("结构化提取结果")

    if st.button("开始提取"):
        # 1. 处理输入文本
        lines = text_input.split('\n')

        # 2. 调用您的 LLM 提取后端 (模拟)
        # results = [extract_disaster_info(line) for line in lines]

        # 模拟返回结果
        results = [
            {"地点": "北京朝阳区", "灾害类型": "积水", "情况": "车辆无法通行"},
            {"地点": "海淀", "灾害类型": "塌方", "情况": "暂无人员伤亡"}
        ]

        # 3. 使用 Pandas DataFrame 展示结构化结果
        df = pd.DataFrame(results)
        st.dataframe(df)