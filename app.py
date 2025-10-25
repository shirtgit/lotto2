"""
로또 번호 분석 및 추천 시스템
천재 수학자들의 이론을 기반으로 한 로또 번호 추천 Streamlit 앱
"""

import streamlit as st
import pandas as pd
from data_collector import get_collector
from algorithms import LottoAlgorithms
from statistics_analyzer import StatisticsAnalyzer
from ui_components import (
    apply_custom_css, 
    render_recommendation_card,
    render_statistics_summary,
    get_download_link
)
from mathematical_background import render_mathematical_background, render_combined_approach
from config import MAX_DRAW_NUMBER, MIN_DRAW_NUMBER
import json


# 페이지 설정
st.set_page_config(
    page_title="천재 수학자의 로또 추천 시스템",
    page_icon="icon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 적용
apply_custom_css()


def initialize_session_state():
    """세션 상태 초기화"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'lotto_data' not in st.session_state:
        st.session_state.lotto_data = {}
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []


def render_header():
    """헤더 렌더링"""
    import base64
    import os
    
    # 로고 이미지 인코딩
    logo_html = ""
    if os.path.exists("icon.ico"):
        with open("icon.ico", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/x-icon;base64,{logo_data}" style="width: 80px; height: 80px; margin-bottom: 10px;">'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        {logo_html}
        <h1>🎰 천재 수학자의 로또 번호 추천 시스템</h1>
        <p style="font-size: 18px; color: #888;">
            피보나치, 파스칼, 페르마의 천재적 사고방식으로
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("## 📊 데이터 관리")
        
        collector = get_collector()
        
        # 캐시된 데이터 확인
        if collector.load_cache():
            st.success(f"✅ 캐시된 데이터: {len(collector.data)}회차")
            st.session_state.lotto_data = collector.data
            st.session_state.data_loaded = True
        
        # 데이터 수집 버튼
        col1, col2 = st.columns(2)
        
        with col1:
            start_draw = st.number_input(
                "시작 회차", 
                min_value=MIN_DRAW_NUMBER, 
                max_value=MAX_DRAW_NUMBER,
                value=MIN_DRAW_NUMBER
            )
        
        with col2:
            end_draw = st.number_input(
                "종료 회차",
                min_value=MIN_DRAW_NUMBER,
                max_value=MAX_DRAW_NUMBER,
                value=MAX_DRAW_NUMBER
            )
        
        if st.button("🔄 데이터 수집/업데이트", use_container_width=True):
            with st.spinner("데이터 수집 중..."):
                progress_bar = st.progress(0)
                collector.collect_all_data(start_draw, end_draw, progress_bar)
                st.session_state.lotto_data = collector.data
                st.session_state.data_loaded = True
                progress_bar.progress(100)
                st.success(f"✅ {len(collector.data)}회차 데이터 수집 완료!")
        
        # 기본 통계 표시
        if st.session_state.data_loaded and st.session_state.lotto_data:
            st.markdown("---")
            st.markdown("## 📈 기본 통계")
            
            stats = collector.get_statistics()
            
            st.metric("총 회차", f"{stats.get('total_draws', 0):,}")
            st.metric("최신 회차", f"{stats.get('latest_draw', 0)}")
            
            col1, col2 = st.columns(2)
            with col1:
                odd_ratio = stats.get('odd_ratio', 0)
                st.metric("홀수", f"{odd_ratio*100:.1f}%")
            with col2:
                even_ratio = stats.get('even_ratio', 0)
                st.metric("짝수", f"{even_ratio*100:.1f}%")
            
            col1, col2 = st.columns(2)
            with col1:
                low_ratio = stats.get('low_ratio', 0)
                st.metric("저(1-22)", f"{low_ratio*100:.1f}%")
            with col2:
                high_ratio = stats.get('high_ratio', 0)
                st.metric("고(23-45)", f"{high_ratio*100:.1f}%")
        
        # 정보
        st.markdown("---")
        st.markdown("## ℹ️ 정보")
        st.info("""
        이 시스템은 세 명의 위대한 수학자의 이론을 활용합니다:
        
        🟡 **피보나치**: 자연의 조화  
        🔵 **파스칼**: 확률의 정교함  
        🟢 **페르마**: 정수의 본질
        """)


def render_recommendations_tab():
    """추천 번호 탭 렌더링"""
    st.markdown("## 🎲 AI 추천 번호")
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ 먼저 사이드바에서 데이터를 수집해주세요.")
        return
    
    if not st.session_state.lotto_data:
        st.error("❌ 로또 데이터가 없습니다.")
        return
    
    # 추천 생성 버튼
    if st.button("✨ 번호 생성하기", use_container_width=True, type="primary"):
        with st.spinner("천재들의 사고방식으로 번호를 계산 중..."):
            algorithms = LottoAlgorithms(st.session_state.lotto_data)
            st.session_state.recommendations = algorithms.get_all_recommendations()
        st.success("✅ 5개 세트 생성 완료!")
    
    # 추천 번호 표시
    if st.session_state.recommendations:
        st.markdown("---")
        
        for recommendation in st.session_state.recommendations:
            render_recommendation_card(recommendation)
        
        # CSV 다운로드
        st.markdown("---")
        st.markdown("### 📥 다운로드")
        
        # CSV 데이터 생성
        csv_data = "세트,수학자,방법,번호1,번호2,번호3,번호4,번호5,번호6,설명\n"
        for i, rec in enumerate(st.session_state.recommendations, 1):
            nums = rec['numbers']
            csv_data += f"{i},{rec['mathematician']},{rec['name']},"
            csv_data += f"{nums[0]},{nums[1]},{nums[2]},{nums[3]},{nums[4]},{nums[5]},"
            csv_data += f"\"{rec['reasoning']}\"\n"
        
        st.download_button(
            label="📊 CSV 다운로드",
            data=csv_data,
            file_name="lotto_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # JSON 다운로드
        json_data = json.dumps(st.session_state.recommendations, ensure_ascii=False, indent=2)
        st.download_button(
            label="📄 JSON 다운로드",
            data=json_data,
            file_name="lotto_recommendations.json",
            mime="application/json",
            use_container_width=True
        )


def render_statistics_tab():
    """통계 분석 탭 렌더링"""
    st.markdown("## 📊 통계 분석")
    
    if not st.session_state.data_loaded or not st.session_state.lotto_data:
        st.warning("⚠️ 먼저 사이드바에서 데이터를 수집해주세요.")
        return
    
    analyzer = StatisticsAnalyzer(st.session_state.lotto_data)
    
    # 분석 범위 선택
    st.markdown("### 분석 범위 선택")
    analysis_range = st.radio(
        "분석할 데이터 범위를 선택하세요",
        ["전체", "최근 50회차", "최근 100회차"],
        horizontal=True
    )
    
    recent_n = None
    if analysis_range == "최근 50회차":
        recent_n = 50
    elif analysis_range == "최근 100회차":
        recent_n = 100
    
    # 번호별 출현 빈도
    st.markdown("---")
    st.markdown("### 📈 번호별 출현 빈도")
    freq_chart = analyzer.plot_frequency_chart(recent_n)
    st.plotly_chart(freq_chart, use_container_width=True)
    
    # 가장 많이/적게 나온 번호
    frequency = analyzer.get_number_frequency(recent_n)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 가장 많이 나온 번호 Top 10")
        top_10 = frequency.nlargest(10)
        for num, count in top_10.items():
            st.markdown(f"**{num}번**: {count}회")
    
    with col2:
        st.markdown("#### 🧊 가장 적게 나온 번호 Top 10")
        bottom_10 = frequency.nsmallest(10)
        for num, count in bottom_10.items():
            st.markdown(f"**{num}번**: {count}회")
    
    # 분포 분석
    st.markdown("---")
    st.markdown("### 📊 번호 분포 분석")
    dist_chart = analyzer.plot_distribution_pie_charts(recent_n)
    st.plotly_chart(dist_chart, use_container_width=True)
    
    # 연속 번호 패턴
    st.markdown("---")
    st.markdown("### 🔗 연속 번호 출현 패턴")
    consecutive_chart = analyzer.plot_consecutive_patterns(recent_n)
    st.plotly_chart(consecutive_chart, use_container_width=True)
    
    # 트렌드 분석
    st.markdown("---")
    st.markdown("### 📉 최근 트렌드")
    trend_n = st.slider("트렌드 분석 회차", 20, 200, 100, 10)
    trend_chart = analyzer.plot_trend_chart(trend_n)
    st.plotly_chart(trend_chart, use_container_width=True)
    
    # 통계 요약
    st.markdown("---")
    st.markdown("### 📋 통계 요약")
    summary = analyzer.get_summary_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 홀짝 비율")
        odd_even = summary['odd_even']
        st.metric("홀수", f"{odd_even['odd_ratio']*100:.1f}%")
        st.metric("짝수", f"{odd_even['even_ratio']*100:.1f}%")
    
    with col2:
        st.markdown("#### 고저 비율")
        high_low = summary['high_low']
        st.metric("저(1-22)", f"{high_low['low_ratio']*100:.1f}%")
        st.metric("고(23-45)", f"{high_low['high_ratio']*100:.1f}%")
    
    with col3:
        st.markdown("#### 구간별 분포")
        range_dist = summary['range_distribution']
        st.metric("1-15", f"{range_dist['range1_ratio']*100:.1f}%")
        st.metric("16-30", f"{range_dist['range2_ratio']*100:.1f}%")
        st.metric("31-45", f"{range_dist['range3_ratio']*100:.1f}%")


def render_background_tab():
    """수학적 배경 탭 렌더링"""
    render_mathematical_background()
    render_combined_approach()


def main():
    """메인 함수"""
    # 세션 상태 초기화
    initialize_session_state()
    
    # 헤더 렌더링
    render_header()
    
    # 사이드바 렌더링
    render_sidebar()
    
    # 메인 탭
    tab1, tab2, tab3 = st.tabs(["🎲 추천 번호", "📊 통계 분석", "📚 수학적 배경"])
    
    with tab1:
        render_recommendations_tab()
    
    with tab2:
        render_statistics_tab()
    
    with tab3:
        render_background_tab()
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 20px;">
        <p><strong>천재들의 사고방식으로 행운을 계산하다</strong></p>
        <p style="font-size: 12px;">
            본 시스템은 교육 및 연구 목적으로 제작되었습니다.<br>
            로또는 확률 게임이며, 당첨을 보장하지 않습니다.
        </p>
        <p style="font-size: 11px; margin-top: 15px; color: #666;">
            © 2025 쇼쇼 (shirtgit). All rights reserved.<br>
            Made with ❤️ and 🧮
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
