#findpeople.py
#저장된 people리스트에서 입력한 ID로 대상 사람 검색
from config import People, id_list
from rfid import read_tag

# def find_target(people, tag_id):
#     try:
        
#         print(tag_id)
#         for person in people:
#             if str(person.id) == str(tag_id):
#                 return person
#     except ValueError: 
#         print("숫자를 입력해주세요.")
#         return None

def find_target(people, tag_id):
    
    want = str(tag_id).strip() if tag_id is not None else None
    if want is None:
        return None

    for person in people:
        # dict 타입일 때
        if isinstance(person, dict):
            pid = str(person.get("tag_id") or person.get("id") or person.get("rfid") or "").strip()
        else:
            # 객체 타입일 때
            pid = str(
                getattr(person, "tag_id", None) or
                getattr(person, "id", None) or
                getattr(person, "rfid", None) or ""
            ).strip()

        if pid == want:
            return person

    return None