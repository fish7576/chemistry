import streamlit as st
import numpy as np
from scipy.optimize import fsolve

st.markdown("**반응식:** 2CrO₄²⁻ + 2H⁺ ⇌ Cr₂O₇²⁻ + H₂O")
st.markdown("pH를 조절해 평형 이동을 관찰(산: 정반응, 염기: 역반응)")

# 입력: 초기 CrO₄²⁻ 농도
cro4_conc = st.slider("[CrO₄²⁻] 초기 농도 (M)", 0.01, 1.0, 0.5, 0.01)

# 입력: pH 슬라이더
ph = st.slider("pH 조절 (산 ↔ 염기)", 0.0, 14.0, 7.0, 0.1)
h_conc = 10 ** (-ph)  # [H⁺] 계산

# 평형 상수 (온도 일정하다고 가정)
K = 100  # 크기만 임의로 설정 (정반응 우세)

# 평형 계산 함수
def equilibrium(x):
    try:
        return K - (x / ((cro4_conc - 2 * x) ** 2 * (h_conc - 2 * x) ** 2))
    except:
        return 1e6

# 평형점 계산
try:
    x_eq = fsolve(equilibrium, 0.0)[0]
    if x_eq < 0 or cro4_conc - 2 * x_eq < 0 or h_conc - 2 * x_eq < 0:
        raise ValueError
except:
    st.error("❌ 평형 계산 실패: 입력값이 비현실적입니다.")
    st.stop()

# 평형 농도 계산
cro4_eq = cro4_conc - 2 * x_eq
h_eq = h_conc - 2 * x_eq
cr2o7_eq = x_eq

# 결과 요약 출력
st.markdown("###  평형 농도 결과")
st.write(f"• 초기 [CrO₄²⁻]: {cro4_conc:.4f} M")
st.write(f"• 초기 [H⁺] (pH {ph:.1f}): {h_conc:.4e} M")
st.markdown("---")
st.write(f"• 평형 [CrO₄²⁻]: {cro4_eq:.4f} M")
st.write(f"• 평형 [H⁺]: {h_eq:.4e} M")
st.write(f"• 평형 [Cr₂O₇²⁻]: {cr2o7_eq:.4f} M")
st.markdown("---")

# 용액 색상 정보
color = "orange" if ph < 7 else "yellow"
st.markdown(f"###  용액 색상: **{color.capitalize()}**")

# 평형 이동 해설
if ph < 7:
    st.success("pH ↓ (산 첨가): **정반응** → Cr₂O₇²⁻ 증가 (주황색)")
elif ph > 7:
    st.info("pH ↑ (염기 첨가): **역반응** → CrO₄²⁻ 증가 (노란색)")
else:
    st.error("pH = 7 (중성): **평형 유지 상태**")

# 평형 상수 값 출력
st.markdown(f"###  평형 상수 (K): {K}")
st.caption("※  평형상수 임의로 지정")
