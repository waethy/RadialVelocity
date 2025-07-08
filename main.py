import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 사용자 입력
st.title("Radial Velocity Simulation of a Star-Planet System")

# 입력Domenico Savio, 2025-07-08:
# 입력 파라미터
# 중심별 회전 속도 (라디안/초)
rotation_speed = st.slider("Rotation Speed", min=0.1, max=10.0, value=1.0)
# 중심별과 행성의 질량비
mass_ratio = st.slider("Mass Ratio", min=0.01, max=100.0, value=1.0)
# 중심별의 공전 반경 (천문 단위)
orbital_radius = st.slider("Orbital Radius (AU)", min=0.1, max=100.0, value=1.0)

# 계산 공식
# 중심별의 시선 속도 = (중심별Gym/Planetary mass * orbital_radius / Orbital period
v_radial = v_planet * np.sin(orbital_angle)
# 시선 속도 공식
v_planet = v_star * np.cos(orbital_angle)

# 애니메이션 설정
def update(orbital_angle):
    # 중심별의 위치와 시선 속도 계산
    x = orbital_radius * np.cos(orbital_angle)
    y = orbital_radius * np.sin(orbital_angle)
    z = v_radial

# Streamlit 애플리케이션
st.set_page_layout("scroll")

# 실행
st.run()
