import cv2
import threading

from datetime import datetime, timedelta

from utils.json_manager import (
    load_intrusion_logs,
    save_intrusion_logs
)


camera = None
camera_lock = threading.Lock()

ESP32_STREAM_URL = "http://192.168.137.163:81/stream"

prev_gray = None
last_intrusion_time = None


# 고정 위험구역 좌표
DANGER_X1 = 250
DANGER_Y1 = 100
DANGER_X2 = 550
DANGER_Y2 = 350


def init_camera():

    global camera

    if camera is None:
        print("camera connecting...")
        camera = cv2.VideoCapture(ESP32_STREAM_URL)
        print("camera connected")


def reconnect_camera():

    global camera

    print("camera reconnecting...")

    try:
        if camera is not None:
            camera.release()
    except:
        pass

    camera = cv2.VideoCapture(ESP32_STREAM_URL)

    print("camera reconnected")


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

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
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
                255,     #흑백
                cv2.THRESH_BINARY
            )

            contours, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:

                if cv2.contourArea(contour) < 500:
                    continue

                x, y, w, h = cv2.boundingRect(
                    contour
                )

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

                if (
                    DANGER_X1 <= center_x <= DANGER_X2
                    and
                    DANGER_Y1 <= center_y <= DANGER_Y2
                ):
                    is_intrusion = True

            prev_gray = gray

        danger_color = (0, 0, 255)

        if is_intrusion:
            danger_color = (0, 255, 255)#노란색

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

            if (
                last_intrusion_time is None
                or
                now - last_intrusion_time >
                timedelta(seconds=5)
            ):

                save_intrusion_log()

                last_intrusion_time = now

        return frame

    except Exception as e:

        print("camera exception:", e)

        reconnect_camera()

        return None