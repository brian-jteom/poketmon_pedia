import requests
from bs4 import BeautifulSoup

# 포켓몬 도감 URL
url = "https://pokemonkorea.co.kr/pokedex/view/12"

# 웹 페이지 요청
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")
# 포켓몬 이미지 URL 추출
image_tag = soup.find("img", src=lambda x: x and x.startswith("https://data1.pokemonkorea.co.kr/"))
image_url = image_tag["src"] if image_tag else "이미지 없음"

# 포켓몬 번호 및 이름 추출
number = soup.find("p", class_="font-lato").text.strip()
name = soup.find("h3").text.strip().replace(number, "").strip()

# 타입 추출
types = [t.text.strip() for t in soup.select(".img-type p")]

# 설명(첫 번째 설명만 추출)
description = soup.find("p", class_="para descript").text.strip()

# 키, 몸무게, 분류 추출
stats = soup.find_all("div", class_="col-4")
height = stats[1].find("p").text.strip()
weight = stats[2].find("p").text.strip()
category = stats[0].find("p").text.strip()

# 성별 확인
gender_icons = soup.select(".icon-man, .icon-woman")
gender = "♂♀" if len(gender_icons) == 2 else "♂" if "icon-man" in gender_icons[0]["class"] else "♀"

# 특성 추출
# 🔹 특성(Ability) 가져오기 (정확한 위치에서 추출)
ability_element = soup.find("h4", text="특성")  # "특성" 제목을 찾음
if ability_element:
    ability = ability_element.find_next("div").get_text(strip=True).split(" ")[0]  # 바로 다음 <div> 태그에서 첫 번째 단어 추출
else:
    ability = "특성 정보 없음"


print(f"특성: {ability}")

# 출력
print(f"이미지: {image_url}")
print(f"번호: {number}")
print(f"이름: {name}")
print(f"타입: {', '.join(types)}")
print(f"설명: {description}")
print(f"키: {height}, 몸무게: {weight}, 분류: {category}")
print(f"성별: {gender}")
print(f"특성: {ability}")