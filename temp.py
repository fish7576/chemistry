import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지

st.title("온도 변화에 따른 평형 이동 시뮬레이션")
st.markdown("### 반응식: 2NO₂(g) ⇌ N₂O₄(g) (발열 반응)")

# 초기 농도 입력
no2_init = st.slider("[NO₂] 초기 농도 (mol/L)", 0.1, 2.0, 1.0, 0.1)

# 온도 설정
T = st.slider("온도 (K)", 300, 800, 500, 10)

# 상수 정의
R = 8.314  # J/(mol·K)
delta_H = -58000  # J/mol (발열 반응 → ΔH < 0)

# 기준 온도와 K값
T0 = 500  # 기준 온도 (K)
K0 = 6.5  # 기준 온도에서의 K값 (임의 설정)

# van't Hoff 방정식으로 온도에 따른 K 계산
ln_K_ratio = (-delta_H / R) * (1 / T - 1 / T0)
K_eq = K0 * np.exp(ln_K_ratio)

st.markdown(f"**계산된 평형 상수 (K<sub>eq</sub>)**: {K_eq:.2f}", unsafe_allow_html=True)

# 평형 농도 계산 함수
def calculate_equilibrium(no2_0, K):
    # 2NO₂ ⇌ N₂O₄
    # NO₂가 x만큼 반응하면 → [NO₂] = no2_0 - 2x, [N₂O₄] = x
    def f(x):
        numerator = x
        denominator = (no2_0 - 2*x)**2
        return K - numerator / denominator
    
    x_vals = np.linspace(0, no2_0 / 2, 1000)
    for x in x_vals:
        if f(x) < 1e-4:
            break
    no2_eq = no2_0 - 2*x
    n2o4_eq = x
    return no2_eq, n2o4_eq

no2_eq, n2o4_eq = calculate_equilibrium(no2_init, K_eq)

# 결과 시각화
fig, ax = plt.subplots()
components = ['NO₂', 'N₂O₄']
values = [no2_eq, n2o4_eq]
colors = ['orange', 'purple']

ax.bar(components, values, color=colors)
ax.set_ylabel("평형 농도 (mol/L)")
ax.set_title("온도에 따른 평형 농도 변화")

st.pyplot(fig)
