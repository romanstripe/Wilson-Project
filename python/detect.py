import serial
import numpy as np
import time
from collections import deque, Counter
from utils import parse_csi_line, csi_to_amp

SERIAL_PORT = "COM4"
BAUD_RATE = 115200

CSI_LEN = 128
WINDOW_SIZE = 10 #버퍼멈춤 해결하려고 조정

# 현장에서 값 조정
RSSI_IN = -36       # 이보다 크면 구역 안 후보
RSSI_OUT = -44     # 이보다 작으면 구역 밖 후보
MOTION_DETECT_TH = 2.0
MOTION_ALERT_TH  = 3.5


ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.2)

rssi_buffer = deque(maxlen=WINDOW_SIZE)
amp_buffer = deque(maxlen=WINDOW_SIZE)
state_history = deque(maxlen=7)

current_zone = "OUT"

print("=== Zone Detection Demo Started ===")

while True:
    line = ser.readline().decode(errors="ignore").strip()

    rssi, csi = parse_csi_line(line, CSI_LEN)

    if csi is None:
        continue

    amp = csi_to_amp(csi, CSI_LEN)

    rssi_buffer.append(rssi)
    amp_buffer.append(amp)

    if len(amp_buffer) < WINDOW_SIZE:
        continue

    rssi_med = np.median(rssi_buffer)

    w = np.array(amp_buffer)
    mean_over_time = np.mean(w, axis=1)
    motion_score = np.std(mean_over_time)

    # hysteresis: 경계 흔들림 방지
    if rssi_med > RSSI_IN:
        current_zone = "IN"
    elif rssi_med < RSSI_OUT:
        current_zone = "OUT"
        amp_buffer.clear()  # ← 핵심: 나가면 버퍼 초기화
        state_history.clear()  # ← 핵심: 이전 판정 초기화


    if current_zone == "OUT":
        raw_state = "SAFE"
    else:
        if motion_score > MOTION_ALERT_TH:
            raw_state = "ALERT"
        elif motion_score > MOTION_DETECT_TH:
            raw_state = "DETECTED"
        else:
            raw_state = "SAFE"  # 구역 안인데 motion 낮으면 SAFE

    state_history.append(raw_state)

    # 최근 7번 중 가장 많이 나온 상태로 최종 결정
    final_state = Counter(state_history).most_common(1)[0][0]

    if final_state == "OUT_OF_ZONE":
        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"SAFE | Outside Detection Zone | "
            f"RSSI={rssi_med:.1f} | motion={motion_score:.2f}"
        )

    elif final_state == "IN_ZONE":
        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"DETECTED | Person/Object in Zone | "
            f"RSSI={rssi_med:.1f} | motion={motion_score:.2f}"
        )

    elif final_state == "ALERT":
        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"ALERT | Movement Detected | "
            f"RSSI={rssi_med:.1f} | motion={motion_score:.2f}"
        )

