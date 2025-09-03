from flask import Flask, jsonify, request, render_template
from findpeople import find_target
from water_logic import calculate_water
from saveinfo import load_people_json, check_json
from config import register_new_card, id_list
from rfid import read_tag, write_tag
from modify_json import drank_json, check_PW, modify_disease
import json, threading, time, serial
import atexit
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
app = Flask(__name__)

# ------------------------------
# 전역 변수 (최근 카드 태그된 사용자 ID)
# ------------------------------
current_tag_id = None 

# ------------------------------
# UART 수신 루프 (백그라운드 스레드)
# ------------------------------
def uart_listener():
    global current_tag_id
    uart = serial.Serial('/dev/serial0', baudrate=115200, timeout=3)
    print("[UART] Listening...")
    while True:
        try:
            data = uart.read(8)
            if data:
                print(f"[UART] Received raw: {data}, current_tag_id={current_tag_id}")
                if current_tag_id:
                    print(f"[UART] Calling drank_json for tag_id={current_tag_id}")
                    drank_json(current_tag_id)
                else:
                    print("[UART] Ignored button press (no card tagged)")
            time.sleep(0.1)
        except Exception as e:
            print("[UART] Error:", e)
            time.sleep(1)
# ------------------------------
# Flask 라우트
# ------------------------------
@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/write_rfid', methods=['POST'])
def write_rfid():
    data = request.get_json()
    admission_id = data.get('id', '')
    
    if not admission_id:
        return jsonify({'error': '입원번호 데이터가 없습니다.'}), 400

    try:
        write_tag(admission_id)
        return jsonify({'message': f'{admission_id}가 카드에 기록되었습니다.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/read_route')
def read_route():
    global current_tag_id

    try:
        x, tag_id = read_tag()
        if not tag_id:
            print("[READ_ROUTE] No tag_id read")
            return jsonify({'error': '카드에서 데이터를 읽을 수 없습니다.'}), 404

        if not check_json(tag_id):
            print(f"[READ_ROUTE] Unregistered tag_id={tag_id}")
            return jsonify({
                'unregistered': True,
                'message': '등록되지 않은 카드입니다. 정보 추가하시겠습니까?'
            })

        current_tag_id = tag_id
        print(f"[READ_ROUTE] Card tagged -> current_tag_id={current_tag_id}")
        return jsonify({'tag_id': tag_id})
    except Exception as e:
        print("[READ_ROUTE] Error:", e)
        return jsonify({'error': str(e)}), 500
    
#User
@app.route('/write_route', methods=['POST'])
def write_route():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '데이터가 비어 있습니다.'}), 400
        
        admission_id = data.get('id')
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        weight = data.get('weight')
        cold = data.get('cold')
        password = data.get('password')

        if not admission_id:
            return jsonify({'error': '입원번호(id)가 필요합니다.'}), 400
        if not name:
            return jsonify({'error': '이름(name)이 필요합니다.'}), 400
        if gender is None:
            return jsonify({'error': '성별(gender)이 필요합니다.'}), 400
        if age is None:
            return jsonify({'error': '나이(age)가 필요합니다.'}), 400
        if weight is None:
            return jsonify({'error': '체중(weight)이 필요합니다.'}), 400
        if cold is None:
            return jsonify({'error': '감기 여부(cold)가 필요합니다.'}), 400
        if password is None:
            return jsonify({'error': '비밀번호(password)가 필요합니다.'}), 400

        # disease만 기본값 허용
        disease = data.get('disease', 'x')

        try:
            write_tag(admission_id)  # 카드에 데이터 기록
            
        except Exception as e:
            return jsonify({'error': f'카드 기록 실패: {str(e)}'}), 500

        try:
            with open("people_data.json", "r", encoding="utf-8") as f:
                people = json.load(f)
        except FileNotFoundError:
            people = []

        new_person = {
            "id": str(admission_id),
            "name": name,
            "gender": int(gender),
            "age": int(age),
            "weight": int(weight),
            "disease": disease,
            "drank": 0,
            "cold": int(cold),
            "password": int(password)
        }

        people.append(new_person)

        with open("people_data.json", "w", encoding="utf-8") as f:
            json.dump(people, f, ensure_ascii=False, indent=2)

        print(f"[WRITE_ROUTE] User saved: {new_person}")

        return jsonify({'message': f'카드와 DB에 사용자 {admission_id} 등록 완료'}), 200

    except Exception as e:
        return jsonify({'error': f'내부 오류: {str(e)}'}), 500

@app.route('/status', methods=['GET'])
def status():
    tag_id = request.args.get("tag_id")
    if not tag_id:
        return jsonify({"ok": False, "error": "tag_id missing"}), 400

    try:
        people = load_people_json()
        person = next((p for p in people if str(getattr(p, "id", None) if not isinstance(p, dict) else p.get("id")) == str(tag_id)), None)

        if not person:
            print(f"[STATUS] No person found for tag_id={tag_id}")
            return jsonify({"ok": False, "error": f"user not found for tag_id={tag_id}"}), 404

        drank_value = person.get("drank", 0) if isinstance(person, dict) else getattr(person, "drank", 0)
        print(f"[STATUS] tag_id={tag_id}, drank={drank_value}")

        return jsonify({"ok": True, "tag_id": tag_id, "today_drank_ml": drank_value}), 200
    except Exception as e:
        print("[STATUS] Error:", e)
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/calc_route', methods=['POST'])
def calc_route():
    try:
        # 1) 요청 파라미터 파싱
        data = request.get_json(silent=True) or {}
        tag_id = data.get('tag_id')
        if not tag_id:
            return jsonify({'ok': False, 'error': 'tag_id missing'}), 400

        # 2) 대상 조회
        people = load_people_json()
        person = find_target(people, tag_id)  # 이 함수도 People/Dict 둘 다 지원한다고 가정

        if person is None:
            return jsonify({
                'ok': False,
                'error': 'person not found',
                'tag_id': tag_id
            }), 404

        # 3) dict / People 객체 둘 다 대응
        if isinstance(person, dict):
            name = person.get('name')
            gender = person.get('gender')
            weight = person.get('weight')
            disease = person.get('disease')
            cold = person.get('cold')
            drank = person.get('drank')
        else:  # People 객체
            name = getattr(person, 'name', None)
            gender = getattr(person, 'gender', None)
            weight = getattr(person, 'weight', None)
            disease = getattr(person, 'disease', None)
            cold = getattr(person, 'cold', None)
            drank = getattr(person, 'drank', None)

        # 4) 권장 수분량 계산
        recommended = calculate_water(weight, gender, disease, cold)

        # 5) 응답
        return jsonify({
            'ok': True,
            'tag_id': tag_id,
            'person': {
                'name': name,
                'gender': gender,
                'weight': weight,
                'disease': disease,
                'cold': cold,
            },
            'recommended_water': recommended,
            'today_drank_ml': drank
        }), 200

    except Exception as e:
        return jsonify({
            'ok': False,
            'error': 'internal server error',
            'detail': str(e)
        }), 500

@app.route('/modify')
def modify_page():
    return render_template('modify.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

# ------------------------------
# GPIO clean-up
# ------------------------------
def cleanup_gpio():
    GPIO.cleanup()
atexit.register(cleanup_gpio)

# ------------------------------
# 메인 실행
# ------------------------------
if __name__=='__main__':
    # UART 수신 스레드 시작
    uart_thread = threading.Thread(target=uart_listener, daemon=True)
    uart_thread.start()

    # Flask 서버 실행
    app.run(host='0.0.0.0', port=5001, debug=True)
