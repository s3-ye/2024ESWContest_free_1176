# config.py
#people클래서 정의, id_list 관리

# 사람 정보를 담는 객체 설계, 저장된 ID목록 관리, 새카드ID등록
class People:
    def __init__(self, id, name, gender, age, weight, disease, drank, cold, password):
        self.id = id
        self.name = name
        self.gender = gender  # 0: 여자, 1: 남자
        self.age = age
        self.weight = weight
        self.disease = disease
        self.drank= drank #마신 물의 양
        self.cold=cold
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "weight": self.weight,
            "disease": self.disease,
            "drank": self.drank,
            "cold": self.cold,
            "password" : self.password
        }


# id리스트
id_list = []

def register_new_card(new_id):
    if new_id not in id_list:
        id_list.append(new_id)
        