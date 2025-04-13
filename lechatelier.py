import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지


# Streamlit 설정
st.set_page_config(page_title="르 샤틀리에 시뮬레이터", layout="centered")
st.title("화학 평형 시뮬레이션")
st.markdown("반응식: A + B ⇌ C 반응비: 1:1:1")

# 입력 슬라이더
A0 = st.slider("A 초기 농도 (mol/L)", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
B0 = st.slider("B 초기 농도 (mol/L)", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
K = st.slider("평형 상수 K", min_value=0.1, max_value=100.0, value=10.0, step=0.1)

# 계산용 x: 생성물 C의 생성 농도
x = np.linspace(0, min(A0, B0) - 1e-6, 1000)  # 너무 0에 가까워지는 걸 방지
A = A0 - x
B = B0 - x
C = x

# 0 이하 농도 방지
valid = (A > 0) & (B > 0)
x = x[valid]
A = A[valid]
B = B[valid]
C = C[valid]

Q = C / (A * B)
diff = abs(Q - K)
eq_index = np.argmin(diff)

# 평형점
x_eq = x[eq_index]
A_eq, B_eq, C_eq = A[eq_index], B[eq_index], C[eq_index]

# 결과 표시
st.subheader("시뮬레이션 결과")
st.markdown(f" 평형점에서 C 농도: **{C_eq:.3f} mol/L**")
st.markdown(f" A, B 평형 농도: **{A_eq:.3f}, {B_eq:.3f} mol/L**")
st.markdown(f" Q = {C_eq / (A_eq * B_eq):.3f} ≒ K = {K}")

# 시각화 - 평형 농도 막대그래프
fig, ax = plt.subplots(figsize=(6, 4))

labels = ['[A]', '[B]', '[C]']
values = [A_eq, B_eq, C_eq]
colors = ['#1f77b4', '#2ca02c', '#d62728']  # 파랑, 초록, 빨강

bars = ax.bar(labels, values, color=colors)

# 농도 값을 막대 위에 표시
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02, f'{height:.2f}',
            ha='center', va='bottom', fontsize=10)

ax.set_ylim(0, max(values) + 0.5)
ax.set_ylabel("농도 (mol/L)")
ax.set_title("평형 농도 비교", fontsize=14)
ax.spines[['top', 'right']].set_visible(False)

st.pyplot(fig)

