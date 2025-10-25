"""
UI 컴포넌트 모듈
로또 번호 시각화 및 재사용 가능한 UI 컴포넌트를 제공합니다.
"""

import streamlit as st
from typing import List
import base64


def render_lotto_ball(number: int, color: str = '#4169E1'):
    """로또 공 스타일의 번호를 렌더링합니다."""
    ball_html = f"""<div style="display: inline-block; width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, {color} 0%, {color}dd 100%); color: white; font-size: 24px; font-weight: bold; text-align: center; line-height: 60px; margin: 5px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3), inset 0 -2px 4px rgba(0, 0, 0, 0.2); border: 3px solid rgba(255, 255, 255, 0.3);">{number}</div>"""
    return ball_html


def render_recommendation_card(recommendation: dict):
    """추천 번호 카드를 렌더링합니다."""
    name = recommendation['name']
    mathematician = recommendation['mathematician']
    color = recommendation['color']
    description = recommendation['description']
    numbers = recommendation['numbers']
    reasoning = recommendation['reasoning']
    
    # 로또 공 HTML 생성
    balls_html = "".join([render_lotto_ball(num, color) for num in numbers])
    
    card_html = f"""<div style="border: 2px solid {color}; border-radius: 15px; padding: 20px; margin: 15px 0; background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h3 style="color: {color}; margin-top: 0;">{name}</h3>
        <p style="color: #888; font-size: 14px; margin: 5px 0;"><strong>{mathematician}</strong> · {description}</p>
        <div style="text-align: center; margin: 20px 0;">{balls_html}</div>
        <p style="background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; font-size: 13px; color: #ccc; margin: 10px 0 0 0;">💡 {reasoning}</p>
    </div>"""
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_statistics_summary(stats: dict):
    """통계 요약 정보를 렌더링합니다."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 회차", f"{stats.get('total_draws', 0):,}")
    
    with col2:
        odd_ratio = stats.get('odd_even', {}).get('odd_ratio', 0)
        st.metric("홀수 비율", f"{odd_ratio*100:.1f}%")
    
    with col3:
        low_ratio = stats.get('high_low', {}).get('low_ratio', 0)
        st.metric("저(1-22) 비율", f"{low_ratio*100:.1f}%")
    
    with col4:
        latest = stats.get('latest_draw', 0)
        st.metric("최신 회차", f"{latest}")


def render_number_grid(numbers: List[int], frequency: dict):
    """번호를 그리드 형태로 표시합니다."""
    max_freq = max(frequency.values()) if frequency else 1
    
    html = "<div style='display: grid; grid-template-columns: repeat(9, 1fr); gap: 5px;'>"
    
    for num in range(1, 46):
        freq = frequency.get(num, 0)
        opacity = 0.3 + (freq / max_freq * 0.7) if max_freq > 0 else 0.3
        
        selected = "border: 3px solid #FFD700;" if num in numbers else ""
        
        html += f"""
        <div style="
            background: rgba(65, 105, 225, {opacity});
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 8px;
            font-weight: bold;
            {selected}
        ">
            {num}<br><span style="font-size: 10px;">{freq}</span>
        </div>
        """
    
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def get_download_link(data: str, filename: str, text: str):
    """다운로드 링크를 생성합니다."""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href


def apply_custom_css():
    """커스텀 CSS를 적용합니다."""
    st.markdown("""
    <style>
        /* 전체 페이지 스타일 */
        .main {
            background-color: #0E1117;
        }
        
        /* 헤더 스타일 */
        h1 {
            color: #FAFAFA;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        h2 {
            color: #FAFAFA;
            border-bottom: 2px solid #4169E1;
            padding-bottom: 10px;
        }
        
        h3 {
            color: #FAFAFA;
        }
        
        /* 사이드바 스타일 */
        .css-1d391kg {
            background-color: #1E1E1E;
        }
        
        /* 버튼 스타일 */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* 탭 스타일 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: #1E1E1E;
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: bold;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* 메트릭 카드 스타일 */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: bold;
        }
        
        /* 프로그레스 바 */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* 데이터프레임 스타일 */
        .dataframe {
            font-size: 14px;
        }
        
        /* 성공 메시지 */
        .stSuccess {
            background-color: rgba(50, 205, 50, 0.1);
            border-left: 4px solid #32CD32;
        }
        
        /* 경고 메시지 */
        .stWarning {
            background-color: rgba(255, 215, 0, 0.1);
            border-left: 4px solid #FFD700;
        }
        
        /* 에러 메시지 */
        .stError {
            background-color: rgba(255, 69, 0, 0.1);
            border-left: 4px solid #FF4500;
        }
    </style>
    """, unsafe_allow_html=True)


def render_fibonacci_visualization():
    """피보나치 수열 시각화"""
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    html = '<div style="text-align: center; padding: 20px;"><h4 style="color: #FFD700;">피보나치 수열</h4><div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">'
    
    for i, num in enumerate(fib):
        size = 30 + (i * 5)
        html += f'<div style="width: {size}px; height: {size}px; border-radius: 50%; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: white; display: inline-flex; align-items: center; justify-content: center; margin: 5px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">{num}</div>'
        
        if i < len(fib) - 1:
            html += '<span style="color: #FFD700; font-size: 20px; margin: 0 5px;">→</span>'
    
    html += '</div><p style="color: #ccc; margin-top: 20px;">각 숫자는 이전 두 숫자의 합. 황금비 φ ≈ 1.618로 수렴</p></div>'
    
    return html


def render_pascal_triangle():
    """파스칼 삼각형 시각화"""
    rows = 6
    from math import comb
    
    html = '<div style="text-align: center; padding: 20px;"><h4 style="color: #4169E1;">파스칼 삼각형</h4><div style="display: flex; flex-direction: column; align-items: center;">'
    
    for n in range(rows):
        html += '<div style="display: flex; justify-content: center; margin: 5px 0;">'
        
        for k in range(n + 1):
            value = comb(n, k)
            html += f'<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #4169E1 0%, #1E90FF 100%); color: white; display: inline-flex; align-items: center; justify-content: center; margin: 3px; border-radius: 8px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">{value}</div>'
        
        html += '</div>'
    
    html += '</div><p style="color: #ccc; margin-top: 20px;">각 수는 바로 위 두 수의 합. 조합 계수 C(n,k) 표현</p></div>'
    
    return html


def render_fermat_primes():
    """페르마 소수 시각화"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    
    html = '<div style="text-align: center; padding: 20px;"><h4 style="color: #32CD32;">1-45 범위의 소수</h4><div style="display: flex; justify-content: center; flex-wrap: wrap; max-width: 600px; margin: 0 auto;">'
    
    for prime in primes:
        html += f'<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #32CD32 0%, #228B22 100%); color: white; display: inline-flex; align-items: center; justify-content: center; margin: 5px; border-radius: 50%; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">{prime}</div>'
    
    html += f'</div><p style="color: #ccc; margin-top: 20px;">총 {len(primes)}개의 소수. 페르마 소정리: a^(p-1) ≡ 1 (mod p)</p></div>'
    
    return html
