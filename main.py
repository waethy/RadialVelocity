import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('Agg')  # Streamlit 호환을 위한 백엔드 설정
from matplotlib.animation import FFMpegWriter
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit 페이지 설정
st.title("Radial Velocity Simulation of a Star-Planet System")
st.write("Calculate and visualize the radial velocity of a star due to a planet's orbit.")

# 사용자 입력
st.sidebar.header("Input Parameters")
rotation_speed = st.sidebar.slider("Rotation Speed (rad/s)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
mass_ratio = st.sidebar.slider("Mass Ratio (M_planet/M_star)", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
orbital_radius = st.sidebar.slider("Orbital Radius (AU)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# 물리적 계산
orbital_period = 2 * np.pi / rotation_speed  # 공전 주기
v_planet = rotation_speed * orbital_radius  # 행성의 궤도 속도
v_star = mass_ratio * v_planet  # 중심별의 궤도 속도

# 애니메이션 설정
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 중심별의 궤도와 위치 플롯
ax1.set_xlim(-orbital_radius * 1.5 * mass_ratio, orbital_radius * 1.5 * mass_ratio)
ax1.set_ylim(-orbital_radius * 1.5 * mass_ratio, orbital_radius * 1.5 * mass_ratio)
ax1.set_xlabel("X (AU)")
ax1.set_ylabel("Y (AU)")
ax1.set_title("Star's Orbit")
ax1.grid(True)
ax1.set_aspect('equal')
star, = ax1.plot([], [], 'ro', label='Star')  # 중심별
orbit, = ax1.plot([], [], 'b--', label='Orbit')  # 궤적
text = ax1.text(0, orbital_radius * 1.2 * mass_ratio, '', fontsize=10)  # 시선 속도 태그

# 시선 속도 플롯
ax2.set_xlim(0, orbital_period)
ax2.set_ylim(-v_star * 1.5, v_star * 1.5)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Radial Velocity (AU/s)")
ax2.set_title("Radial Velocity of Star")
ax2.grid(True)
rv_line, = ax2.plot([], [], 'r-', label='Radial Velocity')
ax2.legend()

# 궤적 데이터
theta = np.linspace(0, 2 * np.pi, 100)
x_orbit = orbital_radius * mass_ratio * np.cos(theta)
y_orbit = orbital_radius * mass_ratio * np.sin(theta)
orbit.set_data(x_orbit, y_orbit)

# 애니메이션 데이터 초기화
times = []
rv_values = []

# 애니메이션 업데이트 함수
def update(frame):
    t = frame * 0.1  # 시간 간격
    angle = rotation_speed * t  # 회전각
    x_star = -orbital_radius * mass_ratio * np.cos(angle)  # 중심별 위치
    y_star = -orbital_radius * mass_ratio * np.sin(angle)
    star.set_data([x_star], [y_star])
    
    v_radial = v_star * np.sin(angle)  # 시선 속도
    text.set_text(f'Radial Velocity: {v_radial:.3f} AU/s')
    
    times.append(t)
    rv_values.append(v_radial)
    rv_line.set_data(times, rv_values)
    
    return star, text, rv_line

# 애니메이션 생성
try:
    ani = FuncAnimation(fig, update, frames=100, interval=100, blit=False)
except Exception():
    st.error("Failed to create animation. Please check Matplotlib configuration.")
    logger.error("Animation creation failed", exc_info=True)
    st.stop()

# mp4로 애니메이션 저장
output_file = "animation.mp4"
try:
    writer = FFMpegWriter(fps=10, bitrate=5000)
    ani.save(output_file, writer=writer)
    logger.info(f"Animation saved to {output_file}")
except Exception():
    st.error("Failed to save animation with ffmpeg. Ensure ffmpeg is correctly installed and accessible.")
    logger.error("Animation saving failed", exc_info=True)
    st.stop()

# mp4 파일을 Streamlit에 표시
if os.path.exists(output_file):
    with open(output_file, 'rb') as f:
        st.video(f.read())
else:
    st.error(f"Animation file {output_file} not found.")
    logger.error(f"File {output_file} not found")
