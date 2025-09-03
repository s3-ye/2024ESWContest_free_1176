import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
reader=SimpleMFRC522()

def read_tag():
    print('카드 인식:')
    id, text = reader.read() 
    return id, text

def write_tag(usage_id):   
    reader.write(usage_id)  # 카드에 입원번호 직접 기록
    print(f'입원번호 {usage_id}가 카드에 기록되었습니다.')
