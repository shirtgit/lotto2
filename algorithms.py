"""
로또 번호 추천 알고리즘 모듈
피보나치, 파스칼, 페르마의 수학 이론을 기반으로 번호를 추천합니다.
"""

import random
from typing import List, Dict, Tuple
from collections import Counter
import numpy as np
from scipy.special import comb
from config import LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER, NUMBERS_PER_DRAW


class LottoAlgorithms:
    """로또 번호 추천 알고리즘을 제공하는 클래스"""
    
    def __init__(self, lotto_data: Dict[int, Dict]):
        self.lotto_data = lotto_data
        self.all_numbers = self._get_all_numbers()
        self.frequency = self._calculate_frequency()
        
    def _get_all_numbers(self) -> List[int]:
        """모든 당첨 번호를 리스트로 반환 (보너스 제외)"""
        all_numbers = []
        for draw_data in self.lotto_data.values():
            all_numbers.extend(draw_data['numbers'])
        return all_numbers
    
    def _calculate_frequency(self) -> Dict[int, int]:
        """각 번호의 출현 빈도 계산"""
        return Counter(self.all_numbers)
    
    def _is_prime(self, n: int) -> bool:
        """소수 판별"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def _get_primes(self, max_num: int = LOTTO_MAX_NUMBER) -> List[int]:
        """범위 내의 모든 소수 반환"""
        return [n for n in range(2, max_num + 1) if self._is_prime(n)]
    
    def _get_fibonacci_sequence(self, max_num: int = LOTTO_MAX_NUMBER) -> List[int]:
        """피보나치 수열 생성 (max_num 이하)"""
        fib = [1, 1]
        while True:
            next_fib = fib[-1] + fib[-2]
            if next_fib > max_num:
                break
            fib.append(next_fib)
        return fib
    
    def _calculate_golden_ratio_positions(self) -> List[int]:
        """황금비를 이용한 위치 계산"""
        phi = 1.618033988749895  # 황금비
        positions = []
        for i in range(1, 7):
            pos = int((LOTTO_MAX_NUMBER - LOTTO_MIN_NUMBER + 1) * (i / (1 + phi)))
            positions.append(max(LOTTO_MIN_NUMBER, min(LOTTO_MAX_NUMBER, pos)))
        return positions
    
    def fibonacci_method(self) -> Tuple[List[int], str]:
        """
        피보나치 수열 기반 추천
        황금비율로 우주의 조화를 찾아내듯이,
        로또 번호에서도 자연스러운 성장 패턴을 찾아낸다.
        """
        fib_sequence = self._get_fibonacci_sequence()
        golden_positions = self._calculate_golden_ratio_positions()
        
        # 피보나치 수열에서 직접 선택
        direct_fibs = [f for f in fib_sequence if LOTTO_MIN_NUMBER <= f <= LOTTO_MAX_NUMBER]
        
        # 과거 데이터에서 피보나치 수의 출현 빈도 계산
        fib_frequency = {num: self.frequency.get(num, 0) for num in direct_fibs}
        
        # 가장 많이 나온 피보나치 수 선택
        sorted_fibs = sorted(fib_frequency.items(), key=lambda x: x[1], reverse=True)
        selected = [num for num, _ in sorted_fibs[:3]]
        
        # 황금비 위치에서 추가 선택
        for pos in golden_positions:
            if len(selected) >= NUMBERS_PER_DRAW:
                break
            if pos not in selected:
                selected.append(pos)
        
        # 부족하면 피보나치 수 중에서 랜덤 선택
        while len(selected) < NUMBERS_PER_DRAW:
            remaining_fibs = [f for f in direct_fibs if f not in selected]
            if remaining_fibs:
                selected.append(random.choice(remaining_fibs))
            else:
                # 피보나치 수가 부족하면 황금비로 계산된 수 추가
                all_nums = list(range(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER + 1))
                remaining = [n for n in all_nums if n not in selected]
                selected.append(random.choice(remaining))
        
        result = sorted(selected[:NUMBERS_PER_DRAW])
        
        reasoning = (
            f"피보나치 수열({', '.join(map(str, direct_fibs[:5]))}...) 중 "
            f"출현 빈도가 높은 번호와 황금비(φ≈1.618) 위치의 조화"
        )
        
        return result, reasoning
    
    def pascal_combinatorial(self) -> Tuple[List[int], str]:
        """
        파스칼 삼각형 방식 1 - 조합론적 접근
        모든 가능성을 계산하고 가장 균형잡힌 조합을 선택한다.
        우연은 없다, 오직 계산된 확률만이 존재한다.
        """
        # 파스칼 삼각형의 특정 행 생성
        row = 10
        pascal_row = [int(comb(row, k)) for k in range(row + 1)]
        
        # 파스칼 계수를 1-45 범위로 매핑
        mapped_numbers = [(pascal_row[i] % 45) + 1 for i in range(len(pascal_row))]
        mapped_numbers = list(set(mapped_numbers))  # 중복 제거
        
        # 과거 데이터에서 자주 함께 나온 번호 쌍 분석
        pair_frequency = Counter()
        for draw_data in self.lotto_data.values():
            numbers = draw_data['numbers']
            for i in range(len(numbers)):
                for j in range(i + 1, len(numbers)):
                    pair = tuple(sorted([numbers[i], numbers[j]]))
                    pair_frequency[pair] += 1
        
        # 가장 빈번한 쌍에서 번호 선택
        selected = []
        for pair, _ in pair_frequency.most_common(30):
            for num in pair:
                if num not in selected:
                    selected.append(num)
                if len(selected) >= NUMBERS_PER_DRAW:
                    break
            if len(selected) >= NUMBERS_PER_DRAW:
                break
        
        # 부족하면 매핑된 파스칼 번호로 채우기
        for num in mapped_numbers:
            if num not in selected:
                selected.append(num)
            if len(selected) >= NUMBERS_PER_DRAW:
                break
        
        # 여전히 부족하면 빈도 높은 번호로 채우기
        if len(selected) < NUMBERS_PER_DRAW:
            sorted_freq = sorted(self.frequency.items(), key=lambda x: x[1], reverse=True)
            for num, _ in sorted_freq:
                if num not in selected:
                    selected.append(num)
                if len(selected) >= NUMBERS_PER_DRAW:
                    break
        
        result = sorted(selected[:NUMBERS_PER_DRAW])
        
        reasoning = (
            f"조합 계수 C({row},k)의 패턴과 "
            f"과거 데이터의 동반 출현 빈도를 조합론적으로 분석"
        )
        
        return result, reasoning
    
    def pascal_probability(self) -> Tuple[List[int], str]:
        """
        파스칼 삼각형 방식 2 - 확률적 분포
        과거의 패턴에서 미래의 확률을 읽어낸다.
        기댓값은 거짓말을 하지 않는다.
        """
        # 각 번호의 출현 확률 계산
        total_draws = len(self.lotto_data)
        probabilities = {}
        for num in range(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER + 1):
            probabilities[num] = self.frequency.get(num, 0) / total_draws if total_draws > 0 else 0
        
        # 기댓값 계산: 확률 * 번호 값
        expected_values = {num: prob * num for num, prob in probabilities.items()}
        
        # 홀짝 균형 분석
        odd_count = sum(1 for num in self.all_numbers if num % 2 == 1)
        even_count = len(self.all_numbers) - odd_count
        target_odd = 3 if odd_count > even_count else 3
        
        # 고저 균형 분석 (1-22: 저, 23-45: 고)
        low_count = sum(1 for num in self.all_numbers if num <= 22)
        high_count = len(self.all_numbers) - low_count
        target_low = 3 if low_count > high_count else 3
        
        # 확률 기반 선택 (가중치 적용)
        selected = []
        
        # 높은 기댓값을 가진 번호 중에서 균형있게 선택
        sorted_expected = sorted(expected_values.items(), key=lambda x: x[1], reverse=True)
        
        odds_selected = 0
        evens_selected = 0
        lows_selected = 0
        highs_selected = 0
        
        for num, _ in sorted_expected:
            if len(selected) >= NUMBERS_PER_DRAW:
                break
            
            is_odd = num % 2 == 1
            is_low = num <= 22
            
            # 균형을 고려한 선택
            if is_odd and odds_selected >= target_odd:
                continue
            if not is_odd and evens_selected >= (NUMBERS_PER_DRAW - target_odd):
                continue
            if is_low and lows_selected >= target_low:
                continue
            if not is_low and highs_selected >= (NUMBERS_PER_DRAW - target_low):
                continue
            
            selected.append(num)
            if is_odd:
                odds_selected += 1
            else:
                evens_selected += 1
            if is_low:
                lows_selected += 1
            else:
                highs_selected += 1
        
        # 부족하면 확률 높은 순으로 채우기
        if len(selected) < NUMBERS_PER_DRAW:
            for num, _ in sorted_expected:
                if num not in selected:
                    selected.append(num)
                if len(selected) >= NUMBERS_PER_DRAW:
                    break
        
        result = sorted(selected[:NUMBERS_PER_DRAW])
        
        reasoning = (
            f"이항분포 모델링과 기댓값 계산으로 "
            f"홀짝 {odds_selected}:{evens_selected}, 고저 균형 최적화"
        )
        
        return result, reasoning
    
    def fermat_prime(self) -> Tuple[List[int], str]:
        """
        페르마 소정리 방식 1 - 소수 기반
        소수는 숫자의 원자이다.
        원자의 배열에서 우주의 비밀을 찾아낸다.
        """
        primes = self._get_primes()
        
        # 소수의 출현 빈도 분석
        prime_frequency = {p: self.frequency.get(p, 0) for p in primes}
        sorted_primes = sorted(prime_frequency.items(), key=lambda x: x[1], reverse=True)
        
        # 페르마 소정리를 이용한 가중치 계산: a^(p-1) mod p = 1
        weighted_primes = []
        for prime, freq in sorted_primes:
            # 작은 소수에 더 높은 가중치 (페르마 소정리의 특성 반영)
            weight = freq * (1 + 1/prime)
            weighted_primes.append((prime, weight))
        
        weighted_primes.sort(key=lambda x: x[1], reverse=True)
        
        # 소수에서 선택 (4개)
        selected = [p for p, _ in weighted_primes[:4]]
        
        # 합성수 중에서 선택 (2개) - 소수와 균형
        composites = [n for n in range(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER + 1) 
                     if not self._is_prime(n) and n > 1]
        composite_frequency = {c: self.frequency.get(c, 0) for c in composites}
        sorted_composites = sorted(composite_frequency.items(), key=lambda x: x[1], reverse=True)
        
        for comp, _ in sorted_composites:
            if comp not in selected:
                selected.append(comp)
            if len(selected) >= NUMBERS_PER_DRAW:
                break
        
        result = sorted(selected[:NUMBERS_PER_DRAW])
        
        prime_count = sum(1 for n in result if self._is_prime(n))
        reasoning = (
            f"페르마 소정리 a^(p-1)≡1(mod p) 적용, "
            f"소수 {prime_count}개와 합성수 {NUMBERS_PER_DRAW - prime_count}개의 조화"
        )
        
        return result, reasoning
    
    def fermat_power(self) -> Tuple[List[int], str]:
        """
        페르마 최후의 정리 방식 2 - 거듭제곱 관계
        거듭제곱의 관계에서 패턴을 발견한다.
        불가능의 증명 속에 가능성이 숨어있다.
        """
        # 완전제곱수
        perfect_squares = [i*i for i in range(1, int(LOTTO_MAX_NUMBER**0.5) + 1) 
                          if i*i <= LOTTO_MAX_NUMBER]
        
        # 제곱수의 출현 빈도
        square_frequency = {s: self.frequency.get(s, 0) for s in perfect_squares}
        
        # 제곱수 간의 차이 계산
        square_differences = []
        for i in range(len(perfect_squares)):
            for j in range(i + 1, len(perfect_squares)):
                diff = perfect_squares[j] - perfect_squares[i]
                if LOTTO_MIN_NUMBER <= diff <= LOTTO_MAX_NUMBER:
                    square_differences.append(diff)
        
        # 제곱수 간의 합 계산
        square_sums = []
        for i in range(len(perfect_squares)):
            for j in range(i + 1, len(perfect_squares)):
                total = perfect_squares[i] + perfect_squares[j]
                if LOTTO_MIN_NUMBER <= total <= LOTTO_MAX_NUMBER:
                    square_sums.append(total)
        
        selected = []
        
        # 제곱수 중 빈도 높은 것 선택 (2개)
        sorted_squares = sorted(square_frequency.items(), key=lambda x: x[1], reverse=True)
        for square, _ in sorted_squares[:2]:
            if square not in selected:
                selected.append(square)
        
        # 제곱수 차이에서 빈도 높은 것 선택 (2개)
        diff_frequency = Counter(square_differences)
        for diff, _ in diff_frequency.most_common(2):
            if diff not in selected:
                selected.append(diff)
            if len(selected) >= NUMBERS_PER_DRAW:
                break
        
        # 제곱수 합에서 빈도 높은 것 선택 (2개)
        if len(selected) < NUMBERS_PER_DRAW:
            sum_frequency = Counter(square_sums)
            for total, _ in sum_frequency.most_common(2):
                if total not in selected:
                    selected.append(total)
                if len(selected) >= NUMBERS_PER_DRAW:
                    break
        
        # 부족하면 일반 빈도로 채우기
        if len(selected) < NUMBERS_PER_DRAW:
            sorted_freq = sorted(self.frequency.items(), key=lambda x: x[1], reverse=True)
            for num, _ in sorted_freq:
                if num not in selected:
                    selected.append(num)
                if len(selected) >= NUMBERS_PER_DRAW:
                    break
        
        result = sorted(selected[:NUMBERS_PER_DRAW])
        
        square_count = sum(1 for n in result if n in perfect_squares)
        reasoning = (
            f"완전제곱수({', '.join(map(str, perfect_squares))})의 차이와 합 패턴 분석, "
            f"제곱수 {square_count}개 포함"
        )
        
        return result, reasoning
    
    def get_all_recommendations(self) -> List[Dict]:
        """모든 추천 알고리즘의 결과를 반환"""
        algorithms = [
            {
                'name': '피보나치 수열',
                'mathematician': '레오나르도 피보나치',
                'color': '#FFD700',
                'method': self.fibonacci_method,
                'description': '황금비율과 자연의 성장 패턴'
            },
            {
                'name': '파스칼 조합론',
                'mathematician': '블레즈 파스칼',
                'color': '#4169E1',
                'method': self.pascal_combinatorial,
                'description': '조합 계수와 동반 출현 분석'
            },
            {
                'name': '파스칼 확률론',
                'mathematician': '블레즈 파스칼',
                'color': '#4169E1',
                'method': self.pascal_probability,
                'description': '이항분포와 기댓값 최적화'
            },
            {
                'name': '페르마 소수론',
                'mathematician': '피에르 드 페르마',
                'color': '#32CD32',
                'method': self.fermat_prime,
                'description': '소수의 특별한 성질 활용'
            },
            {
                'name': '페르마 거듭제곱',
                'mathematician': '피에르 드 페르마',
                'color': '#32CD32',
                'method': self.fermat_power,
                'description': '완전제곱수의 관계 패턴'
            }
        ]
        
        results = []
        for algo in algorithms:
            numbers, reasoning = algo['method']()
            results.append({
                'name': algo['name'],
                'mathematician': algo['mathematician'],
                'color': algo['color'],
                'description': algo['description'],
                'numbers': numbers,
                'reasoning': reasoning
            })
        
        return results
