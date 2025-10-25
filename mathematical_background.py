"""
수학적 배경 설명 모듈
각 알고리즘의 수학적 배경과 이론을 설명합니다.
"""

import streamlit as st
from ui_components import render_fibonacci_visualization, render_pascal_triangle, render_fermat_primes


def render_mathematical_background():
    """수학적 배경 탭의 전체 내용을 렌더링합니다."""
    
    st.markdown("## 천재 수학자들의 이론")
    
    st.markdown("""
    로또 번호 추천 시스템은 세 명의 위대한 수학자의 이론을 기반으로 합니다.
    각 이론이 어떻게 로또 번호 선택에 적용되는지 알아보세요.
    """)
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🟡 피보나치", "🔵 파스칼", "🟢 페르마"])
    
    with tab1:
        render_fibonacci_section()
    
    with tab2:
        render_pascal_section()
    
    with tab3:
        render_fermat_section()


def render_fibonacci_section():
    """피보나치 섹션"""
    st.markdown("### 레오나르도 피보나치 (Leonardo Fibonacci, 1170-1250)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        #### 피보나치 수열이란?
        
        이탈리아 수학자 피보나치가 발견한 수열로, 각 숫자는 바로 앞 두 숫자의 합입니다.
        
        **수열:** 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...
        
        **수식:** F(n) = F(n-1) + F(n-2)
        
        #### 황금비 (Golden Ratio, φ)
        
        피보나치 수열의 연속된 두 항의 비율은 황금비 φ ≈ 1.618에 수렴합니다.
        
        ```
        φ = (1 + √5) / 2 ≈ 1.618033988749895
        ```
        
        #### 자연에서의 피보나치
        
        - 🌻 해바라기 씨앗의 나선 배열
        - 🐚 앵무조개 껍데기의 나선
        - 🌿 식물 잎의 배열 패턴
        - 🌌 은하의 나선 구조
        
        #### 로또 적용 방법
        
        1. **직접 선택**: 1~45 범위의 피보나치 수를 직접 선택
        2. **황금비 구간**: 1~45를 황금비로 나누어 조화로운 위치 선택
        3. **빈도 분석**: 과거 데이터에서 피보나치 수의 출현 패턴 분석
        4. **자연의 조화**: 가장 자연스럽고 균형잡힌 번호 조합 생성
        """)
    
    with col2:
        st.markdown("#### 특징")
        st.info("""
        ✨ **자연의 성장 패턴**
        
        피보나치 수열은 자연의 가장 기본적인 성장 법칙입니다.
        
        🎯 **조화와 균형**
        
        황금비는 가장 아름답고 균형잡힌 비율로 알려져 있습니다.
        """)
    
    # 시각화
    st.markdown("---")
    st.markdown(render_fibonacci_visualization(), unsafe_allow_html=True)
    
    # 실제 적용 예시
    st.markdown("#### 💡 실제 적용 예시")
    st.code("""
# 1~45 범위의 피보나치 수
fibonacci_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34]

# 황금비를 이용한 위치 계산
phi = 1.618033988749895
positions = []
for i in range(1, 7):
    pos = int(45 * (i / (1 + phi)))
    positions.append(pos)
# 결과: [17, 27, 33, 37, 40, 42]
    """, language="python")


def render_pascal_section():
    """파스칼 섹션"""
    st.markdown("### 블레즈 파스칼 (Blaise Pascal, 1623-1662)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        #### 파스칼 삼각형이란?
        
        프랑스 수학자 블레즈 파스칼이 연구한 삼각형 형태의 수 배열입니다.
        각 수는 바로 위의 두 수를 더한 값입니다.
        
        #### 조합 계수 (Binomial Coefficient)
        
        파스칼 삼각형의 각 수는 조합 계수 C(n, r)을 나타냅니다.
        
        ```
        C(n, r) = n! / (r! × (n-r)!)
        ```
        
        #### 확률론의 탄생
        
        파스칼은 페르마와의 서신 교환을 통해 확률론을 창시했습니다.
        
        - 🎲 도박 문제 해결
        - 📊 이항분포 발견
        - 🎯 기댓값 개념 정립
        - ⚖️ 의사결정 이론
        
        #### 로또 적용 방법
        
        **방법 1: 조합론적 접근**
        1. 파스칼 삼각형의 계수를 1~45로 매핑
        2. 과거 데이터의 동반 출현 빈도 분석
        3. 조합론적으로 가장 균형잡힌 6개 선택
        
        **방법 2: 확률적 분포**
        1. 각 번호의 출현 확률을 이항분포로 모델링
        2. 홀짝, 고저, 구간별 균형 최적화
        3. 기댓값 계산으로 다음 번호 예측
        """)
    
    with col2:
        st.markdown("#### 특징")
        st.info("""
        🎲 **확률의 정교함**
        
        우연은 없습니다. 오직 계산된 확률만이 존재합니다.
        
        ⚖️ **완벽한 균형**
        
        모든 가능성을 계산하고 가장 균형잡힌 조합을 선택합니다.
        """)
    
    # 시각화
    st.markdown("---")
    st.markdown(render_pascal_triangle(), unsafe_allow_html=True)
    
    # 실제 적용 예시
    st.markdown("#### 💡 실제 적용 예시")
    st.code("""
from scipy.special import comb

# 파스칼 삼각형 10번째 행
row = 10
pascal_row = [int(comb(row, k)) for k in range(row + 1)]
# 결과: [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]

# 1-45 범위로 매핑
mapped = [(val % 45) + 1 for val in pascal_row]

# 기댓값 계산
probabilities = {num: freq/total for num, freq in frequency.items()}
expected_values = {num: prob * num for num, prob in probabilities.items()}
    """, language="python")


