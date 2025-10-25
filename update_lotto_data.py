"""
GitHub Actions용 로또 데이터 자동 업데이트 스크립트
매주 토요일 21시에 최신 회차 데이터를 수집합니다.
"""

import requests
import json
import os
from datetime import datetime

# 설정
LOTTO_API_URL = "https://www.dhlottery.co.kr/common.do"
CACHE_FILE = "lotto_data.json"


def load_existing_data():
    """기존 데이터 로드"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"기존 데이터 로드 실패: {e}")
            return {}
    return {}


def fetch_draw_data(draw_no):
    """특정 회차의 데이터를 가져옵니다."""
    params = {
        'method': 'getLottoNumber',
        'drwNo': draw_no
    }
    
    try:
        response = requests.get(LOTTO_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
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
        return None
    except Exception as e:
        print(f"{draw_no}회차 데이터 가져오기 실패: {e}")
        return None


def find_latest_draw():
    """최신 회차 번호를 찾습니다."""
    # 현재 추정 최대 회차부터 시작 (1195 + 여유분)
    for draw_no in range(1200, 1190, -1):
        data = fetch_draw_data(draw_no)
        if data:
            print(f"✅ 최신 회차 발견: {draw_no}회차")
            return draw_no, data
    return None, None


def update_data():
    """데이터 업데이트"""
    print("=" * 50)
    print(f"로또 데이터 자동 업데이트 시작: {datetime.now()}")
    print("=" * 50)
    
    # 기존 데이터 로드
    data = load_existing_data()
    existing_draws = [int(k) for k in data.keys()] if data else []
    max_existing = max(existing_draws) if existing_draws else 0
    
    print(f"📊 기존 데이터: {len(existing_draws)}회차 (최대: {max_existing}회차)")
    
    # 최신 회차 확인
    latest_draw_no, latest_data = find_latest_draw()
    
    if not latest_draw_no:
        print("❌ 최신 회차를 찾을 수 없습니다.")
        return
    
    # 새 회차가 있는지 확인
    if latest_draw_no <= max_existing:
        print(f"✅ 이미 최신 데이터입니다. (현재: {max_existing}회차)")
        return
    
    # 누락된 회차 수집
    print(f"\n🔄 {max_existing + 1}회차 ~ {latest_draw_no}회차 수집 중...")
    updated = 0
    
    for draw_no in range(max_existing + 1, latest_draw_no + 1):
        if str(draw_no) in data:
            continue
        
        draw_data = fetch_draw_data(draw_no)
        if draw_data:
            data[str(draw_no)] = draw_data
            updated += 1
            print(f"  ✓ {draw_no}회차 수집 완료")
    
    # 파일 저장
    if updated > 0:
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 총 {updated}개 회차 업데이트 완료!")
            print(f"📁 파일 저장: {CACHE_FILE}")
        except Exception as e:
            print(f"❌ 파일 저장 실패: {e}")
    else:
        print("\n✅ 업데이트할 새 회차가 없습니다.")
    
    print("=" * 50)


if __name__ == "__main__":
    update_data()
