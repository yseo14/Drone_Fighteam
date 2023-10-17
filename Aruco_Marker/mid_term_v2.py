import cv2
from djitellopy import Tello
from droneblocksutils.aruco_utils import detect_markers_in_image, detect_distance_from_image_center
import time

# 아르코 마커 관련 설정
marker_id_1 = 0  # 첫 번째 아르코 마커의 ID
marker_id_2 = 1  # 두 번째 아르코 마커의 ID
marker_id_3 = 2  # 세 번째 아르코 마커의 ID

# Tello 드론 관련 설정
tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()
#
# MIN_DISTANCE = 30
# MAX_SPEED = 40


# 드론 앞으로 전진 함수
def move_forward(distance_cm):
    tello.move_forward(distance_cm)  # 거리는 센티미터 단위로 지정


# 드론 왼쪽으로 회전 함수
def rotate_left(degrees):
    tello.rotate_counter_clockwise(degrees)  # 시계 반대 방향으로 회전


# def move_to_center():
#     while 1:
#         frame = tello.get_frame_read().frame
#         image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True,
#                                                         target_id=None)
#         (H, W) = frame.shape[:2]
#
#         if marker_details:
#             center_x, center_y = marker_details[0][0][0], marker_details[0][0][1]
#             image, x_distance, y_distance, distance = detect_distance_from_image_center(image, center_x, center_y)
#             print(x_distance, y_distance, distance)
#             if tello:
#                 l_r_speed = int((MAX_SPEED * x_distance) / (W // 2))
#                 # *-1 because the documentation says
#                 # that negative numbers go up but I am
#                 # seeing negative numbers go down
#                 u_d_speed = int((MAX_SPEED * y_distance / (H // 2)) * -1)
#
#                 # to keep the oscillations to a minimum, if the distance is 'close'
#                 # then override the speed settings to zero
#                 try:
#                     if abs(distance) <= MIN_DISTANCE:
#                         u_d_speed = 0
#                         l_r_speed = 0
#                         break
#
#                     else:
#                         # we are not close enough to the ArUco marker, so keep flying
#                         tello.send_rc_control(l_r_speed, 0, u_d_speed, 0)
#
#                 except Exception as exc:
#                     print(f"send_rc_control exception: {exc}")
#

try:
    # 초기 상태: 첫 번째 아르코 마커 찾기
    state = "find_marker_1"

    while True:
        # 비디오 프레임 가져오기

        frame = tello.get_frame_read().frame

        # 이미지의 가로 및 세로 크기 가져오기
        image_height, image_width, _ = frame.shape

        # 이미지의 중심 좌표 계산
        image_center_x = image_width // 2
        image_center_y = image_height // 2

        # 아르코 마커 검출
        image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True,
                                                        target_id=None)
        if state == "find_marker_1":
            if marker_details:
                detected_marker_id = marker_details[0][1]
                if detected_marker_id == 0:
                    # 첫 번째 아르코 마커를 발견했을 때
                    marker_center_x, marker_center_y = marker_details[0][0][0], marker_details[0][0][1]
                    print(marker_details)
                    move_forward(245)
                    # move_to_center()
                    rotate_left(90)
                    state = "find_marker_2"

        elif state == "find_marker_2":
            if marker_details:
                detected_marker_id = marker_details[0][1]
                if detected_marker_id == 1:
                    # 두번 째 아르코 마커를 발견했을 때
                    marker_center_x, marker_center_y = marker_details[0][0], marker_details[0][1]
                    print(marker_details)
                    # move_to_center()
                    move_forward(230)
                    rotate_left(130)
                    state = "find_marker_3"

        elif state == "find_marker_3":
            if marker_details:
                detected_marker_id = marker_details[0][1]
                if detected_marker_id == 2:
                    # 세번 째 아르코 마커를 발견했을 때
                    marker_center_x, marker_center_y = marker_details[0][0], marker_details[0][1]
                    print(marker_details)
                    state = "find_marker_4"
                    move_forward(350)
                    # move_to_center()
                    tello.rotate_counter_clockwise(360)
        elif state == "find_marker_4":
            tello.land()
            break
        else:
            # 감지 된 아르코 마커가 없어도 송출
            cv2.imshow("Tello Video", frame)

        # 비디오 화면에 아르코 마커 표시
        cv2.imshow("Tello Video", image)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

# Tello 드론 연결 해제
tello.streamoff()
tello.end()
cv2.destroyAllWindows()