#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  ♥  MIJU 에게 보내는 크리스마스 트리  ♥
  ─────────────────────────────────────
  글자로 그리는 3D 크리스마스 트리 (Python + numpy)

  실행 방법
    1) numpy 설치 (한 번만):   python3 -m pip install --user numpy
    2) 실행:                  python3 tree.py
    3) 끝내기:                Ctrl+C

  꼭 읽어 주세요
    - 맥 기본 '터미널' 앱은 트루컬러(24비트 색)를 제대로 못 보여 줘서 색이 이상하게 나와요.
      iTerm2 (https://iterm2.com) 또는 VS Code 의 내장 터미널에서 실행해 주세요.
    - 터미널 창을 가로 96칸 x 세로 54줄 이상으로 키워 주세요. (작으면 안내 문구가 나와요)
      글꼴 크기를 조금 줄이면(Cmd + -) 쉽게 맞출 수 있어요.

  한 바퀴(약 2분 20초) 동안 벌어지는 일
     0초  눈 쌓인 땅 → 회오리와 트리 → 번쩍 → 장식 볼 → 전구 → 금색 별 → 하트
    10초  선물 상자 → 지팡이 사탕 → 눈사람 → 눈 → MIJU 메시지와 하트 별자리
    15초  루돌프가 산타 썰매를 끌고 하늘을 지나가요 (Ho Ho Ho!)
    20초  불꽃놀이 (하트 불꽃 포함)
    24초  라벤더 선물 상자가 열리고 큰 하트가 떠올라 두근두근… 펑! 하트 비
    28초  "I love you, MIJU" 와 무지개 전구
    31초  서울의 겨울밤: 한강대교 아치 조명, 불꽃 폭포, 다리 위 불꽃놀이, 무지개분수, 유람선, 남산타워
    40초  카메라가 용산을 지나 남산타워로 날아가며 줌인
    47초  남산(능선·숲·성곽·산책로·케이블카·팔각정·봉수대·사랑의 자물쇠)과 타워에 분홍·라벤더 조명
          → 타워 몸통으로 줌인해 큰 네온 글씨 M I J U 가 한 글자씩 → 하트 불꽃
    55초  한강대교 드론 쇼: 다리에서 떠오른 드론이 트리 → 하트 → MIJU ♥ + 불꽃 폭포와 마무리 불꽃
    68초  MIJU 글자가 별빛이 되어 트리 꼭대기 별로 → 번쩍! → 라벤더 선물 강조
    74초  라벤더 편지 봉투가 열리고, 미주에게 쓴 한글 편지가 한 장씩 써져요 → 처음부터 다시

  브라우저로 보기 (HTML)
    python3 tree.py --html   → 같은 폴더에 tree.html 이 생겨요. 더블클릭하면 Chrome·Safari 에서 재생돼요.
    열면 '컴퓨터(16:9)' / '휴대폰(9:16)' 중에서 고를 수 있어요. 인터넷 없이 재생돼요.
    (내용을 바꿨다면 이 명령을 다시 실행해 주세요.)
    터미널에서 휴대폰 모양 미리 보기:  TREE_LAYOUT=phone python3 tree.py   (창을 72x64 이상으로)

  쉽게 바꾸기
    - 맨 위 [색 팔레트] 에서 색을 바꿀 수 있어요.  (R, G, B) 0~255
    - 그 아래 [개수·문구 설정] 에서 하트 개수, 눈 양, 메시지, 불꽃 등을 바꿀 수 있어요.
      예) 「하트 더 많이」 → NUM_HEARTS, SNOW_HEART_CHANCE, NUM_BURST_HEARTS 를 키우면 돼요.
    - 서울 장면·편지의 색, 문구, 시간표는 [서울 장면 · 편지] 칸에 모여 있어요.
