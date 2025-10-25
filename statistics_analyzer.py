"""
통계 분석 모듈
로또 데이터의 다양한 통계 분석 기능을 제공합니다.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
from config import LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER


class StatisticsAnalyzer:
    """로또 데이터 통계 분석 클래스"""
    
    def __init__(self, lotto_data: Dict[int, Dict]):
        self.lotto_data = lotto_data
        self.df = self._create_dataframe()
        
    def _create_dataframe(self) -> pd.DataFrame:
        """로또 데이터를 DataFrame으로 변환"""
        data_list = []
        for draw_no, draw_data in sorted(self.lotto_data.items()):
            row = {
                'draw_no': draw_no,
                'draw_date': draw_data.get('draw_date'),
                'bonus': draw_data.get('bonus')
            }
            for i, num in enumerate(draw_data['numbers'], 1):
                row[f'num{i}'] = num
            data_list.append(row)
        
        return pd.DataFrame(data_list)
    
    def get_number_frequency(self, recent_n: int = None) -> pd.Series:
        """번호별 출현 빈도를 계산합니다."""
        if recent_n:
            df = self.df.tail(recent_n)
        else:
            df = self.df
        
        all_numbers = []
        for col in ['num1', 'num2', 'num3', 'num4', 'num5', 'num6']:
            all_numbers.extend(df[col].tolist())
        
        frequency = Counter(all_numbers)
        
        # 모든 번호를 포함하도록 보완
        for num in range(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER + 1):
            if num not in frequency:
                frequency[num] = 0
        
        return pd.Series(frequency).sort_index()
    
    def plot_frequency_chart(self, recent_n: int = None):
        """번호별 출현 빈도 차트를 생성합니다."""
        frequency = self.get_number_frequency(recent_n)
        
        fig = go.Figure(data=[
            go.Bar(
                x=frequency.index.tolist(),
                y=frequency.values.tolist(),
                marker_color='lightblue',
                text=frequency.values.tolist(),
                textposition='auto',
            )
        ])
        
        title = f"번호별 출현 빈도"
        if recent_n:
            title += f" (최근 {recent_n}회차)"
        
        fig.update_layout(
            title=title,
            xaxis_title="번호",
            yaxis_title="출현 횟수",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def get_odd_even_ratio(self, recent_n: int = None) -> Dict:
        """홀짝 비율을 계산합니다."""
        if recent_n:
            df = self.df.tail(recent_n)
        else:
            df = self.df
        
        all_numbers = []
        for col in ['num1', 'num2', 'num3', 'num4', 'num5', 'num6']:
            all_numbers.extend(df[col].tolist())
        
        odd_count = sum(1 for num in all_numbers if num % 2 == 1)
        even_count = len(all_numbers) - odd_count
        
        return {
            'odd_count': odd_count,
            'even_count': even_count,
            'odd_ratio': odd_count / len(all_numbers) if all_numbers else 0,
            'even_ratio': even_count / len(all_numbers) if all_numbers else 0
        }
    
    def get_high_low_ratio(self, recent_n: int = None) -> Dict:
        """고저 비율을 계산합니다 (1-22: 저, 23-45: 고)."""
        if recent_n:
            df = self.df.tail(recent_n)
        else:
            df = self.df
        
        all_numbers = []
        for col in ['num1', 'num2', 'num3', 'num4', 'num5', 'num6']:
            all_numbers.extend(df[col].tolist())
        
        low_count = sum(1 for num in all_numbers if num <= 22)
        high_count = len(all_numbers) - low_count
        
        return {
            'low_count': low_count,
            'high_count': high_count,
            'low_ratio': low_count / len(all_numbers) if all_numbers else 0,
            'high_ratio': high_count / len(all_numbers) if all_numbers else 0
        }
    
    def get_range_distribution(self, recent_n: int = None) -> Dict:
        """구간별 분포를 계산합니다 (1-15, 16-30, 31-45)."""
        if recent_n:
            df = self.df.tail(recent_n)
        else:
            df = self.df
        
        all_numbers = []
        for col in ['num1', 'num2', 'num3', 'num4', 'num5', 'num6']:
            all_numbers.extend(df[col].tolist())
        
        range1 = sum(1 for num in all_numbers if 1 <= num <= 15)
        range2 = sum(1 for num in all_numbers if 16 <= num <= 30)
        range3 = sum(1 for num in all_numbers if 31 <= num <= 45)
        
        total = len(all_numbers)
        
        return {
            'range1_count': range1,
            'range2_count': range2,
            'range3_count': range3,
            'range1_ratio': range1 / total if total else 0,
            'range2_ratio': range2 / total if total else 0,
            'range3_ratio': range3 / total if total else 0
        }
    
    def plot_distribution_pie_charts(self, recent_n: int = None):
        """분포 파이 차트를 생성합니다."""
        odd_even = self.get_odd_even_ratio(recent_n)
        high_low = self.get_high_low_ratio(recent_n)
        range_dist = self.get_range_distribution(recent_n)
        
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=1, cols=3,
            specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]],
            subplot_titles=('홀짝 비율', '고저 비율', '구간별 분포')
        )
        
        # 홀짝
        fig.add_trace(
            go.Pie(labels=['홀수', '짝수'], 
                   values=[odd_even['odd_count'], odd_even['even_count']],
                   marker_colors=['#FF6B6B', '#4ECDC4']),
            row=1, col=1
        )
        
        # 고저
        fig.add_trace(
            go.Pie(labels=['저(1-22)', '고(23-45)'], 
                   values=[high_low['low_count'], high_low['high_count']],
                   marker_colors=['#95E1D3', '#F38181']),
            row=1, col=2
        )
        
        # 구간별
        fig.add_trace(
            go.Pie(labels=['1-15', '16-30', '31-45'], 
                   values=[range_dist['range1_count'], range_dist['range2_count'], range_dist['range3_count']],
                   marker_colors=['#A8E6CF', '#FFD3B6', '#FFAAA5']),
            row=1, col=3
        )
        
        title = "번호 분포 분석"
        if recent_n:
            title += f" (최근 {recent_n}회차)"
        
        fig.update_layout(
            title_text=title,
            height=400,
            showlegend=True
        )
        
        return fig
    
    def get_consecutive_patterns(self, recent_n: int = None) -> Dict:
        """연속 번호 출현 패턴을 분석합니다."""
        if recent_n:
            df = self.df.tail(recent_n)
        else:
            df = self.df
        
        consecutive_counts = {0: 0, 1: 0, 2: 0, 3: 0}  # 연속 쌍의 개수
        
        for _, row in df.iterrows():
            numbers = sorted([row[f'num{i}'] for i in range(1, 7)])
            consecutive_pairs = 0
            for i in range(len(numbers) - 1):
                if numbers[i + 1] - numbers[i] == 1:
                    consecutive_pairs += 1
            
            if consecutive_pairs <= 3:
                consecutive_counts[consecutive_pairs] += 1
            else:
                consecutive_counts[3] += 1
        
        return consecutive_counts
    
    def plot_consecutive_patterns(self, recent_n: int = None):
        """연속 번호 패턴 차트를 생성합니다."""
        patterns = self.get_consecutive_patterns(recent_n)
        
        labels = ['없음', '1쌍', '2쌍', '3쌍 이상']
        values = [patterns[i] for i in range(4)]
        
        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
                text=values,
                textposition='auto'
            )
        ])
        
        title = "연속 번호 출현 패턴"
        if recent_n:
            title += f" (최근 {recent_n}회차)"
        
        fig.update_layout(
            title=title,
            xaxis_title="연속 번호 쌍의 개수",
            yaxis_title="출현 횟수",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def get_recent_trend(self, recent_n: int = 100) -> pd.DataFrame:
        """최근 N회차의 트렌드를 분석합니다."""
        df = self.df.tail(recent_n)
        
        trend_data = []
        for _, row in df.iterrows():
            numbers = [row[f'num{i}'] for i in range(1, 7)]
            trend_data.append({
                'draw_no': row['draw_no'],
                'avg': np.mean(numbers),
                'std': np.std(numbers),
                'min': min(numbers),
                'max': max(numbers),
                'range': max(numbers) - min(numbers)
            })
        
        return pd.DataFrame(trend_data)
    
    def plot_trend_chart(self, recent_n: int = 100):
        """트렌드 차트를 생성합니다."""
        trend_df = self.get_recent_trend(recent_n)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_df['draw_no'],
            y=trend_df['avg'],
            mode='lines+markers',
            name='평균',
            line=dict(color='#4169E1', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_df['draw_no'],
            y=trend_df['min'],
            mode='lines',
            name='최소값',
            line=dict(color='#32CD32', width=1, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_df['draw_no'],
            y=trend_df['max'],
            mode='lines',
            name='최대값',
            line=dict(color='#FFD700', width=1, dash='dash')
        ))
        
        fig.update_layout(
            title=f"당첨번호 트렌드 분석 (최근 {recent_n}회차)",
            xaxis_title="회차",
            yaxis_title="번호",
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def get_summary_statistics(self) -> Dict:
        """전체 통계 요약 정보를 반환합니다."""
        total_draws = len(self.df)
        frequency = self.get_number_frequency()
        
        most_common = frequency.nlargest(5)
        least_common = frequency.nsmallest(5)
        
        odd_even = self.get_odd_even_ratio()
        high_low = self.get_high_low_ratio()
        range_dist = self.get_range_distribution()
        
        return {
            'total_draws': total_draws,
            'most_common': most_common.to_dict(),
            'least_common': least_common.to_dict(),
            'odd_even': odd_even,
            'high_low': high_low,
            'range_distribution': range_dist,
            'latest_draw': self.df['draw_no'].max() if not self.df.empty else 0
        }
