import cv2
import mediapipe as mp

# Mediapipe 손 인식 모듈 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 손가락 상태를 분석하여 가위, 바위, 보를 결정하는 함수
def classify_hand_landmarks(landmarks):
    thumb_open = landmarks[4].x < landmarks[3].x  # 엄지 (왼쪽 손일 경우)
    index_open = landmarks[8].y < landmarks[6].y  # 검지
    middle_open = landmarks[12].y < landmarks[10].y  # 중지
    ring_open = landmarks[16].y < landmarks[14].y  # 약지
    pinky_open = landmarks[20].y < landmarks[18].y  # 새끼

    if not index_open and not middle_open and not ring_open and not pinky_open:
        return "Rock"
    elif index_open and middle_open and not ring_open and not pinky_open:
        return "Sissors"
    elif index_open and middle_open and ring_open and pinky_open:
        return "Paper"
    return "판별 불가"

# 웹캠 입력 시작
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 입력 이미지를 좌우 반전
    frame = cv2.flip(frame, 1)

    # 이미지 색상을 RGB로 변환
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Mediapipe를 이용해 손을 감지
    results = hands.process(image)

    # 감지된 손이 있으면 랜드마크를 그린다
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 손가락 랜드마크 리스트 가져오기
            landmarks = hand_landmarks.landmark

            # 가위, 바위, 보 판별
            result = classify_hand_landmarks(landmarks)
            cv2.putText(image, result, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3, cv2.LINE_AA)

    # 결과 영상 보여주기
    cv2.imshow('Rock Paper Scissors', image)

    # ESC를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 웹캠 및 모든 창 종료
cap.release()
cv2.destroyAllWindows()
hands.close()