"""

import math
import os
import signal
import sys
import time

import numpy as np

# ════════════════════════════════════════════════════════════════════
#  [색 팔레트]  (R, G, B) 0~255
# ════════════════════════════════════════════════════════════════════
# ── 밤하늘 ──
STAR_WHITE    = (235, 240, 255)   # 하얀 별
STAR_BLUE     = (150, 185, 255)   # 푸른 별
STAR_WARM     = (255, 222, 170)   # 노르스름한 별
STAR_PINK     = (255, 165, 210)   # 분홍 별 (MIJU 하늘에만 있는 별)
MILKY_VIOLET  = (125, 95, 200)    # 은하수 보랏빛 안개
MILKY_BLUE    = (70, 115, 210)    # 은하수 푸른 안개
AURORA_MINT   = (80, 255, 190)    # 오로라 민트빛 (아래쪽 밝은 테두리)
AURORA_VIOLET = (165, 105, 255)   # 오로라 보랏빛 (중간)
AURORA_ROSE   = (255, 120, 205)   # 오로라 장밋빛 (위쪽 끝자락)
SHOOTING_STAR = (255, 240, 250)   # 별똥별
CONSTELLATION = (255, 150, 215)   # 하트 별자리의 별
CONST_LINE    = (150, 110, 200)   # 하트 별자리 잇는 선
MOON_RIM      = (120, 110, 255)   # 물체 가장자리에 비치는 보랏빛 달빛

# ── 행성 ──
PLANET_SILVER = (210, 214, 230)   # 왼쪽 위 은빛 행성
RING_SILVER   = (185, 180, 215)   # 은빛 행성의 고리
PLANET_BLUE   = (60, 130, 255)    # 오른쪽 위 푸른 행성
PLANET_BLUE_2 = (140, 220, 255)   # 푸른 행성 줄무늬
PLANET_PURPLE = (170, 90, 235)    # 왼쪽 중간 작은 보랏빛 행성

# ── 땅 ──
SNOW          = (240, 246, 255)   # 쌓인 눈
SNOW_BLUE     = (175, 200, 255)   # 눈 그늘의 푸른 기운
ICE_RIM       = (95, 140, 215)    # 둥근 땅 옆면 (얼음)
SNOW_GLINT    = (230, 245, 255)   # 눈 위 반짝임

# ── 트리 ──
PINE_DARK     = (8, 85, 45)       # 진한 초록
PINE          = (22, 150, 72)     # 보통 초록
PINE_LIGHT    = (95, 220, 110)    # 밝은 초록
PINE_MINT     = (110, 235, 185)   # 위쪽 잎끝의 민트빛
TRUNK_BROWN   = (125, 72, 35)     # 갈색 기둥
TRUNK_DARK    = (75, 40, 20)      # 기둥 나무결

# ── 회오리 · 번쩍 ──
SWIRL_WHITE   = (255, 255, 255)   # 흰 빛 회오리
SWIRL_ICE     = (205, 225, 255)   # 회오리 두 번째 줄기 (살짝 얼음빛)
FLASH_WHITE   = (255, 250, 240)   # 꼭대기 번쩍

# ── 장식 볼 ──
RED           = (230, 25, 50)     # 빨강 볼
GOLD          = (255, 190, 50)    # 금색 볼
SILVER        = (200, 212, 235)   # 은색 볼

# ── 전구 ──
BULB_WARM     = (255, 225, 160)   # 따뜻한 흰색 전구
BULB_RED      = (255, 55, 55)     # 빨강 전구
BULB_GOLD     = (255, 185, 35)    # 금색 전구
BULB_GREEN    = (60, 255, 110)    # 초록 전구

# ── 꼭대기 별 ──
STAR_GOLD     = (255, 200, 60)    # 금색 별
STAR_RAY      = (255, 230, 140)   # 별빛 빛살

# ── 하트 ──
PINK          = (255, 95, 175)    # 분홍 하트
HOT_PINK      = (255, 50, 140)    # 진한 분홍 (두근 할 때)
LOVE_HEART    = (255, 70, 150)    # 선물에서 떠오르는 큰 하트
LOVE_GLOW     = (255, 150, 205)   # 큰 하트 둘레 빛

# ── 선물 상자 ──
WHITE         = (240, 240, 250)   # 흰 상자
GIFT_RED      = (215, 30, 55)     # 빨강 상자
GIFT_GREEN    = (30, 160, 85)     # 초록 상자
GIFT_GOLD     = (240, 180, 45)    # 금색 상자
BLUE          = (55, 105, 240)    # 파랑 상자
LAVENDER      = (175, 135, 255)   # 라벤더 상자 (MIJU 에게 주는 특별 상자, 나중에 열려요)

# ── 지팡이 사탕 ──
CANE_RED      = (235, 30, 50)     # 사탕 빨간 줄
CANE_WHITE    = (250, 250, 255)   # 사탕 흰 줄

# ── 눈사람 ──
SNOWMAN       = (245, 248, 255)   # 눈사람 몸
COAL          = (45, 45, 60)      # 눈·단추 (숯)
CARROT        = (255, 130, 30)    # 당근 코
SCARF_RED     = (235, 45, 95)     # 목도리 분홍빛 빨강
SCARF_WHITE   = (255, 235, 245)   # 목도리 흰 줄
HAT_RED       = (220, 30, 45)     # 산타 모자
STICK         = (140, 85, 45)     # 나뭇가지 팔

# ── 루돌프 · 산타 썰매 ──
DEER_BROWN    = (190, 120, 70)    # 사슴 몸
DEER_LIGHT    = (235, 200, 150)   # 사슴 뿔·눈
RUDOLPH_NOSE  = (255, 35, 35)     # 루돌프 빨간 코
SANTA_RED     = (235, 35, 45)     # 산타 옷·모자
SANTA_FUR     = (255, 255, 255)   # 산타 흰 털
SANTA_SKIN    = (255, 205, 175)   # 산타 얼굴
SLEIGH_RED    = (205, 25, 45)     # 썰매
SLEIGH_GOLD   = (255, 200, 80)    # 썰매 금장식·고삐
SACK          = (170, 120, 70)    # 선물 자루
TRAIL_GOLD    = (255, 215, 120)   # 썰매가 남기는 금가루
TRAIL_PINK    = (255, 150, 210)   # 썰매가 남기는 분홍가루
HOHO          = (255, 240, 250)   # "Ho Ho Ho!" 글씨

# ── 불꽃놀이 ──
FW_GOLD       = (255, 200, 80)    # 금색 불꽃
FW_PINK       = (255, 90, 180)    # 분홍 불꽃
FW_MINT       = (90, 255, 200)    # 민트 불꽃
FW_VIOLET     = (180, 120, 255)   # 보라 불꽃
FW_SKY        = (110, 190, 255)   # 하늘색 불꽃
FW_RED        = (255, 60, 80)     # 빨강 불꽃

# ── 눈송이 · 메시지 ──
SNOWFLAKE     = (225, 238, 255)   # 내리는 눈
MSG_PINK      = (255, 120, 190)   # 메시지 분홍
MSG_GOLD      = (255, 210, 110)   # 메시지 금색
NAME_GLOW     = (255, 235, 160)   # 'MIJU' 이름 반짝임

# ════════════════════════════════════════════════════════════════════
#  [개수·문구 설정]
# ════════════════════════════════════════════════════════════════════
NAME              = "MIJU"                        # 받는 사람 이름
MESSAGE           = "Merry Christmas, " + NAME    # 맨 아래 첫 메시지 (영어·기호만! 한글은 칸이 두 배라 어긋나요)
MESSAGE2          = "I love you, " + NAME         # 하트가 터진 뒤 바뀌는 메시지
NUM_STARS         = 500    # 배경 별 개수
NUM_ORNAMENTS     = 34     # 장식 볼 개수
NUM_LIGHTS        = 170    # 전구 개수
LIGHT_TURNS       = 5.5    # 전구 줄이 트리를 감는 바퀴 수
NUM_HEARTS        = 5      # 트리에 달리는 하트 개수
NUM_SNOW          = 240    # 내리는 눈송이 개수
SNOW_HEART_CHANCE = 0.07   # 눈송이 중 분홍 하트 비율 (0~1)
NUM_BURST_HEARTS  = 90     # 큰 하트가 터질 때 쏟아지는 작은 하트 개수
ROTATE_SECONDS    = 17.0   # 트리가 한 바퀴 도는 시간(초)
FPS               = 30     # 1초에 다시 그리는 횟수

# 선물: (자리 각도°, 중심에서 거리, 가로, 깊이, 높이, 상자색, 리본색, 상자 자체 회전°)
# 각도는 '열리는 상자' 기준이에요. 열릴 때 그 상자가 정면에 오도록 전체를 자동으로 돌려 놔요.
GIFTS = [
    (60,  1.02, 0.36, 0.30, 0.27, GIFT_RED,   GIFT_GOLD, 10),
    (120, 1.00, 0.26, 0.26, 0.38, WHITE,      GIFT_RED,  -25),
    (180, 1.04, 0.42, 0.32, 0.22, GIFT_GREEN, WHITE,     35),
    (240, 1.00, 0.30, 0.30, 0.33, GIFT_GOLD,  GIFT_RED,  -5),
    (300, 1.03, 0.38, 0.28, 0.25, BLUE,       SILVER,    20),
    (0,   1.05, 0.30, 0.28, 0.24, LAVENDER,   PINK,      -30),
]
OPEN_GIFT   = 5               # 몇 번째 상자가 열릴지 (0부터 셈) → 라벤더 상자
SNOWMAN_DEG = 90              # 눈사람 자리 (열리는 상자 기준 각도)
CANE_DEGS   = [150, 270, 330] # 지팡이 사탕 자리

# 불꽃놀이: (터지는 시각 초, 가로 칸, 세로 줄, 모양, 색1, 색2)   모양: ring / ring2 / heart / willow
FIREWORKS = [
    (20.4, 18, 13, 'ring',   FW_GOLD,   FW_RED),
    (21.0, 79, 16, 'heart',  FW_PINK,   FW_PINK),
    (21.7, 24, 22, 'ring2',  FW_MINT,   FW_VIOLET),
    (22.3, 72, 10, 'willow', FW_GOLD,   FW_GOLD),
    (22.9, 14, 15, 'heart',  FW_RED,    FW_PINK),
    (23.4, 84, 24, 'ring2',  FW_SKY,    FW_PINK),
    (24.0, 28, 9,  'heart',  FW_PINK,   FW_VIOLET),
    (24.4, 70, 19, 'ring',   FW_VIOLET, FW_MINT),
]

# ════════════════════════════════════════════════════════════════════
#  [시간표]  (초)
# ════════════════════════════════════════════════════════════════════
T_GROUND   = (0.0, 1.0)     # 1. 눈 땅
T_TREE     = (1.0, 4.0)     # 2. 회오리 + 트리
T_FLASH    = (4.0, 4.9)     # 3. 8방향 번쩍
T_BALLS    = (4.6, 6.4)     # 4. 장식 볼
T_LIGHTS   = (6.3, 8.3)     # 5. 전구
T_STAR     = (8.2, 9.0)     # 6. 꼭대기 별
T_HEARTS   = (9.0, 10.3)    # 7. 하트
T_GIFTS    = (10.2, 12.1)   # 8. 선물
T_CANES    = (11.9, 12.7)   #    지팡이 사탕
T_SNOWMAN  = (12.4, 13.6)   #    눈사람
T_SNOW     = 13.3           # 9. 눈 내리기 시작
T_MESSAGE  = (13.6, 15.0)   #    MIJU 메시지와 하트 별자리
T_CHASE    = 15.0           # 10. 전구 빛 달리기
T_SLEIGH   = (15.4, 21.0)   # 11. 루돌프와 산타 썰매
T_OPEN     = 24.6           # 12. 라벤더 상자 뚜껑이 열려요
T_RISE     = (25.0, 27.0)   #     큰 하트가 떠올라요
T_BURST    = 28.0           #     두근두근 하다가 펑!
T_MESSAGE2 = (28.4, 29.8)   #     두 번째 메시지

# ════════════════════════════════════════════════════════════════════
#  [서울 장면 · 편지 — 색]
# ════════════════════════════════════════════════════════════════════
HAN_TEAL      = (30, 150, 165)    # 한강 청록빛
HAN_BLUE      = (40, 85, 205)     # 한강 푸른빛
HAN_PURPLE    = (120, 70, 195)    # 한강 보랏빛
CITY_HAZE     = (125, 60, 150)    # 지평선 위 도시 불빛 안개
BUILDING_1    = (45, 52, 85)      # 건물 벽 (남색)
BUILDING_2    = (58, 50, 92)      # 건물 벽 (보랏빛)
BUILDING_3    = (42, 60, 88)      # 건물 벽 (푸른 회색)
BUILDING_4    = (68, 62, 100)     # 건물 벽 (연보라 회색)
WIN_YELLOW    = (255, 205, 110)   # 노란 창문 불빛
WIN_WHITE     = (235, 240, 255)   # 흰 창문 불빛
WIN_PINK      = (255, 140, 200)   # 분홍 창문 불빛
ROOF_SNOW     = (190, 200, 230)   # 지붕에 쌓인 눈
LAND_SNOW     = (80, 95, 140)     # 강변 땅 (눈 덮인 밤)
STREET_LAMP   = (255, 170, 80)    # 가로등·강변 조명
BRIDGE_STEEL  = (95, 105, 150)    # 다리 철골
BRIDGE_GOLD   = (255, 215, 140)   # 반포대교 조명 (금빛)
BRIDGE_LAV    = (190, 150, 255)   # 한남대교 조명 (라벤더)
BRIDGE_ICE    = (160, 210, 255)   # 먼 다리 조명 (얼음빛)
BOAT_WHITE    = (225, 230, 245)   # 유람선 선체
BOAT_LIGHT    = (255, 220, 150)   # 유람선 창문 불빛
HILL_DARK     = (22, 45, 42)      # 남산 숲 그늘
HILL_PINE     = (45, 95, 70)      # 남산 소나무 숲 (밝은 쪽)
FORTRESS      = (255, 225, 170)   # 한양도성 성곽 조명
LOVE_LOCKS    = [(255, 80, 150), (255, 60, 60), (255, 200, 80), (185, 145, 255), (110, 235, 200)]  # 사랑의 자물쇠
BEACON_FIRE   = (255, 140, 40)    # 봉수대 불빛
TOWER_WHITE   = (232, 236, 250)   # 남산타워 흰 조명
TOWER_PINK    = (255, 105, 185)   # 타워 분홍 조명
TOWER_LAV     = (185, 145, 255)   # 타워 라벤더 조명
TOWER_RED     = (255, 40, 40)     # 꼭대기·옥상 항공 경고등
NEON_PINK     = (255, 80, 170)    # MIJU 네온 분홍
NEON_GOLD     = (255, 205, 90)    # MIJU 네온 금색
DRONE_PINK    = (255, 110, 190)   # 드론 분홍
DRONE_LAV     = (185, 150, 255)   # 드론 라벤더
DRONE_GOLD    = (255, 205, 100)   # 드론 금색
ENVELOPE      = (175, 135, 255)   # 편지 봉투 라벤더
ENVELOPE_DARK = (95, 70, 160)     # 봉투 안쪽 그늘
ENVELOPE_LINE = (215, 190, 255)   # 봉투 접힌 선
LETTER_TEXT   = (255, 205, 230)   # 편지 글씨 (연분홍)

# ════════════════════════════════════════════════════════════════════
#  [서울 장면 · 편지 — 문구]
# ════════════════════════════════════════════════════════════════════
TOWER_TEXT    = NAME              # 남산타워에 세로로 켜지는 글자 (영어 대문자)
DRONE_TEXT    = NAME + " ♥"       # 드론이 마지막에 만드는 글자 (영어 대문자 · 공백 · ♥)
SEOUL_CAPTIONS = [                # (시작 초, 끝 초, 화면 아래 자막)
    (33.4, 39.6, "Hangang Bridge, Seoul  -  Christmas Eve"),
    (40.4, 46.6, "Yongsan  ->  Namsan"),
    (47.4, 54.2, "Namsan  -  N Seoul Tower"),
    (57.8, 67.6, "Drone Show over Hangang Bridge"),
]
# 편지 (한글 OK). 문단마다 한 줄씩 적으면, 화면 폭에 맞춰 알아서 줄을 바꾸고 여러 장으로 넘겨 가며 써요.
#   ♥ 는 하트 글자로 보여요. 문단 앞에 '*' 를 붙이면 금빛으로 강조돼요.
LETTER_TITLE = "To. 미주에게 ♥"
LETTER_PARAS = [
    "미주야, 메리 크리스마스!",
    "올해 크리스마스에는 너에게 조금 특별한 선물을 해주고 싶었어",
    "세상에는 수많은 반짝이는 것들이 있지만, 나에게 가장 특별하게 빛나는 건 너라는 걸 전해주고 싶었거든",
    "그래서 작은 별도 만들고, 크리스마스트리도 만들고, 서울의 밤하늘에도 너의 이름을 새겨봤어",
    "이 모든 장면이 언젠가 지나가더라도, 오늘 너를 위해 준비했던 이 순간만큼은 오래 기억에 남았으면 좋겠어",
    "앞으로 함께할 날들에도 지금처럼 서로에게 따뜻한 사람이 되어주자",
    "추운 겨울에는 서로의 온기가 되어주고, 평범한 날에는 서로의 작은 행복이 되어주면서 말이야",
    "내가 준비한 이 작은 크리스마스가 너에게 예쁜 추억으로 남았으면 좋겠어",
]
LETTER_LAST = [                   # 마지막 장 (금빛 · 분홍으로 번갈아 반짝여요)
    "*내 겨울을 따뜻하게 만들어줘서 고마워",
    "메리 크리스마스, 미주야",
    "항상 많이 아끼고 사랑해 ♥",
]
LETTER_FOOTER = ["Forever yours,", "Merry Christmas, " + NAME + " ♥"]   # 편지 맨 아래 두 줄
LETTER_CHAR_SEC = 0.05            # 편지 글자가 하나 써지는 시간(초)
LETTER_READ_SEC = 0.06            # 한 장을 다 쓴 뒤, 글자 하나당 읽을 시간(초)
LETTER_PARAS_PER_PAGE = 3         # 한 장에 들어가는 문단 수

# ════════════════════════════════════════════════════════════════════
#  [서울 장면 · 편지 — 시간표]  (초)
# ════════════════════════════════════════════════════════════════════
T_SEOUL_IN     = (31.0, 33.0)     # 21. 트리 → 서울 야경으로 전환
T_BRIDGES      = 33.0             #     다리 조명이 차례로 켜지기 시작
T_ARCH_LIGHTS  = 34.2             #     한강대교 아치 조명이 아래부터 꼭대기까지
T_FOUNTAIN     = 35.8             #     반포대교 달빛무지개분수
WATERFALLS     = [(36.3, 40.6), (62.5, 68.2)]   # 한강대교 불꽃 폭포 (시작 초, 끝 초)
# 한강대교에서 쏘아 올리는 불꽃: (터지는 시각, 가로 위치 x, 높이 y, 모양, 색1, 색2)
#   x 는 강 가운데가 0 (왼쪽 -, 오른쪽 +), 높이는 다리 상판이 0.4 예요.
BRIDGE_FIREWORKS = [
    (36.9, -1.6, 1.9, 'ring',   FW_GOLD,   FW_RED),
    (37.4,  1.4, 2.2, 'heart',  FW_PINK,   FW_PINK),
    (37.9,  0.0, 2.6, 'ring2',  FW_MINT,   FW_VIOLET),
    (38.5, -2.1, 2.3, 'willow', FW_GOLD,   FW_GOLD),
    (39.0,  2.0, 1.8, 'ring',   FW_SKY,    FW_PINK),
    (39.4, -0.5, 2.1, 'heart',  FW_RED,    FW_PINK),
    (66.9, -2.9, 1.6, 'ring',   FW_GOLD,   FW_PINK),   # 드론 쇼 마무리 불꽃
    (67.3, -0.3, 1.7, 'heart',  FW_PINK,   FW_PINK),
    (67.7, -1.6, 1.3, 'willow', FW_GOLD,   FW_GOLD),
]
T_CAM_MOVE     = (40.0, 47.0)     # 22. 한강 → 용산 → 남산 카메라 이동·줌인
T_TOWER_LIGHT  = (47.0, 48.6)     # 23. 타워 꼭대기부터 분홍·라벤더 조명
T_ZOOM         = (48.6, 52.3)     #     MIJU 가 크게 보이도록 타워 몸통으로 줌인 → 다시 줌아웃
T_LETTERS      = (49.3, 51.7)     #     M → I → J → U 한 글자씩
T_TOWER_GLOW   = 52.1             #     타워 전체가 환하게
T_TOWER_HEARTS = [52.9, 53.8]     #     타워 꼭대기 하트 불꽃
T_PULLBACK     = (54.5, 57.5)     # 24. 카메라가 한강으로 물러나요
DRONE_STEPS    = [                #     드론 쇼 (시작 초, 모양)
    (56.5, 'scatter'), (58.3, 'tree'), (61.7, 'heart'), (64.9, 'text')]
DRONE_MOVE_SEC = 1.8              #     모양 하나로 바뀌는 데 걸리는 시간
T_STARDUST     = (68.0, 70.2)     # 25. MIJU 글자가 별빛이 되어 트리로 날아가요
T_RETURN       = (68.6, 70.0)     #     서울 → 트리 전환
T_TOP_FLASH    = 70.2             #     트리 꼭대기 번쩍 + 분홍·금빛 퍼짐
T_GIFT_GLOW    = (70.6, 74.5)     #     라벤더 선물 강조
T_ENV          = 73.6             # 26. 편지 봉투 등장
T_ENV_OPEN     = (74.6, 75.8)     #     봉투가 열려요
T_LINES        = 76.0             #     편지 글자가 써지기 시작

LOOP = 140.0                      # (편지 길이에 맞춰 아래에서 다시 계산해요)

# ════════════════════════════════════════════════════════════════════
#  화면 · 카메라
# ════════════════════════════════════════════════════════════════════
# 화면 모양: pc = 가로 96칸 x 세로 54줄 (16:9),  phone = 72칸 x 64줄 (9:16 세로 화면)
#   터미널에서 휴대폰 모양으로 보기:  TREE_LAYOUT=phone python3 tree.py
LAYOUT = os.environ.get('TREE_LAYOUT', 'pc')
if LAYOUT == 'phone':
    W, H, K, CY = 72, 64, 0.85, 36.0     # K: PC 대비 크기, CY: 트리 장면의 화면 중심 줄
else:
    W, H, K, CY = 96, 54, 1.0, 27.0


def MX(x):
    """PC(96x54) 기준 가로 위치 → 지금 화면."""
    return W / 2 + (np.asarray(x, float) - 48) * K


def MY(y):
    """PC(96x54) 기준 세로 위치 → 지금 화면 (트리 장면 기준)."""
    return CY + (np.asarray(y, float) - 27) * K


# 화면 모양별 하늘 배치: 행성 (가로, 세로, 반지름) · 하트 별자리 (가로, 세로, 크기)
if LAYOUT == 'phone':
    PLANET_POS = [(12, 8, 5.0), (61, 6, 5.5), (6, 26, 2.8)]
    CONST_POS = (57.0, 19.0, 0.33)
else:
    PLANET_POS = [(12, 10, 6.2), (85, 9.5, 7.0), (8, 29, 3.4)]
    CONST_POS = (69.0, 5.2, 0.42)
RAMP = " .,:;-=+*#%@"
RAMP_ARR = np.array(list(RAMP))
CAM_D, TARGET_Y, PITCH, FOCAL = 6.6, 1.25, 0.15, 178.0 * K
_CP, _SP = math.cos(PITCH), math.sin(PITCH)
LIGHT = np.array([-1.0, 1.0, -1.0])
LIGHT /= np.linalg.norm(LIGHT)          # 왼쪽 위 앞에서 오는 빛
AMBIENT = 0.17
FAR = 1e8                                # 하늘에 붙은 것 (트리 뒤로 숨어요)

TIERS = [  # (아래 높이, 꼭대기 높이, 아래 반지름) 원뿔 4층
    (0.35, 1.30, 1.00),
    (0.85, 1.80, 0.80),
    (1.35, 2.25, 0.60),
    (1.85, 2.65, 0.40),
]
TREE_TOP = 2.65
STAR_Y = 2.84
GROUND_R = 1.42
TRUNK_R = 0.14

# 열리는 상자가 큰 하트가 떠오를 때(약 26.5초) 정면을 보도록 전체 배치를 돌려요
_FACE_T = 26.5
TURN = (360.0 * _FACE_T / ROTATE_SECONDS - 90.0) - GIFTS[OPEN_GIFT][0]


def col(c):
    return np.array(c, float) / 255.0


def lerp(a, b, u):
    return a + (b - a) * u


def clip01(x):
    return np.clip(x, 0.0, 1.0)


def ease_out_cubic(u):
    u = clip01(u)
    return 1 - (1 - u) ** 3


def ease_out_back(u, s=1.9):
    u = clip01(u)
    return 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2


def smooth(u):
    u = clip01(u)
    return u * u * (3 - 2 * u)


def rainbow(h):
    h = np.asarray(h) % 1.0
    return np.stack([clip01(np.abs(h * 6 - 3) - 1), clip01(2 - np.abs(h * 6 - 2)),
                     clip01(2 - np.abs(h * 6 - 4))], -1)


def heartbeat(ph):
    """0..1 주기 안에서 '두-근' 두 번 뛰는 모양."""
    return (np.exp(-(ph / 0.06) ** 2) + 0.65 * np.exp(-((ph - 0.2) / 0.06) ** 2)
            + np.exp(-((ph - 1) / 0.06) ** 2))


def norm_rows(v):
    return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-9)


def rot_y(P, a):
    c, s = math.cos(a), math.sin(a)
    out = np.empty_like(P)
    out[:, 0] = P[:, 0] * c + P[:, 2] * s
    out[:, 1] = P[:, 1]
    out[:, 2] = -P[:, 0] * s + P[:, 2] * c
    return out


def to_cam(P, yaw=0.0, normal=False):
    """월드 좌표 → 카메라 좌표 (카메라는 살짝 위에서 내려다봐요)."""
    if yaw:
        P = rot_y(P, yaw)
    y = P[:, 1] if normal else P[:, 1] - TARGET_Y
    z = P[:, 2]
    out = np.empty_like(P)
    out[:, 0] = P[:, 0]
    out[:, 1] = y * _CP + z * _SP
    out[:, 2] = -y * _SP + z * _CP + (0.0 if normal else CAM_D)
    return out


def project(Pc):
    z = np.maximum(Pc[:, 2], 0.05)
    sx = W * 0.5 + FOCAL * Pc[:, 0] / z
    sy = CY - FOCAL * 0.5 * Pc[:, 1] / z         # 글자는 세로로 길어서 0.5배
    return sx, sy, z


def tree_radius(y):
    y = np.asarray(y, float)
    r = np.where((y >= 0) & (y < TIERS[0][0] + 0.02), TRUNK_R, 0.0)
    for b, tp, R in TIERS:
        m = (y >= b) & (y <= tp)
        r = np.where(m, np.maximum(r, R * (tp - y) / (tp - b)), r)
    return r


def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.cos(phi), np.sin(th) * np.sin(phi)], 1)


def torus(n, R, r, rng):
    a = rng.random(n) * 2 * math.pi
    b = rng.random(n) * 2 * math.pi
    N = np.stack([np.cos(a) * np.cos(b), np.sin(b), np.sin(a) * np.cos(b)], 1)
    P = np.stack([np.cos(a) * R, np.zeros(n), np.sin(a) * R], 1) + N * r
    return P, N, a


def place(P, deg, dist, normal=False):
    """물체 자신의 좌표(x=옆, y=위, z=바깥쪽) → 트리 둘레의 자리."""
    th = math.radians(deg)
    f = np.array([math.cos(th), 0.0, math.sin(th)])
    s = np.array([-math.sin(th), 0.0, math.cos(th)])
    out = P[:, :1] * s + P[:, 1:2] * np.array([0.0, 1.0, 0.0]) + P[:, 2:3] * f
    return out if normal else out + f * dist


# ════════════════════════════════════════════════════════════════════
#  장면 만들기 (처음 한 번만 계산)
# ════════════════════════════════════════════════════════════════════
RNG = np.random.default_rng(20251225)


def build_ground():
    n = 6900
    rr = GROUND_R * np.sqrt(RNG.random(n))
    a = RNG.random(n) * 2 * math.pi
    x, z = rr * np.cos(a), rr * np.sin(a)
    bump = 0.018 * np.sin(x * 9 + 1) * np.sin(z * 11) + 0.008 * RNG.random(n)
    y = 0.07 * (1 - (rr / GROUND_R) ** 2) + bump
    slope = 0.14 * rr / GROUND_R ** 2
    N = np.stack([np.cos(a) * slope, np.ones(n), np.sin(a) * slope], 1)
    N += RNG.normal(0, 0.12, (n, 3))
    N = norm_rows(N)
    tint = clip01(0.5 + 0.5 * np.sin(x * 5 + z * 3) * np.cos(z * 4) + RNG.normal(0, 0.15, n))
    C = lerp(col(SNOW), col(SNOW_BLUE), (tint * 0.55)[:, None])
    m = 1600   # 옆면 (얼음 띠)
    a2 = RNG.random(m) * 2 * math.pi
    y2 = -0.15 * RNG.random(m)
    P2 = np.stack([GROUND_R * np.cos(a2), y2, GROUND_R * np.sin(a2)], 1)
    N2 = np.stack([np.cos(a2), np.zeros(m), np.sin(a2)], 1)
    C2 = lerp(col(ICE_RIM), col(SNOW_BLUE), clip01(1 + y2 / 0.05)[:, None] * 0.7)
    P = np.concatenate([np.stack([x, y, z], 1), P2])
    return dict(P=P, N=np.concatenate([N, N2]), C=np.concatenate([C, C2]),
                r=np.concatenate([rr, np.full(m, GROUND_R)]),
                side=np.concatenate([np.zeros(n, bool), np.ones(m, bool)]),
                glint=RNG.choice(n, 80, replace=False),
                gw=RNG.uniform(1.5, 4.0, 80), gp=RNG.uniform(0, 6.28, 80))


def build_tree():
    total = 21000
    areas = [R * math.hypot(R, tp - b) for b, tp, R in TIERS]
    Ps, Ns, Cs, Ss, As = [], [], [], [], []
    for (b, tp, R), ar in zip(TIERS, areas):
        n = int(total * ar / sum(areas))
        f = 1 - np.sqrt(RNG.random(n))           # 0=아래 테두리, 1=꼭대기
        a = RNG.random(n) * 2 * math.pi
        Ht = tp - b
        r = R * (1 - f)
        r = r * (1 + 0.08 * np.sin(a * 13 + f * 22) * (0.6 + 0.4 * np.sin(a * 5))
                 + 0.05 * (RNG.random(n) - 0.5))
        y = b + f * Ht - 0.035 * (1 + np.sin(a * 16)) * clip01(1 - f / 0.1)
        P = np.stack([r * np.cos(a), y, r * np.sin(a)], 1)
        N = np.stack([np.cos(a) * Ht, np.full(n, R), np.sin(a) * Ht], 1)
        N = norm_rows(norm_rows(N) + RNG.normal(0, 0.3, (n, 3)))
        g = clip01(RNG.random(n) * 0.65 + 0.35 * (0.5 + 0.5 * np.sin(a * 7 + y * 9)))
        lo = lerp(col(PINE_DARK), col(PINE), clip01(g / 0.45)[:, None])
        hi = lerp(col(PINE), col(PINE_LIGHT), clip01((g - 0.45) / 0.55)[:, None])
        C = np.where((g < 0.45)[:, None], lo, hi)
        mint = clip01((y / TREE_TOP) * 0.35 * RNG.random(n) * (f < 0.3))
        C = lerp(C, col(PINE_MINT), mint[:, None])
        snow = ((f < 0.13) & (RNG.random(n) < 0.5)) | (RNG.random(n) < 0.025)
        C[snow] = col(SNOW)
        S = np.where(snow, 0.35, 0.08)
        A = 0.62 + 0.25 * RNG.random(n)
        Ps.append(P); Ns.append(N); Cs.append(C); Ss.append(S); As.append(A)
    m = 900   # 갈색 기둥
    a = RNG.random(m) * 2 * math.pi
    y = RNG.random(m) * 0.42
    Ps.append(np.stack([TRUNK_R * np.cos(a), y, TRUNK_R * np.sin(a)], 1))
    Ns.append(np.stack([np.cos(a), np.zeros(m), np.sin(a)], 1))
    grain = clip01(0.5 + 0.5 * np.sin(a * 14 + np.sin(y * 30) * 1.5))
    Cs.append(lerp(col(TRUNK_BROWN), col(TRUNK_DARK), grain[:, None] * 0.8))
    Ss.append(np.full(m, 0.05)); As.append(np.ones(m))
    return dict(P=np.concatenate(Ps), N=np.concatenate(Ns), C=np.concatenate(Cs),
                S=np.concatenate(Ss), A=np.concatenate(As))


def surface_points(heights, angles, out=0.05):
    r = tree_radius(heights) + out
    return np.stack([r * np.cos(angles), heights, r * np.sin(angles)], 1)


def build_ornaments():
    n = NUM_ORNAMENTS
    i = np.arange(n)
    y = 0.5 + (2.35 - 0.5) * (i + 0.5) / n + RNG.uniform(-0.03, 0.03, n)
    a = i * 2.39996 + 0.4
    palette = np.array([col(RED), col(GOLD), col(SILVER)])
    return dict(c=surface_points(y, a, 0.05), color=palette[i % 3], unit=fib_sphere(150),
                t0=T_BALLS[0] + i * (T_BALLS[1] - T_BALLS[0] - 0.25) / max(n - 1, 1),
                rad=np.where(i % 3 == 2, 0.072, 0.082),
                sw=RNG.uniform(2.0, 4.5, n), sp=RNG.uniform(0, 6.28, n))


def build_lights():
    n = NUM_LIGHTS
    u = np.arange(n) / max(n - 1, 1)
    y = 0.42 + u * (2.52 - 0.42)
    a = u * LIGHT_TURNS * 2 * math.pi
    pal = np.array([col(BULB_WARM), col(BULB_RED), col(BULB_GOLD), col(BULB_GREEN)])
    return dict(P=surface_points(y, a, 0.035), color=pal[np.arange(n) % 4],
                t0=T_LIGHTS[0] + u * (T_LIGHTS[1] - T_LIGHTS[0] - 0.1),
                f=RNG.uniform(2.0, 6.0, n), ph=RNG.uniform(0, 6.28, n))


def build_hearts():
    n = NUM_HEARTS
    i = np.arange(n)
    y = 0.62 + (2.2 - 0.62) * ((i * 0.618 + 0.13) % 1.0)
    a = i * (2 * math.pi / max(n, 1)) + 0.9
    span = T_HEARTS[1] - T_HEARTS[0] - 0.3
    return dict(P=surface_points(y, a, 0.07),
                t0=T_HEARTS[0] + i * span / max(n - 1, 1), ph=RNG.uniform(0, 1, n))


def build_star():
    """꼭대기 별: 카메라를 보는 별 모양 평면 + 깎은 면처럼 보이는 법선."""
    g = np.linspace(-1, 1, 70)
    X, Y = np.meshgrid(g, g)
    X, Y = X.ravel(), Y.ravel()
    ang = np.arctan2(Y, X)
    rad = np.hypot(X, Y)
    k = 5
    local = ((ang - math.pi / 2) % (2 * math.pi / k)) / (2 * math.pi / k)
    tri = np.abs(local - 0.5) * 2
    ri, ro = 0.42, 1.0
    th = (1 - tri) * (math.pi / k)
    Dx, Dy = ri * math.cos(math.pi / k) - ro, ri * math.sin(math.pi / k)
    bound = ro * Dy / (np.cos(th) * Dy - np.sin(th) * Dx)
    inside = rad <= bound
    X, Y, ang, local = X[inside], Y[inside], ang[inside], local[inside]
    sector = 2 * math.pi / k
    vert = np.where(local < 0.5, ang - local * sector, ang + (1 - local) * sector)
    side = np.where(local < 0.5, 1.0, -1.0)
    perp = np.stack([-np.sin(vert), np.cos(vert)], 1) * side[:, None]
    nxy = np.stack([np.cos(vert), np.sin(vert)], 1) * 0.6 - perp * 1.3
    N = norm_rows(np.stack([nxy[:, 0], nxy[:, 1], -np.ones(len(X))], 1))
    return dict(xy=np.stack([X, Y], 1), N=N)


def build_gifts():
    out = []
    for gi, (deg, dist, w, d, h, bc, rc, yaw) in enumerate(GIFTS):
        sp = 0.022
        rw = min(w, d) * 0.12
        P, N, R = [], [], []

        def grid(u0, u1, v0, v1):
            us = np.arange(u0 + sp / 2, u1, sp)
            vs = np.arange(v0 + sp / 2, v1, sp)
            U, V = np.meshgrid(us, vs)
            U = U.ravel() + RNG.uniform(-sp / 3, sp / 3, U.size)
            V = V.ravel() + RNG.uniform(-sp / 3, sp / 3, V.size)
            return U, V

        U, V = grid(-w / 2, w / 2, -d / 2, d / 2)            # 윗면
        P.append(np.stack([U, np.full(U.size, h), V], 1))
        N.append(np.tile([0, 1, 0], (U.size, 1)))
        R.append((np.abs(U) < rw) | (np.abs(V) < rw))
        for sx in (-1, 1):                                    # 옆면 ±x
            U, V = grid(-d / 2, d / 2, 0, h)
            P.append(np.stack([np.full(U.size, sx * w / 2), V, U], 1))
            N.append(np.tile([sx, 0, 0], (U.size, 1)))
            R.append(np.abs(U) < rw)
        for sz in (-1, 1):                                    # 옆면 ±z
            U, V = grid(-w / 2, w / 2, 0, h)
            P.append(np.stack([U, V, np.full(U.size, sz * d / 2)], 1))
            N.append(np.tile([0, 0, sz], (U.size, 1)))
            R.append(np.abs(U) < rw)
        P = np.concatenate(P); N = np.concatenate(N).astype(float); R = np.concatenate(R)
        C = np.where(R[:, None], col(rc), col(bc))
        S = np.where(R, 0.55, 0.12)
        unit = fib_sphere(110)                                # 매듭: 고리 두 개 + 가운데
        bows_P, bows_N = [], []
        for sgn in (-1, 1):
            sc = np.array([0.055, 0.032, 0.028]) * (min(w, d) / 0.3) ** 0.5
            q = unit * sc
            ang = sgn * 0.55
            c_, s_ = math.cos(ang), math.sin(ang)
            q = np.stack([q[:, 0] * c_ - q[:, 1] * s_, q[:, 0] * s_ + q[:, 1] * c_, q[:, 2]], 1)
            n_ = unit / sc
            n_ = np.stack([n_[:, 0] * c_ - n_[:, 1] * s_, n_[:, 0] * s_ + n_[:, 1] * c_, n_[:, 2]], 1)
            q += [sgn * sc[0] * 0.85, h + sc[1] * 0.9, 0]
            bows_P.append(q); bows_N.append(norm_rows(n_))
        bows_P.append(unit[:60] * 0.022 + [0, h + 0.018, 0]); bows_N.append(unit[:60])
        bP = np.concatenate(bows_P); bN = np.concatenate(bows_N)
        P = np.concatenate([P, bP]); N = np.concatenate([N, bN])
        C = np.concatenate([C, np.tile(col(rc), (len(bP), 1))])
        S = np.concatenate([S, np.full(len(bP), 0.6)])
        a = math.radians(deg + TURN)
        out.append(dict(P=P, N=N, C=C, S=S, h=h, d=d, lid=P[:, 1] >= h - 0.045,
                        yaw=math.radians(yaw),
                        base=np.array([dist * math.cos(a), 0.0, dist * math.sin(a)]),
                        size=max(w, d),
                        t0=T_GIFTS[0] + gi * (T_GIFTS[1] - T_GIFTS[0] - 0.45) / max(len(GIFTS) - 1, 1)))
    return out


def build_canes():
    rs = np.random.default_rng(7)
    out = []
    Hc, R, rc = 0.40, 0.07, 0.034
    for k, deg in enumerate(CANE_DEGS):
        n1, n2 = 360, 260
        y = rs.random(n1) * Hc
        a1 = rs.random(n1) * 2 * math.pi
        P1 = np.stack([rc * np.cos(a1), y, rc * np.sin(a1)], 1)
        N1 = np.stack([np.cos(a1), np.zeros(n1), np.sin(a1)], 1)
        phi = rs.random(n2) * math.pi                       # 고리 부분
        a2 = rs.random(n2) * 2 * math.pi
        c = np.stack([R - R * np.cos(phi), Hc + R * np.sin(phi), np.zeros(n2)], 1)
        n1v = np.stack([np.cos(phi), -np.sin(phi), np.zeros(n2)], 1)
        N2 = n1v * np.cos(a2)[:, None] + np.array([0, 0, 1.0]) * np.sin(a2)[:, None]
        P2 = c + N2 * rc
        s = np.concatenate([y, Hc + R * phi])
        aa = np.concatenate([a1, a2])
        stripe = ((s * 9 + aa / (2 * math.pi)) % 1.0) < 0.5
        C = np.where(stripe[:, None], col(CANE_RED), col(CANE_WHITE))
        P = np.concatenate([P1, P2]); N = np.concatenate([N1, N2])
        ry = rs.uniform(0, 6.28)
        P = rot_y(P, ry); N = rot_y(N, ry)
        out.append(dict(P=place(P, deg + TURN, 1.24), N=place(N, deg + TURN, 0, True), C=C,
                        H=Hc + R, t0=T_CANES[0] + k * (T_CANES[1] - T_CANES[0] - 0.4) / max(len(CANE_DEGS) - 1, 1)))
    return out


def build_snowman():
    """눈사람: 자기 좌표에서 만들고 (x=옆, y=위, z=바깥쪽) 트리 옆 자리에 세워요."""
    rs = np.random.default_rng(3)
    r0, r1, r2 = 0.20, 0.145, 0.105
    y0 = 0.18
    y1 = y0 + r0 + r1 - 0.06
    y2 = y1 + r1 + r2 - 0.04
    t0 = T_SNOWMAN[0]
    parts = []

    def ball(r, cy, n, tt, coal_dirs):
        U = fib_sphere(n)
        C = np.tile(col(SNOWMAN), (n, 1)) * (0.92 + 0.08 * rs.random(n))[:, None]
        for d in coal_dirs:
            d = np.array(d, float); d /= np.linalg.norm(d)
            C[U @ d > 0.972] = col(COAL)
        parts.append(dict(P=U * r + [0, cy, 0], N=U, C=C, spec=0.3, t0=tt, piv=np.array([0, cy, 0])))

    ball(r0, y0, 900, t0, [])
    ball(r1, y1, 650, t0 + 0.3, [(0, 0.35, 0.94), (0, 0.0, 1), (0, -0.35, 0.94)])
    ball(r2, y2, 520, t0 + 0.6, [(-0.38, 0.3, 0.88), (0.38, 0.3, 0.88)])
    ta = t0 + 0.85
    head = np.array([0, y2, 0])
    # 당근 코
    n = 80
    s = rs.random(n); a = rs.random(n) * 2 * math.pi
    rr = 0.026 * (1 - s)
    P = np.stack([rr * np.cos(a), y2 + rr * np.sin(a), r2 - 0.01 + s * 0.11], 1)
    N = norm_rows(np.stack([np.cos(a), np.sin(a), np.full(n, 0.3)], 1))
    parts.append(dict(P=P, N=N, C=np.tile(col(CARROT), (n, 1)), spec=0.2, t0=ta, piv=head))
    # 산타 모자 + 흰 테 + 방울
    n = 360
    s = np.sqrt(rs.random(n)); s = 1 - s; a = rs.random(n) * 2 * math.pi
    base, tip = np.array([0, y2 + 0.065, 0]), np.array([0.08, y2 + 0.27, -0.02])
    cen = base + (tip - base) * s[:, None] + np.array([0.03, 0, 0]) * np.sin(s * math.pi)[:, None]
    rr = 0.092 * (1 - s)
    P = cen + np.stack([rr * np.cos(a), np.zeros(n), rr * np.sin(a)], 1)
    N = norm_rows(np.stack([np.cos(a), np.full(n, 0.45), np.sin(a)], 1))
    parts.append(dict(P=P, N=N, C=np.tile(col(HAT_RED), (n, 1)), spec=0.15, t0=ta, piv=head))
    P, N, _ = torus(200, 0.094, 0.022, rs)
    parts.append(dict(P=P + base, N=N, C=np.tile(col(SNOWMAN), (200, 1)), spec=0.3, t0=ta, piv=head))
    U = fib_sphere(70)
    parts.append(dict(P=U * 0.03 + tip, N=U, C=np.tile(col(SNOWMAN), (70, 1)), spec=0.3, t0=ta, piv=head))
    # 목도리 + 늘어진 끝
    ys = y1 + r1 * 0.78
    P, N, a = torus(300, 0.1, 0.03, rs)
    C = np.where((np.sin(a * 8) > 0)[:, None], col(SCARF_RED), col(SCARF_WHITE))
    parts.append(dict(P=P + [0, ys, 0], N=N, C=C, spec=0.1, t0=ta, piv=head))
    n = 90
    x = rs.uniform(0.035, 0.085, n); y = rs.uniform(ys - 0.17, ys, n)
    z = np.sqrt(np.maximum(r1 ** 2 - x ** 2 - (y - y1) ** 2, 0)) + 0.03
    C = np.where((np.sin(y * 70) > 0)[:, None], col(SCARF_RED), col(SCARF_WHITE))
    parts.append(dict(P=np.stack([x, y, z], 1), N=np.tile([0, 0, 1.0], (n, 1)), C=C,
                      spec=0.1, t0=ta, piv=head))
    return dict(parts=parts, y1=y1, r1=r1, deg=SNOWMAN_DEG + TURN, dist=1.22, t_arm=ta + 0.1,
                base=place(np.zeros((1, 3)), SNOWMAN_DEG + TURN, 1.22)[0])


def snowman_arms(tt, sm):
    pts = []
    for side in (-1, 1):
        ang = 0.45 if side < 0 else 0.55 + 0.45 * math.sin(tt * 6.0)   # 오른팔은 손 흔들기
        d = np.array([side * math.cos(ang), math.sin(ang), 0.05])
        st = np.array([side * sm['r1'] * 0.9, sm['y1'] + 0.02, 0])
        s = np.linspace(0, 0.24, 26)[:, None]
        pts.append(st + d * s)
        end = st + d * 0.17
        for fa in (0.7, -0.5):                                         # 손가락 가지
            c, s_ = math.cos(fa * side), math.sin(fa * side)
            fd = np.array([d[0] * c - d[1] * s_, d[0] * s_ + d[1] * c, 0])
            pts.append(end + fd * np.linspace(0, 0.07, 8)[:, None])
    return np.concatenate(pts)


def build_snow():
    n = NUM_SNOW
    return dict(x=RNG.uniform(-2.8, 2.8, n), z=RNG.uniform(-2.4, 2.4, n),
                y0=RNG.uniform(0, 0.5, n), v=RNG.uniform(0.28, 0.55, n),
                s0=T_SNOW + RNG.random(n) * 1.6,
                sw=RNG.uniform(0.7, 1.8, n), sp=RNG.uniform(0, 6.28, n),
                amp=RNG.uniform(0.05, 0.16, n),
                heart=RNG.random(n) < SNOW_HEART_CHANCE)


def build_background():
    Y, X = np.mgrid[0:H, 0:W].astype(float)
    nx, ny = 0.42, 0.91                       # 은하수: 왼쪽 아래 → 오른쪽 위로 비스듬히
    dist = (X - W / 2) * nx + (Y * 2 - H) * ny
    noise = (0.5 + 0.25 * np.sin(X * 0.21 + Y * 0.5) * np.sin(X * 0.07 - Y * 0.31)
             + 0.25 * RNG.random((H, W)))
    mw = 0.23 * np.exp(-(dist / 13.0) ** 2) * noise
    mix = clip01(0.5 + 0.5 * np.sin(X * 0.09 + Y * 0.13))[..., None]
    mwc = lerp(col(MILKY_BLUE), col(MILKY_VIOLET), mix)
    sx = RNG.integers(0, W, NUM_STARS)
    sy = RNG.integers(0, H, NUM_STARS)
    pal = np.array([col(STAR_WHITE), col(STAR_BLUE), col(STAR_WARM), col(STAR_PINK)])
    sc = pal[RNG.choice(4, NUM_STARS, p=[0.5, 0.25, 0.15, 0.10])]
    return dict(mw=mw.ravel(), mwc=mwc.reshape(-1, 3), X=X, Y=Y,
                sidx=(sy * W + sx), sc=sc, sb=RNG.uniform(0.3, 1.0, NUM_STARS),
                sf=RNG.uniform(0.6, 3.5, NUM_STARS), sp=RNG.uniform(0, 6.28, NUM_STARS))


def build_love_heart():
    """선물에서 떠오르는 큰 하트 (도톰하게 부푼 모양)."""
    rs = np.random.default_rng(5)
    n = 5200
    tt = rs.random(n) * 2 * math.pi
    r = np.sqrt(rs.random(n))
    ex = 16 * np.sin(tt) ** 3 / 17.0
    ey = (13 * np.cos(tt) - 5 * np.cos(2 * tt) - 2 * np.cos(3 * tt) - np.cos(4 * tt)) / 17.0
    X, Y = ex * r, ey * r + 0.05
    bul = np.sqrt(np.maximum(0.05, 1 - r ** 2))
    N = norm_rows(np.stack([ex * r * 1.1, ey * r * 1.1, -bul], 1))
    te = np.linspace(0, 2 * math.pi, 90, endpoint=False)
    edge = np.stack([16 * np.sin(te) ** 3,
                     13 * np.cos(te) - 5 * np.cos(2 * te) - 2 * np.cos(3 * te) - np.cos(4 * te)], 1) / 17.0
    return dict(xy=np.stack([X, Y], 1), N=N, edge=edge * 1.04 + [0, 0.05])


def build_burst():
    rs = np.random.default_rng(14)
    n = NUM_BURST_HEARTS
    ang = rs.uniform(0, 2 * math.pi, n)
    sp = rs.uniform(9, 30, n)
    pal = np.array([col(PINK), col(HOT_PINK), col(FW_RED), col(SCARF_WHITE), col(MSG_GOLD), col(FW_VIOLET)])
    return dict(vx=np.cos(ang) * sp * K, vy=(-np.sin(ang) * sp * 0.5 - 4) * K, c=pal[rs.choice(6, n, p=[.3, .25, .12, .13, .1, .1])],
                ch=np.where(rs.random(n) < 0.8, '♥', '*'), sw=rs.uniform(1, 3, n), ph=rs.uniform(0, 6.28, n))


def build_fireworks(spec=None, seed0=100):
    out = []
    for k, (tb, x, y, kind, c1, c2) in enumerate(FIREWORKS if spec is None else spec):
        rs = np.random.default_rng(seed0 + k)
        if kind == 'heart':
            n = 76
            tt = np.linspace(0, 2 * math.pi, n, endpoint=False)
            d = np.stack([16 * np.sin(tt) ** 3,
                          13 * np.cos(tt) - 5 * np.cos(2 * tt) - 2 * np.cos(3 * tt) - np.cos(4 * tt)], 1) / 16.0
            sp = np.ones(n) * rs.uniform(0.97, 1.03, n)
            cc = np.tile(col(c1), (n, 1)); R, grav, dur = 11.0, 2.0, 1.9
        elif kind == 'willow':
            n = 54
            a = rs.uniform(0, 2 * math.pi, n)
            d = np.stack([np.cos(a), np.sin(a)], 1)
            sp = rs.uniform(0.6, 1.0, n)
            cc = np.tile(col(c1), (n, 1)); R, grav, dur = 12.0, 11.0, 2.4
        else:
            n1, n2 = 64, (26 if kind == 'ring2' else 0)
            a = np.concatenate([np.linspace(0, 2 * math.pi, n1, endpoint=False), rs.uniform(0, 6.28, n2)])
            a = a + rs.normal(0, 0.03, len(a))
            d = np.stack([np.cos(a), np.sin(a)], 1)
            sp = np.concatenate([rs.uniform(0.92, 1.05, n1), rs.uniform(0.45, 0.6, n2)])
            cc = np.concatenate([np.tile(col(c1), (n1, 1)), np.tile(col(c2), (n2, 1))])
            if kind == 'ring':
                cc[1::4] = col(c2)
            R, grav, dur = 14.0, 4.5, 1.8
        out.append(dict(t=tb, x=x, y=y, d=d, sp=sp, c=cc, R=R, g=grav, dur=dur,
                        tw=rs.uniform(10, 30, len(sp)), willow=(kind == 'willow')))
    return out


# ── 루돌프 · 산타 썰매 글자 그림 ──
SPRITE_PAL = {'r': SANTA_RED, 'w': SANTA_FUR, 's': SANTA_SKIN, 'R': SLEIGH_RED, 'g': SLEIGH_GOLD,
              'k': SACK, 'p': PINK, 'y': GOLD, 'b': FW_SKY, 'd': DEER_BROWN, 'a': DEER_LIGHT,
              'n': RUDOLPH_NOSE}
SLEIGH_ART = [
    (r"         .*    ", "         rw    "),
    (r"  .--.  /__\   ", "  kkkk  rrrr   "),
    (r" (#*#) (^o^)   ", " kpyb  wsrsw   "),
    (r"\=============)", "gRRRRRRRRRRRRRg"),
    (r" '--'-------'-'", " gggggggggggggg"),
]
DEER_ART = [
    (r"        \Y/ ", "        aaa "),
    (r"        (o)@", "        dadn"),
    (r" ,______/   ", " dddddddd   "),
    (r" (______)   ", " dddddddd   "),
]
DEER_LEGS = [(r"  /|  /|    ", "  dddddd    "), (r"  |\  |\    ", "  dddddd    ")]


def make_sprite(rows):
    xs, ys, ch, cl = [], [], [], []
    for r, (row, key) in enumerate(rows):
        key = key.ljust(len(row))
        for c, (a, k) in enumerate(zip(row, key)):
            if a != ' ':
                xs.append(c); ys.append(r); ch.append(a); cl.append(col(SPRITE_PAL.get(k, DEER_BROWN)))
    return np.array(xs, float), np.array(ys, float), np.array(ch, dtype='<U1'), np.array(cl)


SPR_SLEIGH = make_sprite(SLEIGH_ART)
SPR_RUDOLPH = [make_sprite(DEER_ART + [L]) for L in DEER_LEGS]
SPR_DEER = [make_sprite([DEER_ART[0], (DEER_ART[1][0][:-1] + ' ', DEER_ART[1][1])] + DEER_ART[2:] + [L])
            for L in DEER_LEGS]

GROUND = build_ground()
TREE = build_tree()
ORN = build_ornaments()
LIGHTS = build_lights()
HEARTS = build_hearts()
STAR = build_star()
GIFT_LIST = build_gifts()
CANES = build_canes()
SNOWMAN_M = build_snowman()
SNOWF = build_snow()
BG = build_background()
LOVE = build_love_heart()
BURST = build_burst()
FW = build_fireworks()
for _f in FW:                                   # 트리 장면 불꽃은 화면 모양에 맞춰 옮겨요
    _f['x'], _f['y'] = float(MX(_f['x'])), float(MY(_f['y']))
    _f['R'] *= K
    _f['g'] *= K

# 하트 별자리 (오른쪽 위 하늘)
_ht = np.linspace(0, 2 * math.pi, 15)[:-1]
CONST_PTS = np.stack([CONST_POS[0] + CONST_POS[2] * 16 * np.sin(_ht) ** 3,
                      CONST_POS[1] - CONST_POS[2] * 0.5 * (13 * np.cos(_ht) - 5 * np.cos(2 * _ht)
                                           - 2 * np.cos(3 * _ht) - np.cos(4 * _ht))], 1)

# 큰 하트가 머무는 자리 (카메라 좌표) — 트리 앞 한가운데
HEART_END = np.array([0.0, 0.2, 5.05])


# ════════════════════════════════════════════════════════════════════
#  한 프레임 그리기
# ════════════════════════════════════════════════════════════════════
KERNEL = [(0, 0, 1.0), (-1, 0, .42), (1, 0, .42), (-2, 0, .13), (2, 0, .13),
          (0, -1, .30), (0, 1, .30), (-1, -1, .11), (1, -1, .11), (-1, 1, .11), (1, 1, .11)]


class Frame:
    def __init__(self):
        n = W * H
        self.zbuf = np.full(n, np.inf)
        self.scol = np.zeros((n, 3))
        self.slum = np.zeros(n)
        self.solid = np.zeros(n, bool)
        self.sglyph = np.zeros(n, bool)
        self.schar = np.full(n, '', dtype='<U1')   # 물결 같은 고정 글자
        self.water = np.zeros(n, bool)
        self.glow = np.zeros((n, 3))
        self.ochar = np.full(n, ' ', dtype='<U1')
        self.ocol = np.zeros((n, 3))
        self.has_o = np.zeros(n, bool)
        self.items = []
        self.fade = 1.0

    # ── 단단한 물체 (깊이 계산) ──
    def add_solid(self, Pc, Nc, C, spec=0.1, shin=24.0, emit=0.0, alb=1.0, ecol=(1.25, 1.25, 1.25), glyph=0):
        n = len(Pc)
        if n == 0:
            return
        b = lambda v: np.broadcast_to(np.asarray(v, float), (n,))
        self.items.append((Pc, Nc, np.broadcast_to(C, (n, 3)), b(spec), b(shin), b(emit), b(alb),
                           np.broadcast_to(np.asarray(ecol, float), (n, 3)), b(glyph)))

    def rasterize(self):
        if not self.items:
            return
        Pc, Nc, C, S, SH, E, A, EC, GL = (np.concatenate(z) for z in zip(*self.items))
        if self.fade < 1.0:      # 끝날 때 반짝이며 흩어지기
            keep = RNG.random(len(Pc)) < self.fade
            Pc, Nc, C, S, SH, E, A, EC, GL = (v[keep] for v in (Pc, Nc, C, S, SH, E, A, EC, GL))
        sx, sy, z = project(Pc)
        c = np.floor(sx).astype(np.int64)
        r = np.floor(sy).astype(np.int64)
        ok = (c >= 0) & (c < W) & (r >= 0) & (r < H) & (Pc[:, 2] > 0.2)
        if not ok.any():
            return
        sel = np.nonzero(ok)[0]
        idx = r[sel] * W + c[sel]
        order = np.lexsort((z[sel], idx))
        ids = idx[order]
        first = np.ones(len(ids), bool)
        first[1:] = ids[1:] != ids[:-1]
        win = sel[order[first]]
        cell = ids[first]
        n = Nc[win]
        p = Pc[win]
        v = -norm_rows(p)
        diff = clip01(n @ LIGHT)
        shade = AMBIENT + (1 - AMBIENT) * diff
        hv = norm_rows(LIGHT[None, :] + v)
        spec = S[win] * clip01(np.sum(n * hv, 1)) ** SH[win]
        rim = clip01(1 - np.abs(np.sum(n * v, 1))) ** 3 * 0.32
        colr = (C[win] * (0.2 + 0.8 * shade)[:, None] + spec[:, None]
                + rim[:, None] * col(MOON_RIM))
        lum = (0.1 + 0.9 * shade) * A[win] + spec + rim * 0.25
        e = E[win]
        colr = colr * (1 - e)[:, None] + e[:, None] * EC[win]
        lum = lum + e * 1.1
        self.zbuf[cell] = z[win]
        self.scol[cell] = colr
        self.slum[cell] = lum
        self.solid[cell] = True
        self.sglyph[cell] = GL[win] > 0

    # ── 빛나는 것 (겹치면 더해짐) ──
    def add_glow(self, sx, sy, rgb, z=None, halo=1.0):
        sx = np.atleast_1d(np.asarray(sx, float)); sy = np.atleast_1d(np.asarray(sy, float))
        rgb = np.broadcast_to(rgb, (len(sx), 3)) * self.fade
        c = np.floor(sx).astype(np.int64)
        r = np.floor(sy).astype(np.int64)
        ok = (c >= 0) & (c < W) & (r >= 0) & (r < H)
        if z is not None:
            zz = np.broadcast_to(z, (len(sx),))
            ii = np.nonzero(ok)[0]
            ok[ii] = zz[ii] <= self.zbuf[r[ii] * W + c[ii]] + 0.12
        c, r, rgb = c[ok], r[ok], rgb[ok]
        if len(c) == 0:
            return
        I, Wt = [], []
        for dx, dy, w in KERNEL:
            if halo <= 0 and (dx or dy):
                continue
            cc, rr = c + dx, r + dy
            m = (cc >= 0) & (cc < W) & (rr >= 0) & (rr < H)
            I.append(rr[m] * W + cc[m])
            Wt.append(rgb[m] * (w if (dx == 0 and dy == 0) else w * halo))
        I = np.concatenate(I); Wt = np.concatenate(Wt)
        for ch in range(3):
            self.glow[:, ch] += np.bincount(I, Wt[:, ch], minlength=W * H)

    def add_glow3d(self, Pc, rgb, halo=1.0, depth=True):
        sx, sy, z = project(Pc)
        self.add_glow(sx, sy, rgb, z if depth else None, halo)

    # ── 글자 덮어쓰기 (하트·눈·메시지·썰매) ──
    def overlay(self, sx, sy, chars, rgb, z=None):
        sx = np.atleast_1d(np.asarray(sx, float)); sy = np.atleast_1d(np.asarray(sy, float))
        c = np.floor(sx).astype(np.int64)
        r = np.floor(sy).astype(np.int64)
        ok = (c >= 0) & (c < W) & (r >= 0) & (r < H)
        idx = r * W + c
        if z is not None:
            zz = np.broadcast_to(z, (len(sx),))
            ii = np.nonzero(ok)[0]
            ok[ii] = zz[ii] < self.zbuf[idx[ii]] + 0.1
        chars = np.broadcast_to(np.asarray(chars, dtype='<U1'), (len(sx),))
        rgb = np.broadcast_to(rgb, (len(sx), 3)) * self.fade
        self.ochar[idx[ok]] = chars[ok]
        self.ocol[idx[ok]] = rgb[ok]
        self.has_o[idx[ok]] = True


# ── 배경 ──
def draw_planet(bc, bl, bch, cx, cy, rad, base, band=None, ring=False, t=0.0, k=1.0):
    if k < 0.03:
        return
    x0, x1 = int(max(0, cx - rad * 2.3)), int(min(W, cx + rad * 2.3 + 1))
    y0, y1 = int(max(0, cy - rad)), int(min(H, cy + rad + 1))
    if x0 >= x1 or y0 >= y1:
        return
    Y, X = np.mgrid[y0:y1, x0:x1].astype(float)
    dx = (X + 0.5 - cx) / rad
    dy = (Y + 0.5 - cy) * 2 / rad
    d2 = dx * dx + dy * dy
    L = np.array([-0.85, 0.55, -0.45]); L /= np.linalg.norm(L)

    def put(mask, colr, lum):
        ii = (Y[mask].astype(int) * W + X[mask].astype(int))
        bc[ii] = colr * k
        bl[ii] = lum * k
        bch[ii] = ''

    if ring:   # 고리 뒤쪽 (행성에 가려지는 부분)
        ang = -0.38
        u = dx * math.cos(ang) - dy * math.sin(ang)
        v = (dx * math.sin(ang) + dy * math.cos(ang)) / 0.28
        rr = np.hypot(u, v)
        band_ = (rr > 1.35) & (rr < 2.15) & ~((rr > 1.68) & (rr < 1.76))
        back = band_ & (v < 0) & (d2 > 1)
        front = band_ & (v >= 0)
        rl = 0.28 + 0.22 * np.sin(rr * 18) ** 2
        rshade = np.where(u < 0, 1.0, 0.55)
        if back.any():
            put(back, col(RING_SILVER) * (0.3 + 0.6 * rl[back] * rshade[back])[:, None],
                rl[back] * rshade[back] * 0.75)
    inside = d2 <= 1
    if inside.any():
        nz = -np.sqrt(np.maximum(0, 1 - d2[inside]))
        n = np.stack([dx[inside], -dy[inside], nz], 1)
        diff = clip01(n @ L) ** 1.1
        tex = 0.85 + 0.15 * np.sin(dy[inside] * 7 + 1.5 * np.sin(dx[inside] * 3 + t * 0.15))
        c = np.broadcast_to(col(base), (inside.sum(), 3)) * tex[:, None]
        if band is not None:
            bm = clip01(np.sin(dy[inside] * 5.5 + np.sin(dx[inside] * 2 + t * 0.2) * 0.8) * 1.5)
            c = lerp(c, np.broadcast_to(col(band), c.shape), (bm * 0.45)[:, None])
        rimg = clip01(np.sqrt(d2[inside]) - 0.8) * 2.5 * clip01(n @ L + 0.4)
        shade = 0.035 + 0.95 * diff
        put(inside, c * (0.15 + 0.85 * shade)[:, None] + rimg[:, None] * 0.25 * c,
            shade * 0.92 + rimg * 0.15)
    if ring and front.any():
        put(front, col(RING_SILVER) * (0.3 + 0.7 * rl[front] * rshade[front])[:, None],
            rl[front] * rshade[front] * 0.85)


def background(tg, star_k=1.0, planet_k=1.0, aurora_k=1.0):
    n = W * H
    lum = BG['mw'] * (0.85 + 0.15 * np.sin(tg * 0.6 + BG['X'].ravel() * 0.05)) * (0.35 + 0.65 * star_k)
    colr = BG['mwc'] * 0.55
    X, Y = BG['X'], BG['Y']                      # 오로라 커튼
    base = 8.5 + 2.4 * np.sin(X * 0.055 + tg * 0.22) + 1.3 * np.sin(X * 0.13 - tg * 0.37)
    streak = 0.5 + 0.5 * np.sin(X * 0.65 + 2.2 * np.sin(X * 0.045 + tg * 0.3) + tg * 0.5)
    d = base - Y
    prof = np.where(d >= 0, np.exp(-d / 3.2), np.exp(-(d / 1.0) ** 2))
    edge = clip01(1 - np.abs(X - W / 2) / (W / 2 + 2)) ** 0.8
    alum = aurora_k * (0.34 * streak * prof * edge * (0.75 + 0.25 * np.sin(tg * 0.8))).ravel()
    hue1 = lerp(col(AURORA_MINT), col(AURORA_VIOLET), clip01(d / 4.0)[..., None])
    hue = lerp(hue1, col(AURORA_ROSE), clip01((d - 4) / 4.0)[..., None]).reshape(-1, 3)
    tot = lum + alum + 1e-6
    colr = (colr * lum[:, None] + hue * 0.75 * alum[:, None]) / tot[:, None]
    colr = colr * clip01(0.6 + tot * 2.0)[:, None]
    lum = tot
    bch = np.full(n, '', dtype='<U1')
    tw = 0.5 + 0.5 * np.sin(BG['sf'] * tg + BG['sp'])   # 별 깜빡이
    b = BG['sb'] * (0.18 + 0.82 * tw ** 2) * star_k
    si = BG['sidx']
    lum[si] = np.maximum(lum[si], b * 0.75)
    colr[si] = BG['sc'] * (0.35 + 0.65 * b)[:, None]
    bch[si] = np.where(b > 0.8, '*', np.where(b > 0.6, '+', ''))
    (p1x, p1y, p1r), (p2x, p2y, p2r), (p3x, p3y, p3r) = PLANET_POS
    draw_planet(colr, lum, bch, p1x + 0.4 * math.sin(tg * 0.3), p1y + 0.8 * math.sin(tg * 0.45),
                p1r, PLANET_SILVER, None, ring=True, t=tg, k=planet_k)
    draw_planet(colr, lum, bch, p2x + 0.4 * math.sin(tg * 0.27 + 2), p2y + 0.8 * math.sin(tg * 0.4 + 1.3),
                p2r, PLANET_BLUE, PLANET_BLUE_2, t=tg, k=planet_k)
    draw_planet(colr, lum, bch, p3x + 0.3 * math.sin(tg * 0.33 + 4), p3y + 0.7 * math.sin(tg * 0.5 + 2.6),
                p3r, PLANET_PURPLE, None, t=tg, k=planet_k)
    return colr, lum, bch


def shooting_star(fr, tg):
    period = 6.5
    k = math.floor(tg / period)
    u = (tg - k * period) / 0.9
    if u > 1:
        return
    rs = np.random.default_rng(k + 7)
    x0, y0 = rs.uniform(0.57 * W, 0.96 * W), rs.uniform(0, 7)
    dx, dy = -1.0, rs.uniform(0.3, 0.5)
    head = u * 45
    s = np.linspace(0, 12, 30)
    inten = (1 - s / 12) ** 1.5 * math.sin(math.pi * u) * 1.1
    tint = lerp(col(SHOOTING_STAR), col(STAR_PINK), (s / 12)[:, None])
    fr.add_glow(x0 + dx * (head - s), y0 + dy * (head - s), tint * inten[:, None], z=FAR, halo=0.4)


# ── 새 장면들 ──
def draw_fireworks(fr, t):
    for f in FW:
        lu = (t - (f['t'] - 0.75)) / 0.75
        if 0 < lu < 1:                                   # 쏘아 올리기
            py = lerp(float(MY(46.0)), f['y'], ease_out_cubic(lu))
            px = f['x'] + 0.6 * math.sin(lu * 9)
            k = np.arange(8)
            fr.add_glow(px - 0.15 * k * math.cos(lu * 9), py + k * 0.8,
                        col(FW_GOLD) * (0.7 * (1 - k / 8) ** 1.5)[:, None], z=FAR, halo=0.3)
        fw_burst(fr, f, t, f['x'], f['y'])


def fw_burst(fr, f, t, cx, cy, z=FAR):
    bu = (t - f['t']) / f['dur']
    if not (0 < bu < 1):
        return
    if bu < 0.12:                                    # 터지는 순간 번쩍
        fr.add_glow([cx], [cy], col(FLASH_WHITE) * (1 - bu / 0.12) * 1.6, z=z, halo=2.2)
    tails = 6 if f['willow'] else 4
    xs, ys, cs = [], [], []
    for j in range(tails):
        b = bu - j * 0.03
        if b <= 0:
            break
        e = ease_out_cubic(min(1.0, b * 1.5))
        x = cx + f['d'][:, 0] * f['sp'] * f['R'] * e
        y = cy - f['d'][:, 1] * f['sp'] * f['R'] * 0.5 * e + f['g'] * b * b
        inten = (1 - b) ** 1.2 * (1 - j / tails) ** 1.3 * 1.05
        if bu > 0.55:                                # 끝자락은 타닥타닥
            inten = inten * (0.35 + 0.65 * (np.sin(f['tw'] * t) > 0))
        xs.append(x); ys.append(y); cs.append(f['c'] * np.broadcast_to(inten, x.shape)[:, None])
    if xs:
        fr.add_glow(np.concatenate(xs), np.concatenate(ys), np.concatenate(cs), z=z, halo=0.45)


def sleigh_xy(tt):
    u = (tt - T_SLEIGH[0]) / (T_SLEIGH[1] - T_SLEIGH[0])
    return -58 + u * (W + 66), float(MY(11 - 3.2 * math.sin(math.pi * min(max(u, 0.0), 1.0))))


def draw_sleigh(fr, t, tg):
    if not (T_SLEIGH[0] <= t <= T_SLEIGH[1] + 1.6):
        return
    # 금가루·분홍가루 꼬리 (썰매가 지나간 자리에 남아요)
    dt = 0.02
    ids = math.floor(t / dt) - np.arange(80)
    te = ids * dt
    ok = (te >= T_SLEIGH[0]) & (te <= T_SLEIGH[1])
    if ok.any():
        ids, te = ids[ok], te[ok]
        age = t - te
        h1 = (np.sin(ids * 12.9898) * 43758.5453) % 1.0
        h2 = (np.sin(ids * 78.233) * 12543.123) % 1.0
        ex = np.array([sleigh_xy(v)[0] for v in te]) + 1
        ey = np.array([sleigh_xy(v)[1] for v in te]) + 4
        x = ex + (h1 - 0.5) * 3
        y = ey + age * 1.5 + age * age * 2.5 + (h2 - 0.5) * 1.5
        inten = clip01(1 - age / 1.6) ** 1.6 * (0.45 + 0.55 * (0.5 + 0.5 * np.sin(h1 * 50 + t * 18)) ** 2)
        pal = np.array([col(TRAIL_GOLD), col(TRAIL_PINK), col(SNOW_GLINT)])
        fr.add_glow(x, y, pal[(h2 * 3).astype(int) % 3] * inten[:, None], z=FAR, halo=0.35)
    if t > T_SLEIGH[1]:
        return
    x0, y0 = sleigh_xy(t)
    x0 = round(x0)
    ys = round(y0 + 0.5 * math.sin(tg * 7))
    # 고삐
    xr = np.arange(x0 + 14, x0 + 52)
    fr.overlay(xr + 0.5, np.full(len(xr), ys + 2.5), '-', col(SLEIGH_GOLD) * 0.75, FAR)
    sx, sy, ch, cl = SPR_SLEIGH
    fr.overlay(x0 + sx + 0.5, ys + sy + 0.5, ch, cl, FAR)
    for k, off in enumerate((17, 30, 43)):              # 사슴 둘 + 맨 앞 루돌프
        yk = round(y0 + 0.9 * math.sin(tg * 7 - (k + 1) * 0.9)) - 1
        legs = int(tg * 8 + k) % 2
        spr = SPR_RUDOLPH[legs] if k == 2 else SPR_DEER[legs]
        sx, sy, ch, cl = spr
        fr.overlay(x0 + off + sx + 0.5, yk + sy + 0.5, ch, cl, FAR)
        if k == 2:                                       # 루돌프 빨간 코 반짝
            pulse = 0.75 + 0.5 * (0.5 + 0.5 * math.sin(tg * 9))
            fr.add_glow([x0 + off + 11.5], [yk + 1.5], col(RUDOLPH_NOSE) * pulse, z=FAR, halo=1.8)
    u = (t - T_SLEIGH[0]) / (T_SLEIGH[1] - T_SLEIGH[0])
    if 0.22 < u < 0.62:                                  # Ho Ho Ho!
        txt = "Ho Ho Ho!"
        shown = int(clip01((u - 0.22) / 0.12) * len(txt) + 0.999)
        bx = x0 + 4 + np.arange(shown)
        wob = 0.5 + 0.5 * np.sin(tg * 6 - np.arange(shown))
        cc = lerp(col(HOHO), col(TRAIL_PINK), wob[:, None] * 0.6)
        fr.overlay(bx + 0.5, np.full(shown, ys - 1.5), np.array(list(txt[:shown])), cc, FAR)


def heart_center(t, yaw, gift):
    top = gift['base'] + [0, gift['h'] + 0.02, 0]
    p0 = to_cam(top[None], yaw)[0]
    hu = (t - T_RISE[0]) / (T_RISE[1] - T_RISE[0])
    e = smooth(hu)
    c = lerp(p0, HEART_END, e)
    c[0] += 0.025 * math.sin(t * 2.2) * min(1.0, hu * 2)
    return c, hu


def draw_message(fr, msg, t0, t1, t, tg):
    n = len(msg)
    x0 = (W - n) // 2
    name_at = msg.find(NAME)
    for k, chh in enumerate(msg):
        tk = t0 + k * (t1 - t0) / n
        if t < tk:
            continue
        if chh == ' ':
            fr.overlay([x0 + k + 0.5], [H - 0.5], ' ', np.zeros(3))
            continue
        age = t - tk
        wave = 0.78 + 0.32 * math.sin(tg * 3.2 - k * 0.45)
        if name_at <= k < name_at + len(NAME):
            base = lerp(col(MSG_GOLD), col(NAME_GLOW), 0.5 + 0.5 * math.sin(tg * 4 + k))
            wave += 0.15
        else:
            base = lerp(col(MSG_PINK), col(MSG_GOLD), 0.5 + 0.5 * math.sin(k * 0.35 + tg * 0.8))
        if chh == '♥':
            base = col(HOT_PINK) * (0.8 + 0.4 * float(heartbeat((tg * 1.1) % 1.0)))
        pop = 1.4 * math.exp(-age / 0.18)
        cc = clip01(base * min(1.0, wave + pop) + max(0.0, pop - 0.3) * 0.6)
        fr.add_glow([x0 + k + 0.5], [H - 0.5], base * (0.05 + 0.5 * pop), halo=0.3)
        fr.overlay([x0 + k + 0.5], [H - 0.5], chh, cc)
    if name_at >= 0 and t > t1:
        if RNG.random() < 0.5:
            fr.add_glow([x0 + name_at + RNG.random() * len(NAME)], [H - 1.5], col(NAME_GLOW) * 0.5, halo=0.3)


# ── 메인 렌더 ──
def render_tree(t, tg, fade=1.0, show_msg=True, gift_glow=0.0):
    """트리 장면 한 장 (t = 트리 장면 시각)."""
    yaw = 2 * math.pi * t / ROTATE_SECONDS
    fr = Frame()
    fr.fade = fade
    bg_col, bg_lum, bg_ch = background(tg)
    opener = GIFT_LIST[OPEN_GIFT]

    # 1. 눈 땅 ──────────────────────────────────────────────
    gu = (t - T_GROUND[0]) / (T_GROUND[1] - T_GROUND[0])
    Rnow = GROUND_R * ease_out_cubic(gu) * 1.001
    gm = (GROUND['r'] <= Rnow) & (~GROUND['side'] | (gu >= 0.97))
    if gm.any():
        fr.add_solid(to_cam(GROUND['P'][gm], yaw), to_cam(GROUND['N'][gm], yaw, True),
                     GROUND['C'][gm], spec=0.25, shin=12, alb=0.85)

    # 2. 트리 ──────────────────────────────────────────────
    tu = (t - T_TREE[0]) / (T_TREE[1] - T_TREE[0])
    grow = (TREE_TOP + 0.03) * (0.45 * clip01(tu) + 0.55 * smooth(tu))
    grow_ext = grow + max(0.0, t - T_TREE[1]) * 1.0
    if tu > 0:
        ty = TREE['P'][:, 1]
        m = ty <= grow
        e = clip01(1 - (grow_ext - ty[m]) / 0.35) * 0.9
        fr.add_solid(to_cam(TREE['P'][m], yaw), to_cam(TREE['N'][m], yaw, True),
                     TREE['C'][m], spec=TREE['S'][m], shin=14, emit=e, alb=TREE['A'][m])

    # 3. 장식 볼 ────────────────────────────────────────────
    sc = ease_out_back((t - ORN['t0']) / 0.28)
    vis = np.nonzero(t >= ORN['t0'])[0]
    if len(vis):
        U = ORN['unit']
        cen = to_cam(ORN['c'][vis], yaw)
        rad = ORN['rad'][vis] * sc[vis]
        Nn = to_cam(np.tile(U, (len(vis), 1)), 0.0, True)
        Pc = (cen[:, None, :] + Nn.reshape(len(vis), -1, 3) * rad[:, None, None]).reshape(-1, 3)
        C = np.repeat(ORN['color'][vis], len(U), 0)
        pop = np.repeat(clip01(1 - (t - ORN['t0'][vis]) / 0.25) * 0.6, len(U))
        fr.add_solid(Pc, Nn, C, spec=0.9, shin=40, emit=pop, alb=1.05)

    # 4. 꼭대기 별 ─────────────────────────────────────────
    su = (t - T_STAR[0]) / (T_STAR[1] - T_STAR[0])
    star_c = to_cam(np.array([[0.0, STAR_Y, 0.0]]))[0]
    star_s = ease_out_back(su, 2.2) if su > 0 else 0.0
    if star_s > 0.01:
        spin = 0.25 * math.sin(tg * 0.9)
        cs, ss = math.cos(spin), math.sin(spin)
        Rm = np.array([[cs, ss], [-ss, cs]])
        xy = STAR['xy'] @ Rm * 0.21 * star_s
        Ns = STAR['N'].copy()
        Ns[:, :2] = STAR['N'][:, :2] @ Rm
        Pc = np.stack([star_c[0] + xy[:, 0], star_c[1] + xy[:, 1],
                       np.full(len(xy), star_c[2] - 0.1)], 1)
        fr.add_solid(Pc, Ns, col(STAR_GOLD), spec=0.5, shin=18,
                     emit=0.45 * clip01(1 - su * 1.5), alb=0.95)

    # 5. 선물 (열리는 상자는 뚜껑이 젖혀져요) ──────────────
    for gi, g in enumerate(GIFT_LIST):
        u = (t - g['t0']) / 0.45
        if u <= 0:
            continue
        P, N = g['P'], g['N']
        if gi == OPEN_GIFT and t >= T_OPEN:
            phi = 1.95 * ease_out_back((t - T_OPEN) / 0.55, 1.4)
            lid = g['lid']
            P, N = P.copy(), N.copy()
            yh, zh = g['h'], g['d'] / 2
            c, s = math.cos(phi), math.sin(phi)
            yy, zz = P[lid, 1] - yh, P[lid, 2] - zh
            P[lid, 1] = yy * c - zz * s + yh
            P[lid, 2] = yy * s + zz * c + zh
            ny, nz = N[lid, 1].copy(), N[lid, 2].copy()
            N[lid, 1] = ny * c - nz * s
            N[lid, 2] = ny * s + nz * c
        P = rot_y(P, g['yaw']) + g['base']
        N = rot_y(N, g['yaw'])
        P = P + [0, -(g['h'] + 0.12) * (1 - ease_out_back(u, 1.4)), 0]
        m = P[:, 1] >= 0.015
        if m.any():
            fr.add_solid(to_cam(P[m], yaw), to_cam(N[m], yaw, True), g['C'][m], spec=g['S'][m], shin=22)

    # 6. 지팡이 사탕 ────────────────────────────────────────
    for cn in CANES:
        u = (t - cn['t0']) / 0.4
        if u <= 0:
            continue
        P = cn['P'] + [0, -(cn['H'] + 0.1) * (1 - ease_out_back(u, 1.6)), 0]
        m = P[:, 1] >= 0.015
        if m.any():
            fr.add_solid(to_cam(P[m], yaw), to_cam(cn['N'][m], yaw, True), cn['C'][m], spec=0.7, shin=30)

    # 7. 눈사람 ────────────────────────────────────────────
    sm = SNOWMAN_M
    for part in sm['parts']:
        u = (t - part['t0']) / 0.3
        if u <= 0:
            continue
        s_ = ease_out_back(u, 2.0)
        Pl = part['piv'] + (part['P'] - part['piv']) * s_
        fr.add_solid(to_cam(place(Pl, sm['deg'], sm['dist']), yaw),
                     to_cam(place(part['N'], sm['deg'], 0, True), yaw, True), part['C'], spec=part['spec'], shin=16)
    if t >= sm['t_arm']:
        A = snowman_arms(tg, sm)
        grow_a = clip01((t - sm['t_arm']) / 0.3)
        A = A[: max(1, int(len(A) * grow_a))]
        fr.add_solid(to_cam(place(A, sm['deg'], sm['dist']), yaw),
                     to_cam(place(np.tile([0, 0, 1.0], (len(A), 1)), sm['deg'], 0, True), yaw, True),
                     col(STICK), spec=0.05, emit=0.15)

    # 8. 큰 하트 (선물에서 떠올라요) ────────────────────────
    heart_on = T_RISE[0] <= t < T_BURST
    if heart_on:
        hc, hu = heart_center(t, yaw, opener)
        hs = 0.05 + 0.33 * ease_out_back(hu, 1.3)
        beat = 0.0
        if t > T_RISE[1]:
            beat = float(heartbeat(((t - T_RISE[1]) * 1.5) % 1.0))
            hs *= 1 + 0.13 * beat
        swell = clip01((t - (T_BURST - 0.3)) / 0.3)
        hs *= 1 + 0.35 * swell ** 2
        w = 0.25 * math.sin(tg * 1.6)
        cw, sw = math.cos(w), math.sin(w)
        xy = LOVE['xy'] * hs
        Pc = np.stack([hc[0] + xy[:, 0] * cw, hc[1] + xy[:, 1], hc[2] + xy[:, 0] * sw], 1)
        Nh = LOVE['N'].copy()
        Nh[:, 0], Nh[:, 2] = LOVE['N'][:, 0] * cw - LOVE['N'][:, 2] * sw, LOVE['N'][:, 0] * sw + LOVE['N'][:, 2] * cw
        Ch = lerp(col(LOVE_HEART), col(HOT_PINK), clip01(0.5 - LOVE['xy'][:, 1] * 0.5)[:, None])
        fr.add_solid(Pc, Nh, Ch, spec=0.8, shin=20, emit=0.25 + 0.25 * beat + 0.5 * swell, alb=1.1,
                     ecol=lerp(Ch * 1.2, np.ones(3) * 1.3, swell), glyph=1)

    fr.rasterize()

    # ═══ 빛나는 것들 ═══
    shooting_star(fr, tg)
    draw_fireworks(fr, t)

    if 0 < gu < 1:     # 땅 퍼질 때 테두리 빛
        a = np.linspace(0, 2 * math.pi, 100, endpoint=False)
        ring = np.stack([Rnow * np.cos(a), np.full(100, 0.03), Rnow * np.sin(a)], 1)
        fr.add_glow3d(to_cam(ring, yaw), col(SNOW_GLINT) * (0.55 * (1 - gu)), halo=0.5)
    if gu > 0.3:       # 눈 반짝임
        gi_ = GROUND['glint']
        gl = np.maximum(0, np.sin(GROUND['gw'] * tg + GROUND['gp'])) ** 24
        ok = (GROUND['r'][gi_] <= Rnow) & (gl > 0.05)
        if ok.any():
            fr.add_glow3d(to_cam(GROUND['P'][gi_[ok]] + [0, 0.02, 0], yaw),
                          col(SNOW_GLINT) * (gl[ok] * 0.9)[:, None], halo=0.35)

    # 흰 빛 회오리 두 줄기
    if 0 < tu and t < T_FLASH[0] + 0.35:
        shrink = 1.0 - clip01((t - T_FLASH[0]) / 0.35)
        h = min(grow, TREE_TOP)
        for strand, sc_ in ((0, col(SWIRL_WHITE)), (1, col(SWIRL_ICE))):
            s = np.linspace(0, 1, 140)
            hs_ = np.maximum(h - s * 1.0 * shrink, 0.0)
            th = 2 * math.pi * 3.0 * hs_ / TREE_TOP + strand * math.pi
            rr = tree_radius(hs_) + 0.17 + 0.04 * np.sin(s * 20 + tg * 8)
            P = np.stack([rr * np.cos(th), hs_, rr * np.sin(th)], 1)
            inten = (1 - s) ** 1.7 * 0.9 * (0.4 + 0.6 * shrink)
            fr.add_glow3d(to_cam(P, yaw), sc_ * inten[:, None], halo=0.7)
            fr.add_glow3d(to_cam(P[:1], yaw), sc_ * 1.6, halo=1.6)
            k = 26
            sd = RNG.random(k) * 0.8
            hd = np.maximum(h - sd * shrink, 0)
            thd = 2 * math.pi * 3.0 * hd / TREE_TOP + strand * math.pi + RNG.normal(0, 0.15, k)
            rd = tree_radius(hd) + 0.17 + RNG.uniform(-0.05, 0.25, k)
            Pd = np.stack([rd * np.cos(thd), hd - RNG.random(k) * 0.1, rd * np.sin(thd)], 1)
            fr.add_glow3d(to_cam(Pd, yaw), sc_ * ((1 - sd) * 0.5)[:, None], halo=0)

    # 꼭대기 8방향 번쩍
    fu = (t - T_FLASH[0]) / (T_FLASH[1] - T_FLASH[0])
    top_s = project(to_cam(np.array([[0.0, TREE_TOP + 0.05, 0.0]])))
    tx, ty_ = top_s[0][0], top_s[1][0]
    if 0 < fu < 1:
        L = 18 * ease_out_cubic(min(1, fu * 1.8))
        I = (1 - fu) ** 1.6 * 1.5
        d = np.linspace(0, 1, 50)
        for k in range(8):
            ang = k * math.pi / 4
            ln = L * (1.0 if k % 2 == 0 else 0.6)
            fr.add_glow(tx + math.cos(ang) * d * ln, ty_ - math.sin(ang) * d * ln * 0.5,
                        col(FLASH_WHITE) * (I * (1 - d) ** 1.2)[:, None], halo=0.6)
        fr.add_glow([tx], [ty_], col(FLASH_WHITE) * I * 2.0, halo=2.5)

    # 장식 볼 반짝 하이라이트
    if len(vis):
        cen = to_cam(ORN['c'][vis], yaw)
        v = -norm_rows(cen)
        hv = norm_rows(LIGHT[None, :] + v)
        hp = cen + hv * (ORN['rad'][vis] * sc[vis] * 0.85)[:, None]
        spk = np.maximum(0, np.sin(ORN['sw'][vis] * tg + ORN['sp'][vis])) ** 10
        fr.add_glow3d(hp, (spk * 0.9 + 0.15)[:, None] * np.ones(3), halo=0.8)

    # 전구 (마지막엔 무지개 물결)
    lit = np.nonzero(t >= LIGHTS['t0'])[0]
    if len(lit):
        tw = 0.68 + 0.32 * np.sin(LIGHTS['f'][lit] * tg + LIGHTS['ph'][lit])
        pop = 1.3 * np.exp(-(t - LIGHTS['t0'][lit]) / 0.15)
        inten = 0.85 * tw + pop
        colors = LIGHTS['color'][lit]
        if t >= T_CHASE:   # 빛이 줄줄이 달려가요
            k = (lit - 48 * (t - T_CHASE)) % 28
            k = np.minimum(k, 28 - k)
            inten = 0.42 * tw + 1.35 * np.exp(-(k / 2.4) ** 2)
        if t >= T_BURST:
            mix = clip01((t - T_BURST) / 0.8)
            colors = lerp(colors, rainbow(lit / 42.0 - t * 0.45) * 0.85 + 0.15, mix)
        fr.add_glow3d(to_cam(LIGHTS['P'][lit], yaw), colors * inten[:, None], halo=0.9)

    # 꼭대기 별빛
    if star_s > 0.01:
        sx_, sy_, _ = project(star_c[None])
        cxs, cys = sx_[0], sy_[0]
        d = np.linspace(0.1, 1, 40)
        for k in range(8):
            ang = k * math.pi / 4 + tg * 0.3
            flick = 0.7 + 0.3 * math.sin(tg * 4.0 + k * 1.7)
            ln = (11.0 if k % 2 == 0 else 6.0) * star_s * flick
            fr.add_glow(cxs + math.cos(ang) * d * ln, cys - math.sin(ang) * d * ln * 0.5,
                        col(STAR_RAY) * (0.55 * flick * (1 - d) ** 1.5)[:, None], halo=0.35)
        fr.add_glow([cxs], [cys], col(STAR_RAY) * (0.5 + 0.2 * math.sin(tg * 5)) * star_s, halo=1.0)
        fr.add_glow(cxs + (RNG.random(3) - 0.5) * 16, cys + (RNG.random(3) - 0.5) * 7,
                    col(STAR_RAY) * 0.6, halo=0)

    # 선물·사탕 올라올 때 눈가루
    for obj, dur in [(g, 0.7) for g in GIFT_LIST] + [(c_, 0.6) for c_ in CANES]:
        u = (t - obj['t0']) / dur
        if 0 < u < 1:
            base = obj['base'] if 'base' in obj else obj['P'][:1].mean(0) * [1, 0, 1]
            sz = obj.get('size', 0.2)
            a = np.linspace(0, 2 * math.pi, 16, endpoint=False) + obj['t0']
            rr = sz * (0.5 + 0.6 * u)
            P = base + np.stack([rr * np.cos(a), 0.05 + 0.25 * u * np.abs(np.sin(a * 3)), rr * np.sin(a)], 1)
            fr.add_glow3d(to_cam(P, yaw), col(SNOW_GLINT) * (0.7 * (1 - u)), halo=0.4)
    # 눈사람 눈뭉치가 톡 생길 때
    for part in sm['parts'][:3]:
        u = (t - part['t0']) / 0.5
        if 0 < u < 1:
            a = np.linspace(0, 2 * math.pi, 14, endpoint=False)
            r_ = 0.22 * (0.6 + 0.8 * u)
            Pl = part['piv'] + np.stack([r_ * np.cos(a), 0.3 * r_ * np.sin(a * 2), r_ * np.sin(a)], 1)
            fr.add_glow3d(to_cam(place(Pl, sm['deg'], sm['dist']), yaw), col(SNOW_GLINT) * (0.6 * (1 - u)), halo=0.4)

    # 상자가 열릴 때 안에서 새어 나오는 빛
    ou = (t - T_OPEN) / 1.0
    if 0 < ou < 1.4:
        top = opener['base'] + [0, opener['h'], 0]
        k = 30
        rs = np.random.default_rng(int(t * 30))
        hgt = rs.random(k) * 0.6 * min(1.0, ou * 2)
        P = top + np.stack([rs.normal(0, 0.06, k), hgt, rs.normal(0, 0.06, k)], 1)
        inten = clip01(1.4 - ou) * (1 - hgt / 0.6)
        fr.add_glow3d(to_cam(P, yaw), lerp(col(TRAIL_GOLD), col(LOVE_GLOW), rs.random(k)[:, None]) * inten[:, None],
                      halo=0.5)
        fr.add_glow3d(to_cam(top[None], yaw), col(LOVE_GLOW) * clip01(1.2 - ou) * 1.2, halo=2.0)

    # 큰 하트 둘레 빛 + 맴도는 반짝이
    if heart_on:
        E = LOVE['edge'] * hs * 1.02
        Pe = np.stack([hc[0] + E[:, 0] * cw, hc[1] + E[:, 1], hc[2] + E[:, 0] * sw - 0.02], 1)
        fr.add_glow3d(Pe, col(LOVE_GLOW) * (0.18 + 0.25 * beat + 0.5 * swell), halo=0.9, depth=False)
        k = 10
        a = tg * 2.5 + np.arange(k) * 2 * math.pi / k
        orb = np.stack([hc[0] + np.cos(a) * hs * 1.5, hc[1] + np.sin(a * 2) * hs * 0.4 + 0.02,
                        hc[2] + np.sin(a) * hs * 1.5], 1)
        fr.add_glow3d(orb, col(NAME_GLOW) * (0.5 + 0.5 * np.sin(a * 3 + tg * 6))[:, None] ** 2, halo=0.5)

    # 펑! (충격파 고리 + 번쩍)
    bt = t - T_BURST
    bsx, bsy, bz = project(HEART_END[None])
    bsx, bsy, bz = bsx[0], bsy[0], bz[0]
    if 0 <= bt < 0.9:
        fr.add_glow([bsx], [bsy], lerp(col(FLASH_WHITE), col(LOVE_GLOW), min(1.0, bt * 3)) * (1 - bt / 0.9) ** 2 * 3.0,
                    halo=2.5)
        a = np.linspace(0, 2 * math.pi, 120, endpoint=False)
        rr = 4 + 38 * ease_out_cubic(bt / 0.9)
        fr.add_glow(bsx + np.cos(a) * rr, bsy + np.sin(a) * rr * 0.5,
                    col(LOVE_GLOW) * (0.7 * (1 - bt / 0.9) ** 1.5), halo=0.6)

    # ═══ 글자 덮어쓰기 ═══
    # 하트 ♥ (두근두근)
    on = np.nonzero(t >= HEARTS['t0'])[0]
    if len(on):
        Pc = to_cam(HEARTS['P'][on], yaw)
        sx_, sy_, z_ = project(Pc)
        beat_ = heartbeat((tg * 1.1 + HEARTS['ph'][on]) % 1.0)
        b = 0.5 + 0.7 * beat_ + 1.2 * np.exp(-(t - HEARTS['t0'][on]) / 0.2)
        cc = lerp(col(PINK), col(HOT_PINK), clip01(beat_)[:, None]) * np.minimum(b, 1.0)[:, None] \
            + clip01(b - 1.0)[:, None] * 0.7
        cell = np.clip(np.floor(sy_).astype(int), 0, H - 1) * W + np.clip(np.floor(sx_).astype(int), 0, W - 1)
        vis_h = z_ < fr.zbuf[cell] + 0.1
        if vis_h.any():
            fr.add_glow(sx_[vis_h], sy_[vis_h], col(PINK) * (0.25 + 0.35 * beat_[vis_h])[:, None], halo=1.4)
        fr.overlay(sx_, sy_, '♥', cc, z_)

    # 하트 별자리 (MIJU 별자리)
    cu = clip01((t - (T_MESSAGE[0] + 0.3)) / 1.2)
    if cu > 0:
        npts = len(CONST_PTS)
        shown = int(cu * npts + 0.999)
        for j in range(shown):
            a_, b_ = CONST_PTS[j], CONST_PTS[(j + 1) % npts]
            if j < shown - 1 or cu >= 1:
                s = np.linspace(0.2, 0.8, 5)
                fr.overlay(a_[0] + (b_[0] - a_[0]) * s, a_[1] + (b_[1] - a_[1]) * s, '.',
                           col(CONST_LINE) * 0.8, FAR)
        tw = 0.6 + 0.4 * np.sin(tg * 3 + np.arange(shown) * 1.3)
        pts = CONST_PTS[:shown]
        fr.add_glow(pts[:, 0], pts[:, 1], col(CONSTELLATION) * (0.35 * tw)[:, None], z=FAR, halo=0.5)
        fr.overlay(pts[:, 0], pts[:, 1], '*', col(CONSTELLATION) * tw[:, None], FAR)
        if cu >= 1:
            fr.overlay(CONST_POS[0] - len(NAME) / 2 + np.arange(len(NAME)) + 0.5, np.full(len(NAME), CONST_POS[1] + 0.3),
                       np.array(list(NAME)), col(CONSTELLATION) * (0.75 + 0.25 * math.sin(tg * 2)), FAR)

    # 눈 (가끔 분홍 하트)
    if t >= T_SNOW:
        S_ = SNOWF
        act = t >= S_['s0']
        top = 3.7
        y = top + S_['y0'] - ((t - S_['s0']) * S_['v']) % (top + 0.3)
        x = S_['x'] + S_['amp'] * np.sin(S_['sw'] * tg + S_['sp'])
        z = S_['z'] + 0.6 * S_['amp'] * np.cos(S_['sw'] * 0.7 * tg + S_['sp'])
        P = np.stack([x, y, z], 1)[act]
        sx_, sy_, z_ = project(to_cam(P))
        hrt = S_['heart'][act]
        ch = np.where(hrt, '♥', np.where(z_ < 6.0, '*', np.where(z_ < 7.4, '+', '.')))
        bright = clip01(1.25 - (z_ - 4.5) / 6.0)
        cc = np.where(hrt[:, None], col(PINK)[None], col(SNOWFLAKE)[None]) * bright[:, None]
        fr.overlay(sx_, sy_, ch, cc, z_)

    # 루돌프와 산타 썰매 (눈보다 앞에 보이게)
    draw_sleigh(fr, t, tg)

    # 펑! 하고 쏟아지는 작은 하트들
    if 0 <= bt < LOOP - T_BURST:
        k_ = 2.2
        dr = (1 - math.exp(-k_ * bt)) / k_
        x = bsx + BURST['vx'] * dr + 1.2 * np.sin(BURST['sw'] * tg + BURST['ph']) * min(1.0, bt)
        y = bsy + BURST['vy'] * dr + 0.6 * bt * bt + 1.4 * bt
        life = clip01(1.0 - (bt - 2.6) / 1.4)
        tw = 0.65 + 0.35 * np.sin(BURST['sw'] * 4 * tg + BURST['ph'])
        cc = BURST['c'] * (tw * life + clip01(1 - bt / 0.3) * 0.6)[:, None]
        if life > 0.02:
            fr.add_glow(x, y, BURST['c'] * (0.18 * life), halo=0.6)
            fr.overlay(x, y, BURST['ch'], cc, bz)

    # 라벤더 선물 강조 (서울에서 돌아온 뒤)
    if gift_glow > 0:
        gc = to_cam((opener['base'] + [0, opener['h'] * 0.5, 0])[None], yaw)
        gx, gy, _ = project(gc)
        gx, gy = gx[0], gy[0]
        a = np.linspace(0, 2 * math.pi, 40, endpoint=False) + tg * 1.5
        tw = 0.5 + 0.5 * np.sin(a * 3 + tg * 6)
        fr.add_glow(gx + np.cos(a) * 7.5, gy + np.sin(a) * 3.2,
                    lerp(col(LAVENDER), col(LOVE_GLOW), tw[:, None]) * (gift_glow * 0.6 * tw)[:, None], halo=0.5)
        fr.add_glow([gx], [gy], col(LAVENDER) * gift_glow * 0.7, halo=2.0)
        bob = 0.6 * math.sin(tg * 3)
        fr.overlay([gx + 0.5], [gy - 5 + bob], '♥', col(HOT_PINK) * min(1.0, gift_glow * 1.3))
        label = "for " + NAME
        fr.overlay(gx - len(label) / 2 + np.arange(len(label)) + 0.5, np.full(len(label), gy - 7 + bob),
                   np.array(list(label)), col(ENVELOPE_LINE) * gift_glow)

    # 맨 아래 메시지
    if show_msg and T_MESSAGE[0] <= t < T_BURST:
        draw_message(fr, "♥  " + MESSAGE + "  ♥", T_MESSAGE[0], T_MESSAGE[1], t, tg)
    elif show_msg and t >= T_MESSAGE2[0]:
        draw_message(fr, "♥  " + MESSAGE2 + "  ♥", T_MESSAGE2[0], T_MESSAGE2[1], t, tg)

    return compose_arrays(fr, bg_col, bg_lum, bg_ch)


_COLOR_CACHE = {}


def compose_arrays(fr, bg_col, bg_lum, bg_ch):
    """한 장면을 (글자, 색, 밝기) 배열로 합쳐요."""
    colr = bg_col.copy()
    lum = bg_lum.copy()
    s = fr.solid
    colr[s] = fr.scol[s]
    lum[s] = fr.slum[s]
    g = fr.glow
    gl = g.max(1)
    colr = colr + g
    lum = lum + gl
    m = colr.max(1)
    over = clip01((m - 1.0) / 1.2)          # 아주 밝으면 하얗게
    colr = colr / np.maximum(m, 1.0)[:, None]
    colr = colr * (1 - over)[:, None] + over[:, None]
    idx = np.clip((lum * 12).astype(np.int64), 0, 11)
    chars = RAMP_ARR[idx].astype('<U1')
    bgm = (~s) & (bg_ch != '') & (gl < 0.35)
    chars[bgm] = bg_ch[bgm]
    chars[fr.sglyph] = '♥'
    sc = s & (fr.schar != '') & (gl < 0.3)
    chars[sc] = fr.schar[sc]
    o = fr.has_o
    chars[o] = fr.ochar[o]
    colr[o] = fr.ocol[o]
    return chars, colr, lum


def to_ansi(arr):
    """(글자, 색) 배열 → 터미널 문자열 (지우지 않고 커서를 맨 위로 옮겨 덮어써요)."""
    chars, colr = arr[0], arr[1]
    rgb = (clip01(colr) * 255).astype(np.int64) // 3 * 3
    codes = ((rgb[:, 0] << 16) | (rgb[:, 1] << 8) | rgb[:, 2]).tolist()
    chl = chars.tolist()
    parts = ['\x1b[H\x1b[48;2;0;0;0m']
    last = -1
    cache = _COLOR_CACHE
    for y in range(H):
        base = y * W
        for i in range(base, base + W):
            c = chl[i]
            if c == '\x01':                   # 앞 글자(한글)가 두 칸을 차지해요
                continue
            if c == ' ' or c == '':
                parts.append(' ')
                continue
            k = codes[i]
            if k != last:
                sq = cache.get(k)
                if sq is None:
                    sq = cache[k] = '\x1b[38;2;%d;%d;%dm' % (k >> 16, (k >> 8) & 255, k & 255)
                parts.append(sq)
                last = k
            parts.append(c)
        if y < H - 1:
            parts.append('\r\n')
    return ''.join(parts)


# ════════════════════════════════════════════════════════════════════
#  21~24. 서울의 겨울밤 — 3D 광선 추적으로 그려요
#  (화면 한 칸마다 카메라에서 빛줄기를 쏘아 건물·다리·타워·한강에 닿는 곳을 찾아요)
# ════════════════════════════════════════════════════════════════════
RIVER_HALF = 3.5                               # 한강 반폭 (x = -3.5 ~ 3.5, 강은 앞으로 흘러가요)
TOWER_X, TOWER_Z, TOWER_Y0 = 6.5, 41.0, 2.4    # 남산타워 자리 (남산 꼭대기)
# 남산 능선: 타원체 여러 개를 겹쳐요 (중심 x, 중심 z, 반지름 x, 높이, 반지름 z)
HILLS = np.array([
    [6.5, 41.0, 3.2, 2.42, 3.0],     # 정상 (타워)
    [3.6, 40.5, 3.0, 1.60, 2.8],     # 서쪽 어깨
    [9.8, 42.0, 4.2, 1.90, 3.2],     # 동쪽 능선
    [13.5, 43.0, 3.5, 1.20, 3.0],    # 동쪽 끝자락
    [6.0, 37.8, 3.5, 1.00, 2.2],     # 남쪽 산기슭
])


def hill_height(x, z):
    x, z = np.asarray(x, float), np.asarray(z, float)
    h = np.zeros(np.broadcast(x, z).shape)
    for cx, cz, rx, ry, rz in HILLS:
        h = np.maximum(h, ry * np.sqrt(np.maximum(0, 1 - ((x - cx) / rx) ** 2 - ((z - cz) / rz) ** 2)))
    return h


TOWER_H = 2.36
# 타워 마디: (반지름, 아래, 위)  — 받침, 몸통 3단, 아래 고리, 전망대, 지붕, 안테나 받침, 안테나
TOWER_SEGS = [(0.16, -0.05, 0.12), (0.095, 0.12, 0.70), (0.085, 0.70, 1.15), (0.075, 1.15, 1.42),
              (0.16, 1.42, 1.50), (0.20, 1.50, 1.72), (0.13, 1.72, 1.80), (0.05, 1.80, 2.00),
              (0.022, 2.00, TOWER_H)]
CYL = np.array([[TOWER_X, TOWER_Z, r, TOWER_Y0 + a, TOWER_Y0 + b] for r, a, b in TOWER_SEGS])
N_TOWER_SEG = len(CYL)
# 정상의 다른 것들: 타워 아래 건물, 팔각정(기둥·지붕), 봉수대 다섯 개
PAVILION = (5.75, 40.3)
BEACONS = [(7.05 + 0.11 * i, 40.35) for i in range(5)]
_extra = [[TOWER_X, TOWER_Z, 0.30, TOWER_Y0 - 0.06, TOWER_Y0 + 0.1, 1]]
_ph = float(hill_height(*PAVILION))
_extra += [[PAVILION[0], PAVILION[1], 0.07, _ph - 0.02, _ph + 0.08, 2],
           [PAVILION[0], PAVILION[1], 0.11, _ph + 0.08, _ph + 0.12, 3]]
for bx, bz in BEACONS:
    _bh = float(hill_height(bx, bz))
    _extra.append([bx, bz, 0.035, _bh - 0.02, _bh + 0.07, 4])
CYL = np.concatenate([CYL, np.array(_extra)[:, :5]])
CYL_KIND = np.array([0] * N_TOWER_SEG + [e[5] for e in _extra])
TOWER_LETTER_Y = np.linspace(1.30, 0.42, max(len(TOWER_TEXT), 1))
L_CITY = np.array([-0.5, 0.75, -0.55]); L_CITY /= np.linalg.norm(L_CITY)
B_BUILD, B_DECK, B_PIER, B_HULL, B_CABIN, B_ARCH = 0, 1, 2, 3, 4, 5
K_NONE, K_GROUND, K_BOX, K_CYL, K_ELL = -1, 0, 1, 2, 3
MAIN_Z, BANPO_Z = 6.0, 20.0                                # 한강대교(아치) · 반포대교(분수)
DECK_TOP = 0.40                                            # 한강대교 상판 높이
ARCH_SPANS = [(-3.5, -1.17), (-1.17, 1.17), (1.17, 3.5)]   # 강 위 아치 3개
ARCH_RISE = 1.1
BRIDGES = [(MAIN_Z, BRIDGE_GOLD, T_BRIDGES, DECK_TOP), (BANPO_Z, BRIDGE_LAV, T_BRIDGES + 0.8, 0.32),
           (34.0, BRIDGE_ICE, T_BRIDGES + 1.6, 0.32)]      # (z, 조명색, 켜지는 시각, 상판 높이)
BRIDGE_LX = np.arange(-6.4, 6.41, 0.13)
LEFT_LIT = 0.42

ALLPIX = np.arange(W * H)
COLS_C = (ALLPIX % W) + 0.5 - W / 2
ROWS_C = (ALLPIX // W) + 0.5 - H / 2
ROWS_I = (ALLPIX // W).astype(float)
_LOC = np.full(W * H, -1, np.int64)
_CORNER_SEL = np.array([[(i >> 2) & 1, (i >> 1) & 1, i & 1] for i in range(8)], float)


def tower_radius(yrel):
    r = np.full(np.shape(yrel), 0.022)
    for rr, a, b in TOWER_SEGS:
        r = np.where((yrel >= a) & (yrel < b), rr, r)
    return r


def build_city():
    rs = np.random.default_rng(1225)
    L = []
    pal = [col(c) for c in (BUILDING_1, BUILDING_2, BUILDING_3, BUILDING_4)]

    def add(x0, x1, y1, z0, z1, kind, c, bank, y0=0.0):
        L.append((x0, y0, z0, x1, y1, z1, kind, c, bank, rs.uniform(1, 999)))

    near_bridge = lambda z: any(abs(z - b[0]) < 0.7 for b in BRIDGES)
    for z in np.arange(2.5, 64.0, 1.15):                     # 왼쪽 강변 (강남·반포)
        for k, xc in enumerate((-4.25, -5.3, -6.5, -7.9)):
            if rs.random() < 0.15 or near_bridge(z):
                continue
            w, d = rs.uniform(0.35, 0.75), rs.uniform(0.35, 0.8)
            h = rs.uniform(0.35, 1.0) * (1 + 0.35 * k) * (1 + 0.5 * (z > 18))
            if rs.random() < 0.08:
                h *= 1.6
            xj, zj = xc + rs.uniform(-0.15, 0.15), z + rs.uniform(-0.2, 0.2)
            add(xj - w / 2, xj + w / 2, h, zj - d / 2, zj + d / 2, B_BUILD, pal[rs.integers(4)], -1)
    for z in np.arange(2.5, 35.0, 1.1):                      # 오른쪽 강변 (용산)
        for k, xc in enumerate((4.25, 5.3, 6.5, 7.9)):
            if rs.random() < 0.15 or near_bridge(z) or (xc < 5.5 and 19.5 < z < 26.5):
                continue
            w, d = rs.uniform(0.35, 0.75), rs.uniform(0.35, 0.8)
            h = min(2.1, rs.uniform(0.35, 1.0) * (1 + 0.3 * k) * (0.8 + 0.6 * (8 < z < 28)))
            xj, zj = xc + rs.uniform(-0.15, 0.15), z + rs.uniform(-0.2, 0.2)
            add(xj - w / 2, xj + w / 2, h, zj - d / 2, zj + d / 2, B_BUILD, pal[rs.integers(4)], 1)
    lx, lz = -8.5, 66.0                                      # 멀리 보이는 초고층 타워
    for hw, y0, y1 in ((0.45, 0.0, 2.6), (0.34, 2.6, 4.4), (0.22, 4.4, 5.4)):
        add(lx - hw, lx + hw, y1, lz - hw, lz + hw, B_BUILD, col(BUILDING_3), -1, y0=y0)
    for bz, _, _, top in BRIDGES:                            # 다리 상판 + 교각
        add(-6.5, 6.5, top, bz - 0.14, bz + 0.14, B_DECK, col(BRIDGE_STEEL), 0, y0=top - 0.09)
        piers = [a for a, _ in ARCH_SPANS] + [ARCH_SPANS[-1][1]] if bz == MAIN_Z else np.arange(-3.0, 3.01, 1.0)
        for px in piers:
            hw = 0.12 if bz == MAIN_Z else 0.07
            add(px - hw, px + hw, top - 0.09, bz - 0.12, bz + 0.12, B_PIER, col(BRIDGE_STEEL) * 0.6, 0)
    for xa, xb in ARCH_SPANS:                                # 한강대교 아치 (앞뒤 두 줄)
        xs = np.linspace(xa, xb, 15)
        ys = DECK_TOP + ARCH_RISE * np.sin(np.pi * (xs - xa) / (xb - xa))
        for zr in (MAIN_Z - 0.12, MAIN_Z + 0.12):
            for i in range(14):
                add(xs[i], xs[i + 1], max(ys[i], ys[i + 1]) + 0.03, zr - 0.03, zr + 0.03, B_ARCH,
                    col(BRIDGE_STEEL) * 1.3, 0, y0=min(ys[i], ys[i + 1]) - 0.03)
    arr = np.array([l[:6] for l in L], float)
    out = dict(mn=arr[:, :3], mx=arr[:, 3:6], kind=np.array([l[6] for l in L]),
               c=np.array([l[7] for l in L]), bank=np.array([l[8] for l in L]),
               seed=np.array([l[9] for l in L]))
    tall = np.nonzero((out['kind'] == B_BUILD) & (out['mx'][:, 1] > 1.15))[0]
    out['roof'] = np.stack([(out['mn'][tall, 0] + out['mx'][tall, 0]) / 2, out['mx'][tall, 1] + 0.03,
                            (out['mn'][tall, 2] + out['mx'][tall, 2]) / 2], 1)
    out['roof_ph'] = out['seed'][tall] % 1.0
    return out


CITY = build_city()


def boat_state(t):
    u = clip01((t - T_SEOUL_IN[0]) / 19.0)
    return np.array([1.6, 0.004 * math.sin(t * 2.0), 15.0 - 11.8 * u])


def city_boxes(t):
    """고정된 건물·다리 + 움직이는 유람선."""
    b = boat_state(t)
    parts = [((-0.26, 0.0, -0.65), (0.26, 0.09, 0.65), B_HULL),
             ((-0.18, 0.09, -0.45), (0.18, 0.18, 0.40), B_CABIN),
             ((-0.10, 0.18, -0.20), (0.10, 0.22, 0.10), B_CABIN)]
    mn = np.array([p[0] for p in parts]) + b
    mx = np.array([p[1] for p in parts]) + b
    BX = dict(mn=np.concatenate([CITY['mn'], mn]), mx=np.concatenate([CITY['mx'], mx]),
              kind=np.concatenate([CITY['kind'], [p[2] for p in parts]]),
              c=np.concatenate([CITY['c'], np.tile(col(BOAT_WHITE), (3, 1))]),
              bank=np.concatenate([CITY['bank'], [0, 0, 0]]),
              seed=np.concatenate([CITY['seed'], [11.0, 13.0, 17.0]]))
    BX['corners'] = BX['mn'][:, None, :] + (BX['mx'] - BX['mn'])[:, None, :] * _CORNER_SEL[None]
    return BX


def make_cam(pos, yaw, pitch, f):
    f = f * K
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    return dict(pos=np.asarray(pos, float), yaw=yaw, pitch=pitch, f=f,
                fwd=np.array([sy * cp, sp, cy * cp]), right=np.array([cy, 0.0, -sy]),
                up=np.array([-sy * sp, cp, -cy * sp]))


_CAM_TGT = np.array([TOWER_X, TOWER_Y0 + 0.55, TOWER_Z])
_CAM_A = np.array([0.0, 0.9, 0.0])
_CAM_B = np.array([3.4, 2.8, 23.0])
_CAM_D = np.array([-1.0, 1.1, -1.0])
_dB = _CAM_TGT - _CAM_B
_YAW_B = math.atan2(_dB[0], _dB[2])
_PITCH_B = math.atan2(_dB[1], math.hypot(_dB[0], _dB[2]))


def seoul_camera(t):
    """한강 → 용산 → 남산타워 줌인 → 다시 한강으로."""
    a_end = _CAM_A + [0, 0, 0.06 * (T_CAM_MOVE[0] - T_SEOUL_IN[0])]
    if t < T_CAM_MOVE[0]:
        return make_cam(_CAM_A + [0, 0, 0.06 * (t - T_SEOUL_IN[0])], 0.0, 0.02, 150.0)
    if t < T_CAM_MOVE[1]:
        u = (t - T_CAM_MOVE[0]) / (T_CAM_MOVE[1] - T_CAM_MOVE[0])
        e = smooth(u)
        pos = lerp(a_end, _CAM_B, e) + [0, 0.35 * math.sin(math.pi * e), 0]
        k = smooth(u * 1.25 - 0.1)
        return make_cam(pos, lerp(0.0, _YAW_B, k), lerp(0.02, _PITCH_B, k),
                        lerp(150.0, 260.0, smooth((u - 0.35) / 0.65)))
    if t < T_PULLBACK[0]:
        u = (t - T_CAM_MOVE[1]) / (T_PULLBACK[0] - T_CAM_MOVE[1])
        zk = float(smooth((t - T_ZOOM[0]) / 0.7) - smooth((t - T_ZOOM[1]) / 0.7))
        pos = _CAM_B + _dB * 0.03 * u
        d = _CAM_TGT + [0, 0.31 * zk, 0] - pos
        return make_cam(pos, math.atan2(d[0], d[2]), math.atan2(d[1], math.hypot(d[0], d[2])),
                        260.0 + 30.0 * u + 580.0 * zk / K)
    b_end = _CAM_B + _dB * 0.03
    if t < T_PULLBACK[1]:
        u = (t - T_PULLBACK[0]) / (T_PULLBACK[1] - T_PULLBACK[0])
        e = smooth(u)
        return make_cam(lerp(b_end, _CAM_D, e), lerp(_YAW_B, 0.0, e), lerp(_PITCH_B, 0.03, e),
                        lerp(290.0, 170.0, smooth(u * 1.4)))
    return make_cam(_CAM_D + [0, 0, 0.03 * (t - T_PULLBACK[1])], 0.0, 0.03, 170.0)


def cam_project(P, cam):
    d = np.atleast_2d(P) - cam['pos']
    xc, yc, zc = d @ cam['right'], d @ cam['up'], d @ cam['fwd']
    zs = np.maximum(zc, 0.05)
    return W / 2 + cam['f'] * xc / zs, H / 2 - 0.5 * cam['f'] * yc / zs, zc


def hsh(a, b, c):
    return (np.sin(a * 12.9898 + b * 78.233 + c * 37.719) * 43758.5453) % 1.0


def cast(o, D, pix, basis, f, BX, plane=True):
    """빛줄기 D(칸마다)가 처음 닿는 물체를 찾아요. 반환: 거리, 종류, 번호, 법선."""
    n = len(pix)
    tb = np.full(n, np.inf); kind = np.full(n, K_NONE); pid = np.zeros(n, np.int64)
    nrm = np.zeros((n, 3))
    if plane:                                                 # 땅·강 (y = 0)
        dy = D[:, 1]
        down = dy < -1e-6
        tb[down] = -o[1] / dy[down]
        kind[down] = K_GROUND
        nrm[down] = (0.0, 1.0, 0.0)
    # 상자 (건물·다리·배): 화면에서 차지하는 칸만 검사해요
    right, up, fwd = basis
    d = BX['corners'] - o
    zc, xc, yc = d @ fwd, d @ right, d @ up
    front = zc > 0.05
    anyf, allf = front.any(1), front.all(1)
    zs = np.maximum(zc, 0.05)
    sx = W / 2 + f * xc / zs
    sy = H / 2 - 0.5 * f * yc / zs
    c0 = np.clip(np.floor(sx.min(1)) - 1, 0, W).astype(np.int64)
    c1 = np.clip(np.floor(sx.max(1)) + 2, 0, W).astype(np.int64)
    r0 = np.clip(np.floor(sy.min(1)) - 1, 0, H).astype(np.int64)
    r1 = np.clip(np.floor(sy.max(1)) + 2, 0, H).astype(np.int64)
    part = anyf & ~allf
    c0[part] = 0; c1[part] = W; r0[part] = 0; r1[part] = H
    wb, hb = c1 - c0, r1 - r0
    keep = np.nonzero(anyf & (wb > 0) & (hb > 0))[0]
    if len(keep):
        cnt = wb[keep] * hb[keep]
        rep = np.repeat(np.arange(len(keep)), cnt)
        k = np.arange(int(cnt.sum())) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        wr = wb[keep][rep]
        pp = (r0[keep][rep] + k // wr) * W + c0[keep][rep] + k % wr
        _LOC[pix] = np.arange(n)
        li = _LOC[pp]
        _LOC[pix] = -1
        ok = li >= 0
        bi, li = keep[rep][ok], li[ok]
        Dp = D[li]
        inv = 1.0 / np.where(np.abs(Dp) < 1e-9, 1e-9, Dp)
        t1 = (BX['mn'][bi] - o) * inv
        t2 = (BX['mx'][bi] - o) * inv
        tn = np.minimum(t1, t2)
        tnear, tfar = tn.max(1), np.maximum(t1, t2).min(1)
        hit = (tfar >= tnear) & (tnear > 0.05)
        if hit.any():
            li, bi, tnear, tn, Dp = li[hit], bi[hit], tnear[hit], tn[hit], Dp[hit]
            order = np.lexsort((tnear, li))
            ls = li[order]
            first = np.ones(len(ls), bool)
            first[1:] = ls[1:] != ls[:-1]
            w = order[first]
            w = w[tnear[w] < tb[li[w]]]
            L_ = li[w]
            tb[L_] = tnear[w]; kind[L_] = K_BOX; pid[L_] = bi[w]
            ax = tn[w].argmax(1)
            nn = np.zeros((len(w), 3))
            nn[np.arange(len(w)), ax] = -np.sign(Dp[w, ax])
            nrm[L_] = nn
    # 원기둥 (남산타워)
    ox, oz = o[0] - CYL[:, 0], o[2] - CYL[:, 1]
    Dx, Dy, Dz = D[:, :1], D[:, 1:2], D[:, 2:3]
    a = np.maximum(Dx ** 2 + Dz ** 2, 1e-12)
    b = 2 * (ox * Dx + oz * Dz)
    c = ox ** 2 + oz ** 2 - CYL[:, 2] ** 2
    disc = b * b - 4 * a * c
    ts = (-b - np.sqrt(np.maximum(disc, 0))) / (2 * a)
    ys = o[1] + ts * Dy
    tside = np.where((disc > 0) & (ts > 0.05) & (ys >= CYL[:, 3]) & (ys <= CYL[:, 4]), ts, np.inf)
    tt = (CYL[:, 4] - o[1]) / np.where(np.abs(Dy) < 1e-9, 1e-9, Dy)
    px, pz = ox + tt * Dx, oz + tt * Dz
    tcap = np.where((tt > 0.05) & (px * px + pz * pz <= CYL[:, 2] ** 2), tt, np.inf)
    tc = np.minimum(tside, tcap)
    j = tc.argmin(1)
    tm = tc[np.arange(n), j]
    m = tm < tb
    if m.any():
        tb[m] = tm[m]; kind[m] = K_CYL; pid[m] = j[m]
        hp = o + D[m] * tm[m][:, None]
        capm = tcap[np.nonzero(m)[0], j[m]] <= tside[np.nonzero(m)[0], j[m]]
        rad = np.stack([hp[:, 0] - CYL[j[m], 0], np.zeros(m.sum()), hp[:, 2] - CYL[j[m], 1]], 1)
        nrm[m] = np.where(capm[:, None], np.array([0.0, 1.0, 0.0]), norm_rows(rad))
    # 타원체 여러 개 (남산 능선)
    for ei, (cx, cz, rx, ry, rz) in enumerate(HILLS):
        hc, hr = np.array([cx, 0.0, cz]), np.array([rx, ry, rz])
        oc = (o - hc) / hr
        Dd = D / hr
        a = (Dd * Dd).sum(1)
        b = 2 * (Dd @ oc)
        c = oc @ oc - 1
        disc = b * b - 4 * a * c
        te = (-b - np.sqrt(np.maximum(disc, 0))) / (2 * a)
        m = (disc > 0) & (te > 0.05) & (te < tb)
        if m.any():
            tb[m] = te[m]; kind[m] = K_ELL; pid[m] = ei
            hp = o + D[m] * te[m][:, None]
            nrm[m] = norm_rows((hp - hc) / hr ** 2)
    return tb, kind, pid, nrm


def right_lit(t):
    """용산 창문은 카메라가 다가갈 때 하나씩 켜져요."""
    return 0.18 + 0.6 * smooth((t - T_CAM_MOVE[0]) / (T_CAM_MOVE[1] - T_CAM_MOVE[0] - 1.0))


def tower_state(t, tg):
    front = TOWER_H + 1.0
    if t >= T_TOWER_LIGHT[0]:
        front = TOWER_H * (1 - smooth((t - T_TOWER_LIGHT[0]) / (T_TOWER_LIGHT[1] - T_TOWER_LIGHT[0]))) - 0.06
    glow = clip01((t - T_TOWER_GLOW) / 0.6) * (0.8 + 0.2 * math.sin(tg * 2.4))
    return front, float(glow)


def city_shade(hp, kind, pid, nrm, tb, t, tg, f, BX):
    n = len(tb)
    colr = np.zeros((n, 3)); lum = np.zeros(n)
    wat = np.zeros(n, bool); wv = np.zeros(n)
    diff = clip01(nrm @ L_CITY)
    m = kind == K_GROUND                                     # 한강 · 강변
    if m.any():
        x, z = hp[m, 0], hp[m, 2]
        river = np.abs(x) < RIVER_HALF
        w = 0.5 + 0.5 * np.sin(x * 4.0 + tg * 1.3 + 2 * np.sin(z * 0.9 + tg * 0.6)) * np.sin(z * 7.0 - tg * 2.2 + x * 1.3)
        base = lerp(col(HAN_TEAL), col(HAN_BLUE), clip01(z / 18.0)[:, None])
        base = lerp(base, col(HAN_PURPLE), (0.5 + 0.5 * np.sin(x * 0.7 + z * 0.18 + tg * 0.2))[:, None] * 0.55)
        wc = base * (0.3 + 0.55 * w)[:, None]
        wl = 0.1 + 0.2 * w
        ax = np.abs(x) - RIVER_HALF
        prom = (ax >= 0) & (ax < 0.16)
        lamp = (prom & ((z % 0.45) < 0.14)) | (~prom & (((x % 1.15) < 0.08) | ((z % 1.15) < 0.08))
                                                & (((x + z) % 0.24) < 0.1))
        lc = np.tile(col(LAND_SNOW) * 0.5, (len(x), 1)); ll = np.full(len(x), 0.07)
        lc[prom] = col(LAND_SNOW) * 0.7; ll[prom] = 0.15
        lc[lamp] = col(STREET_LAMP); ll[lamp] = 0.5
        colr[m] = np.where(river[:, None], wc, lc)
        lum[m] = np.where(river, wl, ll)
        ii = np.nonzero(m)[0][river]
        wat[ii] = True
        wv[ii] = w[river]
    m = kind == K_BOX                                        # 건물 · 다리 · 유람선
    if m.any():
        b = pid[m]; bk = BX['kind'][b]; p = hp[m]; nn = nrm[m]; dd = diff[m]
        top = nn[:, 1] > 0.5
        u = np.where(np.abs(nn[:, 0]) > 0.5, p[:, 2], p[:, 0])
        cab = bk == B_CABIN
        FH = np.where(cab, 0.045, 0.055); WW = np.where(cab, 0.07, 0.05)
        fl, cl = np.floor(p[:, 1] / FH), np.floor(u / WW)
        sd = BX['seed'][b]
        h1, h2 = hsh(sd, fl, cl), hsh(sd + 3.7, fl, cl)
        fy, fu = (p[:, 1] / FH) % 1.0, (u / WW) % 1.0
        coarse = (tb[m] / f) > WW * 0.7
        inwin = ((fy > 0.25) & (fy < 0.8) & (fu > 0.2) & (fu < 0.75)) | coarse
        lf = np.where(BX['bank'][b] > 0, right_lit(t), LEFT_LIT)
        lf = np.where(cab, 0.9, lf)
        lit = inwin & (h1 < lf) & ~top & ((bk == B_BUILD) | cab)
        wcol = np.where((h2 < 0.55)[:, None], col(WIN_YELLOW),
                        np.where((h2 < 0.85)[:, None], col(WIN_WHITE), col(WIN_PINK)))
        wcol[cab] = col(BOAT_LIGHT)
        c = BX['c'][b] * (0.3 + 0.7 * dd)[:, None]
        l = 0.05 + 0.2 * dd
        hull = bk == B_HULL
        c[hull] = col(BOAT_WHITE) * (0.45 + 0.55 * dd[hull])[:, None]; l[hull] = 0.28 + 0.35 * dd[hull]
        deck = bk == B_DECK
        l[deck] = 0.14 + 0.3 * dd[deck]
        arch = bk == B_ARCH
        l[arch] = 0.22 + 0.3 * dd[arch]
        roof = top & (bk == B_BUILD)
        c[roof] = col(ROOF_SNOW) * (0.35 + 0.4 * dd[roof])[:, None]; l[roof] = 0.16 + 0.15 * dd[roof]
        c = np.where(lit[:, None], wcol * (0.75 + 0.25 * h2)[:, None], c)
        l = np.where(lit, (0.58 + 0.32 * h2) * np.where(coarse, 0.7, 1.0), l)
        colr[m] = c; lum[m] = l
    ckind = np.where(kind == K_CYL, CYL_KIND[np.clip(pid, 0, len(CYL_KIND) - 1)], -1)
    m = ckind > 0                                            # 타워 아래 건물 · 팔각정 · 봉수대
    if m.any():
        ck = CYL_KIND[pid[m]]; p = hp[m]; dd = diff[m]
        c = np.tile(col(ROOF_SNOW), (len(p), 1)) * (0.4 + 0.6 * dd)[:, None]
        l = 0.2 + 0.3 * dd
        ang = np.arctan2(p[:, 2] - CYL[pid[m], 1], p[:, 0] - CYL[pid[m], 0])
        win = (ck == 1) & (hsh(np.floor(ang * 9), np.floor(p[:, 1] * 40), 5.0) < 0.6) & (((p[:, 1] * 40) % 1) > 0.3)
        c[win] = col(WIN_YELLOW); l[win] = 0.7
        c[ck == 3] = col(HAN_TEAL) * 0.6; l[ck == 3] = 0.25        # 팔각정 단청 지붕
        c[ck == 2] = col(GIFT_RED) * 0.8; l[ck == 2] = 0.3         # 붉은 기둥
        colr[m] = c; lum[m] = l
    m = ckind == 0                                           # 남산타워
    if m.any():
        p = hp[m]; yr = p[:, 1] - TOWER_Y0; dd = diff[m]
        front, glow = tower_state(t, tg)
        c = np.tile(col(TOWER_WHITE), (len(p), 1)) * (0.5 + 0.5 * dd)[:, None]
        l = 0.32 + 0.4 * dd
        pink = yr >= front
        if pink.any():
            stripe = 0.5 + 0.5 * np.sin(yr * 24 - tg * 3.0)
            pc = lerp(col(TOWER_PINK), col(TOWER_LAV), stripe[:, None]) * (0.75 + 0.25 * dd)[:, None]
            c[pink] = pc[pink]; l[pink] = 0.72 + 0.2 * dd[pink]
            edge = np.abs(yr - front) < 0.06
            c[edge] = 1.0; l[edge] = 1.05
        if glow > 0:
            c = c * (1 - 0.3 * glow) + 0.38 * glow
            l = l + 0.22 * glow
        colr[m] = c; lum[m] = l
    m = kind == K_ELL                                        # 남산 숲 (소나무 숲 덩어리 + 눈 덮인 나무 끝)
    if m.any():
        p = hp[m]; nn = nrm[m]
        x, y, z = p[:, 0], p[:, 1], p[:, 2]
        canopy = (0.5 + 0.3 * np.sin(x * 9 + z * 7) * np.sin(y * 11 + x * 3)
                  + 0.2 * np.sin(x * 23 - z * 19 + y * 17))
        bump = np.stack([np.cos(x * 9 + z * 7), np.zeros(len(x)), np.cos(z * 13 - x * 5)], 1) * 0.35
        dd = clip01(norm_rows(nn + bump) @ L_CITY)
        hs = hsh(np.floor(x * 18), np.floor(y * 24), np.floor(z * 18))
        c = lerp(col(HILL_DARK), col(HILL_PINE), clip01(canopy)[:, None]) * (0.35 + 0.65 * dd)[:, None]
        l = 0.05 + 0.2 * dd * (0.6 + 0.6 * canopy)
        sn = (canopy > 0.72) & (nn[:, 1] > 0.45) | (hs > 0.86)
        c[sn] = col(ROOF_SNOW) * (0.35 + 0.3 * dd[sn])[:, None]; l[sn] = 0.15 + 0.12 * dd[sn]
        colr[m] = c; lum[m] = l
    return colr, lum, wat, wv


def wglow(fr, cam, P, rgb, tg, halo=0.6, refl=0.4):
    """3D 빛 한 점 + 한강에 비친 빛 (물결 따라 흔들려요)."""
    P = np.atleast_2d(np.asarray(P, float))
    if len(P) == 0:
        return
    rgb = np.broadcast_to(np.asarray(rgb, float), (len(P), 3))
    sx, sy, zc = cam_project(P, cam)
    ok = zc > 0.15
    if ok.any():
        fr.add_glow(sx[ok], sy[ok], rgb[ok], z=zc[ok], halo=halo)
    if refl > 0:
        sx, sy, zc = cam_project(P * [1, -1, 1], cam)
        sx = sx + 0.8 * np.sin(sy * 1.2 + tg * 2.6 + P[:, 0] * 2)
        c, r = np.floor(sx).astype(np.int64), np.floor(sy).astype(np.int64)
        ok = (zc > 0.15) & (c >= 0) & (c < W) & (r >= 0) & (r < H)
        ii = np.nonzero(ok)[0]
        ok[ii] = fr.water[r[ii] * W + c[ii]]
        if ok.any():
            fr.add_glow(sx[ok], sy[ok], rgb[ok] * refl, halo=0.25)
            fr.add_glow(sx[ok] + 0.4 * np.sin(tg * 3 + sy[ok]), sy[ok] + 1.0, rgb[ok] * refl * 0.5, halo=0)


def tower_front_points(cam, heights, out=0.012):
    """타워 몸통에서 카메라 쪽을 보는 면의 점."""
    dvec = np.array([cam['pos'][0] - TOWER_X, 0.0, cam['pos'][2] - TOWER_Z])
    dvec /= max(np.linalg.norm(dvec), 1e-9)
    heights = np.asarray(heights, float)
    r = tower_radius(heights) + out
    return np.stack([TOWER_X + dvec[0] * r, TOWER_Y0 + heights, TOWER_Z + dvec[2] * r], 1)


# ── 3x5 점 글꼴 (드론 쇼 글자) ──
FONT = {k: v.replace(' ', '') for k, v in {
    'A': ".#. #.# ### #.# #.#", 'B': "##. #.# ##. #.# ##.", 'C': ".## #.. #.. #.. .##",
    'D': "##. #.# #.# #.# ##.", 'E': "### #.. ##. #.. ###", 'F': "### #.. ##. #.. #..",
    'G': ".## #.. #.# #.# .##", 'H': "#.# #.# ### #.# #.#", 'I': "### .#. .#. .#. ###",
    'J': "### ..# ..# #.# .#.", 'K': "#.# #.# ##. #.# #.#", 'L': "#.. #.. #.. #.. ###",
    'M': "#.# ### #.# #.# #.#", 'N': "##. #.# #.# #.# #.#", 'O': ".#. #.# #.# #.# .#.",
    'P': "##. #.# ##. #.. #..", 'Q': ".#. #.# #.# ##. .##", 'R': "##. #.# ##. #.# #.#",
    'S': ".## #.. .#. ..# ##.", 'T': "### .#. .#. .#. .#.", 'U': "#.# #.# #.# #.# .#.",
    'V': "#.# #.# #.# .#. .#.", 'W': "#.# #.# #.# ### #.#", 'X': "#.# #.# .#. #.# #.#",
    'Y': "#.# #.# .#. .#. .#.", 'Z': "### ..# .#. #.. ###",
}.items()}
HEART_GLYPH = ["##.##", "#####", ".###.", "..#.."]


def text_dots(text, du=0.2, dv=0.3):
    pts, gid = [], []
    x = 0
    for gi, ch in enumerate(text):
        if ch == ' ':
            x += 1
            continue
        if ch == '♥':
            for r, row in enumerate(HEART_GLYPH):
                for c, v in enumerate(row):
                    if v == '#':
                        pts.append((x + c, r + 0.5)); gid.append(gi)
            x += 6
            continue
        g = FONT.get(ch.upper(), FONT['O'])
        for r in range(5):
            for c in range(3):
                if g[r * 3 + c] == '#':
                    pts.append((x + c, r)); gid.append(gi)
        x += 4
    P = np.array(pts, float)
    width = x - 1
    uv = np.stack([(P[:, 0] - width / 2) * du, (2 - P[:, 1]) * dv], 1)
    return uv, np.array(gid), [text[g] for g in gid]


def build_drones():
    uv_text, gid, gch = text_dots(DRONE_TEXT)
    n = len(uv_text)
    rs = np.random.default_rng(77)
    # 크리스마스트리 모양
    tree = [(0.0, 1.5)]
    j = 1
    while len(tree) + (j + 1) + 3 <= n:
        w = 0.26 * j
        for u in np.linspace(-w / 2, w / 2, j + 1):
            tree.append((u, 1.5 - j * 0.3))
        j += 1
    trunk_y = 1.5 - j * 0.3
    for k in range(3):
        if len(tree) < n:
            tree.append((0.0, trunk_y - k * 0.28))
    extra = 0
    while len(tree) < n:
        extra += 1
        tree.append(((-1) ** extra * 0.3 * ((extra + 1) // 2), 1.55))
    tree = np.array(tree[:n])
    tcol = np.where((np.arange(n) % 2 == 0)[:, None], col(DRONE_PINK), col(DRONE_LAV))
    tcol[0] = col(DRONE_GOLD)
    tcol[tree[:, 1] < trunk_y + 0.05] = col(DRONE_GOLD)
    tcol[tree[:, 1] > 1.52] = col(DRONE_GOLD)
    # 하트 모양
    tt = np.linspace(0, 2 * math.pi, n, endpoint=False)
    heart = np.stack([16 * np.sin(tt) ** 3 / 16 * 1.3,
                      (13 * np.cos(tt) - 5 * np.cos(2 * tt) - 2 * np.cos(3 * tt) - np.cos(4 * tt)) / 16 * 1.25], 1)
    hcol = np.where((np.arange(n) % 2 == 0)[:, None], col(DRONE_PINK), col(HOT_PINK))
    # 글자 (글자마다 금색·분홍 번갈아, ♥ 는 분홍)
    xcol = np.array([col(DRONE_PINK) if ch == '♥' else (col(DRONE_GOLD) if g % 2 == 0 else col(DRONE_PINK))
                     for g, ch in zip(gid, gch)])
    scatter = rs.normal(0, 1, (n, 2)) * [1.4, 0.9]
    scol = np.array([col(DRONE_PINK), col(DRONE_LAV), col(DRONE_GOLD)])[np.arange(n) % 3]
    barge = np.stack([(np.arange(n) % 10 - 4.5) * 0.18, np.zeros(n)], 1)

    def ordered(uv, cc):           # 왼쪽부터 순서대로 짝지어서 드론이 서로 엉키지 않게
        o = np.argsort(uv[:, 0] + 0.05 * uv[:, 1], kind='stable')
        return uv[o], cc[o]
    forms = {}
    ds = 1.0 if LAYOUT == 'pc' else 1.3          # 휴대폰은 화면이 좁아서 드론 간격을 넓혀요
    for name, (uv, cc) in dict(scatter=(scatter, scol), tree=(tree, tcol), heart=(heart, hcol),
                                text=(uv_text, xcol)).items():
        forms[name] = ordered(uv * ds, cc)
    return dict(n=n, forms=forms, barge=barge, bz=(np.arange(n) // 10 - 2) * 0.2,
                delay=np.arange(n) / n * 0.5, ph=rs.uniform(0, 6.28, n))


DRONES = build_drones()
DRONE_C = np.array([-1.9, 3.3 if LAYOUT == 'pc' else 3.9, 18.0])       # 드론 쇼가 펼쳐지는 하늘 (한강 위)


def drone_positions(t, tg):
    D_ = DRONES
    n = D_['n']
    P = np.stack([DRONE_C[0] + D_['barge'][:, 0], np.full(n, DECK_TOP + 0.03), MAIN_Z + 0.25 * D_['bz']], 1)
    C = np.tile(col(DRONE_LAV), (n, 1))
    for ts, name in DRONE_STEPS:
        uv, cc = D_['forms'][name]
        u = smooth((t - ts - D_['delay']) / DRONE_MOVE_SEC)
        tgt = np.stack([DRONE_C[0] + uv[:, 0], DRONE_C[1] + uv[:, 1], np.full(n, DRONE_C[2])], 1)
        P = lerp(P, tgt, u[:, None])
        P[:, 2] -= 0.6 * np.sin(math.pi * u)                 # 이동할 때 살짝 앞으로 나왔다 들어가요
        C = lerp(C, cc, u[:, None])
    P[:, 1] += 0.03 * np.sin(tg * 2.3 + D_['ph'])
    on = clip01((t - DRONE_STEPS[0][0] - D_['delay']) / 0.4)
    blink = np.where(t - DRONE_STEPS[0][0] < 1.2, 0.6 + 0.4 * (np.sin(tg * 14 + D_['ph']) > 0), 1.0)
    return P, C * (on * blink)[:, None]


# 서울 하늘에 내리는 눈 (카메라 주변에 계속 내려요)
_rsn = np.random.default_rng(31)
SEOUL_SNOW = dict(oz=_rsn.uniform(0.8, 14.0, 260), ox=_rsn.uniform(-1, 1, 260), oy=_rsn.uniform(0, 1, 260),
                  v=_rsn.uniform(0.25, 0.5, 260), sw=_rsn.uniform(0.7, 1.8, 260), sp=_rsn.uniform(0, 6.28, 260),
                  heart=_rsn.random(260) < SNOW_HEART_CHANCE)
_rob = np.random.default_rng(41)
ORBIT = dict(a0=_rob.uniform(0, 6.28, 44), r=_rob.uniform(0.3, 0.7, 44), h=_rob.uniform(0.1, 2.3, 44),
             ch=np.array(['*', '+', '.', '*', '♥', '+'])[np.arange(44) % 6],
             c=np.array([col(SNOWFLAKE), col(NEON_GOLD), col(STAR_PINK)])[np.arange(44) % 3])
TOWER_FW = build_fireworks([(tt, 0, 0, 'heart', c, c) for tt, c in zip(T_TOWER_HEARTS, (NEON_PINK, TOWER_LAV))], 300)
for _f in TOWER_FW:
    _f['R'] = 13.0


BRIDGE_FW = build_fireworks(BRIDGE_FIREWORKS, 500)
for _f, _spec in zip(BRIDGE_FW, BRIDGE_FIREWORKS):
    _f['wx'], _f['wy'] = _spec[1], _spec[2]
    _f['dz'] = (np.random.default_rng(int(_spec[0] * 10)).random(len(_f['sp'])) - 0.5) * 0.5
_WF_X = np.arange(-3.4, 3.41, 0.11)


def draw_bridge_show(fr, cam, t, tg):
    """한강대교: 아치 조명, 행거, 불꽃 폭포, 다리에서 쏘아 올리는 불꽃 (강물에 비쳐요)."""
    zf = MAIN_Z - 0.16
    prog = float(clip01((t - T_ARCH_LIGHTS) / 1.6))
    if prog > 0:
        u = np.linspace(0, 1, 34)
        Ps, Cs = [], []
        _n34 = 34
        show = t >= DRONE_STEPS[0][0] or any(a <= t < b for a, b in WATERFALLS)
        for k, (xa, xb) in enumerate(ARCH_SPANS):
            x = xa + (xb - xa) * u
            y = DECK_TOP + ARCH_RISE * np.sin(np.pi * u) + 0.035
            on = (1 - np.abs(2 * u - 1)) <= prog                 # 교각에서 꼭대기로 불이 올라가요
            alt = np.where((np.arange(34) % 2 == 0)[:, None], col(BRIDGE_GOLD), col(WIN_WHITE))
            if show:                                             # 쇼가 시작되면 분홍·라벤더 물결
                alt = lerp(col(TOWER_PINK), col(TOWER_LAV), (0.5 + 0.5 * np.sin(x * 2.5 - tg * 2.5))[:, None])
            inten = 0.85 + 0.25 * np.sin(u * 20 - tg * 3 + k)
            Ps.append(np.stack([x, y, np.full(34, zf)], 1)[on]); Cs.append((alt * inten[:, None])[on])
            Ps.append(np.stack([x, y - 0.07, np.full(34, zf)], 1)[on]); Cs.append((alt * (0.45 * inten)[:, None])[on])
            hx = np.arange(xa + 0.18, xb - 0.1, 0.18)            # 아치와 상판을 잇는 행거
            hy = DECK_TOP + ARCH_RISE * np.sin(np.pi * (hx - xa) / (xb - xa))
            for s_ in np.linspace(0.15, 0.85, 4):
                Ps.append(np.stack([hx, DECK_TOP + (hy - DECK_TOP) * s_, np.full(len(hx), zf)], 1))
                Cs.append(np.tile(col(BRIDGE_ICE) * 0.08 * prog, (len(hx), 1)))
        wglow(fr, cam, np.concatenate(Ps), np.concatenate(Cs), tg, halo=0.4, refl=0.4)
    wk = 0.0                                                     # 불꽃 폭포
    for a, b in WATERFALLS:
        if a <= t < b:
            wk = float(clip01((t - a) / 0.8) * clip01((b - t) / 0.8))
            spread = float(clip01((t - a) / 1.2))
    if wk > 0:
        xs = _WF_X[np.abs(_WF_X) <= 3.4 * spread + 0.05]
        Ps, Cs = [], []
        for j in range(4):
            hj = hsh(xs * 7.0, j, 1.0)
            age = (tg * 0.9 + hj) % 1.0
            y = DECK_TOP - 0.1 - 1.1 * age ** 2
            keep = y > 0.01
            x = xs + 0.03 * np.sin(hj * 40 + tg * 3)
            flick = 0.55 + 0.45 * (np.sin(hj * 60 + tg * 25) > 0)
            Ps.append(np.stack([x, y, np.full(len(xs), zf - 0.02)], 1)[keep])
            Cs.append((lerp(col(FLASH_WHITE), col(FW_GOLD), age[:, None]) * (wk * flick * (1 - 0.6 * age))[:, None])[keep])
        Ps.append(np.stack([xs, np.full(len(xs), DECK_TOP - 0.1), np.full(len(xs), zf - 0.02)], 1))
        Cs.append(np.tile(col(FLASH_WHITE) * 0.5 * wk, (len(xs), 1)))
        wglow(fr, cam, np.concatenate(Ps), np.concatenate(Cs), tg, halo=0.35, refl=0.45)
    for f in BRIDGE_FW:                                          # 다리에서 쏘아 올리는 불꽃
        cx, cy = f['wx'], f['wy']
        lu = (t - (f['t'] - 0.8)) / 0.8
        if 0 < lu < 1:
            yh = lerp(DECK_TOP + 0.05, cy, ease_out_cubic(lu))
            k = np.arange(7)
            P = np.stack([np.full(7, cx), yh - k * 0.06, np.full(7, zf)], 1)
            wglow(fr, cam, P, col(FW_GOLD) * (0.7 * (1 - k / 7) ** 1.5)[:, None], tg, halo=0.3, refl=0.3)
        bu = (t - f['t']) / f['dur']
        if not (0 < bu < 1):
            continue
        if bu < 0.12:
            wglow(fr, cam, [[cx, cy, zf]], col(FLASH_WHITE) * (1 - bu / 0.12) * 1.6, tg, halo=2.2, refl=0.4)
        R_, gr = f['R'] * 0.05, f['g'] * 0.06
        tails = 6 if f['willow'] else 4
        Ps, Cs = [], []
        for j in range(tails):
            b = bu - j * 0.03
            if b <= 0:
                break
            e = ease_out_cubic(min(1.0, b * 1.5))
            P = np.stack([cx + f['d'][:, 0] * f['sp'] * R_ * e, cy + f['d'][:, 1] * f['sp'] * R_ * e - gr * b * b,
                          zf + f['dz'] * e], 1)
            inten = (1 - b) ** 1.2 * (1 - j / tails) ** 1.3 * 1.05
            if bu > 0.55:
                inten = inten * (0.35 + 0.65 * (np.sin(f['tw'] * t) > 0))
            Ps.append(P); Cs.append(f['c'] * np.broadcast_to(inten, (len(P),))[:, None])
        if Ps:
            wglow(fr, cam, np.concatenate(Ps), np.concatenate(Cs), tg, halo=0.45, refl=0.35)


# 남산 산책로 (지그재그로 정상까지), 한양도성 성곽, 케이블카, 사랑의 자물쇠
_u = np.linspace(0, 1, 70)
_tx = 6.3 + 1.7 * np.sin(_u * 9) * (1 - _u * 0.7)
_tz = lerp(37.2, 39.4, _u)
TRAIL = np.stack([_tx, hill_height(_tx, _tz) + 0.03, _tz - 0.05], 1)
_wx = np.linspace(1.2, 15.5, 260)
_wz = 40.1 + 0.4 * np.sin(_wx * 0.8)
FORT = np.stack([_wx, hill_height(_wx, _wz) + 0.035, _wz], 1)
FORT = FORT[FORT[:, 1] > 0.08]
CABLE_LO = np.array([2.4, float(hill_height(2.4, 38.0)) + 0.08, 38.0])
CABLE_HI = np.array([5.3, float(hill_height(5.3, 39.6)) + 0.12, 39.6])
_lock_rs = np.random.default_rng(14)
LOCK_A = np.linspace(0, 2 * math.pi, 120, endpoint=False)
LOCK_C = np.array([col(c) for c in LOVE_LOCKS])[_lock_rs.integers(0, len(LOVE_LOCKS), 120)]
LOCK_PH = _lock_rs.uniform(0, 6.28, 120)


def cable_point(u):
    u = np.asarray(u, float)[..., None]
    return CABLE_LO + (CABLE_HI - CABLE_LO) * u + np.array([0, 0.12, 0]) * np.sin(np.pi * u)


def draw_namsan(fr, cam, t, tg):
    wglow(fr, cam, TRAIL, col(STREET_LAMP) * 0.32, tg, halo=0.3, refl=0.2)                  # 산책로 가로등
    wglow(fr, cam, FORT, col(FORTRESS) * (0.2 + 0.04 * np.sin(FORT[:, 0] * 6 - tg * 2))[:, None],
          tg, halo=0.2, refl=0.15)                                                             # 한양도성 성곽 조명
    s_ = np.linspace(0, 1, 50)                                                                 # 케이블카 줄
    for dz in (-0.04, 0.04):
        wglow(fr, cam, cable_point(s_) + [0, 0, dz], col(BRIDGE_ICE) * 0.09, tg, halo=0, refl=0)
    wglow(fr, cam, np.array([CABLE_LO, CABLE_HI]) + [0, 0.03, 0], col(WIN_YELLOW) * 0.6, tg, halo=0.6, refl=0.2)
    uc = (tg * 0.06) % 2.0
    uc = uc if uc < 1 else 2 - uc
    cab = cable_point(np.array([uc, 1 - uc])) + [[0, -0.05, -0.04], [0, -0.05, 0.04]]
    wglow(fr, cam, cab, np.array([col(BOAT_LIGHT), col(WIN_PINK)]) * 0.8, tg, halo=0.6, refl=0.2)  # 오르내리는 케이블카
    ph = float(hill_height(*PAVILION))                                                         # 팔각정 처마 등
    wglow(fr, cam, [[PAVILION[0], ph + 0.09, PAVILION[1] - 0.11]], col(WIN_YELLOW) * 0.5, tg, halo=0.6, refl=0.2)
    for i, (bx, bz) in enumerate(BEACONS):                                                     # 봉수대 다섯 불빛
        fl = 0.45 + 0.35 * math.sin(tg * 9 + i * 1.7) * math.sin(tg * 5.3 + i)
        wglow(fr, cam, [[bx, float(hill_height(bx, bz)) + 0.1, bz]], col(BEACON_FIRE) * fl, tg, halo=0.5, refl=0.2)
    lp = np.stack([TOWER_X + 0.42 * np.cos(LOCK_A), np.full(120, TOWER_Y0 + 0.13),               # 사랑의 자물쇠
                   TOWER_Z + 0.42 * np.sin(LOCK_A)], 1)
    wglow(fr, cam, lp, LOCK_C * (0.25 + 0.2 * np.sin(tg * 3 + LOCK_PH))[:, None], tg, halo=0, refl=0)


def draw_caption(fr, text, t0, t1, t, tg):
    if not (t0 <= t < t1):
        return
    n = len(text)
    x0 = (W - n) // 2
    a = float(clip01((t1 - t) / 0.6))
    for k, ch in enumerate(text):
        tk = t0 + k * 0.035
        if t < tk:
            continue
        if ch == ' ':
            fr.overlay([x0 + k + 0.5], [H - 0.5], ' ', np.zeros(3))
            continue
        pop = math.exp(-(t - tk) / 0.2)
        c = lerp(col(ENVELOPE_LINE), col(MSG_PINK), 0.5 + 0.5 * math.sin(tg * 2 - k * 0.3)) * 0.8 * a + pop * 0.5
        fr.overlay([x0 + k + 0.5], [H - 0.5], ch, clip01(c))


def render_seoul(t, tg):
    cam = seoul_camera(t)
    f = cam['f']
    fr = Frame()
    bg_col, bg_lum, bg_ch = background(tg, star_k=0.45, planet_k=0.0, aurora_k=0.22)
    hr = H / 2 + 0.5 * f * math.tan(cam['pitch'])            # 지평선 위 도시 불빛 안개
    dh = hr - (ROWS_I + 0.5)
    haze = np.where(dh > 0, np.exp(-np.maximum(dh, 0) / 5.0), 0.0)
    bg_col = bg_col + col(CITY_HAZE)[None] * (haze * 0.35)[:, None]
    bg_lum = bg_lum + 0.07 * haze

    # ── 광선 추적: 건물·다리·배·타워·남산·한강 ──
    BX = city_boxes(t)
    o = cam['pos']
    D = cam['fwd'] + cam['right'] * (COLS_C / f)[:, None] + cam['up'] * (-ROWS_C / (0.5 * f))[:, None]
    tb, kind, pid, nrm = cast(o, D, ALLPIX, (cam['right'], cam['up'], cam['fwd']), f, BX)
    idx = np.nonzero(kind >= 0)[0]
    hp = o + D[idx] * tb[idx][:, None]
    c, l, wat, wv = city_shade(hp, kind[idx], pid[idx], nrm[idx], tb[idx], t, tg, f, BX)
    wi = idx[wat]
    if len(wi):                                              # 한강에 비친 도시 (거꾸로 비친 빛줄기)
        ww = wv[wat]
        Dm = D[wi] * [1, -1, 1]
        Dm[:, 0] += 0.006 * np.sin(ROWS_I[wi] * 1.3 + tg * 2.5 + hp[wat, 0] * 3)
        om = o * [1, -1, 1]
        rtb, rk, rp, rn = cast(om, Dm, wi, (cam['right'], cam['up'] * [1, -1, 1], cam['fwd'] * [1, -1, 1]),
                               f, BX, plane=False)
        rc = np.tile(col(CITY_HAZE) * 0.2, (len(wi), 1))
        rl = np.full(len(wi), 0.03)
        ri = np.nonzero(rk >= 0)[0]
        if len(ri):
            rhp = om + Dm[ri] * rtb[ri][:, None]
            cc, ll, _, _ = city_shade(rhp, rk[ri], rp[ri], rn[ri], rtb[ri], t, tg, f, BX)
            rc[ri] = cc; rl[ri] = ll
        fres = 0.45 + 0.35 * clip01(hp[wat, 2] / 14.0)
        c[wat] += rc * (fres * (0.55 + 0.45 * ww))[:, None]
        l[wat] += rl * fres * 0.85
        strong = rl * fres > 0.22
        wch = np.where(ww > 0.68, '~', np.where(ww > 0.42, '-', np.where(ww > 0.2, '.', ' ')))
        wch = np.where(strong, np.where(ww > 0.5, '~', '='), wch)
        fr.schar[wi] = wch
        fr.water[wi] = True
    fr.zbuf[idx] = tb[idx]
    fr.scol[idx] = c
    fr.slum[idx] = l
    fr.solid[idx] = True

    # ── 빛나는 것들 ──
    shooting_star(fr, tg)
    for k, (bz, bc, ton, top) in enumerate(BRIDGES):         # 다리 조명이 차례로 켜져요
        prog = float(clip01((t - ton) / 2.2))
        if prog <= 0:
            continue
        fx = (BRIDGE_LX + 6.5) / 13.0
        on = fx <= prog
        inten = 0.55 + 0.35 * np.sin(BRIDGE_LX * 3 - tg * 4 + k) + 1.2 * np.exp(-((fx - prog) / 0.03) ** 2)
        P = np.stack([BRIDGE_LX, np.full(len(BRIDGE_LX), top + 0.015), np.full(len(BRIDGE_LX), bz - 0.15)], 1)
        wglow(fr, cam, P[on], col(bc) * (0.75 * inten[on])[:, None], tg, halo=0.45, refl=0.5)
    fu = float(clip01((t - T_FOUNTAIN) / 0.8))               # 반포대교 달빛무지개분수
    if fu > 0:
        X, S = np.meshgrid(np.arange(-3.3, 3.31, 0.3), np.linspace(0, 1, 12))
        X, S = X.ravel(), S.ravel()
        P = np.stack([X, 0.27 + 0.18 * S - 0.45 * S * S, BANPO_Z - 0.15 - 0.75 * S], 1)
        inten = fu * 0.42 * (1 - 0.5 * S) * (0.6 + 0.4 * np.sin(S * 12 - tg * 10 + X * 3))
        wglow(fr, cam, P, rainbow(X * 0.15 + S * 0.3 - tg * 0.25) * inten[:, None], tg, halo=0.35, refl=0.3)
    draw_bridge_show(fr, cam, t, tg)                         # 한강대교 아치 조명 · 불꽃 폭포 · 불꽃
    blink = ((tg * 0.7 + CITY['roof_ph']) % 1.0) < 0.45      # 옥상 빨간 경고등
    if blink.any():
        wglow(fr, cam, CITY['roof'][blink], col(TOWER_RED) * 0.7, tg, halo=0.5, refl=0.35)
    b = boat_state(t)                                        # 유람선 불빛과 물보라
    wglow(fr, cam, np.array([b + [0, 0.26, -0.05], b + [-0.27, 0.06, -0.6], b + [0.27, 0.06, -0.6]]),
          np.array([col(SNOWFLAKE), col(FW_RED), col(BULB_GREEN)]) * 0.8, tg, halo=0.5, refl=0.45)
    s = np.linspace(0, 1, 24)
    wake = np.concatenate([np.stack([b[0] + sg * (0.2 + 0.5 * s), np.full(24, 0.01), b[2] + 0.7 + 1.8 * s], 1)
                           for sg in (-1, 1)])
    wglow(fr, cam, wake, col(SNOW_GLINT) * (0.35 * (1 - np.tile(s, 2)) * (0.6 + 0.4 * np.sin(np.tile(s, 2) * 20 - tg * 6)))[:, None],
          tg, halo=0.3, refl=0)
    draw_namsan(fr, cam, t, tg)
    # 남산타워 조명
    front, glow = tower_state(t, tg)
    hs = np.arange(0.05, TOWER_H, 0.12)
    tp = tower_front_points(cam, hs)
    tc = np.where((hs >= front)[:, None], lerp(col(TOWER_PINK), col(TOWER_LAV), (0.5 + 0.5 * np.sin(hs * 6))[:, None]) * 0.32,
                  col(TOWER_WHITE) * 0.16) * (1 + 1.2 * glow)
    wglow(fr, cam, tp, tc, tg, halo=0.5 + 0.8 * glow, refl=0.3)
    if (tg % 1.4) < 0.7:
        wglow(fr, cam, [[TOWER_X, TOWER_Y0 + TOWER_H + 0.02, TOWER_Z]], col(TOWER_RED) * 0.9, tg, halo=0.8, refl=0.3)
    top_sx, top_sy, top_z = cam_project([[TOWER_X, TOWER_Y0 + TOWER_H, TOWER_Z]], cam)
    for fw in TOWER_FW:                                      # 꼭대기 하트 불꽃
        fw_burst(fr, fw, t, top_sx[0], top_sy[0] - 3, z=FAR)
    if t >= DRONE_STEPS[0][0]:                               # 드론 쇼
        P, C = drone_positions(t, tg)
        wglow(fr, cam, P, C * 0.95, tg, halo=0.3, refl=0.45)
    if 0.3 < (tg * 1.7) % 1.0 < 0.34 and fr.water.any():     # 강물 위 반짝임
        wc = np.nonzero(fr.water)[0]
        pick = wc[RNG.integers(0, len(wc), 6)]
        fr.add_glow((pick % W) + 0.5, (pick // W) + 0.5, col(SNOW_GLINT) * 0.5, halo=0.3)

    # ── 글자 덮어쓰기 ──
    if t >= T_TOWER_LIGHT[0]:                                # 타워 주위를 도는 눈꽃·별빛
        a = ORBIT['a0'] + tg * 0.7 * np.where(np.arange(44) % 2 == 0, 1.0, -0.8)
        P = np.stack([TOWER_X + ORBIT['r'] * np.cos(a), TOWER_Y0 + ORBIT['h'] + 0.05 * np.sin(tg + a),
                      TOWER_Z + ORBIT['r'] * np.sin(a)], 1)
        sx, sy, zc = cam_project(P, cam)
        k = float(clip01((t - T_TOWER_LIGHT[0]) / 1.0))
        tw = 0.6 + 0.4 * np.sin(tg * 5 + ORBIT['a0'] * 7)
        if f > 220:
            fr.overlay(sx, sy, ORBIT['ch'], ORBIT['c'] * (k * tw)[:, None], zc)
        else:
            fr.add_glow(sx, sy, ORBIT['c'] * (0.25 * k * tw)[:, None], z=zc, halo=0)
    ox = SEOUL_SNOW['ox'] * 0.36 * SEOUL_SNOW['oz']          # 서울에 내리는 눈
    span = 0.8 * SEOUL_SNOW['oz']
    yy = 0.4 * SEOUL_SNOW['oz'] - ((tg * SEOUL_SNOW['v'] + SEOUL_SNOW['oy'] * span) % span)
    P = np.stack([o[0] + ox + 0.1 * np.sin(SEOUL_SNOW['sw'] * tg + SEOUL_SNOW['sp']), o[1] + yy,
                  o[2] + SEOUL_SNOW['oz']], 1)
    P = rot_y(P - o, cam['yaw']) + o
    sx, sy, zc = cam_project(P, cam)
    ch = np.where(SEOUL_SNOW['heart'], '♥', np.where(zc < 3, '*', np.where(zc < 7, '+', '.')))
    bright = clip01(1.3 - zc / 12.0)
    cc = np.where(SEOUL_SNOW['heart'][:, None], col(PINK)[None], col(SNOWFLAKE)[None]) * bright[:, None]
    fr.overlay(sx, sy, ch, cc, zc)
    # M → I → J → U (타워에 세로로)
    lp = tower_front_points(cam, TOWER_LETTER_Y, out=0.02)
    sx, sy, zc = cam_project(lp, cam)
    rows_gap = 0.5 * f * abs(TOWER_LETTER_Y[0] - TOWER_LETTER_Y[-1]) / max(len(TOWER_TEXT) - 1, 1) / max(zc.mean(), 0.1)
    off = 1.0 - float(clip01((t - T_STARDUST[0]) / 0.4))
    span_l = (T_LETTERS[1] - T_LETTERS[0]) / max(len(TOWER_TEXT), 1)
    big = rows_gap >= 5.5
    # 글자 간격을 화면에서 정확히 같게: 한 줄(같은 칸)에 같은 줄 간격으로 세워요
    n_l = len(TOWER_TEXT)
    LX = math.floor(float(np.mean(sx))) + 0.5
    step_i = max(7 if big else 2, int(round((float(sy[-1]) - float(sy[0])) / max(n_l - 1, 1))))
    top_i = math.floor((float(sy[0]) + float(sy[-1])) / 2 - step_i * (n_l - 1) / 2)
    LY = [top_i + k * step_i + 0.5 for k in range(n_l)]
    for k, chh in enumerate(TOWER_TEXT):
        tk = T_LETTERS[0] + k * span_l
        if t < tk or off <= 0:
            continue
        pop = 1.4 * math.exp(-(t - tk) / 0.25)
        neon = 0.5 + 0.5 * math.sin(tg * 2.4 - k * 0.5) if t > T_LETTERS[1] + 0.5 else 1.0
        bri = min(1.0, 0.6 + 0.4 * neon + pop) * off
        cc = lerp(col(NEON_PINK), col(NEON_GOLD), 0.5 + 0.5 * math.sin(tg * 1.7 + k * 1.3))
        cx_, cy_ = LX, LY[k]
        if big:                                             # 줌인: 3x5 큰 네온 글자
            px_, py_ = np.meshgrid(np.arange(-2, 3), np.arange(-3, 4))
            fr.overlay(cx_ + px_.ravel(), cy_ + py_.ravel(), ' ', np.zeros(3), zc[k] - 0.05)
            g = FONT.get(chh.upper(), FONT['O'])
            dots = [(c - 1, r - 2) for r in range(5) for c in range(3) if g[r * 3 + c] == '#']
            dx_ = np.array([d[0] for d in dots], float); dy_ = np.array([d[1] for d in dots], float)
            grad = lerp(col(NEON_GOLD), col(NEON_PINK), ((dy_ + 2) / 4)[:, None])
            fr.add_glow(cx_ + dx_, cy_ + dy_, grad * (0.3 + 0.3 * neon + pop) * off, z=zc[k] - 0.05, halo=0.9)
            fr.overlay(cx_ + dx_, cy_ + dy_, '#', clip01(grad * bri + max(0.0, pop - 0.4) * 0.6), zc[k] - 0.05)
        else:
            fr.add_glow([cx_], [cy_], cc * (0.35 + 0.4 * neon + pop) * off, z=zc[k] - 0.05, halo=1.2)
            if rows_gap >= 1.6:                             # 한 글자 + 양옆을 어둡게 해서 또렷하게
                fr.overlay([cx_ - 1, cx_ + 1], [cy_, cy_], ' ', np.zeros(3), zc[k] - 0.05)
                fr.overlay([cx_], [cy_], chh, clip01(cc * bri + max(0.0, pop - 0.4) * 0.6), zc[k] - 0.05)
    for t0, t1, txt in SEOUL_CAPTIONS:
        draw_caption(fr, txt, t0, t1, t, tg)
    return compose_arrays(fr, bg_col, bg_lum, bg_ch)


# ════════════════════════════════════════════════════════════════════
#  25. 별빛이 되어 트리로 — 26. 마지막 편지
# ════════════════════════════════════════════════════════════════════
_sx, _sy, _ = project(to_cam(np.array([[0.0, STAR_Y, 0.0]])))
STAR_SCREEN = np.array([_sx[0], _sy[0]])
_Y, _X = np.mgrid[0:H, 0:W].astype(float)
WASH_D = np.hypot(_X.ravel() + 0.5 - STAR_SCREEN[0], (_Y.ravel() + 0.5 - STAR_SCREEN[1]) * 2)
WASH_A = np.arctan2((_Y.ravel() - STAR_SCREEN[1]) * 2, _X.ravel() - STAR_SCREEN[0])
DISSOLVE_THR = clip01(0.7 * np.random.default_rng(9).random(W * H) + 0.3 * (ROWS_I / H))
_rsd = np.random.default_rng(55)
_NSD = 10 * max(len(TOWER_TEXT), 1)
STARDUST = dict(letter=np.arange(_NSD) // 10, jit=_rsd.normal(0, 0.8, (_NSD, 2)),
                ctrl=np.stack([_rsd.uniform(-25, 25, _NSD), _rsd.uniform(8, 20, _NSD)], 1),
                delay=(np.arange(_NSD) // 10) * 0.15 + _rsd.uniform(0, 0.4, _NSD),
                c=np.array([col(NEON_GOLD), col(NEON_PINK), col(STAR_RAY)])[np.arange(_NSD) % 3])
_SD_SRC = []


def draw_stardust(fr, t, tg):
    if not (T_STARDUST[0] <= t < T_STARDUST[1] + 0.3):
        return
    if not _SD_SRC:
        cam = seoul_camera(T_STARDUST[0])
        sx, sy, _ = cam_project(tower_front_points(cam, TOWER_LETTER_Y, out=0.02), cam)
        _SD_SRC.append(np.stack([sx, sy], 1))
    src = _SD_SRC[0]
    S = STARDUST
    p0 = src[S['letter']] + S['jit']
    p2 = STAR_SCREEN
    p1 = (p0 + p2) / 2 + np.stack([S['ctrl'][:, 0], -S['ctrl'][:, 1]], 1)
    u = (t - T_STARDUST[0] - S['delay']) / 1.5
    for j in range(5):
        e = smooth(u - j * 0.035)[:, None]
        pos = (1 - e) ** 2 * p0 + 2 * (1 - e) * e * p1 + e * e * p2
        live = (u - j * 0.035 > 0) & (u < 1)
        if live.any():
            fr.add_glow(pos[live, 0], pos[live, 1], S['c'][live] * (0.9 * (1 - j / 5)), halo=0.6 if j == 0 else 0.2)
            if j == 0:
                fr.overlay(pos[live, 0], pos[live, 1], '*', clip01(S['c'][live] * 1.2))
    start = (u > 0) & (u < 0.12)
    if start.any():
        fr.add_glow(p0[start, 0], p0[start, 1], col(FLASH_WHITE) * 0.8, halo=1.0)
    arrived = float(np.mean(u >= 1))
    if arrived > 0:
        fr.add_glow([p2[0]], [p2[1]], col(STAR_RAY) * (0.5 + 1.5 * arrived), halo=1.5)


def draw_top_flash(fr, t, tg):
    u = (t - T_TOP_FLASH) / 0.9
    if 0 <= u < 1:
        I = (1 - u) ** 1.8
        fr.add_glow([STAR_SCREEN[0]], [STAR_SCREEN[1]], col(FLASH_WHITE) * 3.0 * I, halo=2.5)
        d = np.linspace(0, 1, 60)
        for k in range(8):
            ang = k * math.pi / 4 + 0.2
            ln = 45 * ease_out_cubic(min(1.0, u * 2.5)) * (1.0 if k % 2 == 0 else 0.6)
            fr.add_glow(STAR_SCREEN[0] + math.cos(ang) * d * ln, STAR_SCREEN[1] - math.sin(ang) * d * ln * 0.5,
                        lerp(col(FLASH_WHITE), col(NEON_GOLD), d[:, None]) * (1.4 * I * (1 - d) ** 1.2)[:, None], halo=0.6)
    v = (t - T_TOP_FLASH) / 2.0
    if 0 <= v < 1:                                           # 화면 전체로 퍼지는 분홍·금빛
        R = 130 * ease_out_cubic(v)
        ring = np.exp(-((WASH_D - R) / 14.0) ** 2) * (1 - v) * 0.55
        fill = clip01(1 - WASH_D / (R + 1)) * (1 - v) ** 1.5 * 0.3
        cc = lerp(col(PINK), col(GOLD), (0.5 + 0.5 * np.sin(WASH_A * 3 + tg))[:, None])
        fr.glow += cc * (ring + fill)[:, None]


ENV_W, ENV_H = 31, 12
ENV_X0, ENV_Y0 = (W - ENV_W) // 2, H - 18
LETTER_TOP = 4                                  # 'To. 미주에게' 줄
LETTER_BODY = (8, ENV_Y0 - 10)                  # 편지 본문이 들어가는 줄 범위


def is_wide(ch):
    o = ord(ch)
    return 0x1100 <= o <= 0x11FF or 0x2E80 <= o <= 0xA4CF or 0xAC00 <= o <= 0xD7A3 or 0xF900 <= o <= 0xFAFF \
        or 0xFE30 <= o <= 0xFE4F or 0xFF00 <= o <= 0xFF60 or 0xFFE0 <= o <= 0xFFE6


def text_width(txt):
    return sum(2 if is_wide(c) else 1 for c in txt)


def wrap_text(txt, maxw):
    """화면 폭(maxw 칸)에 맞춰 띄어쓰기 단위로 줄을 바꿔요 (한글은 두 칸)."""
    lines, cur = [], ''
    for word in txt.split(' '):
        cand = word if not cur else cur + ' ' + word
        if text_width(cand) <= maxw:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def build_letter_pages():
    maxw = W - 8
    cap = LETTER_BODY[1] - LETTER_BODY[0] + 1
    pages, page, used = [], [], 0
    for para in LETTER_PARAS:
        gold = para.startswith('*')
        lines = wrap_text(para.lstrip('*'), maxw)
        need = len(lines) * 2 + (1 if page else 0)
        if page and (used + need > cap or len(page) >= LETTER_PARAS_PER_PAGE):
            pages.append(page); page, used = [], 0
            need = len(lines) * 2
        page.append((lines, 'gold' if gold else 'body'))
        used += need
    if page:
        pages.append(page)
    last = [(wrap_text(p.lstrip('*'), maxw), 'gold' if p.startswith('*') else 'last') for p in LETTER_LAST]
    pages.append(last)
    out, tt = [], T_LINES
    for pi, pg in enumerate(pages):
        rows, r, items = sum(len(l) * 2 for l, _ in pg) + len(pg) - 1, 0, []
        r = LETTER_BODY[0] + max(0, (cap - rows) // 2)
        n = 0
        for lines, sty in pg:
            for ln in lines:
                items.append(dict(text=ln, row=r, t0=tt + n * LETTER_CHAR_SEC, style=sty))
                n += len(ln)
                r += 2
            r += 1
        t_typed = tt + n * LETTER_CHAR_SEC
        final = pi == len(pages) - 1
        t_end = t_typed + 1.6 + n * LETTER_READ_SEC
        out.append(dict(items=items, t0=tt, t_end=None if final else t_end))
        tt = t_end + 0.25
    return out, t_typed


LETTER_PAGES, _T_LAST_TYPED = build_letter_pages()
T_FOOTER = (_T_LAST_TYPED + 0.8, _T_LAST_TYPED + 0.8 + sum(len(x) for x in LETTER_FOOTER) * 0.05)
LOOP = T_FOOTER[1] + 6.0                         # 처음부터 다시


def draw_letter(fr, t, tg):
    a = float(clip01((t - T_ENV) / 0.8))
    if a <= 0:
        return
    cells = {}
    body, dark, line = col(ENVELOPE), col(ENVELOPE_DARK), col(ENVELOPE_LINE)
    p = float(smooth((t - T_ENV_OPEN[0]) / (T_ENV_OPEN[1] - T_ENV_OPEN[0])))
    for r in range(1, ENV_H - 1):
        for c in range(1, ENV_W - 1):
            cells[(r, c)] = (':', dark * 0.8)
    if p > 0.5:                                              # 열린 봉투 안쪽에서 새어 나오는 분홍빛
        for r in range(1, 4):
            for c in range(3, ENV_W - 3):
                cells[(r, c)] = (':', col(PINK) * (0.75 - 0.15 * r))
    for c in range(1, ENV_W - 1):
        cells[(0, c)] = ('_', body)
        cells[(ENV_H - 1, c)] = ('_', body)
    for r in range(1, ENV_H):
        cells[(r, 0)] = ('|', body)
        cells[(r, ENV_W - 1)] = ('|', body)
    mid = ENV_W // 2
    hgt = int(round(7 * (1 - 2 * p))) if p < 0.5 else int(round(7 * (2 * p - 1)))
    sgn = 1 if p < 0.5 else -1                               # 닫힘: 아래로 접힌 덮개 / 열림: 위로 젖힌 덮개
    for k in range(1, hgt + 1):
        lc = int(round(1 + 12 * (k - 1) / max(hgt - 1, 1)))
        r = sgn * k
        for c in range(lc + 1, ENV_W - 1 - lc):
            cells[(r, c)] = (';', body * 0.75)
        cells[(r, lc)] = ('\\' if sgn > 0 else '/', line)
        cells[(r, ENV_W - 1 - lc)] = ('/' if sgn > 0 else '\\', line)
    if hgt >= 1:
        cells[(sgn * hgt, mid)] = ('♥', col(HOT_PINK) * (0.8 + 0.2 * float(heartbeat((tg * 1.1) % 1.0))))
    keys = list(cells.keys())
    xs = np.array([ENV_X0 + c + 0.5 for _, c in keys])
    ys = np.array([ENV_Y0 + r + 0.5 for r, _ in keys])
    fr.overlay(xs, ys, np.array([cells[k][0] for k in keys]), np.array([cells[k][1] for k in keys]) * a)
    if a < 1:
        ang = np.linspace(0, 2 * math.pi, 30, endpoint=False)
        fr.add_glow(W / 2 + np.cos(ang) * 20 * a, ENV_Y0 + 6 + np.sin(ang) * 7 * a, col(ENVELOPE_LINE) * (0.5 * (1 - a)), halo=0.4)
    if p > 0.5:                                              # 분홍 빛과 작은 하트가 떠올라요
        op = (p - 0.5) * 2
        fr.add_glow([W / 2], [ENV_Y0 + 0.5], col(PINK) * 0.9 * op, halo=2.5)
        k = np.arange(16)
        start = T_ENV_OPEN[0] + 0.6 + k * 0.1
        age = (t - start) % 1.6
        live = t > start
        x = W / 2 + (k % 8 - 3.5) * 2.2 + 1.5 * np.sin(age * 3 + k)
        y = ENV_Y0 - 0.5 - age * 6.5
        al = clip01(1 - age / 1.6) * live
        hc = np.array([col(PINK), col(HOT_PINK), col(ENVELOPE_LINE)])[k % 3]
        fr.add_glow(x[live], y[live], hc[live] * (0.25 * al[live])[:, None], halo=0.6)
        fr.overlay(x[live], y[live], np.where(k[live] % 4 == 3, '*', '♥'), hc[live] * al[live][:, None])
    # 편지 글자 (한 번에 모아서 그려요 · 한글은 두 칸)
    G, O = [[], [], []], [[], [], [], []]

    def put_line(txt, row, t0, style, alpha=1.0):
        x = (W - text_width(txt)) // 2
        if t < t0:
            return
        O[0] += [x - 0.5, x + text_width(txt) + 0.5]; O[1] += [row + 0.5] * 2      # 양옆 한 칸 비우기
        O[2] += [' ', ' ']; O[3] += [np.zeros(3)] * 2
        name_at = txt.find(NAME)
        for kk, ch in enumerate(txt):
            tk = t0 + kk * LETTER_CHAR_SEC
            if t < tk:
                break
            wide = is_wide(ch)
            pop = math.exp(-(t - tk) / 0.15)
            wave = 0.82 + 0.18 * math.sin(tg * 2.5 - kk * 0.35)
            if style == 'last':                              # 금색 · 분홍 번갈아 반짝
                base = col(NEON_GOLD) if (kk + int(tg * 2.5)) % 2 == 0 else col(NEON_PINK)
            elif style == 'gold' or style == 'title':
                base = lerp(col(MSG_GOLD), col(NAME_GLOW), 0.5 + 0.5 * math.sin(tg * 3 + kk * 0.4))
            elif 0 <= name_at <= kk < name_at + len(NAME):
                base = lerp(col(MSG_GOLD), col(NAME_GLOW), 0.5 + 0.5 * math.sin(tg * 4 + kk))
            else:
                base = lerp(col(LETTER_TEXT), col(ENVELOPE_LINE), 0.5 + 0.5 * math.sin(tg * 0.9 + kk * 0.2 + row))
            if ch == '♥':
                base = col(HOT_PINK) * (0.8 + 0.4 * float(heartbeat((tg * 1.1) % 1.0)))
            cc = clip01(base * min(1.0, wave + pop) + max(0.0, pop - 0.3) * 0.6) * alpha
            if ch != ' ':
                G[0].append(x + (1.0 if wide else 0.5)); G[1].append(row + 0.5)
                G[2].append(base * (0.05 + 0.45 * pop) * (1.5 if style in ('last', 'title', 'gold') else 1.0) * alpha)
            O[0].append(x + 0.5); O[1].append(row + 0.5); O[2].append(ch); O[3].append(cc)
            if wide:                                         # 한글 오른쪽 반 칸 자리 표시
                O[0].append(x + 1.5); O[1].append(row + 0.5); O[2].append('\x01'); O[3].append(cc)
            x += 2 if wide else 1

    if t >= T_LINES - 0.6:
        put_line(LETTER_TITLE, LETTER_TOP, T_LINES - 0.6, 'title')
    for pg in LETTER_PAGES:
        if t < pg['t0'] or (pg['t_end'] is not None and t >= pg['t_end']):
            continue
        fade = 1.0 if pg['t_end'] is None else float(clip01((pg['t_end'] - t) / 0.5))
        for it in pg['items']:
            put_line(it['text'], it['row'], it['t0'], it['style'], fade)
    for i, ln in enumerate(LETTER_FOOTER):
        put_line(ln, H - 2 * len(LETTER_FOOTER) + 2 * i, T_FOOTER[0] + i * 0.7, 'gold' if i == 0 else 'body')
    if G[0]:
        fr.add_glow(np.array(G[0]), np.array(G[1]), np.array(G[2]), halo=0.4)
    if O[0]:
        fr.overlay(np.array(O[0]), np.array(O[1]), np.array(O[2]), np.array(O[3]))


# ── 장면 섞기 ──
def dissolve(A, B, m):
    """A → B 로 반짝이 가루처럼 칸마다 바뀌어요."""
    take = DISSOLVE_THR < m
    chars = np.where(take, B[0], A[0])
    colr = np.where(take[:, None], B[1], A[1])
    lum = np.where(take, B[2], A[2])
    if 0 < m < 1:
        edge = np.abs(DISSOLVE_THR - m) < 0.03
        if edge.any():
            chars[edge] = np.where(RNG.random(edge.sum()) < 0.5, '*', '+')
            colr[edge] = lerp(col(PINK), col(GOLD), RNG.random(edge.sum())[:, None])
    return chars, colr, lum


def layer_over(base, fr, dim=1.0):
    """기존 장면 위에 빛과 글자를 한 겹 더 얹어요."""
    chars, colr, lum = base[0].copy(), base[1] * dim, base[2] * dim
    g = fr.glow
    gl = g.max(1)
    colr = colr + g
    lum2 = lum + gl
    m = colr.max(1)
    over = clip01((m - 1.0) / 1.2)
    colr = colr / np.maximum(m, 1.0)[:, None]
    colr = colr * (1 - over)[:, None] + over[:, None]
    gm = gl > 0.04
    chars[gm] = RAMP_ARR[np.clip((lum2[gm] * 12).astype(np.int64), 0, 11)]
    o = fr.has_o
    chars[o] = fr.ochar[o]
    colr[o] = fr.ocol[o]
    return chars, colr, lum2


def tree_time_return(t):
    """서울에서 돌아온 트리의 시각 — 라벤더 선물이 정면에 오도록 맞춰요."""
    return t - (T_GIFT_GLOW[0] + T_GIFT_GLOW[1]) / 2 + (_FACE_T + ROTATE_SECONDS)


def render(tg):
    return to_ansi(render_arrays(tg))


def render_arrays(tg):
    """한 장면을 (글자, 색, 밝기) 배열로 — 터미널·HTML 이 함께 써요."""
    t = tg % LOOP
    if t < T_SEOUL_IN[0]:
        out = render_tree(t, tg)
    elif t < T_SEOUL_IN[1]:
        m = float(smooth((t - T_SEOUL_IN[0]) / (T_SEOUL_IN[1] - T_SEOUL_IN[0])))
        out = dissolve(render_tree(t, tg), render_seoul(t, tg), m)
    elif t < T_RETURN[0]:
        out = render_seoul(t, tg)
    else:
        gg = float(clip01((t - T_GIFT_GLOW[0]) / 0.5) * clip01((T_GIFT_GLOW[1] - t) / 0.8))
        tree = render_tree(tree_time_return(t), tg, show_msg=False, gift_glow=gg)
        if t < T_RETURN[1]:
            m = float(smooth((t - T_RETURN[0]) / (T_RETURN[1] - T_RETURN[0])))
            out = dissolve(render_seoul(t, tg), tree, m)
        else:
            out = tree
    if T_STARDUST[0] <= t < T_TOP_FLASH + 2.0 or t >= T_ENV - 0.3:
        fr2 = Frame()
        draw_stardust(fr2, t, tg)
        draw_top_flash(fr2, t, tg)
        dim = 1.0
        if t >= T_ENV - 0.3:
            dim = float(lerp(1.0, 0.33, smooth((t - T_ENV + 0.3) / 1.0)))
            draw_letter(fr2, t, tg)
        out = layer_over(out, fr2, dim)
    end = float(clip01((LOOP - t) / 0.8))
    if end < 1:
        out = (out[0], out[1] * end, out[2])
    return out


# ════════════════════════════════════════════════════════════════════
#  HTML 로 내보내기:  python3 tree.py --html   →  tree.html
#  (컴퓨터 16:9 · 휴대폰 9:16 두 가지가 한 파일에 들어 있고, 열 때 골라요)
# ════════════════════════════════════════════════════════════════════
HTML_FPS = 30
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#000000">
<title>Merry Christmas, __NAME__ ♥</title>
<style>
 html,body{margin:0;height:100%;background:#000;overflow:hidden;font-family:-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;-webkit-user-select:none;user-select:none}
 #wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
 #stage{position:relative}
 canvas{position:absolute;left:0;top:0}
 #glow{mix-blend-mode:screen;opacity:.55;pointer-events:none}
 #cover{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;
   background:radial-gradient(ellipse at center,#2a1640 0%,#000 72%);color:#ffd2ea;text-align:center;z-index:5;padding:20px;box-sizing:border-box}
 #cover h1{font-weight:600;font-size:clamp(24px,6vw,44px);margin:0 0 6px;color:#ff8cc8;text-shadow:0 0 18px #ff4fa8}
 #cover p{margin:2px;font-size:clamp(13px,3.4vw,17px);opacity:.85}
 .btns{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:14px}
 button{font:inherit;font-size:clamp(15px,4vw,18px);color:#fff;background:rgba(175,135,255,.16);border:1.5px solid #b99bff;
   border-radius:16px;padding:16px 22px;min-width:150px;cursor:pointer;line-height:1.35;box-sizing:border-box}
 @media (max-width:520px){.btns{flex-direction:column;width:100%;max-width:280px}.btns button{width:100%}}
 button small{display:block;font-size:12px;opacity:.7}
 button.rec{background:rgba(255,95,175,.25);border-color:#ff7ac0;box-shadow:0 0 18px rgba(255,80,170,.45)}
 button:disabled{opacity:.5}
 #hint{position:fixed;right:10px;bottom:6px;color:#a58bd6;font-size:11px;opacity:.55;z-index:3;display:none}
</style></head><body>
<div id="wrap"><div id="stage"><canvas id="cv"></canvas><canvas id="glow"></canvas></div></div>
<div id="cover"><h1>♥ __NAME__ 에게 ♥</h1>
 <p>어떤 화면으로 볼까요?</p>
 <div class="btns">
  <button id="bpc">💻 컴퓨터<small>가로 16:9</small></button>
  <button id="bph">📱 휴대폰<small>세로 9:16</small></button>
 </div>
 <p id="msg" style="margin-top:14px;font-size:13px;opacity:.65">화면을 고르면 바로 시작돼요</p>
</div>
<div id="hint">Space 일시정지 · F 전체 화면</div>
<script id="d_pc" type="application/octet-stream">__DATA_PC__</script>
<script id="d_phone" type="application/octet-stream">__DATA_PHONE__</script>
<script>
(()=>{
const META={pc:__META_PC__,phone:__META_PHONE__};
const $=id=>document.getElementById(id);
const cover=$('cover'),msg=$('msg'),cv=$('cv'),gl=$('glow'),ctx=cv.getContext('2d'),gctx=gl.getContext('2d');
const portrait=innerHeight>innerWidth;
(portrait?$('bph'):$('bpc')).classList.add('rec');
let W,H,FPS,N,FS,buf,C,V,cw=8,chh=16,dpr=1,cur=-1,start=0,paused=false,pauseAt=0,FN='',FW='';
const CHS=new Map();const chOf=c=>{let s=CHS.get(c);if(s===undefined){s=String.fromCharCode(c);CHS.set(c,s);}return s;};
const isWide=c=>(c>=0x1100&&c<=0x11FF)||(c>=0x2E80&&c<=0xA4CF)||(c>=0xAC00&&c<=0xD7A3)||(c>=0xF900&&c<=0xFAFF)||(c>=0xFF00&&c<=0xFF60);
const COL=new Array(32768);
const colOf=v=>COL[v]||(COL[v]='rgb('+(((v>>10)&31)*255/31|0)+','+(((v>>5)&31)*255/31|0)+','+((v&31)*255/31|0)+')');
function layout(){
  dpr=Math.min(window.devicePixelRatio||1,3);
  const vw=innerWidth,vh=innerHeight;
  cw=Math.min(vw/W,vh/H/2);chh=cw*2;
  const w=cw*W,h=chh*H,st=$('stage');
  st.style.width=w+'px';st.style.height=h+'px';
  for(const c of[cv,gl]){c.width=Math.round(w*dpr);c.height=Math.round(h*dpr);c.style.width=w+'px';c.style.height=h+'px';}
  ctx.setTransform(dpr,0,0,dpr,0,0);
  FN=(chh*0.82)+'px Menlo,"SF Mono",Consolas,"DejaVu Sans Mono","Courier New",monospace';
  FW=(chh*0.96)+'px "Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Noto Sans CJK KR",sans-serif';
  ctx.font=FN;
  ctx.textAlign='center';ctx.textBaseline='middle';
  gl.style.filter='blur('+Math.max(2,cw*0.7)+'px) brightness(1.4)';
  if(cur>=0)draw();
}
function step(to){
  if(to<cur){C.fill(0);V.fill(0);cur=-1;}
  while(cur<to){cur++;
    const o=cur*FS,dc=new Uint16Array(buf,o,W*H),dv=new Uint16Array(buf,o+W*H*2,W*H);
    for(let i=0;i<W*H;i++){C[i]^=dc[i];V[i]^=dv[i];}
  }
}
function draw(){
  ctx.fillStyle='#000';ctx.fillRect(0,0,W*cw,H*chh);
  let last=-1,wideOn=false;ctx.font=FN;
  for(let i=0;i<W*H;i++){const c=C[i];if(!c)continue;const v=V[i];
    if(v!==last){ctx.fillStyle=colOf(v);last=v;}
    const wd=isWide(c);if(wd!==wideOn){ctx.font=wd?FW:FN;wideOn=wd;}
    ctx.fillText(chOf(c),(i%W+(wd?1:0.5))*cw,((i/W|0)+0.5)*chh);}
  gctx.setTransform(1,0,0,1,0,0);gctx.clearRect(0,0,gl.width,gl.height);gctx.drawImage(cv,0,0);
}
function frame(now){
  if(!paused){const f=Math.floor((now-start)/1000*FPS)%N;if(f!==cur){step(f);draw();}}
  requestAnimationFrame(frame);
}
async function go(kind){
  $('bpc').disabled=$('bph').disabled=true;msg.textContent='불러오는 중… ♥';
  const el=document.documentElement;if(el.requestFullscreen)el.requestFullscreen().catch(()=>{});
  try{
    const m=META[kind];W=m.W;H=m.H;FPS=m.FPS;N=m.N;FS=W*H*4;
    const b64=$('d_'+kind).textContent.trim();
    const bin=atob(b64),u8=new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++)u8[i]=bin.charCodeAt(i);
    const st=new Blob([u8]).stream().pipeThrough(new DecompressionStream('deflate'));
    buf=await new Response(st).arrayBuffer();
  }catch(e){msg.textContent='이 브라우저는 지원하지 않아요. 최신 Chrome · Safari 로 열어 주세요.';return;}
  C=new Uint16Array(W*H);V=new Uint16Array(W*H);
  layout();addEventListener('resize',layout);
  cover.style.display='none';if(kind==='pc')$('hint').style.display='block';
  start=performance.now();requestAnimationFrame(frame);
}
$('bpc').onclick=()=>go('pc');$('bph').onclick=()=>go('phone');
addEventListener('keydown',e=>{
  if(!buf)return;
  if(e.code==='Space'){paused=!paused;if(paused)pauseAt=performance.now();else start+=performance.now()-pauseAt;e.preventDefault();}
  if(e.key==='f'||e.key==='F'){const el=document.documentElement;document.fullscreenElement?document.exitFullscreen():el.requestFullscreen&&el.requestFullscreen();}
});
})();
</script></body></html>
"""


