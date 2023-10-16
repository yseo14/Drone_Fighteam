import cv2
from djitellopy import Tello
from droneblocksutils.aruco_utils import detect_markers_in_image
import time

# 아르코 마커 관련 설정
marker_size = 100  # 아르코 마커의 크기 (mm)
marker_id_1 = 0  # 첫 번째 아르코 마커의 ID
marker_id_2 = 1  # 두 번째 아르코 마커의 ID
marker_id_3 = 2  # 세 번째 아르코 마커의 ID
distance_to_marker = 30  # 아르코 마커 앞으로 전진할 거리 (센티미터)

# Tello 드론 관련 설정
tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()


# Tello 드론 앞으로 전진 함수
def move_forward(distance_cm):
    tello.move_forward(distance_cm)  # 거리는 센티미터 단위로 지정


# Tello 드론 왼쪽으로 회전 함수
def rotate_left(degrees):
    tello.rotate_counter_clockwise(degrees)  # 시계 반대 방향으로 회전


try:
    # 초기 상태: 첫 번째 아르코 마커 찾기
    state = "find_marker_1"

    while True:
        # Tello의 비디오 프레임을 가져옵니다.
        frame = tello.get_frame_read().frame

        # 아르코 마커 검출
        image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True,
                                                        target_id=None)

        if state == "find_marker_1":
            if marker_details:
                detected_marker_id = marker_details[0][1]
                if detected_marker_id == 0:
                    # 첫 번째 아르코 마커를 발견했을 때
                    # marker_center_x, marker_center_y = marker_details[0][0], marker_details[0][1]

                    move_forward(distance_to_marker)
                    rotate_left(90)
                    state = "find_marker_2"

        elif state == "find_marker_2":
            if marker_details:
                detected_marker_id = marker_details[0][1]
                if detected_marker_id == 1:
                    # 첫 번째 아르코 마커를 발견했을 때
                    # marker_center_x, marker_center_y = marker_details[0][0], marker_details[0][1]

                    move_forward(distance_to_marker)
                    rotate_left(90)
                    state = "find_marker_3"

        elif state == "find_marker_3":
            if marker_details:
                detected_marker_id = marker_details[0][1]
                if detected_marker_id == 2:
                    # 첫 번째 아르코 마커를 발견했을 때
                    # marker_center_x, marker_center_y = marker_details[0][0], marker_details[0][1]
                    state = "find_marker_4"
                    tello.rotate_counter_clockwise(360)
        elif state == "find_marker_4":
            break

        # 비디오 화면에 아르코 마커 표시
        cv2.imshow("Tello Video", image)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

tello.land()

# Tello 드론 연결 해제
tello.streamoff()
tello.end()
cv2.destroyAllWindows()
