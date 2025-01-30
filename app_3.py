import streamlit as st
import pandas as pd

# CSV 파일 로드
csv_filename = "pokemon_data.csv"

# 데이터프레임 로드
df = pd.read_csv(csv_filename)

# Streamlit UI
st.title("포켓몬 도감 데이터")

# 데이터 전체 테이블 출력
st.dataframe(df)

# 포켓몬 필터링 (선택 박스)
pokemon_name = st.selectbox("포켓몬 선택", df["이름"].unique())

# 선택한 포켓몬 정보 출력
selected_pokemon = df[df["이름"] == pokemon_name].iloc[0]

st.subheader(f"📌 {selected_pokemon['이름']} 정보")
st.image(selected_pokemon["이미지"], caption=selected_pokemon["이름"])

st.write(f"**번호:** {selected_pokemon['번호']}")
st.write(f"**타입:** {selected_pokemon['타입']}")
st.write(f"**설명:** {selected_pokemon['설명']}")
st.write(f"**키:** {selected_pokemon['키']}")
st.write(f"**몸무게:** {selected_pokemon['몸무게']}")
st.write(f"**분류:** {selected_pokemon['분류']}")
st.write(f"**성별:** {selected_pokemon['성별']}")
st.write(f"**특성:** {selected_pokemon['특성']}")

# 검색 기능 추가
search_query = st.text_input("검색어 입력 (예: 물)")
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]
    st.subheader("🔎 검색 결과")
    st.dataframe(filtered_df)