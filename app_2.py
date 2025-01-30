import requests
from bs4 import BeautifulSoup
import time
import csv

# CSV 파일 저장 설정
csv_filename = "pokemon_data.csv"

# 포켓몬 도감 크롤링 함수
def get_pokemon_data(pokemon_id):
    url = f"https://pokemonkorea.co.kr/pokedex/view/{pokemon_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)

    # 페이지가 존재하지 않는 경우
    if response.status_code != 200:
        print(f"❌ [{pokemon_id}] 페이지 없음 (404)")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
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
        ability_element = soup.find("h4", text="특성")  # "특성" 제목을 찾음
        if ability_element:
            ability = ability_element.find_next("div").get_text(strip=True).split(" ")[0]  # 바로 다음 <div> 태그에서 첫 번째 단어 추출
        else:
            ability = "특성 정보 없음"
        print(pokemon_id, "진행")
        # 결과 딕셔너리 반환
        return {
            "번호": number,
            "이름": name,
            "타입": ", ".join(types),
            "설명": description,
            "키": height,
            "몸무게": weight,
            "분류": category,
            "성별": gender,
            "특성": ability,
            "이미지": image_url,
        }

    except Exception as e:
        print(f"⚠️ [{pokemon_id}] 데이터 추출 실패: {e}")
        return None

# 크롤링 실행 (1~1000번 포켓몬)
pokemon_list = []
for pokemon_id in range(1, 50):
    data = get_pokemon_data(pokemon_id)
    print("poketon_data", data)
    if data:
        pokemon_list.append(data)
    
    # 서버에 부담을 주지 않도록 대기 (0.5초)
    time.sleep(0.5)

# CSV 파일 저장
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=pokemon_list[0].keys())
    writer.writeheader()
    writer.writerows(pokemon_list)

print(f"\n✅ 크롤링 완료! '{csv_filename}' 파일에 저장됨.")