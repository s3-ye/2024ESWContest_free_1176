import json
import serial
from saveinfo import load_ids_from_json, load_people_json
def drank_json(tag_id):
    try:
        with open('people_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        updated = False
        for person in data:
            print(f"[drank_json] comparing person_id={person['id']} <-> tag_id={tag_id}")
            if str(person['id']).strip() == str(tag_id).strip():
                before = person.get("drank", 0)
                person['drank'] = before + 200
                after = person['drank']
                print(f"[drank_json] MATCH! tag_id={tag_id}, before={before}, after={after}")
                updated = True
                break

        if updated:
            with open('people_data.json', "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("[drank_json] File updated successfully.")
        else:
            print(f"[drank_json] No matching tag_id={tag_id} in file")

    except Exception as e:
        print("[drank_json] Error:", e)


# def drank_json(tag_id):
#     try:
#         with open('people_data.json', 'r', encoding='utf-8') as f:
#             data = json.load(f)

#         for person in data:
#             pid = person.get("id") if isinstance(person, dict) else getattr(person, "id", None)
#             if str(pid) == str(tag_id):
#                 if isinstance(person, dict):
#                     before = person.get("drank", 0)
#                     person["drank"] = before + 200
#                     after = person["drank"]
#                 else:
#                     before = getattr(person, "drank", 0)
#                     person.drank = before + 200
#                     after = person.drank

#                 print(f"[drank_json] tag_id={pid}, before={before}, after={after}")
#                 break

#         with open('people_data.json', "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print("[drank_json] Error:", e)
     
       
def check_PW(PW, password):
    print(f'pw: "{PW}"')
    print(f'password: "{password}"')
    if (PW!=password):
        return 0
    
    else:
        return 1
    

def modify_disease(id, people):

        with open('people_data.json', 'r') as f:
            people_data = json.load(f)
        
        for person in people_data:
            if str(person['id'])==str(id):
                new_disease=input('new disease info: ')
                person['disease'] =  new_disease
                break
            else:
                print('cant find password')
                return False
            
        with open('people_data.json', "w", encoding="utf-8") as f:
            json.dump(people_data, f, ensure_ascii=False,indent=2)

        print('success')
        return True


def modify_cold(id, people):

        with open('people_data.json', 'r') as f:
            people_data = json.load(f)
        
        for person in people_data:
            if str(person['id'])==str(id):
                new_cold=int(input("cold (1:예, 0:아니오): "))
                person['cold'] =  new_cold
                break
            else:
                print('cant find password')
                return False
            
        with open('people_data.json', "w", encoding="utf-8") as f:
            json.dump(people_data, f, ensure_ascii=False,indent=2)

        print('success')
        return True


def modify_weight(id, people):

        with open('people_data.json', 'r') as f:
            people_data = json.load(f)
        
        for person in people_data:
            if str(person['id'])==str(id):
                new_weight = int(input("weight(kg): "))
                person['weight'] =  new_weight
                break
            else:
                print('cant find password')
                return False
            
        with open('people_data.json', "w", encoding="utf-8") as f:
            json.dump(people_data, f, ensure_ascii=False,indent=2)

        print('success')
        return True