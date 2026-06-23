import cv2
import threading

from datetime import datetime, timedelta

from utils.json_manager import (
    load_intrusion_logs,
    save_intrusion_logs
)

#전역변수
camera = None #카메라 객체 저장
camera_lock = threading.Lock()

ESP32_STREAM_URL = "http://192.168.137.252:81/stream"

#이전 프레임 저장
prev_gray = None
#마지막 침입 시간
last_intrusion_time = None


# 고정 위험구역 좌표
# 위험구역 좌표-화면에서 위험구역의 사각형을 정의한다. 좌상단이 (250, 100) 우하단이 (550, 330)인 사각형을 만든다.
DANGER_X1 = 250
DANGER_Y1 = 100
DANGER_X2 = 550
DANGER_Y2 = 350

#카메라 연결 함수
def init_camera():

    global camera

    if camera is None:
        print("camera connecting...")
        camera = cv2.VideoCapture(ESP32_STREAM_URL) #영상 스트림에 연결하는 함수
        print("camera connected")

#카메라 재연결 함수
def reconnect_camera():

    global camera

    print("camera reconnecting...")

    try:
        if camera is not None: #연결상태는 동일
            camera.release()
    except:
        pass

    camera = cv2.VideoCapture(ESP32_STREAM_URL)

    print("camera reconnected")

#침입기록을 json에 저장
def save_intrusion_log():

    logs = load_intrusion_logs()

    logs.append({

        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "message": "Danger Zone Intrusion"

    })

    save_intrusion_logs(logs)

    print("intrusion log saved")

    
def get_frame():

    global camera
    global prev_gray
    global last_intrusion_time

    if camera is None:
        return None

    try:

        if not camera.isOpened():
            reconnect_camera()
            return None

        with camera_lock:
            success, frame = camera.read()

        if not success:
            reconnect_camera()
            return None

        gray = cv2.cvtColor(  # 컬러정보 제거-움직임 감지는 색상이 필요없다..
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur( #노이즈를 제거한다. 부드럽게
            gray,
            (21, 21),
            0
        )

        is_intrusion = False

        if prev_gray is None:

            prev_gray = gray

        else:

            diff = cv2.absdiff(
                prev_gray,
                gray
            )

            _, thresh = cv2.threshold(
                diff,
                25,
                255,     #흑백       차이가 25픽셀 이상 나면 흰색/그렇지 않으면 검정
                cv2.THRESH_BINARY
            )
            #움직인 영역의 경계 찾기
            #움직임 영역 -> 테두리 생성
            contours, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:

                if cv2.contourArea(contour) < 500:
                    continue

                x, y, w, h = cv2.boundingRect(
                    contour  # 움직인 영역을 감싸는 사각형이다. x축, y축, width, height인 것 같다.
                )
                #움직임의 중심 좌표를 구한다. 근데 어떻게?
                center_x = x + w // 2
                center_y = y + h // 2

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (center_x, center_y),
                    5,
                    (255, 0, 0),
                    -1
                )
                #중심점이 위험구역 안에 있으면 침입으로 간주한다.
                if (
                    DANGER_X1 <= center_x <= DANGER_X2
                    and
                    DANGER_Y1 <= center_y <= DANGER_Y2
                ):
                    is_intrusion = True

            prev_gray = gray

        danger_color = (0, 0, 255)
        
        #침입 시 노란색으로 변한다.
        if is_intrusion:
            danger_color = (0, 255, 255)#노란색
        
        #위험구역 표시
        cv2.rectangle(
            frame,
            (DANGER_X1, DANGER_Y1),
            (DANGER_X2, DANGER_Y2),
            danger_color,
            3
        )

        cv2.putText(
            frame,
            "DANGER ZONE",
            (DANGER_X1, DANGER_Y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            danger_color,
            2
        )

        if is_intrusion:
            #침입 메시지
            cv2.putText(
                frame,
                "INTRUSION DETECTED",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

            now = datetime.now()
            
            #로그 저장
            if (
                last_intrusion_time is None
                or
                now - last_intrusion_time >
                timedelta(seconds=5)         #5초마다 한 번 씩 로그를 저장
            ):

                save_intrusion_log()

                last_intrusion_time = now
        #최종반환 - generate_frames()에서 JPEG로 변환되어 브라우저로 전송된다.
        return frame

    except Exception as e:

        print("camera exception:", e)

        reconnect_camera()

        return None