def export_frames(path):
    """지금 화면 모양(LAYOUT)으로 모든 장면을 그려 압축해서 저장해요."""
    import zlib
    n = int(round(LOOP * HTML_FPS))
    comp = zlib.compressobj(9)
    parts = []
    prev_c = np.zeros(W * H, np.uint16)
    prev_v = np.zeros(W * H, np.uint16)
    for i in range(n):
        ch, co, _ = render_arrays(i / HTML_FPS)
        cp = np.array(ch, dtype='<U1').view(np.uint32).astype(np.int64)
        c = np.where((cp <= 32) | (cp > 0xFFFF), 0, cp).astype(np.uint16)   # 0 = 빈칸 (한글 오른쪽 반 칸 포함)
        q = (clip01(co) * 31 + 0.5).astype(np.uint16)
        v = (q[:, 0] << 10) | (q[:, 1] << 5) | q[:, 2]
        v[c == 0] = 0
        parts.append(comp.compress((c ^ prev_c).astype('<u2').tobytes() + (v ^ prev_v).astype('<u2').tobytes()))
        prev_c, prev_v = c, v
    parts.append(comp.flush())
    with open(path, 'wb') as fh:
        fh.write(b''.join(parts))
    with open(path + '.json', 'w') as fh:
        fh.write('{"W":%d,"H":%d,"FPS":%d,"N":%d}' % (W, H, HTML_FPS, n))


