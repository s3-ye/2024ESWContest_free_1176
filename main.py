# main.py

import json
import os
from saveinfo import savenewinfo,load_ids_from_json, load_people_json
from water_logic import calculate_water
from config import People, register_new_card, id_list
from findpeople import find_target
from rfid import read_tag, write_tag
from modify_json import drank_json, check_PW, modify_disease, modify_cold, modify_weight


def main():
    #JSON에 저장된 기존 ID리스트로 초기화/home/yeseo/python_env/
    id_list=load_ids_from_json()

    while True:
            print('select an option:')
            print('1. 새로운 ID/정보 등록')
            print('2. 권장량 분석')
            print('3.modify disease')
            print('0. exit')

            action=input('Enter the number of your choice:').strip()

            if action=='1':
              
                ID=input("새로운 카드 ID를 입력하세요: ")
                write_tag(ID)
                new_card_id= read_tag()
                register_new_card(new_card_id)
                savenewinfo(new_card_id)


            elif action=='2':
                people = load_people_json() #JSON에 적혀있는 정보 불러오기
                target = find_target(people)
                print(target)

                if target:
                    

                    water = calculate_water(target.weight, target.gender, target.disease,target.cold)
                    print(f"{target.name}님의:")
                    
                    print(f"섭취량/권장량: {target.drank}/{water}ml")
                    print('if you want to drink ...->push button')
                    drank_json(target.id, people)
                    print(target.drank)
            

            elif action=='3':
                people = load_people_json() #JSON에 적혀있는 정보 불러오기
                target = find_target(people)
            
                if target:
                    PW = int(input('enter your PW: '))
                  
                    check = check_PW(PW,target.password)
                    print(check)
                    if check == 1:
                        change = input('if you want change cold no.1, weight no.2, disease no.3: ').strip()
                        if change == '1':
                            modify_cold(target.id, people)
                        elif change == '2':
                            modify_weight(target.id, people)
                        elif change == '3':
                            modify_disease(target.id, people)
                    else:
                        print("password mismatch")


            elif action=='0':
                break

            else:
                print("잘못 입력함. \n'1', '2', or '0'중에서 입력해주세요.")


if __name__ == "__main__":
    main()