# Streamlit Cloud 배포 가이드

## 📋 배포 전 체크리스트

### ✅ 필수 파일 확인
- [x] `requirements.txt` - Python 패키지 목록
- [x] `app.py` - 메인 애플리케이션
- [x] `.streamlit/config.toml` - Streamlit 설정
- [x] `lotto_data.json` - 로또 데이터 (옵션)

### ✅ 파일 준비 완료
모든 파일이 Streamlit Cloud 배포 형식으로 준비되었습니다.

## 🚀 배포 방법

### 1. GitHub 저장소 푸시
```bash
git add .
git commit -m "Streamlit Cloud 배포 준비 완료"
git push origin main
```

### 2. Streamlit Cloud 배포

#### 2-1. Streamlit Cloud 접속
1. https://streamlit.io/cloud 접속
2. GitHub 계정으로 로그인

#### 2-2. 새 앱 배포
1. **"New app"** 버튼 클릭
2. 저장소 선택:
   - **Repository**: `shirtgit/lotto2`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. **Advanced settings** (선택사항):
   - Python version: `3.11`
4. **"Deploy!"** 버튼 클릭

### 3. 배포 완료
- 약 5-10분 후 배포 완료
- 자동으로 앱 URL 생성
- 예: `https://lotto2-xxxxx.streamlit.app`

## ⚙️ 배포 후 설정

### GitHub Actions 권한 (중요!)
1. GitHub 저장소 → **Settings**
2. **Actions** → **General**
3. "Workflow permissions":
   - ✅ **"Read and write permissions"**
   - ✅ **"Allow GitHub Actions to create and approve pull requests"**
4. **Save**

### Streamlit Secrets (필요시)
API 키 등 민감한 정보가 있다면:
1. Streamlit Cloud 대시보드
2. 앱 선택 → **Settings** → **Secrets**
3. TOML 형식으로 입력

## 🔄 자동 업데이트

### GitHub Actions로 데이터 자동 업데이트
- **스케줄**: 매주 토요일 21:00 KST
- **동작**: 최신 로또 회차 자동 수집
- **배포**: Streamlit이 자동으로 최신 코드 반영

### 수동 재배포
1. Streamlit Cloud 대시보드
2. 앱 선택 → **⋮** 메뉴
3. **"Reboot app"** 클릭

## 📊 모니터링

### 앱 상태 확인
- Streamlit Cloud 대시보드에서 실시간 로그 확인
- 에러 발생 시 이메일 알림

### GitHub Actions 로그
- GitHub 저장소 → **Actions** 탭
- 자동 업데이트 실행 기록 확인

## 🐛 문제 해결

### 배포 실패 시
1. `requirements.txt` 패키지 버전 확인
2. Python 버전 호환성 확인 (3.11 권장)
3. 로그 메시지 확인

### 데이터 로드 실패 시
1. `lotto_data.json` 파일 존재 확인
2. GitHub Actions 실행 기록 확인
3. 수동으로 데이터 수집 버튼 클릭

### 아이콘 표시 안 될 때
- `icon.ico` 파일이 저장소에 있는지 확인
- Streamlit Cloud에서 파일 접근 권한 확인

## 💡 최적화 팁

### 성능 향상
- `lotto_data.json` 캐싱 활용
- 큰 파일은 Git LFS 사용 고려
- 불필요한 패키지 제거

### 비용 절감
- Streamlit Community Cloud는 무료
- GitHub Actions 무료 한도: 월 2,000분
- 충분히 무료로 운영 가능

## 🔗 유용한 링크

- [Streamlit Cloud 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Streamlit 포럼](https://discuss.streamlit.io/)

---

## ✅ 완료!

모든 파일이 준비되었습니다. 
위 단계를 따라하면 몇 분 안에 배포 완료됩니다! 🚀

**배포 URL은 자동으로 생성되며, 전 세계 어디서나 접속 가능합니다.**

© 2025 쇼쇼 (shirtgit)