def export_html(path):
    """컴퓨터용·휴대폰용을 동시에 그려서 한 파일짜리 HTML 로 묶어요 (인터넷 없이 재생돼요)."""
    import base64
    import subprocess
    import tempfile
    t0 = time.time()
    tmp = tempfile.mkdtemp()
    me = os.path.abspath(__file__)
    procs = {}
    for lay in ('pc', 'phone'):
        env = dict(os.environ, TREE_LAYOUT=lay)
        procs[lay] = subprocess.Popen([sys.executable, me, '--frames', os.path.join(tmp, lay + '.bin')], env=env)
    print('  컴퓨터용 · 휴대폰용 장면을 동시에 그리는 중… (1~2분 걸려요)')
    for lay, pr in procs.items():
        if pr.wait() != 0:
            raise SystemExit('  %s 장면을 그리다 문제가 생겼어요.' % lay)
    html = HTML_TEMPLATE.replace('__NAME__', NAME)
    for lay in ('pc', 'phone'):
        fn = os.path.join(tmp, lay + '.bin')
        with open(fn, 'rb') as fh:
            data = base64.b64encode(fh.read()).decode('ascii')
        with open(fn + '.json') as fh:
            meta = fh.read()
        html = html.replace('__DATA_%s__' % lay.upper(), data).replace('__META_%s__' % lay.upper(), meta)
        os.remove(fn); os.remove(fn + '.json')
    os.rmdir(tmp)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('  완성: %s  (%.1f MB, %.0f초 걸림)' % (path, len(html) / 1e6, time.time() - t0))


