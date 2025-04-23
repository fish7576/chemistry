import streamlit as st
import numpy as np
from scipy.optimize import root_scalar

st.markdown("**반응식:** 2CrO₄²⁻ + 2H⁺ ⇌ Cr₂O₇²⁻ + H₂O")
st.markdown("황산(H₂SO₄)과 수산화나트륨(NaOH)의 농도를 조절")

# 입력: 초기 CrO₄²⁻ 농도
cro4_conc = st.slider("[CrO₄²⁻] 초기 농도 (M)", 0.01, 1.0, 0.5, 0.01)

# 입력: H₂SO₄, NaOH 농도
h2so4_conc = st.slider("[H₂SO₄] 농도 (M)", 0.0, 1.0, 0.0, 0.01)
naoh_conc = st.slider("[NaOH] 농도 (M)", 0.0, 1.0, 0.0, 0.01)

# H⁺ 계산 (음수 방지)
h_conc = max(2 * h2so4_conc - naoh_conc, 1e-14)
ph = -np.log10(h_conc)

# 평형 상수 (가정값)
K = 100

# 평형 계산 함수
def equilibrium(x):
    a = cro4_conc - 2 * x
    b = h_conc - 2 * x
    if a <= 0 or b <= 0:
        return 1e6
    return (x / (a**2 * b**2)) - K

# 가능한 반응 정도 x의 최대치
x_max = min(cro4_conc / 2, h_conc / 2)


if x_max <= 0:
    st.error("NULL")
    st.stop()

# 수치적 해 찾기
try:
    sol = root_scalar(equilibrium, bracket=[0, x_max], method='bisect')
    if not sol.converged:
        raise ValueError
    x_eq = sol.root
except:
    st.error("NULL")
    st.stop()

# 평형 농도 계산
cro4_eq = cro4_conc - 2 * x_eq
h_eq = h_conc - 2 * x_eq
cr2o7_eq = x_eq

# 결과 출력
st.markdown("### 평형 농도 결과")
st.write(f"• [H₂SO₄]: {h2so4_conc:.4f} M → 공급 H⁺: {2*h2so4_conc:.4f} M")
st.write(f"• [NaOH]: {naoh_conc:.4f} M → 중화된 H⁺: {naoh_conc:.4f} M")
st.write(f"• 초기 [H⁺]: {h_conc:.4e} M  (pH ≈ {ph:.2f})")
st.write(f"• 평형 [CrO₄²⁻]: {cro4_eq:.4f} M")
st.write(f"• 평형 [H⁺]: {h_eq:.4e} M")
st.write(f"• 평형 [Cr₂O₇²⁻]: {cr2o7_eq:.4f} M")

# 색상 예측 (비율 기반)
ratio = cr2o7_eq / (cro4_eq + 1e-8)
if ratio > 2:
    color = "주황"
elif ratio < 0.5:
    color = "노랑"
else:
    color = "혼합색 (주황-노랑 중간)"

st.markdown(f"### 용액 색상 예측: **{color}**")

# 평형 이동 해설
if 2*h2so4_conc > naoh_conc:
    st.success("산이 많아져 정반응 → 주황색 (Cr₂O₇²⁻ 증가)")
elif naoh_conc > 2*h2so4_conc:
    st.info("염기가 많아져 역반응 → 노란색 (CrO₄²⁻ 증가)")
else:
    st.write("산-염기 균형 상태: 평형 유지")

# 상수 안내
st.markdown(f"### 평형 상수 (K): {K}")
st.caption("※ 이 값은 시뮬레이션을 위해 임의로 설정한 상수입니다.")
