import streamlit as st
import pandas as pd
import urllib.request
import json
from pandas import json_normalize
from urllib.parse import urlencode, quote_plus, unquote
import plotly.express as px
import re

# --- 24:00 처리 함수 ---
def fix_24hour_times(dt_series):
    def fix_time(s):
        if isinstance(s, str) and re.match(r"\d{4}-\d{2}-\d{2} 24:00", s):
            day = pd.to_datetime(s[:10])
            day = day + pd.Timedelta(days=1)
            return day.strftime('%Y-%m-%d') + " 00:00"
        return s
    return dt_series.apply(fix_time)

# --- API 요청 함수 ---
@st.cache_data(show_spinner=False)
def get_air_quality_df(station='광교동', rows=300):
    api = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
    key = unquote('8imLOEIhmGIxq8Ud7TglAuHG2zQ%2BA2wGRiPnVhbHb60UJDhwJlbMqzv4SOTE5B9D3Moc713ob6bioiJywC3S3Q%3D%3D')
    queryParams = '?' + urlencode({
        quote_plus('serviceKey'): key,
        quote_plus('returnType'): 'json',
        quote_plus('numOfRows'): str(rows),
        quote_plus('pageNo'): '1',
        quote_plus('stationName'): station,
        quote_plus('dataTerm'): '3MONTH',
        quote_plus('ver'): '1.0'
    })
    url = api + queryParams
    text = urllib.request.urlopen(url).read().decode('utf-8')
    json_return = json.loads(text)
    get_data = json_return.get('response')
    df = json_normalize(get_data['body']['items'])
    return df

# --- 위험도 색상 판별 함수 ---
def get_color(value, safe, danger):
    if pd.isna(value):
        return 'gray'
    if value <= safe:
        return 'green'
    elif value >= danger:
        return 'red'
    else:
        return 'orange'

# --- Streamlit UI 시작 ---
st.set_page_config("광교동 미세먼지 시각화", layout="wide", page_icon="🌫️")
st.title("🌫️ 광교동 미세먼지 실시간 시각화")
st.caption("공공데이터포털 환경부 OpenAPI 활용, 최근 3개월간 데이터 (출처: 에어코리아)")

# --- 데이터 불러오기 ---
with st.spinner('데이터 불러오는 중...'):
    df = get_air_quality_df('광교동', 300)

# --- 컬럼 라벨 정리 ---
col_map = {
    'dataTime': '측정시각',
    'pm10Value': '미세먼지(PM10) ㎍/㎥',
    'pm25Value': '초미세먼지(PM2.5) ㎍/㎥',
    'o3Value': '오존(O3) ppm',
    'no2Value': '이산화질소(NO2) ppm',
    'coValue': '일산화탄소(CO) ppm',
    'so2Value': '아황산가스(SO2) ppm',
    'khaiValue': '통합대기환경지수',
}
df = df[[*col_map.keys()]].copy()
df.rename(columns=col_map, inplace=True)

# --- 시간 및 수치형 처리 ---
df['측정시각'] = fix_24hour_times(df['측정시각'])
df['측정시각'] = pd.to_datetime(df['측정시각'], format='%Y-%m-%d %H:%M')

for c in col_map.values():
    if 'ppm' in c or '㎍/㎥' in c or '지수' in c:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# --- 최신 측정값 표시 ---
latest = df.iloc[0]
st.subheader(f"가장 최근 측정 시각: {latest['측정시각']:%Y-%m-%d %H:%M}")
st.metric("통합대기환경지수 (KHAI)", latest['통합대기환경지수'])

# --- 항목별 원형 그래프 정의 ---
st.subheader("🌀 항목별 오염도 원형 그래프")

pollutants = [
    {
        'name': '미세먼지(PM10)',
        'value': latest['미세먼지(PM10) ㎍/㎥'],
        'unit': '㎍/㎥',
        'safe': 30,
        'danger': 80
    },
    {
        'name': '초미세먼지(PM2.5)',
        'value': latest['초미세먼지(PM2.5) ㎍/㎥'],
        'unit': '㎍/㎥',
        'safe': 15,
        'danger': 35
    },
    {
        'name': '오존(O3)',
        'value': latest['오존(O3) ppm'],
        'unit': 'ppm',
        'safe': 0.03,
        'danger': 0.09
    },
    {
        'name': '이산화질소(NO2)',
        'value': latest['이산화질소(NO2) ppm'],
        'unit': 'ppm',
        'safe': 0.03,
        'danger': 0.2
    },
    {
        'name': '일산화탄소(CO)',
        'value': latest['일산화탄소(CO) ppm'],
        'unit': 'ppm',
        'safe': 2.0,
        'danger': 9.0
    },
    {
        'name': '아황산가스(SO2)',
        'value': latest['아황산가스(SO2) ppm'],
        'unit': 'ppm',
        'safe': 0.02,
        'danger': 0.15
    }
]

# --- 항목별 원형 그래프 그리기 ---
for item in pollutants:
    val = item['value']
    label = item['name']
    unit = item['unit']
    color = get_color(val, item['safe'], item['danger'])

    pie_df = pd.DataFrame({
        '항목': [label, '기타'],
        '값': [val, max(item['danger'] * 1.2, val * 1.5) - val]
    })

    fig = px.pie(
        pie_df,
        names='항목',
        values='값',
        color='항목',
        color_discrete_map={
            label: color,
            '기타': 'lightgray'
        },
        hole=0.5
    )
    fig.update_layout(
        title=f"{label} : {val} {unit}",
        height=300,
        showlegend=False
    )
    fig.update_traces(textinfo='none')
    st.plotly_chart(fig, use_container_width=True)

# --- 데이터 테이블 및 다운로드 ---
with st.expander("📋 전체 데이터 테이블 보기"):
    st.dataframe(df.style.highlight_max(axis=0), height=400)

csv = df.to_csv(index=False, encoding='utf-8-sig')
st.download_button("📥 CSV 다운로드", csv, file_name="광교동_미세먼지.csv", mime="text/csv")