# ════════════════════════════════════════════════════════════════════
#  실행
# ════════════════════════════════════════════════════════════════════
def _term_size():
    try:
        s = os.get_terminal_size()
        return s.columns, s.lines
    except OSError:
        return W, H


def main():
    if len(sys.argv) > 2 and sys.argv[1] == '--frames':    # (HTML 만들 때 내부에서 써요)
        export_frames(sys.argv[2])
        return
    if len(sys.argv) > 1 and sys.argv[1] == '--html':      # 브라우저용 tree.html 만들기
        out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tree.html')
        export_html(out_path)
        return
    if len(sys.argv) > 2 and sys.argv[1] == '--dump':      # 디버그: 한 장면을 글자로만 출력
        import re
        s = render(float(sys.argv[2]))
        print(re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', s).replace('\r', ''))
        return
    if len(sys.argv) > 1 and sys.argv[1] == '--bench':
        t0 = time.perf_counter()
        for i in range(200):
            render(i * LOOP / 200.0)
        print('평균 %.1f ms/프레임' % ((time.perf_counter() - t0) / 200 * 1000))
        return

    out = sys.stdout.buffer

    def stop(*_):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    out.write(b'\x1b[?1049h\x1b[?25l\x1b[48;2;0;0;0m\x1b[2J')
    out.flush()
    try:
        start = time.perf_counter()
        nxt = start
        frame = 0
        size_ok = True
        cols, lines = W, H
        while True:
            if frame % 15 == 0:
                cols, lines = _term_size()
                ok = cols >= W and lines >= H
                if ok != size_ok:
                    out.write(b'\x1b[48;2;0;0;0m\x1b[2J')
                size_ok = ok
            if not size_ok:
                msg = ('\x1b[H\x1b[38;2;255;120;190m 창을 %dx%d 이상으로 키워 주세요 (지금 %dx%d). '
                       'Cmd + - 로 글자를 줄여도 돼요 ♥\x1b[K' % (W, H, cols, lines))
                out.write(msg.encode('utf-8'))
                out.flush()
                time.sleep(0.2)
                frame += 1
                nxt = time.perf_counter()
                continue
            out.write(render(time.perf_counter() - start).encode('utf-8'))
            out.flush()
            frame += 1
            nxt += 1.0 / FPS
            delay = nxt - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            else:
                nxt = time.perf_counter()
    except KeyboardInterrupt:
        pass
    finally:
        out.write(b'\x1b[0m\x1b[?25h\x1b[?1049l')
        out.write(('\x1b[38;2;255;105;180m  ♥ Merry Christmas, %s ♥\x1b[0m\n' % NAME).encode('utf-8'))
        out.flush()


if __name__ == '__main__':
    main()
