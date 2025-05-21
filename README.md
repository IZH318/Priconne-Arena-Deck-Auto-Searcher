# 프리코네 아레나 조합 자동 검색기 (Priconne Arena Deck Auto Searcher)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)



[여기 동영상 4-6]



<BR>
이 프로그램은 인기 모바일 게임 '프린세스 커넥트! Re:Dive' (이하 프리코네)의 아레나(배틀 아레나, 프린세스 아레나) 방어덱 조합을 효율적으로 검색하기 위해 개발된 자동화 도구입니다.
<BR><BR>
사용자는 게임 화면의 방어덱 부분을 간단히 드래그하여 캡처하는 것만으로, 프로그램이 자동으로 캐릭터 아이콘을 인식하고, 이를 바탕으로 [pcrdfans.com](https://pcrdfans.com)에서 공략 조합을 찾아주는 편리한 기능을 제공합니다.

---

**📢 중요: 자세한 사용 방법, 각 기능에 대한 설명, 문제 해결 가이드 등은 프로그램과 함께 제공되는 `_설명서(Manual).html` 파일을 반드시 참고해 주십시오.**

---

## ✨ 주요 기능

*   **아레나 조합 캡처 및 자동 인식**:
    *   마우스 드래그를 통한 간편한 화면 캡처
    *   OpenCV 기반 캐릭터 아이콘 자동 감지 및 분리
*   **다단계 캐릭터 아이콘 유사도 비교**:
    *   캡처 아이콘 vs 로컬 인게임 아이콘 비교 (SSIM 기반)
    *   ★6 아이콘 자동 ★3 아이콘 변환 처리
    *   인게임 아이콘 vs 웹사이트 스프라이트 아이콘 비교 (pcrdfans.com)
*   **PCRDfans.com 웹사이트 자동 검색 및 필터링**:
    *   Selenium 기반 웹 자동화 검색
    *   다국어(영어, 일본어, 중국어 간체) 인터페이스 및 검색 지원
    *   서버별 필터링 및 정렬 옵션 동기화
*   **최적화**:
    *   이미지 캐싱, 병렬 처리, ROI 기반 유사도 계산 등으로 성능 및 정확도 향상
    *   반응형 GUI 유지 (백그라운드 스레드 작업)

## 🚀 빠른 시작 (기본 작업 순서)

1.  **언어/Language, 게임 서버/Game Server, 정렬/Sorting** 드롭다운 박스 설정
2.  **[사이트 연결]** 버튼 클릭 (최초 실행 시 또는 필요시)
    *   필요한 캐릭터 아이콘 자동 다운로드 및 웹사이트 초기 연결
3.  **[아레나 조합 캡쳐]** 버튼 클릭 후, 게임 화면에서 상대방 방어덱 5명 드래그하여 캡처
4.  **임계값** 설정 (기본값 0.50, 필요시 조정)
5.  **[아레나 조합 검색]** 버튼 클릭
    *   자동으로 웹사이트에서 조합 검색 실행

*(선택사항)*:
*   **[(수동) 전체 캐릭터 아이콘 다운로드]** 버튼 클릭
*   **[유사도 비교 테스트]** 버튼으로 인식 결과 상세 확인

## 📋 요구 사항

*   Windows 운영체제 (다른 OS에서는 테스트되지 않았습니다)
*   Python 3.8 이상 (스크립트 실행 시)
*   Google Chrome 브라우저 (최신 버전 권장)
*   안정적인 인터넷 연결
*   필요 라이브러리 (스크립트 실행 시):
    *   `tkinter` (Python 표준 라이브러리)
    *   `opencv-python`
    *   `Pillow`
    *   `scikit-image`
    *   `selenium`
    *   `webdriver-manager`
    *   `requests`
    *   `beautifulsoup4`
    *   `numpy`

## ⚙️ 설치 (스크립트 실행 시)

1.  Python을 설치합니다. **(※ 설치 시 반드시 "Add Python to PATH" 옵션 선택)**
2.  프로그램 폴더에 `requirements.txt` 파일이 있다면, 터미널에서 다음 명령어를 실행합니다:
    ```bash
    pip install -r requirements.txt
    ```
3.  `requirements.txt` 파일이 없다면, 위에 명시된 개별 라이브러리를 설치합니다:
    ```bash
    pip install opencv-python Pillow scikit-image selenium webdriver-manager requests beautifulsoup4 numpy
    ```
    *   **❗ 패키지 설치 중 오류 발생 시:** `pip`를 최신 버전으로 업그레이드한 후 다시 시도해 보세요.
        ```bash
        python -m pip install --upgrade pip
        ```
4.  메인 Python 스크립트 파일 (`Priconne Arena Deck Auto Searcher.py`)을 실행합니다.

*(실행 파일(.exe)은 별도의 설치 과정이 필요 없습니다.)*

## 🛠️ 사용된 주요 기술

*   **Python**: 주 개발 언어
*   **Tkinter**: GUI 구성
*   **OpenCV**: 캐릭터 아이콘 윤곽선 감지 등 이미지 처리
*   **Pillow (PIL)**: 이미지 파일 처리, 화면 캡처, Tkinter 이미지 변환
*   **scikit-image**: 이미지 구조적 유사도(SSIM) 계산
*   **Selenium**: 웹 브라우저 자동화 (pcrdfans.com 제어)
*   **webdriver-manager**: ChromeDriver 자동 관리
*   **Requests**: 웹페이지 및 이미지 다운로드
*   **BeautifulSoup4**: HTML 파싱 (웹사이트 정보 추출)
*   **NumPy**: 이미지 데이터 처리 및 수치 연산
*   **ThreadPoolExecutor**: 병렬 처리를 통한 성능 향상

## ⚠️ 주의사항 및 면책 조항

*   이 프로그램은 공개된 웹사이트 정보를 활용하며, 게임 클라이언트를 직접 수정하거나 서버와 비정상적인 통신을 하지 않습니다.
*   웹사이트(`pcrdfans.com`, `redive.estertion.win`)의 구조 변경 시 프로그램이 정상적으로 작동하지 않을 수 있습니다.
*   자세한 내용은 `_설명서(Manual).html`을 참고하십시오.
*    **프로그램 사용으로 인해 발생하는 모든 문제에 대한 책임은 전적으로 사용자 본인에게 있습니다.**

## 📜 라이선스

이 프로그램은 [GNU General Public License v3 (GPLv3)](LICENSE) 라이선스를 따릅니다.

---

💖 이 프로그램이 프리코네 아레나 공략에 도움이 되기를 바랍니다! 피드백 및 버그 제보는 언제나 환영합니다.
