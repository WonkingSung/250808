# streamlit_multiple_plotly_graphs.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 CSV 파일 업로드 및 다양한 Plotly 그래프 시각화")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())

    # 열 선택
    all_columns = df.columns.tolist()
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    x_axis = st.selectbox("X축 열 선택", options=all_columns)
    y_axis = st.selectbox("Y축 열 선택 (숫자형만 가능)", options=numeric_columns)

    st.subheader("📉 다양한 Plotly 그래프")

    # 산점도
    st.markdown("### 🌟 산점도 (Scatter)")
    scatter_fig = px.scatter(df, x=x_axis, y=y_axis, title="산점도")
    st.plotly_chart(scatter_fig, use_container_width=True)

    # 꺾은선 그래프
    st.markdown("### 🌟 꺾은선 그래프 (Line)")
    line_fig = px.line(df, x=x_axis, y=y_axis, title="꺾은선 그래프")
    st.plotly_chart(line_fig, use_container_width=True)

    # 막대 그래프
    st.markdown("### 🌟 막대 그래프 (Bar)")
    bar_fig = px.bar(df, x=x_axis, y=y_axis, title="막대 그래프")
    st.plotly_chart(bar_fig, use_container_width=True)

    # 히트맵 (가능할 경우에만)
    if x_axis in numeric_columns and y_axis in numeric_columns:
        st.markdown("### 🌟 히트맵 (Heatmap)")
        heatmap_fig = px.density_heatmap(df, x=x_axis, y=y_axis, title="히트맵")
        st.plotly_chart(heatmap_fig, use_container_width=True)
    else:
        st.markdown("### 🚫 히트맵")
        st.info("히트맵은 X축과 Y축이 모두 숫자형일 때만 표시됩니다.")
else:
    st.info("CSV 파일을 업로드하면 다양한 시각화를 자동으로 생성합니다.")