def render_fermat_section():
    """페르마 섹션"""
    st.markdown("### 피에르 드 페르마 (Pierre de Fermat, 1607-1665)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        #### 페르마 소정리 (Fermat's Little Theorem)
        
        프랑스 수학자 피에르 드 페르마가 발견한 정수론의 기본 정리입니다.
        
        **정리:** p가 소수이고 a가 p의 배수가 아니면,
        
        ```
        a^(p-1) ≡ 1 (mod p)
        ```
        
        #### 소수의 특별한 성질
        
        소수는 1과 자기 자신으로만 나누어지는 2 이상의 자연수입니다.
        
        **1~45 범위의 소수:**
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43 (총 14개)
        
        #### 페르마의 마지막 정리 (Fermat's Last Theorem)
        
        n ≥ 3일 때, x^n + y^n = z^n을 만족하는 양의 정수 해가 존재하지 않습니다.
        
        이 정리는 357년간 증명되지 않다가 1995년 앤드루 와일즈에 의해 증명되었습니다.
        
        #### 완전제곱수
        
        어떤 정수를 제곱한 수를 완전제곱수라고 합니다.
        
        **1~45 범위의 완전제곱수:**
        1, 4, 9, 16, 25, 36 (1², 2², 3², 4², 5², 6²)
        
        #### 로또 적용 방법
        
        **방법 1: 소수론**
        1. 페르마 소정리를 이용한 가중치 계산
        2. 소수의 출현 빈도 분석
        3. 소수와 합성수의 균형있는 조합
        
        **방법 2: 거듭제곱**
        1. 완전제곱수의 출현 패턴 분석
        2. 제곱수 간의 차이와 합 계산
        3. 거듭제곱 관계의 번호 쌍 추출
        """)
    
    with col2:
        st.markdown("#### 특징")
        st.info("""
        🔢 **정수의 본질**
        
        소수는 숫자의 원자입니다. 원자의 배열에서 우주의 비밀을 찾습니다.
        
        ⚡ **불가능 속의 가능**
        
        불가능의 증명 속에 가능성이 숨어있습니다.
        """)
    
    # 시각화
    st.markdown("---")
    st.markdown(render_fermat_primes(), unsafe_allow_html=True)
    
    # 실제 적용 예시
    st.markdown("#### 💡 실제 적용 예시")
    st.code("""
def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

# 1-45 범위의 소수
primes = [n for n in range(2, 46) if is_prime(n)]
# 결과: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

# 완전제곱수와 그 차이
squares = [i*i for i in range(1, 7)]  # [1, 4, 9, 16, 25, 36]
differences = [squares[i+1] - squares[i] for i in range(len(squares)-1)]
# 결과: [3, 5, 7, 9, 11] (모두 홀수!)
    """, language="python")
    
    # 페르마의 마지막 정리 설명
    st.markdown("---")
    st.markdown("#### 📜 페르마의 마지막 정리 이야기")
    st.markdown("""
    1637년, 페르마는 디오판토스의 『산술』 여백에 이렇게 썼습니다:
    
    > "나는 이 정리에 대한 놀라운 증명을 발견했으나,  
    > 여백이 부족하여 여기 적을 수 없다."
    
    이 한 줄의 메모는 수학계에 357년간의 숙제를 남겼고,  
    1995년 앤드루 와일즈가 150페이지가 넘는 증명으로 마침내 해결했습니다.
    
    **수학의 아름다움:** 간단해 보이는 문제가 가장 깊은 진리를 담고 있습니다.
    """)


def render_combined_approach():
    """종합 접근법 설명"""
    st.markdown("---")
    st.markdown("## 🎯 종합 접근법: 세 천재의 조화")
    
    st.markdown("""
    이 시스템은 단순히 과거 데이터만을 분석하는 것이 아닙니다.  
    세 명의 천재 수학자가 발견한 자연의 법칙과 수학적 진리를 결합합니다.
    
    ### 왜 이 세 이론인가?
    
    1. **피보나치**: 자연의 성장 패턴과 조화
       - 우주의 기본 구조를 반영
       - 황금비는 가장 안정적인 비율
    
    2. **파스칼**: 확률과 조합의 정교함
       - 모든 경우의 수를 과학적으로 계산
       - 데이터 기반의 최적 조합 도출
    
    3. **페르마**: 정수의 근본적 성질
       - 소수와 제곱수의 특별한 패턴
       - 수학의 가장 깊은 진리 활용
    
    ### 시스템의 철학
    
    > "완전한 무작위는 존재하지 않는다.  
    > 모든 것에는 패턴이 있고, 그 패턴은 수학으로 설명할 수 있다."
    
    이 시스템은 단순한 번호 생성기가 아닙니다.  
    **천재들의 사고방식으로 우주의 조화를 읽어내는 도구**입니다.
    """)
    
    # 3개 컬럼으로 요약
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        ">
            <h4 style="color: white;">🟡 피보나치</h4>
            <p style="color: white; font-size: 14px;">자연의 조화</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4169E1 0%, #1E90FF 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        ">
            <h4 style="color: white;">🔵 파스칼</h4>
            <p style="color: white; font-size: 14px;">확률의 정교함</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #32CD32 0%, #228B22 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        ">
            <h4 style="color: white;">🟢 페르마</h4>
            <p style="color: white; font-size: 14px;">정수의 본질</p>
        </div>
        """, unsafe_allow_html=True)
