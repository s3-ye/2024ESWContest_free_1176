#saveinfo
#새로운 카드 등록 -> 기존JSON파일에서 사람 정보 불러옴 -> 중복체크 
#-> 신규 사람 정보 입력 및 저장
import json
from config import People
    
# Process in Route app.py /Write_Route
# def savenewinfo(new_id):
#     # 기존 데이터 불러오기
#     try:
#         with open("people_data.json", "r", encoding="utf-8") as f:
#             data = json.load(f)
#             people_list = [
#                 People(
#                     item["id"], item["name"], item["gender"], item["age"],
#                     item["weight"], item["disease"], item["drank"],
#                     item["cold"], item["password"]
#                 )
#                 for item in data
#             ]
#     except FileNotFoundError:
#         people_list = []

#     for p in people_list:

#         if str(p.id) == str(new_id):
#             print(f"ID {new_id}는 이미 등록되어 있습니다. 추가하지 않습니다.")
#             return  # 중복될 경우 함수 종료
        
#     # 중복이 아닌 경우 새로운 사람 정보 입력
#     print(f"새 카드 등록됨: ID = {new_id}. 사람 정보를 입력하세요.")
#     name = input("name: ")
#     gender = int(input("gender (0:여자, 1:남자): "))
#     age = int(input("age(year): "))
#     weight = int(input("weight(kg): "))
#     disease = input("disease (없으면 x): ")
#     cold = int(input("cold (1:예, 0:아니오): "))
#     password = int(input("password: "))
#     drank = int(input('0'))

#     new_person = People(new_id, name, gender, age, weight, disease, drank, cold, password)
#     people_list.append(new_person)

#     with open("people_data.json", "w", encoding="utf-8") as f:
#         json.dump([p.to_dict() for p in people_list], f, ensure_ascii=False, indent=4)

#     print(f"ID {new_id}의 사람 정보가 저장되었습니다.")

#json에서 정보 읽어와서 그 내용을 People클래스 객체로 변환 후 반환
def load_people_json():
    try:
        with open("people_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [
                People(
                    item["id"], item["name"], item["gender"], item["age"],
                    item["weight"], item["disease"], item["drank"],
                    item["cold"], item["password"]
                )
                for item in data
            ]
    except FileNotFoundError:
        return []
    
    #json파일에서 id만 따로 반환  
def load_ids_from_json(filename="people_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            id_list = [str(item["id"]) for item in data]
            return id_list
    except FileNotFoundError:
        return []

def check_json(tag_id, filename="people_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 데이터 내 id 값과 비교 (양쪽 공백 제거 권장)
        for item in data:
            if item["id"].strip() == str(tag_id).strip():
                return True
        return False
    except FileNotFoundError:
        # 파일 없으면 등록된 카드 없음으로 간주
        return False