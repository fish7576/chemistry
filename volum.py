import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지


st.subheader("반응식: N₂ (g) + 3H₂ (g) ⇌ 2NH₃ (g)")

# 초기 몰수 설정
n_N2 = st.slider("N₂ 초기 몰수 (mol)", 0.1, 5.0, 1.0, 0.1)
n_H2 = st.slider("H₂ 초기 몰수 (mol)", 0.1, 5.0, 3.0, 0.1)

# 부피 조절
V = st.slider("반응 용기 부피 (L)", 1.0, 10.0, 5.0, 0.5)

# 초기 농도 계산
c_N2 = n_N2 / V
c_H2 = n_H2 / V

# 평형상수 (임의 값, 실제는 온도에 따라 달라짐)
K_eq = 0.5  # (NH3)^2 / (N2)*(H2)^3

# 평형 계산 함수
def calculate_equilibrium(c_n2, c_h2, K):
    def f(x):
        num = (2*x)**2
        denom = (c_n2 - x) * (c_h2 - 3*x)**3
        return K - num / denom

    x_vals = np.linspace(0, min(c_n2, c_h2 / 3) * 0.999, 1000)
    for x in x_vals:
        if f(x) < 1e-4 and (c_n2 - x) > 0 and (c_h2 - 3*x) > 0:
            break
    return c_n2 - x, c_h2 - 3*x, 2*x

c_n2_eq, c_h2_eq, c_nh3_eq = calculate_equilibrium(c_N2, c_H2, K_eq)

# 결과 시각화
fig, ax = plt.subplots()
components = ['N₂', 'H₂', 'NH₃']
values = [c_n2_eq, c_h2_eq, c_nh3_eq]
colors = ['blue', 'gray', 'green']

ax.bar(components, values, color=colors)
ax.set_ylabel("평형 농도 (mol/L)")
ax.set_title("부피에 따른 평형 농도 변화")

st.pyplot(fig)
