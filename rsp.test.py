import cv2
import mediapipe as mp
import time

# Mediapipe 손 인식 모듈 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 승패 판단 함수
def determine_winner(player1_move, player2_move):
    if player1_move == player2_move:
        return "Draw"
    if (player1_move == "Rock" and player2_move == "Scissors") or \
       (player1_move == "Scissors" and player2_move == "Paper") or \
       (player1_move == "Paper" and player2_move == "Rock"):
        return "Player 1 Wins"
    return "Player 2 Wins"

# 모션 인식 함수 (기존의 classify_hand_landmarks 함수 사용)
def classify_hand_landmarks(landmarks):
    thumb_open = landmarks[4].x < landmarks[3].x  # 엄지 (왼쪽 손일 경우)
    index_open = landmarks[8].y < landmarks[6].y  # 검지
    middle_open = landmarks[12].y < landmarks[10].y  # 중지
    ring_open = landmarks[16].y < landmarks[14].y  # 약지
    pinky_open = landmarks[20].y < landmarks[18].y  # 새끼

    if not index_open and not middle_open and not ring_open and not pinky_open:
        return "Rock"  # 바위
    elif index_open and middle_open and not ring_open and not pinky_open:
        return "Scissors"  # 가위
    elif index_open and middle_open and ring_open and pinky_open:
        return "Paper"  # 보
    return "Unknown"

# 카메라 동작 및 카운트다운 표시 함수
def start_game():
    cap = cv2.VideoCapture(0)
    countdown = 3

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # 카운트다운 표시
        if countdown > 0:
            cv2.putText(frame, str(countdown), (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 10)
            time.sleep(1)  # 1초 대기
            countdown -= 1
        else:
            # 동작 인식 후 판단
            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0].landmark
                player1_move = classify_hand_landmarks(landmarks)
                player2_move = "Rock"  # 임시로 player2의 동작을 "바위"로 설정 (추후 네트워크 연결 가능)

                winner = determine_winner(player1_move, player2_move)
                cv2.putText(frame, winner, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

        # 결과 영상 보여주기
        cv2.imshow('Game', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC를 누르면 종료
            break

    cap.release()
    cv2.destroyAllWindows()

# 수락 시 바로 게임 시작
start_game()
