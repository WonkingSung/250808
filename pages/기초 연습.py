import streamlit as st

st.title("원킹 스트림릿 연습장 🥰 ")
st.write("스트림릿을 배우기 위해 이것저것 시도해보고 있습니다.")
st.write("오늘은 2일차 입니다 !!!!!!!!")
st.success("오늘은 스트림릿으로 다양한 데이터 프로젝트를 진행합니다.")


st.divider()
st.title("2행 2열 예제 ")

내용 = " "

col1, col2 = st.columns(2)
if col1.button("사랑") : 내용 = "사랑합니다."
if col2.button("겸손") : 내용 = "존경합니다."

col3, col4 = st.columns(2)
if col3.button("실존") : 내용 = "제가 할께요."
if col4.button("협력") : 내용 = "함께합시다."

st.markdown(f"# {내용}")

열1, 열2, 열3= st.columns(3)

with 열1: 
    st.image("https://ypzxxdrj8709.edge.naverncp.com/data2/content/image/2023/03/06/.cache/512/20230306580182.jpg", width = 500)
    st.caption("삼일고 사진")
with 열2 :
    st.image("https://i.namu.wiki/i/YsjYCg5NGpwtXAbVLxSZR-WSGzXi2HF-qPmvifFLgQGU3iaOAIVunNtzk6bp_squ3ssIm9LlUoKkPCBNyzHi1g.webp", width = 100)
    st.caption("삼일고 마크")
with 열3 :
    st.image("son.jpeg")

