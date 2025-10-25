"""
로또 데이터 수집 모듈
동행복권 API로부터 데이터를 수집하고 캐싱하는 기능을 제공합니다.
"""

import requests
import json
import os
from typing import Dict, List, Optional
import time
import streamlit as st
from config import LOTTO_API_URL, MAX_DRAW_NUMBER, MIN_DRAW_NUMBER, CACHE_FILE


class LottoDataCollector:
    """로또 데이터를 수집하고 관리하는 클래스"""
    
    def __init__(self):
        self.api_url = LOTTO_API_URL
        self.cache_file = CACHE_FILE
        self.data: Dict[int, Dict] = {}
        
    def load_cache(self) -> bool:
        """캐시된 데이터를 로드합니다."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.data = {int(k): v for k, v in json.load(f).items()}
                return True
            except Exception as e:
                st.error(f"캐시 로드 실패: {e}")
                return False
        return False
    
    def save_cache(self) -> bool:
        """데이터를 캐시 파일로 저장합니다."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            st.error(f"캐시 저장 실패: {e}")
            return False
    
    def fetch_draw_data(self, draw_no: int) -> Optional[Dict]:
        """특정 회차의 데이터를 API로부터 가져옵니다."""
        params = {
            'method': 'getLottoNumber',
            'drwNo': draw_no
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 정상 응답 확인
            if data.get('returnValue') == 'success':
                return {
                    'draw_no': draw_no,
                    'draw_date': data.get('drwNoDate'),
                    'numbers': sorted([
                        data.get('drwtNo1'),
                        data.get('drwtNo2'),
                        data.get('drwtNo3'),
                        data.get('drwtNo4'),
                        data.get('drwtNo5'),
                        data.get('drwtNo6'),
                    ]),
                    'bonus': data.get('bnusNo'),
                    'first_prize_amount': data.get('firstWinamnt'),
                    'first_prize_winners': data.get('firstPrzwnerCo'),
                }
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            st.warning(f"{draw_no}회차 데이터 가져오기 실패: {e}")
            return None
        except Exception as e:
            st.warning(f"{draw_no}회차 처리 중 오류: {e}")
            return None
    
    def collect_all_data(self, start_draw: int = MIN_DRAW_NUMBER, 
                         end_draw: int = MAX_DRAW_NUMBER,
                         progress_bar=None) -> Dict[int, Dict]:
        """모든 회차의 데이터를 수집합니다."""
        
        # 기존 캐시 로드
        self.load_cache()
        
        total_draws = end_draw - start_draw + 1
        collected = 0
        failed = 0
        
        for draw_no in range(start_draw, end_draw + 1):
            # 이미 캐시에 있으면 스킵
            if draw_no in self.data:
                collected += 1
                if progress_bar:
                    progress_bar.progress(collected / total_draws)
                continue
            
            # API로부터 데이터 수집
            draw_data = self.fetch_draw_data(draw_no)
            
            if draw_data:
                self.data[draw_no] = draw_data
                collected += 1
                
                # 주기적으로 캐시 저장
                if collected % 50 == 0:
                    self.save_cache()
            else:
                failed += 1
                # 연속 실패가 많으면 중단 (미래 회차 도달)
                if failed > 5:
                    break
            
            # 진행률 업데이트
            if progress_bar:
                progress_bar.progress(collected / total_draws)
            
            # API 부하 방지를 위한 딜레이
            time.sleep(0.1)
        
        # 최종 캐시 저장
        self.save_cache()
        
        return self.data
    
    def get_all_numbers(self) -> List[int]:
        """모든 당첨 번호를 평면 리스트로 반환합니다 (보너스 제외)."""
        all_numbers = []
        for draw_data in self.data.values():
            all_numbers.extend(draw_data['numbers'])
        return all_numbers
    
    def get_recent_data(self, count: int) -> Dict[int, Dict]:
        """최근 N회차 데이터를 반환합니다."""
        sorted_draws = sorted(self.data.keys(), reverse=True)
        recent_draws = sorted_draws[:count]
        return {draw: self.data[draw] for draw in recent_draws}
    
    def get_number_frequency(self) -> Dict[int, int]:
        """각 번호의 출현 빈도를 계산합니다."""
        frequency = {i: 0 for i in range(1, 46)}
        for draw_data in self.data.values():
            for num in draw_data['numbers']:
                frequency[num] += 1
        return frequency
    
    def get_bonus_frequency(self) -> Dict[int, int]:
        """보너스 번호의 출현 빈도를 계산합니다."""
        frequency = {i: 0 for i in range(1, 46)}
        for draw_data in self.data.values():
            bonus = draw_data.get('bonus')
            if bonus:
                frequency[bonus] += 1
        return frequency
    
    def get_statistics(self) -> Dict:
        """기본 통계 정보를 반환합니다."""
        if not self.data:
            return {}
        
        total_draws = len(self.data)
        all_numbers = self.get_all_numbers()
        
        # 홀짝 통계
        odd_count = sum(1 for num in all_numbers if num % 2 == 1)
        even_count = len(all_numbers) - odd_count
        
        # 고저 통계 (1-22: 저, 23-45: 고)
        low_count = sum(1 for num in all_numbers if num <= 22)
        high_count = len(all_numbers) - low_count
        
        # 구간별 통계 (1-15, 16-30, 31-45)
        range1 = sum(1 for num in all_numbers if 1 <= num <= 15)
        range2 = sum(1 for num in all_numbers if 16 <= num <= 30)
        range3 = sum(1 for num in all_numbers if 31 <= num <= 45)
        
        return {
            'total_draws': total_draws,
            'total_numbers': len(all_numbers),
            'odd_count': odd_count,
            'even_count': even_count,
            'odd_ratio': odd_count / len(all_numbers) if all_numbers else 0,
            'even_ratio': even_count / len(all_numbers) if all_numbers else 0,
            'low_count': low_count,
            'high_count': high_count,
            'low_ratio': low_count / len(all_numbers) if all_numbers else 0,
            'high_ratio': high_count / len(all_numbers) if all_numbers else 0,
            'range1_count': range1,
            'range2_count': range2,
            'range3_count': range3,
            'latest_draw': max(self.data.keys()) if self.data else 0,
        }


# 싱글톤 인스턴스
_collector_instance = None

def get_collector() -> LottoDataCollector:
    """LottoDataCollector 싱글톤 인스턴스를 반환합니다."""
    global _collector_instance
    if _collector_instance is None:
        _collector_instance = LottoDataCollector()
    return _collector_instance
