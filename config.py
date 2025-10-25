"""
Configuration file for Lotto Analysis System
"""

# API Settings
LOTTO_API_URL = "https://www.dhlottery.co.kr/common.do"
MAX_DRAW_NUMBER = 1194  # 최대 회차 번호
MIN_DRAW_NUMBER = 1     # 최소 회차 번호

# Lotto Settings
LOTTO_MIN_NUMBER = 1
LOTTO_MAX_NUMBER = 45
NUMBERS_PER_DRAW = 6

# Color Theme
COLORS = {
    'fibonacci': '#FFD700',      # Gold
    'pascal': '#4169E1',         # Royal Blue
    'fermat': '#32CD32',         # Lime Green
    'background': '#0E1117',     # Dark background
    'text': '#FAFAFA',          # Light text
}

# Cache Settings
CACHE_FILE = 'lotto_data.json'
