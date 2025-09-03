# water_logic.py
#사람 무게,성별,질병,다이어트여부,감기 등에 따른 권장 수분 섭취량 계산

def calculate_water(weight, gender, disease, cold):
    # gender: 0 (여자), 1 (남자)

    # 기본 권장량
    if gender == 0:
        water = weight * 30
    else:
        water = weight * 35

    # 질병 조건
    if disease == "diabetes":
        water += 500

    elif disease == "신장결석":
        water = 3000

    elif disease=="x":
            pass

    if cold==1:
        water += 500


    return water


