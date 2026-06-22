#필요한 모듈 삽입
from flask import (Blueprint, 
                   Response, 
                   render_template,
                   session,
                   redirect)

from ai.camera_manager import get_frame

import cv2
import time

#Blueprint 생성
dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    url_prefix='/dashboard'
)

#라우터 생성
@dashboard_bp.route('/')
def dashboard():
    #로그인 확인
    if session.get('signinedMemberId') is None:
        #로그인페이지로 이동
        return redirect('/member/signin_form')
    #HTML 반환
    return render_template('dashboard/dashboard.html') #dashboard 디렉토리의 dashboard.html
#video_feed()실행
@dashboard_bp.route('/video_feed') #view만 주면 된다.
def video_feed():
    #Response()실행-Flask에서 HTTP응답을 생성하는 객체 
    return Response(
        #generate_frame()->응답 본문을 생성하는 핵심
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
        #HTTP응답의 content-type 헤더를 설정
        #multipart/x-mixed-replace: 서버가 단일 HTTP 연결을 통해 여러 개의 메시지를 클라이언트(현재로 보면 브라우저)
        #각 메시지는 이전것을 대체한다.
        #multipart로 구성된 데이터를 보내는데 새로운 부분(x-mixed)이 오면 기존것을 교체하라
        
        #boundaruy=frame => 매개변수
        #각 데이터(frame)을 구분하는 경계선의 이름을 frame으로 하겠다.
        #긴 종이에 여러장의 사진을 이어 붙이며 사진과 사진 사이에 절취선을 만들고 이를 frame이라고 하는것과 같다.
    )

#실시간 영상 만드는 함수, def generate_frames():
def generate_frames():

    while True:
        #카메라 화면 가져오기
        frame = get_frame() #실행시 camera manager로 넘어간다.
        #카메라 오류 처리
        if frame is None:
            time.sleep(0.1)
            continue
        #JPEG 변환
                      #이미지를 메모리내에서 특정 형식으로 인코딩(압축)하는 함수
        ret, buffer = cv2.imencode('.jpg', frame)#.jpg = JPEG 형식으로 압축 frame = 카메라가 갓 가져온 원본 이미지
        #ret = 인코딩의 성공여부를 나타낸다.
        #buffer = JPEG로 압축된 실제 이미지 데이터가 담긴 바이트 배열
        
        #변환 실패처리-변환에 실패하면 0.1초후 다시 시작하라
        if not ret:
            time.sleep(0.1)
            continue
        #byte 변환 - 브라우저는 바이트 데이터만 받을 수 있다.
        #함수를 실행해 나온 데이터를 frame_bytes라는 변수에 담는다.
        frame_bytes = buffer.tobytes()
        #yield의 핵심: 일시정지 그리고 재개
        yield (
            b'--frame\r\n' #경계선 표시
            b'Content-Type: image/jpeg\r\n\r\n' #데이터 설명
            + frame_bytes + #실제 데이터
            b'\r\n' #끝
        )
        #맨 앞의 b는 byte

        time.sleep(0.03)
        #0.03초 마다 한 장씩 전송한다. 즉 초당 약 33장을 보낸다.