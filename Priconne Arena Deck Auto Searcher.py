# ====================================================================================================
# 프리코네 아레나 조합 자동 검색기 (Priconne Arena Deck Auto Searcher)
# ====================================================================================================
#
# 프로그램 개요:
# 이 프로그램은 인기 모바일 게임 '프린세스 커넥트! Re:Dive' (이하 프리코네(Priconne))의
# 아레나(배틀 아레나, 프린세스 아레나) 방어덱 조합을 효율적으로 검색하기 위해 개발된 자동화 도구입니다.
# 사용자는 게임 화면의 방어덱 부분을 간단히 드래그하여 캡처하는 것만으로, 프로그램이 자동으로
# 캐릭터 아이콘을 인식하고, 이를 바탕으로 공략 조합을 찾아주는 편리한 기능을 제공합니다.
#
# ----------------------------------------------------------------------------------------------------
# 주요 기능 상세 설명:
# ----------------------------------------------------------------------------------------------------
#
# 1. 아레나 조합 캡처 및 자동 인식 (Arena Deck Capture & Auto-Recognition)
#    - 실시간 화면 드래그 캡처:
#      사용자가 마우스 드래그를 통해 게임 내 아레나 화면의 상대방 방어덱 캐릭터 5명을 포함하는
#      영역을 손쉽게 지정하여 캡처할 수 있습니다.
#      (캡처 시 메인 창은 최소화되며, 반투명 오버레이를 통해 정확한 영역 선택 지원)
#    - OpenCV 기반 캐릭터 아이콘 자동 감지:
#      캡처된 이미지 내에서 OpenCV (Computer Vision Library)의 고급 이미지 처리 기술을 활용하여,
#      둥근 모서리 사각형 형태의 캐릭터 아이콘 윤곽선을 자동으로 감지합니다.
#      (이미지 전처리, 엣지 검출, 윤곽선 찾기, 도형 근사화 등의 과정 포함)
#    - 개별 캐릭터 아이콘 분할 및 정렬:
#      감지된 각 캐릭터 아이콘 영역을 정확하게 잘라내어 5개의 개별 이미지 파일로 분할합니다.
#      분할된 아이콘들은 화면상의 좌측부터 우측 순서로 자동 정렬되어 처리됩니다.
#      (분할된 아이콘은 GUI에 미리보기로 즉시 표시되어 사용자가 인식 결과를 확인할 수 있음)
#
# 2. 다단계 캐릭터 아이콘 유사도 비교 (Multi-stage Character Icon Similarity Comparison)
#    - 1단계: 캡처 아이콘 vs 로컬 인게임 아이콘 비교 (SSIM 기반):
#      분할된 캡처 아이콘과 로컬에 저장된 고해상도 인게임 캐릭터 아이콘 전체 세트 간의
#      구조적 유사도(SSIM - Structural Similarity Index Measure)를 계산하여 가장 유사한 캐릭터를 1차 식별합니다.
#      (이미지는 비교 전 표준 크기로 리사이즈 및 그레이스케일 변환, 노이즈 감소를 위한 블러 처리 적용)
#      (로컬 인게임 아이콘은 'redive.estertion.win' 사이트에서 WebP 형식으로 다운로드 후 JPG로 변환하여 관리)
#    - 2단계: ★6 아이콘 자동 ★3 아이콘 변환 처리:
#      만약 1단계에서 식별된 캐릭터 아이콘이 ★6 버전일 경우, 많은 경우 웹사이트 검색 시에는
#      기본 등급(주로 ★3) 아이콘을 사용하므로, 해당 캐릭터의 ★3 아이콘으로 자동 변환하여
#      다음 단계 비교의 정확도를 높입니다. (예: 100161.jpg -> 100131.jpg)
#    - 3단계: (변환된) 인게임 아이콘 vs 웹사이트 스프라이트 아이콘 비교:
#      1, 2단계를 거쳐 최종 식별된 인게임 아이콘(주로 ★3)과 pcrdfans.com에서 사용하는
#      스프라이트 시트 기반 캐릭터 아이콘 간의 유사도를 다시 한번 SSIM으로 비교합니다.
#      이를 통해 웹사이트에서 실제로 클릭해야 할 대상 아이콘을 최종 확정합니다.
#      (pcrdfans.com 스프라이트 아이콘은 프로그램 실행 시 최신 버전으로 자동 다운로드 및 분할 관리)
#
# 3. PCRDfans.com 웹사이트 자동 검색 및 필터링 (Automated PCRDfans.com Search & Filtering)
#    - Selenium 기반 웹 자동화:
#      인식된 캐릭터 조합(최종 확정된 스프라이트 아이콘 기준)을 사용하여, 웹 브라우저 자동화 도구인
#      Selenium을 통해 pcrdfans.com의 아레나 조합 검색 페이지에 자동으로 입력하고 검색을 실행합니다.
#    - 다국어 인터페이스 및 검색 지원:
#      GUI 및 pcrdfans.com 검색 시 한국어, 영어, 일본어, 중국어(간체)를 지원하여
#      다양한 언어 환경의 사용자를 배려합니다. 언어 변경 시 웹사이트도 해당 언어 페이지로 자동 전환됩니다.
#    - 서버별 필터링 및 정렬 옵션 동기화:
#      GUI에서 선택한 게임 서버(예: 한국 서버, 일본 서버 등) 및 정렬 옵션(예: 최신순, 추천순 등)이
#      pcrdfans.com 검색 시 자동으로 반영되어, 사용자 맞춤형 검색 결과를 제공합니다.
#      (선택 옵션 변경 시 웹사이트의 해당 필터 즉시 업데이트)
#
# 4. 이미지 처리 기술 및 프로그램 최적화 (Image Processing Techniques & Program Optimization)
#    - 이미지 캐싱을 통한 반복 작업 성능 최적화:
#      한 번 로드하고 전처리(리사이즈, 변환 등)한 이미지는 메모리 캐시에 저장하여,
#      동일 이미지에 대한 반복적인 파일 I/O 및 처리 시간을 대폭 단축시킵니다.
#    - 병렬 처리를 통한 유사도 비교 속도 향상:
#      다수의 캐릭터 아이콘 간 유사도 비교 작업 시, ThreadPoolExecutor를 활용한 병렬 처리를 통해
#      CPU 멀티 코어를 최대한 활용하여 전체 비교 시간을 크게 줄입니다. (주로 I/O 바운드 작업 및 일부 CPU 바운드 작업)
#    - ROI(Region of Interest, 관심 영역) 기반 유사도 계산 정확도 향상:
#      캐릭터 아이콘 이미지에서 실제 캐릭터 얼굴 및 주요 특징이 포함된 핵심 영역(ROI)만을
#      선택적으로 비교함으로써, 배경이나 테두리 등 불필요한 요소의 영향을 최소화하고
#      유사도 계산의 정확성과 신뢰도를 높입니다.
#    - 반응형 GUI 유지:
#      시간이 오래 걸리는 작업(웹 통신, 대량 파일 다운로드, 복잡한 이미지 처리 등)은
#      별도의 스레드(threading)에서 수행하여 GUI가 응답 없음 상태가 되는 것을 방지하고
#      사용자 경험을 향상시킵니다.
#
# ====================================================================================================

# 기본 파이썬 라이브러리
import datetime  # 로그 및 파일명 등에 사용될 현재 시간 타임스탬프 생성
import json      # 캐릭터 아이콘 메타데이터(버전, 스타일 정보 등) 저장 및 로드
import multiprocessing  # CPU 코어 수 확인 및 병렬 처리 작업자 수 설정에 사용
import queue     # 멀티스레딩 환경에서 스레드 간 안전한 데이터 전달(주로 로그 메시지)
import re        # 정규 표현식을 사용하여 문자열(예: CSS 스타일, 파일명)에서 정보 추출
import shutil    # 파일 및 디렉토리 복사, 삭제 등 고수준 파일 시스템 작업
import threading # GUI의 응답성을 유지하면서 백그라운드 작업(예: 웹 통신, 파일 다운로드) 수행
import time      # 작업 간 지연(딜레이)을 주거나, Selenium의 동적 컨텐츠 로딩 대기
from io import BytesIO  # 메모리 내에서 바이너리 데이터(예: 웹에서 다운로드한 이미지) 처리
from pathlib import Path  # 파일 및 디렉토리 경로를 객체 지향적으로 다루기 위함

# GUI 관련
import tkinter as tk  # 파이썬 표준 GUI 라이브러리, 사용자 인터페이스 구성
from tkinter import messagebox  # 정보, 경고, 오류 등의 표준 대화상자 표시

# 이미지 처리 관련
import cv2  # OpenCV 라이브러리, 이미지에서 윤곽선 찾기, 색 공간 변환, 블러링 등 고급 이미지 처리
import numpy as np  # 다차원 배열(이미지 픽셀 데이터) 처리 및 수치 연산
from PIL import Image, ImageGrab, ImageTk  # Pillow 라이브러리. 이미지 파일 열기/저장, 화면 캡처(ImageGrab), Tkinter용 이미지 객체 변환(ImageTk)
from skimage.metrics import structural_similarity as ssim  # scikit-image 라이브러리, 두 이미지 간의 구조적 유사도(SSIM) 계산

# 웹 관련
import requests  # HTTP 요청을 보내고 웹 서버로부터 응답(HTML, 이미지 파일 등)을 받음
from bs4 import BeautifulSoup  # HTML 및 XML 파서, 웹 페이지 내용을 구조적으로 분석하여 정보 추출
from selenium import webdriver  # 웹 브라우저 자동화 도구, JavaScript로 동적으로 생성되는 웹사이트와 상호작용
from selenium.webdriver.common.by import By  # Selenium에서 웹 요소를 찾는 방법(ID, 클래스명, XPath 등) 정의
from selenium.webdriver.support import expected_conditions as EC  # Selenium에서 특정 조건(예: 요소 표시, 클릭 가능)이 만족될 때까지 대기
from selenium.webdriver.support.ui import WebDriverWait  # Selenium에서 명시적 대기(explicit wait)를 설정하여 안정적인 자동화 지원
# WebDriver 자동 관리를 위한 webdriver-manager 임포트
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# 병렬 처리 관련
from concurrent.futures import ThreadPoolExecutor, as_completed  # 고수준 스레드 풀 관리, 다수의 I/O 바운드 작업(네트워크 요청 등) 병렬 실행

import webbrowser

def get_timestamp():
    """
    현재 시간 기준 포맷팅된 타임스탬프 문자열 반환.
    로그 메시지/파일명 등에 사용, 시간 정보 기록.
    형식: "[YYYY-MM-DD HH:MM:SS.mmm]" (m: 밀리초)
    """
    now = datetime.datetime.now()  # 현재 날짜와 시간 정보 가져오기
    ms = int(now.microsecond / 1000)  # 마이크로초를 밀리초(세 자리)로 변환
    # strftime을 사용하여 날짜/시간 부분을 포맷팅하고, f-string으로 밀리초 부분을 결합
    return now.strftime("[%Y-%m-%d %H:%M:%S.") + f"{ms:03d}]"

class CharacterImageManager:
    """
    pcrdfans.com 웹사이트에서 사용하는 스프라이트 시트 기반 캐릭터 아이콘을 관리하는 클래스.
    - 스프라이트 시트 다운로드 및 버전 관리
    - 개별 캐릭터 아이콘으로 분리 및 저장
    - 관련 메타데이터(div 스타일, HTML 등) 저장 및 로드
    """
    def __init__(self, log_callback=None):
        """
        CharacterImageManager 초기화.
        :param log_callback: 로그 메시지를 전달할 콜백 함수. None이면 로그를 출력하지 않음.
        """
        self.images_dir = Path("character_images")  # 캐릭터 이미지를 저장할 기본 디렉토리 경로 객체
        self.images_dir.mkdir(exist_ok=True)  # 디렉토리가 없으면 생성, 이미 있으면 무시
        self.metadata_file = self.images_dir / "arena_web_metadata.json"  # PCRDfans.com 접속 시 생성되는 메타데이터 파일 경로
        self.metadata = self.load_metadata()  # 메타데이터 파일에서 정보 로드
        self.current_index = 0  # 현재 처리 중인 캐릭터 아이콘의 인덱스 (파일명 생성 시 사용)
        self.current_version = self.metadata.get('current_version')  # 메타데이터에서 현재 저장된 아이콘 버전 로드
        self.log_message = log_callback or (lambda x: None)  # 로그 콜백 함수 설정, 없으면 아무것도 안 하는 람다 함수

    def load_metadata(self):
        """
        메타데이터 파일 (arena_web_metadata.json) 데이터 로드.
        파일 존재 시 JSON 파싱, 딕셔너리 반환. 없으면 기본값 반환.
        :return: 로드된 메타데이터 (dict) 또는 기본값 (dict)
        """
        if self.metadata_file.exists():  # 메타데이터 파일 존재 여부 확인
            with open(self.metadata_file, 'r', encoding='utf-8') as f:  # UTF-8 인코딩으로 파일 열기
                return json.load(f)  # JSON 파일 내용을 파싱하여 딕셔너리로 반환
        return {'current_version': None}  # 파일이 없으면 현재 버전을 None으로 하는 기본 메타데이터 반환

    def save_metadata(self):
        """
        현재 메타데이터 JSON 파일 (arena_web_metadata.json) 저장.
        current_version 정보 함께 저장.
        """
        self.metadata['current_version'] = self.current_version  # 현재 아이콘 버전을 메타데이터에 저장
        with open(self.metadata_file, 'w', encoding='utf-8') as f:  # UTF-8 인코딩으로 파일 쓰기 모드로 열기
            # JSON 데이터를 파일에 저장. ensure_ascii=False로 유니코드 문자 유지, indent=2로 가독성 좋게 포맷팅
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def get_current_version(self):
        """
        메타데이터에 저장된 현재 아이콘 버전 반환.
        :return: 현재 버전 문자열 또는 None
        """
        return self.metadata.get('current_version')  # 딕셔너리의 'current_version' 키 값 반환

    def remove_old_version_folder(self):
        """
        메타데이터에 기록된 이전 버전의 캐릭터 아이콘 폴더 삭제.
        새 버전 아이콘 다운로드 전 공간 확보 및 혼동 방지 목적.
        """
        if self.current_version and self.images_dir.exists():  # 현재 버전 정보가 있고, 기본 이미지 디렉토리가 존재하면
            old_version_dir = self.images_dir / self.current_version  # 이전 버전 폴더 경로 생성
            if old_version_dir.exists():  # 이전 버전 폴더가 실제로 존재하면
                try:
                    shutil.rmtree(old_version_dir)  # 폴더와 그 내용 전체를 재귀적으로 삭제
                    self.log_message(f"{get_timestamp()} 이전 버전 폴더 삭제 완료: {self.current_version}")
                except Exception as e:
                    self.log_message(f"{get_timestamp()} 이전 버전 폴더 삭제 실패: {str(e)}")

    def update_version(self, new_version):
        """
        새 아이콘 버전으로 업데이트.
        버전 변경 시, 이전 버전 폴더 삭제 및 새 버전 정보 메타데이터 저장.
        :param new_version: 업데이트할 새로운 버전 문자열
        :return: 버전이 실제로 업데이트되었으면 True, 아니면 False
        """
        if self.current_version != new_version:  # 현재 버전과 새 버전이 다르면
            self.log_message(f"{get_timestamp()} 버전 변경 감지: {self.current_version} → {new_version}")
            self.remove_old_version_folder()  # 이전 버전 폴더 삭제
            self.current_version = new_version  # 현재 버전을 새 버전으로 업데이트
            self.save_metadata()  # 변경된 메타데이터 저장
            self.log_message(f"{get_timestamp()} 버전 업데이트 완료: {new_version}")
            return True  # 버전 업데이트 성공
        return False  # 버전 변경 없음

    def _extract_style_info(self, style):
        """
        CSS 스타일 문자열에서 캐릭터 아이콘 관련 정보 (위치, 크기, 배경 크기) 정규 표현식 추출.
        스프라이트 시트에서 특정 아이콘 잘라내는 데 사용.
        :param style: 분석할 CSS 스타일 문자열 (예: div 태그의 style 속성값)
        :return: 추출된 정보 딕셔너리 또는 정보 추출 실패 시 None
        """
        # background-position: Xpx Ypx; (X, Y는 스프라이트 내 아이콘의 좌상단 좌표)
        pos_match = re.search(r"background-position:\s*([\-\d\.]+)px\s+([\-\d\.]+)px", style)
        # background-size: SIZEpx; (스프라이트 시트 이미지의 전체 크기)
        size_match = re.search(r"background-size:\s*([\d\.]+)px", style)
        # width: Wpx; height: Hpx; (개별 아이콘의 표시 크기)
        dim_match = re.search(r"width:\s*([\d\.]+)px;\s*height:\s*([\d\.]+)px", style)
        
        if not all([pos_match, size_match, dim_match]):  # 모든 정보가 성공적으로 매칭되었는지 확인
            return None  # 하나라도 없으면 None 반환
            
        return {
            'pos_x': float(pos_match.group(1)),  # X 위치 (음수일 수 있음)
            'pos_y': float(pos_match.group(2)),  # Y 위치 (음수일 수 있음)
            'bg_size': float(size_match.group(1)),  # 배경 스프라이트 시트의 크기 (보통 너비 기준)
            'width': int(float(dim_match.group(1))),  # 아이콘 너비
            'height': int(float(dim_match.group(2)))  # 아이콘 높이
        }

    def _calculate_crop_box(self, style_info, sprite_img):
        """
        추출된 스타일 정보와 원본 스프라이트 이미지를 기반으로,
        실제 스프라이트 이미지에서 잘라낼 영역(crop box)의 좌표 (left, top, right, bottom) 계산.
        :param style_info: _extract_style_info에서 반환된 딕셔너리
        :param sprite_img: 원본 스프라이트 PIL.Image 객체
        :return: 잘라낼 영역의 (x1, y1, x2, y2) 좌표 튜플
        """
        # CSS의 background-size와 실제 스프라이트 이미지의 너비 비율로 스케일 계산
        scale = sprite_img.width / style_info['bg_size']
        # 스케일을 적용하여 실제 crop할 x, y 시작 위치 계산
        crop_x = int(-style_info['pos_x'] * scale)
        crop_y = int(-style_info['pos_y'] * scale)
        # 스케일을 적용하여 crop할 너비와 높이를 계산하고, 이를 시작 위치에 더해 끝 위치 계산
        return (
            crop_x,  # 잘라낼 영역의 왼쪽 x 좌표
            crop_y,  # 잘라낼 영역의 위쪽 y 좌표
            crop_x + int(style_info['width'] * scale),  # 잘라낼 영역의 오른쪽 x 좌표
            crop_y + int(style_info['height'] * scale)  # 잘라낼 영역의 아래쪽 y 좌표
        )

    def _process_single_character(self, div_info, sprite_img, sprite_version):
        """
        단일 캐릭터 아이콘(div 요소) 처리, 이미지 추출/저장, 관련 메타데이터 기록.
        :param div_info: 캐릭터 아이콘 정보를 담고 있는 Selenium WebElement 객체
        :param sprite_img: 원본 스프라이트 PIL.Image 객체
        :param sprite_version: 현재 처리 중인 스프라이트의 버전 문자열
        :return: 저장된 캐릭터 이미지 파일 경로 또는 처리 실패 시 None
        """
        style = div_info.get_attribute("style")  # div 요소의 style 속성값 가져오기
        div_html = div_info.get_attribute("outerHTML")  # div 요소의 전체 HTML 가져오기
        
        style_info = self._extract_style_info(style)  # 스타일 정보 추출
        if not style_info:  # 스타일 정보 추출 실패 시
            return None
            
        crop_box = self._calculate_crop_box(style_info, sprite_img)  # 잘라낼 영역 계산
        # 스프라이트 이미지에서 해당 영역을 잘라내고, 50x50 크기로 리사이즈 (LANCZOS 고품질 필터), RGB 포맷으로 변환
        char_img = sprite_img.crop(crop_box).resize((50, 50), Image.LANCZOS).convert('RGB')
        
        char_filename = f"char_{self.current_index:03d}.png"  # 파일명 생성 (예: char_000.png)
        char_path = self.images_dir / sprite_version / char_filename  # 저장 경로 설정 (예: character_images/버전/char_000.png)
        char_img.save(char_path)  # 이미지 파일 저장
        
        if sprite_version not in self.metadata:  # 해당 스프라이트 버전에 대한 메타데이터가 없으면 새로 생성
            self.metadata[sprite_version] = {}
            
        # 메타데이터에 현재 캐릭터 아이콘 정보 저장
        self.metadata[sprite_version][char_filename] = {
            "div_style": style,  # 원본 div의 style 속성
            "div_html": div_html,  # 원본 div의 outerHTML
            "position": {"x": style_info['pos_x'], "y": style_info['pos_y']},  # CSS 상의 위치
            "size": {"width": style_info['width'], "height": style_info['height']},  # CSS 상의 크기
            "background_size": style_info['bg_size'],  # CSS 상의 배경 크기
            "index": self.current_index  # 부여된 인덱스
        }
        
        self.current_index += 1  # 다음 캐릭터를 위한 인덱스 증가
        return char_path  # 저장된 파일 경로 반환

    def process_sprite_image(self, sprite_url, div_info_list):
        """
        주어진 URL 스프라이트 시트 아이콘 이미지 다운로드,
        제공된 div 요소 목록 기반 개별 캐릭터 이미지 분리 저장.
        :param sprite_url: 스프라이트 시트 이미지의 전체 URL
        :param div_info_list: 캐릭터 아이콘 정보를 담고 있는 Selenium WebElement 객체들의 리스트
        :return: 개별 아이콘들이 저장된 버전별 디렉토리 경로
        """
        response = requests.get(sprite_url)  # 스프라이트 이미지 다운로드 요청
        sprite_img = Image.open(BytesIO(response.content)).convert("RGB")  # 다운로드한 바이트 데이터를 PIL 이미지 객체로 변환 (RGB)
        
        sprite_filename = sprite_url.split('/')[-1]  # URL에서 파일명 추출
        sprite_version = re.search(r'charas-(\d+)\.png', sprite_filename).group(1)  # 파일명에서 버전 정보 추출 (예: charas-123.png -> 123)
        
        self.update_version(sprite_version)  # 현재 버전을 업데이트 (필요시 이전 버전 삭제)
        
        version_dir = self.images_dir / sprite_version  # 현재 버전의 아이콘을 저장할 디렉토리 경로
        if version_dir.exists():  # 버전 디렉토리가 이미 존재하면
            for file in version_dir.glob("*.png"):  # 내부의 모든 .png 파일 삭제 (덮어쓰기 준비)
                file.unlink()
        version_dir.mkdir(exist_ok=True)  # 버전 디렉토리 생성 (없으면)
        
        self.current_index = 0  # 캐릭터 인덱스 초기화
        
        for div_info in div_info_list:  # 제공된 모든 div 요소에 대해
            self._process_single_character(div_info, sprite_img, sprite_version)  # 개별 캐릭터 아이콘 처리
        
        self.save_metadata()  # 모든 처리 후 메타데이터 저장
        return version_dir  # 저장된 버전 디렉토리 경로 반환

    def get_latest_version_dir(self):
        """
        로컬 저장 가장 최근 버전 캐릭터 아이콘 디렉토리 경로 반환.
        :return: 최신 버전 디렉토리 Path 객체 또는 None
        """
        if not self.images_dir.exists():  # 기본 이미지 디렉토리가 없으면
            return None
        current_version = self.metadata.get('current_version')  # 메타데이터에서 현재 버전 가져오기
        if current_version:  # 현재 버전 정보가 있으면
            version_dir = self.images_dir / current_version  # 해당 버전 디렉토리 경로 생성
            if version_dir.exists():  # 해당 버전 디렉토리가 존재하면
                return version_dir  # 경로 반환
        return None  # 조건에 맞지 않으면 None 반환

class AllCharacterImageManager:
    """
    redive.estertion.win 사이트에서 모든 캐릭터의 개별 아이콘(WebP 형식)을 다운로드하고 JPG로 변환하여 관리하는 클래스.
    - 모든 캐릭터 아이콘 일괄 다운로드 (WebP)
    - WebP -> JPG 변환 및 원본 WebP 삭제
    - 관련 메타데이터(캐릭터명, 파일 경로 등) 저장
    - 유사도 검색 시 이 JPG 아이콘들을 사용
    """
    def __init__(self, log_callback=None):
        """
        AllCharacterImageManager 초기화.
        :param log_callback: 로그 메시지를 전달할 콜백 함수.
        """
        self.images_dir = Path("character_images/character_unit_icon_all")  # 모든 캐릭터 아이콘을 저장할 디렉토리
        self.images_dir.mkdir(exist_ok=True, parents=True)  # 디렉토리 생성 (부모 디렉토리 포함, 이미 있어도 무시)
        self.metadata_file = self.images_dir / "character_unit_icon_all_metadata.json"  # redive.estertion.win 접속 시 생성되는 메타데이터
        self.metadata = self.load_metadata()  # 메타데이터 로드
        self.character_groups = {}  # 캐릭터 기본 ID(예: '1001')별 아이콘 파일명 목록을 저장할 딕셔너리
        self.log_message = log_callback or (lambda x: None)  # 로그 콜백 함수
        self.log_queue = queue.Queue()  # 스레드에서 발생하는 로그 메시지를 담을 큐
        self.downloaded_count = 0  # 다운로드된 파일 수 카운터
        self.total_files = 0  # 전체 다운로드 대상 파일 수

    def load_metadata(self):
        """
        메타데이터 파일 (character_unit_icon_all_metadata.json) 데이터 로드.
        :return: 로드된 메타데이터 (dict) 또는 빈 딕셔너리
        """
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}  # 파일 없으면 빈 딕셔너리 반환

    def save_metadata(self):
        """
        현재 메타데이터 JSON 파일 (character_unit_icon_all_metadata.json) 저장.
        """
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def _process_log_queue(self):
        """
        로그 큐 쌓인 메시지 가져와 설정된 로그 콜백 함수 통해 출력.
        스레드 직접 GUI 로그 함수 호출 방지 목적.
        """
        while True:
            try:
                message = self.log_queue.get_nowait()  # 큐에서 논블로킹으로 메시지 가져오기
                self.log_message(message)  # 로그 콜백 함수로 메시지 전달
            except queue.Empty:  # 큐가 비었으면
                break  # 루프 종료

    def _download_single_file(self, file_info):
        """
        단일 캐릭터 아이콘 파일(WebP) 다운로드, 관련 정보 메타데이터 기록.
        ThreadPoolExecutor 의해 병렬 실행 가능.
        :param file_info: (파일명, 캐릭터명) 튜플
        :return: 다운로드 성공 시 True, 실패 시 False
        """
        file_name, char_name = file_info  # 파일명과 캐릭터명 분리
        try:
            img_url = f"https://redive.estertion.win/icon/unit/{file_name}"  # 이미지 다운로드 URL 생성
            img_response = requests.get(img_url)  # 이미지 다운로드 요청
            
            if img_response.status_code != 200:  # HTTP 상태 코드가 200 (성공)이 아니면
                self.log_queue.put(f"{get_timestamp()} 다운로드 실패: {file_name} - HTTP {img_response.status_code}")
                return False
                
            webp_path = self.images_dir / file_name  # WebP 파일을 저장할 로컬 경로
            with open(webp_path, 'wb') as f:  # 바이너리 쓰기 모드로 파일 열기
                f.write(img_response.content)  # 파일 내용 쓰기
            
            base_id = file_name[:4]  # 파일명에서 앞 4자리 (캐릭터 기본 ID) 추출
            if base_id not in self.character_groups:  # 해당 기본 ID에 대한 그룹이 없으면
                self.character_groups[base_id] = []  # 새 리스트 생성
            self.character_groups[base_id].append(file_name)  # 그룹에 현재 파일명 추가
            
            # 메타데이터에 파일 정보 기록
            self.metadata[file_name] = {
                "char_name": char_name,  # 캐릭터명
                "base_id": base_id,  # 기본 ID
                "webp_path": str(webp_path)  # WebP 파일 경로 (문자열로)
            }
            
            self.downloaded_count += 1  # 다운로드 완료 카운트 증가
            progress = (self.downloaded_count / self.total_files) * 100 if self.total_files > 0 else 0 # 진행률 계산
            self.log_queue.put(f"{get_timestamp()} 다운로드 완료: {file_name} ({progress:.1f}%)")  # 로그 큐에 성공 메시지 추가
            return True
            
        except Exception as e:
            self.log_queue.put(f"{get_timestamp()} 다운로드 실패: {file_name} - {str(e)}")  # 로그 큐에 실패 메시지 추가
            return False

    def _convert_to_jpg(self, file_name):
        """
        지정 WebP 파일 JPG 형식 변환, 변환된 JPG 파일 경로 메타데이터 추가.
        :param file_name: 변환할 WebP 파일의 이름 (예: "100131.webp")
        :return: 변환 성공 시 True, 실패 시 False
        """
        try:
            webp_path = self.images_dir / file_name  # 원본 WebP 파일 경로
            jpg_path = self.images_dir / f"{file_name.rsplit('.', 1)[0]}.jpg"  # 변환될 JPG 파일 경로 (확장자 변경)
            
            img = Image.open(webp_path)  # WebP 이미지 열기
            img.convert('RGB').save(jpg_path, 'JPEG')  # RGB로 변환 후 JPEG 형식으로 저장
            
            self.metadata[file_name]["jpg_path"] = str(jpg_path)  # 메타데이터에 JPG 경로 추가
            return True
        except Exception as e:
            self.log_queue.put(f"{get_timestamp()} JPG 변환 실패: {file_name} - {str(e)}")  # 로그 큐에 실패 메시지 추가
            return False

    def _collect_download_files(self):
        """
        redive.estertion.win/icon/unit/ 페이지 파싱, 다운로드할 캐릭터 아이콘 파일 목록 수집.
        :return: (파일명, 캐릭터명) 튜플의 리스트
        """
        response = requests.get("https://redive.estertion.win/icon/unit/")  # 대상 웹페이지 요청
        soup = BeautifulSoup(response.text, 'html.parser')  # HTML 파싱
        items = soup.find_all('span', class_='item')  # 'item' 클래스를 가진 모든 span 태그 찾기
        
        download_files = []  # 다운로드할 파일 정보를 담을 리스트
        for item in items:  # 각 아이템에 대해
            try:
                img_tag = item.find('img')  # 내부의 img 태그 찾기
                if not img_tag:  # img 태그가 없으면 건너뛰기
                    continue
                
                file_name = img_tag['alt']  # img 태그의 alt 속성값 (파일명) 가져오기
                if file_name[0] in ['0', '1']:  # 파일명이 '0' 또는 '1'로 시작하는 경우 (일반 캐릭터 아이콘으로 간주)
                    char_name = item.find('span', class_='name').text  # 'name' 클래스를 가진 span 태그의 텍스트 (캐릭터명) 가져오기
                    download_files.append((file_name, char_name))  # 리스트에 추가
            except Exception as e:
                self.log_message(f"{get_timestamp()} 파일 정보 추출 실패: {str(e)}")  # 오류 발생 시 로그 남기고 계속
                continue
                
        return download_files  # 수집된 파일 목록 반환

    def download_all_icons(self):
        """
        모든 캐릭터 아이콘 redive.estertion.win 다운로드(WebP), JPG 변환, 원본 WebP 파일 삭제.
        병렬 다운로드, 순차 변환.
        :return: 모든 과정 성공 시 True, 하나라도 실패 시 False
        """
        self.log_message(f"{get_timestamp()} 전체 캐릭터 아이콘 다운로드 시작...")
        try:
            self.images_dir.mkdir(exist_ok=True, parents=True)  # 저장 디렉토리 확인 및 생성

            download_files = self._collect_download_files()  # 다운로드할 파일 목록 수집
            self.total_files = len(download_files)  # 전체 파일 수 설정
            self.downloaded_count = 0  # 다운로드 카운터 초기화
            self.log_message(f"{get_timestamp()} 총 {self.total_files}개의 파일을 다운로드합니다.")

            # ThreadPoolExecutor를 사용하여 최대 10개 스레드로 동시에 파일 다운로드
            with ThreadPoolExecutor(max_workers=10) as executor:
                # 각 다운로드 작업을 스레드 풀에 제출하고, future 객체와 파일 정보를 매핑
                future_to_file = {
                    executor.submit(self._download_single_file, file_info): file_info 
                    for file_info in download_files
                }
                
                # 제출된 작업들이 완료되는 순서대로 결과 처리
                for future in as_completed(future_to_file):
                    file_info = future_to_file[future]  # 완료된 future에 해당하는 파일 정보 가져오기
                    try:
                        future.result()  # 작업 결과 확인 (예외 발생 시 여기서 re-raise됨)
                    except Exception as e:
                        self.log_message(f"{get_timestamp()} 작업 실패: {file_info[0]} - {str(e)}\n") # 실패 시 로그
                    self._process_log_queue()  # 각 작업 완료 후 로그 큐 처리

            self.log_message(f"\n{get_timestamp()} WebP 파일을 JPG로 변환 중...")
            converted_count = 0  # JPG 변환 성공 카운터
            deleted_count = 0  # WebP 파일 삭제 카운터
            # 다운로드된 모든 파일(메타데이터에 기록된 파일)에 대해 JPG 변환 및 원본 삭제 시도
            # 이 부분은 순차적으로 처리됨 (파일 I/O가 주 작업이므로 병렬화 효과 크지 않을 수 있음)
            for file_name in list(self.metadata.keys()): # list()로 복사본 순회 (메타데이터 변경 가능성)
                try:
                    if self._convert_to_jpg(file_name):  # JPG 변환 시도
                        converted_count += 1
                        webp_path = self.images_dir / file_name  # 원본 WebP 파일 경로
                        if webp_path.exists():  # WebP 파일이 존재하면
                            webp_path.unlink()  # 삭제
                            deleted_count += 1
                        progress = (converted_count / len(self.metadata)) * 100 if len(self.metadata) > 0 else 0 # 진행률 계산
                        self.log_message(f"{get_timestamp()} JPG 변환 완료 및 WebP 삭제: {file_name} ({progress:.1f}%)")
                except Exception as e:
                    self.log_message(f"{get_timestamp()} 파일 처리 실패: {file_name} - {str(e)}\n") # 실패 시 로그

            self.save_metadata()  # 모든 작업 후 최종 메타데이터 저장
            self.log_message(f"{get_timestamp()} 전체 캐릭터 아이콘 다운로드 및 변환 완료!\n")
            # 최종 결과 요약 로그
            self.log_message(f"{get_timestamp()} - 처리 결과 -")
            self.log_message(f"{get_timestamp()} • 다운로드 완료: {self.downloaded_count}개 파일")
            self.log_message(f"{get_timestamp()} • JPG 변환 완료: {converted_count}개 파일")
            self.log_message(f"{get_timestamp()} • WebP 파일 삭제: {deleted_count}개 파일\n")
            return True
            
        except Exception as e:
            self.log_message(f"{get_timestamp()} 다운로드 중 오류 발생: {str(e)}\n") # 전체 프로세스 중 예외 발생 시 로그
            return False

# 상수 정의
WINDOW_WIDTH = 640  # 메인 윈도우 너비
WINDOW_HEIGHT = 480  # 메인 윈도우 높이
PREVIEW_SIZE = (50, 50)  # 분할된 아이콘 및 테스트 창 미리보기 크기
PROCESSING_SIZE = (32, 32)  # 내부 이미지 비교 시 사용할 표준 처리 크기
ROI_BOUNDS = (6, 23, 2, 30)  # (y_start, y_end, x_start, x_end) 32x32 이미지 기준, 유사도 비교 시 사용할 관심 영역(ROI) 좌표
DEFAULT_THRESHOLD = 0.50  # SSIM 유사도 비교 시 기본 임계값
MIN_THRESHOLD = 0.01  # 임계값 스핀박스 최소값
MAX_THRESHOLD = 1.00  # 임계값 스핀박스 최대값 (SSIM 최대값)
THRESHOLD_STEP = 0.01  # 임계값 스핀박스 증감 단위
MAX_WORKERS = max(1, multiprocessing.cpu_count() - 1)  # 병렬 처리 시 사용할 최대 스레드 수 (CPU 코어 수 - 1, 최소 1개)
MAX_PREVIEW_WIDTH = 400  # 유사도 테스트 창에서 원본 캡처 이미지 미리보기의 최대 너비
TEST_WINDOW_WIDTH = 750  # 유사도 비교 테스트 결과 창의 너비
TEST_WINDOW_HEIGHT = 750  # 유사도 비교 테스트 결과 창의 높이

# 설정값: 다국어 지원 및 서버/정렬 옵션
# 각 언어별로 pcrdfans.com의 URL, 서버 선택 옵션(UI 표시 텍스트, 실제 값), 정렬 옵션을 정의
LANGUAGE_OPTIONS = {
    "中文": {  # 중국어 설정
        "url": "https://pcrdfans.com/battle",
        "server_options": [("全部角色", "1"), ("国服", "2"), ("台服", "3"), ("日服", "4"), ("国际服", "5")],
        "sorting_options": [("综合排序", "1"), ("按时间", "2"), ("按评价", "3")]
    },
    "English": {  # 영어 설정
        "url": "https://pcrdfans.com/en/battle",
        "server_options": [("All", "1"), ("Global", "5"), ("CN", "2"), ("TW", "3"), ("JP", "4")],
        "sorting_options": [("Default Sort", "1"), ("Sort by Time", "2"), ("Sort by Rating", "3")]
    },
    "日本語": {  # 일본어 설정
        "url": "https://pcrdfans.com/jp/battle",
        "server_options": [("すべて", "1"), ("JP", "4"), ("CN", "2"), ("TW", "3"), ("Global", "5")],
        "sorting_options": [("デフォルトのソート", "1"), ("投稿日時", "2"), ("評価", "3")]
    }
}

# GUI 상태, 사용자 설정, 외부 서비스(WebDriver, 이미지 매니저) 상태,
# 처리 중인 데이터(캡처 이미지, 분할 아이콘 등) 등 다양한 상태 정보 관리.
class ArenaDeckApp:
    """
    프리코네 아레나 조합 자동 검색기 메인 클래스.
    GUI 생성, 사용자 입력 처리, 웹 자동화, 이미지 처리 등 모든 기능 총괄.
    """
    def __init__(self, root):
        """
        ArenaDeckApp 애플리케이션 초기화.
        :param root: Tkinter의 최상위 윈도우 객체 (tk.Tk())
        """
        self.root = root  # 메인 윈도우 저장
        self._setup_window()  # 메인 윈도우 기본 설정 (제목, 크기, 위치)
        self._init_variables()  # 애플리케이션에서 사용될 각종 변수 초기화
        self._create_menu()  # 애플리케이션 메뉴 생성 및 배치
        self._create_ui_components()  # GUI 요소들 생성 및 배치
        self._setup_event_handlers()  # 이벤트 핸들러(예: 마우스휠) 설정
        self.log_message(f"{get_timestamp()} 프로그램 실행 성공\n")  # 실행 성공 로그
        self._show_initial_guide()  # 사용자에게 초기 작업 순서 안내 메시지 표시

    def _create_menu(self):
        """
        애플리케이션 메뉴 바 생성.
        """
        menubar = tk.Menu(self.root)

        # "정보(About)" 항목
        main_menu = tk.Menu(menubar, tearoff=0)  # tearoff=0은 메뉴를 창에서 분리할 수 없게 함
        main_menu.add_command(label="정보(About)", command=self.show_program_about)

        # "개발자 웹사이트" 항목
        main_menu.add_command(label="개발자 웹사이트 (Developer Website)", command=self.open_developer_website)

        # 메뉴바에 "정보" 메뉴 추가
        menubar.add_cascade(label="메뉴(Menu)", menu=main_menu)

        # 윈도우에 메뉴바 설정
        self.root.config(menu=menubar)

    def show_program_about(self):
        """
        프로그램 정보(About) 대화상자 표시.
        """
        show_program_about_text = """프리코네 아레나 조합 자동 검색기
(Priconne Arena Deck Auto Searcher)

Version: 1.0.0

Created by (Github) IZH318 in 2025.

이 소프트웨어는 GNU General Public License v3 (GPLv3)에 따라 라이선스가 부여됩니다.
(This software is licensed under the GNU General Public License v3 (GPLv3).)

이 소프트웨어의 사용으로 인해 발생하는 모든 문제에 대한 책임은 사용자 본인에게 있습니다.
(This software's usage is solely the responsibility of the user for any issues that may arise.)
"""
        messagebox.showinfo("정보(About)", show_program_about_text)

    def open_developer_website(self):
        """
        개발자 GitHub 페이지를 웹 브라우저에서 엽니다.
        """
        url = "https://github.com/IZH318"
        try:
            webbrowser.open_new_tab(url)
            self.log_message(f"{get_timestamp()} 개발자 웹사이트({url})를 열었습니다.")
        except Exception as e:
            self.log_message(f"{get_timestamp()} 개발자 웹사이트를 여는 중 오류 발생: {e}")
            messagebox.showerror("오류", f"웹사이트를 여는 중 오류가 발생했습니다: {e}")

    def _show_initial_guide(self):
        """
        프로그램 시작 시 사용자 작업 순서 안내 가이드 메시지 로그창 표시.
        """
        guide_text = (
            f"{get_timestamp()} ===== 작업 순서 =====\n"
            " → ① 언어/Language, 게임 서버/Game Server, 정렬/Sorting 드롭 박스 설정\n"
            " → ② [사이트 연결] 버튼 클릭\n"
            " → ③ [아레나 조합 캡쳐] 버튼 클릭\n"
            " → ④ 임계값 설정\n"
            " → ⑤ [아레나 조합 검색] 버튼 클릭\n"
            " (※ 전체 캐릭터 아이콘과 관련 된 문제 발생 시 [(수동) 전체 캐릭터 아이콘 다운로드] 버튼 클릭하여 다시 다운로드)\n"
        )
        self.log_message(guide_text)  # 로그창에 안내 메시지 출력

    def _setup_window(self):
        """
        메인 윈도우 제목, 크기, 화면 중앙 위치 등 설정.
        """
        self.root.title("프리코네 아레나 조합 자동 검색기")  # 윈도우 제목 설정
        screen_width = self.root.winfo_screenwidth()  # 현재 화면 너비 가져오기
        screen_height = self.root.winfo_screenheight()  # 현재 화면 높이 가져오기
        # 창을 화면 중앙에 위치시키기 위한 x, y 좌표 계산
        x = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")  # 창 크기 및 위치 설정

    def _init_variables(self):
        """
        애플리케이션 사용 주요 클래스 변수 초기화.
        애플리케이션의 현재 상태를 나타내며, 사용자 인터랙션 및 내부 로직에 따라 변경.
        """
        # --- 화면 캡처 관련 상태 변수 ---
        # 사용자가 화면의 특정 영역을 드래그하여 캡처하는 과정과 관련된 상태 저장.
        # 캡처 시작 시점부터 이미지 분할 완료까지 이 변수 업데이트.
        self.start_x = None  # 화면 캡처 시 드래그 시작 x 좌표
        self.start_y = None  # 화면 캡처 시 드래그 시작 y 좌표
        self.rect = None  # 화면 캡처 시 드래그 영역을 표시하는 사각형 객체 (Tkinter Canvas 아이템)
        self.capture_coords = None  # 최종 캡처된 영역의 좌표 (x1, y1, x2, y2)
        self.captured_img = None  # 캡처된 원본 PIL.Image 객체
        self.split_imgs = []  # 캡처된 이미지에서 분할된 개별 캐릭터 아이콘 PIL.Image 객체들의 리스트
        
        # --- 사용자 설정 및 UI 상태 변수 ---
        # GUI를 통해 사용자가 설정하는 값들(언어, 서버, 임계값 등)과 이와 연동된 Tkinter 변수들
        # 이 값들은 웹 자동화 시 필터 조건 등으로 사용.
        self.match_threshold = tk.DoubleVar(value=DEFAULT_THRESHOLD) # 유사도 임계값
        self.selected_language = tk.StringVar(value="English")      # 선택된 언어 (기본: 영어)
        self.selected_server = tk.StringVar(value="1")              # 선택된 서버의 실제 값 (기본: "1")
        self.server_dropdown_var = tk.StringVar()                   # 서버 드롭다운 UI 표시용
        self.selected_sorting = tk.StringVar(value="1")             # 선택된 정렬 방식의 실제 값 (기본: "1")
        self.sorting_dropdown_var = tk.StringVar()                  # 정렬 드롭다운 UI 표시용

        # --- 외부 서비스 연동 상태 변수 ---
        # Selenium WebDriver, 캐릭터 아이콘 매니저 등 외부 모듈/서비스와의 연결 상태 및 인스턴스 관리
        self.driver = None  # Selenium WebDriver 인스턴스 (초기에는 없음)
        self.char_manager = CharacterImageManager(log_callback=self.log_message)  # pcrdfans.com 스프라이트 아이콘 관리
        self.all_char_manager = AllCharacterImageManager(log_callback=self.log_message)  # redive.estertion.win 전체 캐릭터 아이콘 관리
        
        # --- 기타 내부 상태 및 캐시 ---
        self.image_cache = {}  # 이미지 로드 및 전처리 결과를 캐싱하여 성능 향상 (딕셔너리)

    def _create_ui_components(self):
        """
        애플리케이션 사용자 인터페이스(UI) 컴포넌트 생성 및 배치.
        각 부분(상단, 버튼, 임계값 등)별 별도 메서드 호출 생성.
        """
        self._create_top_frame()  # 언어/서버/정렬 선택 드롭다운이 있는 상단 프레임
        self._create_button_frame()  # 사이트 연결, 아이콘 다운로드 버튼 프레임
        self._create_split_preview_frame()  # 분할된 아이콘 미리보기 프레임
        self._create_threshold_frame()  # 유사도 임계값 설정 스핀박스 프레임
        self._create_search_buttons()  # 유사도 테스트, 조합 검색 버튼 프레임
        self._create_result_textbox()  # 로그 및 결과 표시 텍스트 박스

    def _create_top_frame(self):
        """
        언어, 게임 서버, 정렬 방식 선택 드롭다운 메뉴 포함 상단 프레임 생성.
        """
        top_frame = tk.Frame(self.root)  # 메인 윈도우 내에 프레임 생성
        top_frame.pack(pady=5)  # 프레임을 윈도우에 배치 (위/아래 여백 5픽셀)
        
        # 언어 선택 드롭다운
        tk.Label(top_frame, text="언어/Language:").pack(side=tk.LEFT, padx=5)  # 레이블 추가
        self.language_dropdown = tk.OptionMenu(
            top_frame, 
            self.selected_language,  # 선택값을 저장할 Tkinter 변수
            *LANGUAGE_OPTIONS.keys()  # LANGUAGE_OPTIONS 딕셔너리의 키들(언어명)을 옵션으로 제공
        )
        self.language_dropdown.pack(side=tk.LEFT)  # 드롭다운 배치
        
        # 게임 서버 선택 드롭다운
        tk.Label(top_frame, text="게임 서버/Game Server:").pack(side=tk.LEFT, padx=5)
        self.server_dropdown = tk.OptionMenu(top_frame, self.server_dropdown_var, "") # 초기 옵션은 비워둠 (동적 로드)
        self.server_dropdown.pack(side=tk.LEFT)
        # 서버 드롭다운 값(표시 텍스트) 변경 시 _on_server_dropdown_select 콜백 호출하도록 trace 설정
        self._server_dropdown_trace_id = self.server_dropdown_var.trace(
            'w',  # 쓰기 모드 (값이 변경될 때)
            self._on_server_dropdown_select
        )
        self._update_server_dropdown()  # 현재 언어에 맞춰 서버 드롭다운 옵션 업데이트
        
        # 정렬 방식 선택 드롭다운
        tk.Label(top_frame, text="정렬/Sorting:").pack(side=tk.LEFT, padx=5)
        self.sorting_dropdown = tk.OptionMenu(top_frame, self.sorting_dropdown_var, "") # 초기 옵션 비워둠
        self.sorting_dropdown.pack(side=tk.LEFT)
        # 정렬 드롭다운 값 변경 시 _on_sorting_dropdown_select 콜백 호출하도록 trace 설정
        self._sorting_dropdown_trace_id = self.sorting_dropdown_var.trace(
            'w', 
            self._on_sorting_dropdown_select
        )
        self._update_sorting_dropdown()  # 현재 언어에 맞춰 정렬 드롭다운 옵션 업데이트
        
        # 언어 선택(selected_language) 변경 시 _on_language_change 콜백 호출하도록 trace 설정
        self.selected_language.trace('w', self._on_language_change)

    def _create_button_frame(self):
        """
        주요 기능 버튼("사이트 연결", "전체 캐릭터 아이콘 다운로드") 포함 프레임 생성.
        """
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        # "사이트 연결" 버튼
        self.connect_btn = tk.Button(
            button_frame, 
            text="사이트 연결",
            command=self.connect_site  # 클릭 시 connect_site 메서드 호출
        )
        self.connect_btn.pack(side=tk.LEFT, padx=5)

        # "(수동) 전체 캐릭터 아이콘 다운로드" 버튼
        self.download_all_btn = tk.Button(
            button_frame,
            text="(수동) 전체 캐릭터 아이콘 다운로드",
            command=self.download_all_icons  # 클릭 시 download_all_icons 메서드 호출
        )
        self.download_all_btn.pack(side=tk.LEFT, padx=5)

        # "아레나 조합 캡쳐" 버튼 (이 버튼은 button_frame이 아닌 root에 직접 배치됨)
        self.capture_btn = tk.Button(
            self.root,  # 메인 윈도우에 직접 배치
            text="아레나 조합 캡쳐",
            command=self.start_drag_capture  # 클릭 시 start_drag_capture 메서드 호출
        )
        self.capture_btn.pack(pady=5)

    def _create_threshold_frame(self):
        """
        이미지 유사도 비교 사용 임계값(threshold) 설정 스핀박스 포함 프레임 생성.
        """
        threshold_frame = tk.Frame(self.root)
        threshold_frame.pack(pady=5)
        
        tk.Label(threshold_frame, text="임계값: ").pack(side=tk.LEFT)  # "임계값:" 레이블
        self.threshold_spinbox = tk.Spinbox(
            threshold_frame,
            from_=MIN_THRESHOLD,  # 최소값
            to=MAX_THRESHOLD,  # 최대값
            increment=THRESHOLD_STEP,  # 증감 단위
            textvariable=self.match_threshold,  # 값을 저장할 Tkinter 변수
            width=5,  # 스핀박스 너비
            format="%.2f"  # 값 표시 형식 (소수점 둘째 자리까지)
        )
        self.threshold_spinbox.pack(side=tk.LEFT)

    def _create_split_preview_frame(self):
        """
        캡처 이미지 분할 개별 캐릭터 아이콘 미리보기 표시 프레임 생성.
        """
        self.split_preview_frame = tk.Frame(self.root, height=50) # 높이 50으로 프레임 생성
        self.split_preview_frame.pack(pady=5) # 배치

    def _create_search_buttons(self):
        """
         "유사도 비교 테스트" 및 "아레나 조합 검색" 버튼 포함 프레임 생성. (초기 비활성화 상태.)
        """
        search_button_frame = tk.Frame(self.root)
        search_button_frame.pack(pady=10)

        # "유사도 비교 테스트" 버튼
        self.test_btn = tk.Button(
            search_button_frame,
            text="유사도 비교 테스트",
            command=self.test_similarity,  # 클릭 시 test_similarity 메서드 호출
            state=tk.DISABLED  # 초기 상태: 비활성화
        )
        self.test_btn.pack(side=tk.LEFT, padx=5)

        # "아레나 조합 검색" 버튼
        self.search_btn = tk.Button(
            search_button_frame,
            text="아레나 조합 검색",
            command=self.start_search,  # 클릭 시 start_search 메서드 호출
            state=tk.DISABLED  # 초기 상태: 비활성화
        )
        self.search_btn.pack(side=tk.LEFT, padx=5)

    def _create_result_textbox(self):
        """
        프로그램 작업 로그 및 결과 메시지 표시 텍스트 박스, 스크롤바 생성.
        """
        text_frame = tk.Frame(self.root)  # 텍스트 박스와 스크롤바를 담을 프레임
        text_frame.pack(pady=5, fill=tk.BOTH, expand=True)  # 프레임을 채우고 확장 가능하도록 배치
        
        self.result_textbox = tk.Text(text_frame, height=12, width=50)  # 텍스트 박스 생성
        self.result_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # 텍스트 박스 배치
        
        scrollbar = tk.Scrollbar(text_frame, command=self.result_textbox.yview)  # 스크롤바 생성, 텍스트 박스와 연결
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # 스크롤바 배치 (오른쪽, Y축 채움)
        self.result_textbox.config(yscrollcommand=scrollbar.set)  # 텍스트 박스의 스크롤을 스크롤바와 동기화

    def _setup_event_handlers(self):
        """
        UI 컴포넌트 이벤트 핸들러(주로 마우스 이벤트) 설정.
        """
        # 임계값 스핀박스에 마우스 휠 이벤트 바인딩
        self.threshold_spinbox.bind("<MouseWheel>", self.on_threshold_mousewheel)  # Windows, macOS
        self.threshold_spinbox.bind("<Button-4>", self.on_threshold_mousewheel)  # Linux (휠 위로)
        self.threshold_spinbox.bind("<Button-5>", self.on_threshold_mousewheel)  # Linux (휠 아래로)

    def _update_server_dropdown(self):
        """
        현재 선택 언어 맞춰 게임 서버 선택 드롭다운 메뉴 옵션 업데이트.
        """
        language = self.selected_language.get()  # 현재 선택된 언어 가져오기
        menu = self.server_dropdown["menu"]  # 드롭다운의 메뉴 객체 가져오기
        menu.delete(0, "end")  # 기존 메뉴 아이템 모두 삭제
        options = LANGUAGE_OPTIONS[language]["server_options"]  # 해당 언어의 서버 옵션 목록 가져오기
        
        # self.server_dropdown_var의 trace를 일시적으로 해제 (무한 콜백 방지)
        try:
            if hasattr(self, '_server_dropdown_trace_id'): # trace_id가 존재할 때만 삭제 시도
                self.server_dropdown_var.trace_vdelete('w', self._server_dropdown_trace_id)
        except tk.TclError: # 존재하지 않는 trace id 삭제 시도 시 TclError 발생 가능
            pass
        except AttributeError:  # trace_id가 아직 설정되지 않은 경우 등
            pass
            
        # 새 옵션들로 메뉴 다시 채우기
        for label, value in options:  # (표시 텍스트, 실제 값)
            # 각 옵션을 메뉴에 추가. 선택 시 _set_server_value 호출 (사용자 액션임을 표시)
            menu.add_command(
                label=label,
                command=lambda v=value: self._set_server_value(v, user_action=True)
            )
            
        current_value = self.selected_server.get()  # 현재 선택된 서버의 실제 값
        # 현재 값에 해당하는 표시 텍스트를 드롭다운에 설정
        for label, value in options:
            if value == current_value:
                self.server_dropdown_var.set(label)  # 표시 텍스트 설정
                break
        else:  # 현재 값이 옵션 목록에 없으면 (예: 언어 변경 직후)
            if options: # 옵션이 하나라도 있다면
                self.selected_server.set(options[0][1])  # 첫 번째 옵션의 값으로 실제 값 설정
                self.server_dropdown_var.set(options[0][0])  # 첫 번째 옵션의 표시 텍스트로 설정
            else: # 옵션이 없다면 (이론상 발생하기 어려움)
                self.selected_server.set("")
                self.server_dropdown_var.set("")

        # trace 재설정
        self._server_dropdown_trace_id = self.server_dropdown_var.trace(
            'w',
            self._on_server_dropdown_select
        )

    def _update_sorting_dropdown(self):
        """
        현재 선택 언어 맞춰 정렬 방식 선택 드롭다운 메뉴 옵션 업데이트.
        (* '_update_server_dropdown'과 유사한 로직으로 동작.)
        """
        language = self.selected_language.get()
        menu = self.sorting_dropdown["menu"]
        menu.delete(0, "end")
        options = LANGUAGE_OPTIONS[language]["sorting_options"]
        
        # self.sorting_dropdown_var의 trace 일시 해제
        try:
            if hasattr(self, '_sorting_dropdown_trace_id'):
                self.sorting_dropdown_var.trace_vdelete('w', self._sorting_dropdown_trace_id)
        except tk.TclError:
            pass
        except AttributeError:
            pass
            
        for label, value in options:
            menu.add_command(
                label=label,
                command=lambda v=value: self._set_sorting_value(v, user_action=True)
            )
            
        current_value = self.selected_sorting.get()
        for label, value in options:
            if value == current_value:
                self.sorting_dropdown_var.set(label)
                break
        else:
            if options:
                self.selected_sorting.set(options[0][1])
                self.sorting_dropdown_var.set(options[0][0])
            else:
                self.selected_sorting.set("")
                self.sorting_dropdown_var.set("")
            
        # trace 재설정
        self._sorting_dropdown_trace_id = self.sorting_dropdown_var.trace(
            'w',
            self._on_sorting_dropdown_select
        )

    def _set_server_value(self, value, user_action=False):
        """
        선택 서버 실제 값(value) 설정, UI(드롭다운 표시 텍스트) 업데이트.
        사용자 직접 선택 시(user_action=True) 웹사이트 변경 사항 적용.
        :param value: 설정할 서버의 실제 값
        :param user_action: 사용자가 직접 드롭다운 메뉴에서 선택했는지 여부
        """
        self.selected_server.set(value)  # 실제 서버 값 업데이트
        self._update_server_dropdown()  # 드롭다운 UI 업데이트 (표시 텍스트 동기화)
        if user_action:  # 사용자가 직접 선택한 경우
            self._on_server_change()  # 웹사이트에 서버 변경 사항 적용 시도

    def _set_sorting_value(self, value, user_action=False):
        """
        선택 정렬 방식 실제 값(value) 설정, UI 업데이트.
        (* '_set_server_value'와 유사하게 동작.)
        :param value: 설정할 정렬 방식의 실제 값
        :param user_action: 사용자가 직접 드롭다운 메뉴에서 선택했는지 여부
        """
        self.selected_sorting.set(value)
        self._update_sorting_dropdown()
        if user_action:
            self._on_sorting_change()

    def _on_server_dropdown_select(self, *args):
        """
        서버 드롭다운 메뉴 사용자 항목 (표시 텍스트 기준) 선택 시 호출.
        선택 표시 텍스트 해당 실제 값 찾아 설정, 웹사이트 변경 시도.
        """
        language = self.selected_language.get()
        label = self.server_dropdown_var.get()  # 선택된 표시 텍스트
        # 표시 텍스트에 해당하는 실제 값을 LANGUAGE_OPTIONS에서 찾음
        for l, v in LANGUAGE_OPTIONS[language]["server_options"]:
            if l == label:
                self.selected_server.set(v)  # 실제 값 설정
                break
        # self._update_server_dropdown() # _set_server_value에서 호출되므로 중복 방지 위해 주석 처리 가능성.
                                          # 그러나 안전을 위해 유지하거나, _set_server_value의 user_action=False로 호출하는 방법도 고려.
                                          # 현재는 _set_server_value가 user_action=True로 호출하도록 하여 _on_server_change가 트리거 되도록 함.
        self._on_server_change()  # 웹사이트에 변경 적용

    def _on_sorting_dropdown_select(self, *args):
        """
        정렬 드롭다운 메뉴 사용자 항목 선택 시 호출.
        (* '_on_server_dropdown_select'와 유사하게 동작.)
        """
        language = self.selected_language.get()
        label = self.sorting_dropdown_var.get()
        for l, v in LANGUAGE_OPTIONS[language]["sorting_options"]:
            if l == label:
                self.selected_sorting.set(v)
                break
        # self._update_sorting_dropdown() # 위와 동일한 이유로 검토.
        self._on_sorting_change()

    def _on_language_change(self, *args):
        """
        언어 선택 드롭다운 값 변경 시 호출.
        서버/정렬 드롭다운 옵션 새 언어 맞게 업데이트,
        Selenium 드라이버가 연결된 상태라면 웹사이트도 해당 언어 페이지로 변경하는 작업을
        별도 스레드에서 수행.
        """
        # 드라이버(웹 브라우저)가 아직 연결되지 않았으면 서버/정렬 드롭다운만 업데이트하고 종료
        if self.driver is None:
            self._update_server_dropdown()
            self._update_sorting_dropdown()
            return
            
        # 언어 변경에 따른 서버/정렬 드롭다운 UI 업데이트 (메인 스레드에서 즉시 수행)
        self._update_server_dropdown()
        self._update_sorting_dropdown()
        
        # 나머지 장시간 작업(Selenium 및 run_automation)은 별도 스레드에서 실행
        threading.Thread(target=self._perform_language_change_web_operations).start()

    def _perform_language_change_web_operations(self):
        """
        별도 스레드 웹사이트 언어 변경 및 관련 작업 수행.
        """
        # 작업 시작 전 관련 UI 요소 비활성화 (메인 스레드에서 실행되도록 root.after 사용)
        self.root.after(0, self._set_language_change_ui_busy_state, True) # True는 busy 상태(비활성화)

        try:
            language = self.selected_language.get() # 현재 선택된 (새) 언어
            url = LANGUAGE_OPTIONS[language]["url"]
            self.log_message(f"{get_timestamp()} {language} 페이지로 변경 중...")
            
            # Selenium 웹 작업 (페이지 이동, 쿠키/스토리지 정리, 새로고침, 대기)
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
            self.driver.get(url)
            self.driver.refresh()
            
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "battle_search_radio"))
            )
            
            # 웹페이지에 현재 선택된 서버 및 정렬 방식 적용
            self._apply_server_selection()  # Selenium 작업
            self._on_sorting_change()       # Selenium 작업
            
            # 분할된 이미지가 있는 경우, 아레나 조합 자동 검색 실행
            if hasattr(self, 'split_imgs') and self.split_imgs:
                self.log_message(f"{get_timestamp()} 이미지 비교 중... (임계값: {self.match_threshold.get()}) 잠시만 기다려주세요.")
                self.log_message(f"{get_timestamp()} 선택된 아이콘 초기화 중...")
                
                # 웹페이지 패널 확장
                self.log_message(f"{get_timestamp()} 모든 패널 확장 중...")
                collapse_root = self.driver.find_element(By.CLASS_NAME, "ant-collapse-icon-position-left")
                items = collapse_root.find_elements(By.CLASS_NAME, "ant-collapse-item")
                
                for item in items:
                    header = item.find_element(By.CLASS_NAME, "ant-collapse-header")
                    if header.get_attribute("aria-expanded") == "false":
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", header)
                            time.sleep(0.1)
                            self.driver.execute_script("arguments[0].click();", header)
                            time.sleep(0.2)
                        except Exception:
                            continue
                
                self.driver.execute_script("window.scrollTo(0, 0);") # 화면 맨 위로 스크롤
                time.sleep(0.5)
                
                # 아레나 조합 검색 실행 (Selenium 작업이 주이므로 스레드에서 OK)
                self.run_automation(self.split_imgs)
            
            self.log_message(f"{get_timestamp()} 언어 변경 완료!\n")
            
        except Exception as e:
            self.log_message(f"{get_timestamp()} 언어 변경 중 오류 발생: {str(e)}\n")
            # 오류 메시지 박스는 메인 스레드에서 표시
            self.root.after(0, lambda: messagebox.showerror("오류", f"언어 변경 중 오류가 발생했습니다: {str(e)}"))
        finally:
            # 작업 완료 후 관련 UI 요소 다시 활성화 (메인 스레드에서 실행되도록 root.after 사용)
            self.root.after(0, self._set_language_change_ui_busy_state, False) # False는 non-busy 상태(활성화)

    def _set_language_change_ui_busy_state(self, busy):
        """
        언어 변경 작업 중/후 UI 요소 활성/비활성 상태 설정.
        :param busy: True이면 UI를 비활성화(작업 중), False이면 활성화(작업 완료).
        """
        new_state = tk.DISABLED if busy else tk.NORMAL
        
        # 상태를 변경할 UI 요소들
        self.connect_btn.config(state=new_state)
        self.language_dropdown.config(state=new_state)
        self.download_all_btn.config(state=new_state)
        self.server_dropdown.config(state=new_state)
        self.sorting_dropdown.config(state=new_state)
        self.capture_btn.config(state=new_state)
        self.threshold_spinbox.config(state=new_state)

        # test_btn, search_btn은 조건부로 상태 결정
        if not busy: # 활성화 시 (작업 완료 시)
            if self.split_imgs: # 분할된 이미지가 있으면
                self.test_btn.config(state=tk.NORMAL)
                self.search_btn.config(state=tk.NORMAL)
            else: # 분할된 이미지가 없으면
                self.test_btn.config(state=tk.DISABLED)
                self.search_btn.config(state=tk.DISABLED)
        else: # 비활성화 시 (작업 중)
            self.test_btn.config(state=tk.DISABLED)
            self.search_btn.config(state=tk.DISABLED)

    def _on_server_change(self, *args):
        """
        게임 서버 선택 변경 시 호출. (주로 '_set_server_value' 또는 '_on_server_dropdown_select' 의해)
        Selenium 드라이버 연결 상태면 웹사이트 서버 선택 변경.
        """
        if self.driver is None:  # 드라이버 없으면 아무것도 안 함
            return
            
        try:
            self._apply_server_selection()  # 웹사이트에 현재 선택된 서버 적용
        except Exception as e:
            self.log_message(f"{get_timestamp()} 서버 변경 중 오류 발생: {str(e)}")
            messagebox.showerror("오류", f"서버 변경 중 오류가 발생했습니다: {str(e)}")

    def _on_sorting_change(self, *args):
        """
        정렬 방식 선택 변경 시 호출.
        Selenium 드라이버 연결 상태면 웹사이트 정렬 방식 선택 변경.
        """
        if self.driver is None:  # 드라이버 없으면 아무것도 안 함
            return
            
        try:
            current_value = self.selected_sorting.get()  # 현재 선택된 정렬 방식의 실제 값
            if current_value:
                # 웹페이지에서 정렬 방식 라디오 버튼 그룹들을 모두 찾음
                all_radio_groups = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".ant-radio-group.ant-radio-group-solid.battle_search_radio" # 공통 CSS 선택자
                )
                
                # 여러 라디오 그룹 중, 실제 "정렬"에 해당하는 그룹을 찾아 클릭
                # (서버 선택 그룹과 HTML 구조가 유사하여 구분 필요)
                # 여기서는 'body_margin_content' 클래스를 가진 조상이 없는 그룹을 실제 정렬 그룹으로 판단
                for group in all_radio_groups:
                    parents = group.find_elements(
                        By.XPATH,
                        "ancestor::*[contains(@class, 'body_margin_content')]" # 서버 선택 그룹의 특징적 조상
                    )
                    if not parents:  # 해당 조상이 없으면 이 그룹이 정렬 방식 그룹임
                        # 해당 그룹 내에서 현재 값에 맞는 라디오 버튼 input 요소를 찾아 클릭
                        radio_input = group.find_element(
                            By.CSS_SELECTOR,
                            f"input.ant-radio-button-input[value='{current_value}']"
                        )
                        self.driver.execute_script("arguments[0].click();", radio_input) # JavaScript로 클릭
                        time.sleep(0.2)  # 클릭 후 잠시 대기
                        self._update_sorting_dropdown()  # UI 드롭다운 업데이트 (실제론 큰 변화 없을 수 있음)
                        self.log_message(
                            f"{get_timestamp()} 정렬 방식 변경 완료: "
                            f"{self.sorting_dropdown_var.get()}" # 현재 드롭다운에 표시된 텍스트로 로그
                        )
                        break  # 정렬 그룹 찾았으므로 루프 종료
                        
        except Exception as e:
            self.log_message(f"{get_timestamp()} 정렬 방식 적용 중 오류 발생: {str(e)}")
            raise  # 오류 발생 시 예외를 다시 발생시켜 호출한 곳에서 처리할 수 있도록 함

    def _apply_server_selection(self):
        """
        현재 GUI에서 선택된 서버 설정 Selenium을 통해 웹페이지에 적용.
        """
        if self.driver is None:  # 드라이버 없으면 아무것도 안 함
            return
            
        try:
            current_value = self.selected_server.get()  # 현재 선택된 서버의 실제 값
            if current_value:
                # 서버 선택 라디오 버튼 그룹을 찾음 (보통 페이지 상단에 위치)
                group = self.driver.find_element(
                    By.CSS_SELECTOR,
                    ".body_margin_content .battle_search_radio" # 서버 선택 그룹의 특징적 CSS 선택자
                )
                # 해당 그룹 내에서 현재 값에 맞는 라디오 버튼 input 요소를 찾아 클릭
                radio_input = group.find_element(
                    By.CSS_SELECTOR,
                    f"input.ant-radio-button-input[value='{current_value}']"
                )
                self.driver.execute_script("arguments[0].click();", radio_input) # JavaScript로 클릭
                time.sleep(0.2)  # 클릭 후 잠시 대기
                self._update_server_dropdown()  # UI 드롭다운 업데이트
                self.log_message(
                    f"{get_timestamp()} 서버 변경 완료: "
                    f"{self.server_dropdown_var.get()}" # 현재 드롭다운 표시 텍스트로 로그
                )
                
        except Exception as e:
            self.log_message(f"{get_timestamp()} 서버 선택 적용 중 오류 발생: {str(e)}")
            raise  # 예외 다시 발생

    def log_message(self, msg):
        """
        주어진 메시지 GUI 결과 텍스트 박스 추가, 항상 최신 로그 보이도록 스크롤.
        :param msg: 텍스트 박스에 추가할 로그 메시지 문자열
        """
        self.result_textbox.insert(tk.END, f"{msg}\n")  # 텍스트 박스 끝에 메시지 추가
        self.result_textbox.see(tk.END)  # 텍스트 박스 스크롤을 맨 아래로 이동

    def on_threshold_mousewheel(self, event):
        """
        임계값 스핀박스에서 마우스 휠 스크롤 이벤트 발생 시 호출.
        휠 방향에 따라 임계값 증감.
        :param event: 마우스 휠 이벤트 객체
        """
        try:
            val = self.match_threshold.get()  # 현재 임계값 가져오기
            # event.num (Linux) 또는 event.delta (Windows/macOS) 값으로 휠 방향 판단
            if event.num == 5 or event.delta < 0:  # 휠 아래로 (값 감소)
                val = max(MIN_THRESHOLD, round(val - THRESHOLD_STEP, 2)) # 최소값 제한, 소수점 둘째자리 반올림
            elif event.num == 4 or event.delta > 0:  # 휠 위로 (값 증가)
                val = min(MAX_THRESHOLD, round(val + THRESHOLD_STEP, 2)) # 최대값 제한
            self.match_threshold.set(f"{val:.2f}")  # 변경된 값을 다시 문자열 포맷으로 설정
        except Exception:  # 값 변환 등에서 오류 발생 시 무시
            pass

    def _check_driver_status(self):
        """
        Selenium WebDriver 현재 상태 확인.
        드라이버 초기화 여부, 브라우저 창 열림 여부 등 간접 확인.
        :return: 드라이버가 유효하면 True, 아니면 False
        """
        try:
            if self.driver is None:  # 드라이버 객체가 없으면
                return False
            _ = self.driver.current_url  # 드라이버의 속성에 접근 시도 (브라우저 닫혔으면 예외 발생)
            return True
        except Exception:  # 예외 발생 시 (예: 브라우저 닫힘)
            self.driver = None  # 드라이버 참조를 None으로 설정
            return False

    def connect_site(self):
        """
        "사이트 연결" 버튼 클릭 시 호출.
        이미 연결된 상태가 아니면 별도 스레드에서 웹사이트 연결 및 초기화 작업 수행.
        """
        if self._check_driver_status():  # 이미 드라이버가 유효하면
            self.log_message(f"{get_timestamp()} 이미 사이트에 연결되어 있습니다.")
            messagebox.showinfo("알림", "이미 사이트에 연결되어 있습니다.")
            return

        self.log_message(f"{get_timestamp()} 사이트 연결 중...")
        # 연결 작업 중에는 관련 UI 요소들 비활성화
        self.connect_btn.config(state=tk.DISABLED)
        self.language_dropdown.config(state=tk.DISABLED)
        self.download_all_btn.config(state=tk.DISABLED)
        self.server_dropdown.config(state=tk.DISABLED)
        self.sorting_dropdown.config(state=tk.DISABLED)
        # _connect_site_thread 메서드를 별도 스레드에서 실행 (GUI 프리징 방지)
        threading.Thread(target=self._connect_site_thread).start()

    def _connect_site_thread(self):
        """
        별도의 스레드에서 pcrdfans.com 사이트 연결 및 초기 설정 수행.
        - 웹드라이버 초기화
        - 선택된 언어/서버/정렬 방식에 따라 페이지 로드 및 설정 적용
        - 캐릭터 아이콘(스프라이트) 버전 확인, 다운로드 및 처리
        - 필요한 경우 전체 캐릭터 아이콘(estertion.win) 자동 다운로드 트리거
        """
        try:
            # character_images 폴더 생성 (이미 있으면 무시)
            images_dir = Path("character_images")
            images_dir.mkdir(exist_ok=True)
            
            # character_unit_icon_all 폴더 존재 여부 및 JPG 파일 유무 확인 (자동 다운로드 필요성 판단)
            all_icons_dir = images_dir / "character_unit_icon_all"
            need_download = not all_icons_dir.exists() or not any(all_icons_dir.glob("*.jpg"))
            
            # CharacterImageManager 재초기화 (이전에 드라이버가 닫혔을 수 있으므로)
            # 로그 콜백 설정 및 메타데이터 경로 재지정
            self.char_manager = CharacterImageManager(log_callback=self.log_message)
            self.char_manager.images_dir = images_dir # 이 부분은 CharacterImageManager 내부에서 이미 설정됨. 명시적 재설정.
            self.char_manager.metadata_file = images_dir / "arena_web_metadata.json" # 메타데이터 파일 경로
            self.char_manager.metadata = self.char_manager.load_metadata() # 메타데이터 로드
            self.char_manager.current_index = 0 # 인덱스 초기화

            self.log_message(f"{get_timestamp()} 웹드라이버 초기화 중...")
            # webdriver-manager를 사용하여 ChromeDriver 자동 관리 및 초기화
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            
            language = self.selected_language.get()  # 현재 선택된 언어
            
            # 선택된 언어에 따라 URL 설정 및 페이지 로드/새로고침
            # 새로고침은 브라우저 캐시 문제를 피하기 위함일 수 있음
            if language == "English":
                url = "https://pcrdfans.com/en/battle"
                self.log_message(f"{get_timestamp()} 영어 페이지 로드 중...")
                self.driver.get(url)
                self.driver.refresh()
            elif language == "日本語":
                url = "https://pcrdfans.com/jp/battle"
                self.log_message(f"{get_timestamp()} 일본어 페이지 로드 중...")
                self.driver.get(url)
                self.driver.refresh()
            else:  # "中文" (기본값 또는 명시적 선택)
                url = "https://pcrdfans.com/battle"
                self.log_message(f"{get_timestamp()} 중국어 페이지 로드 중...")
                self.driver.get(url)
                self.driver.refresh() # 추가함

            self.log_message(f"{get_timestamp()} 페이지 로딩 대기 중...")
            # 페이지의 아코디언 패널 루트 요소가 나타날 때까지 대기 (최대 15초)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ant-collapse-icon-position-left"))
            )
            
            # 페이지 로딩 완료 후, 현재 GUI에서 선택된 서버 및 정렬 방식을 웹페이지에 적용
            self.log_message(f"{get_timestamp()} 현재 설정된 서버와 정렬 방식 적용 중...")
            try:
                # 서버 설정 적용
                current_server = self.selected_server.get()
                if current_server:
                    group = self.driver.find_element(
                        By.CSS_SELECTOR,
                        ".body_margin_content .battle_search_radio" # 서버 선택 라디오 그룹
                    )
                    radio_input = group.find_element(
                        By.CSS_SELECTOR,
                        f"input.ant-radio-button-input[value='{current_server}']"
                    )
                    self.driver.execute_script("arguments[0].click();", radio_input) # JS로 클릭
                    time.sleep(0.2)
                    self.log_message(f"{get_timestamp()} 서버 설정 적용 완료: {self.server_dropdown_var.get()}")

                # 정렬 방식 적용
                current_sorting = self.selected_sorting.get()
                if current_sorting:
                    all_radio_groups = self.driver.find_elements(By.CSS_SELECTOR, ".ant-radio-group.ant-radio-group-solid.battle_search_radio")
                    for group in all_radio_groups:
                        # 서버 선택 그룹과 구분하기 위해, 'body_margin_content' 조상이 없는 그룹을 정렬 그룹으로 간주
                        parents = group.find_elements(By.XPATH, "ancestor::*[contains(@class, 'body_margin_content')]")
                        if not parents:
                            radio_input = group.find_element(
                                By.CSS_SELECTOR,
                                f"input.ant-radio-button-input[value='{current_sorting}']"
                            )
                            self.driver.execute_script("arguments[0].click();", radio_input)
                            time.sleep(0.2)
                            self.log_message(f"{get_timestamp()} 정렬 방식 적용 완료: {self.sorting_dropdown_var.get()}")
                            break
            except Exception as e:
                self.log_message(f"{get_timestamp()} 서버/정렬 설정 적용 중 오류 발생: {str(e)}")
            
            # 웹사이트의 캐릭터 아이콘(스프라이트) 처리
            self.log_message(f"{get_timestamp()} 패널 처리 중...")
            collapse_root = self.driver.find_element(By.CLASS_NAME, "ant-collapse-icon-position-left") # 아코디언 패널의 루트
            items = collapse_root.find_elements(By.CLASS_NAME, "ant-collapse-item") # 각 아코디언 아이템(패널)
            
            # 1. 모든 패널 열기 (모든 캐릭터 아이콘 div가 DOM에 로드되도록)
            self.log_message(f"{get_timestamp()} 모든 패널 열기 중...")
            for item in items:
                header = item.find_element(By.CLASS_NAME, "ant-collapse-header") # 패널 헤더
                if header.get_attribute("aria-expanded") == "false": # 패널이 닫혀있으면
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", header) # 헤더가 보이도록 스크롤
                        time.sleep(0.1)
                        self.driver.execute_script("arguments[0].click();", header) # JS로 클릭하여 열기
                        time.sleep(0.2) # 패널 열리는 시간 대기
                    except Exception: # 클릭 중 오류 발생 시 (예: 다른 요소에 가려짐) 무시
                        continue
            
            # 2. 모든 캐릭터 아이콘 div 요소 수집
            self.log_message(f"{get_timestamp()} 아이콘 수집 중...")
            all_icon_divs = []
            for item in items: # 열린 각 패널에 대해
                content_box = item.find_element(By.CLASS_NAME, "ant-collapse-content-box") # 패널 내용 부분
                # 특정 스타일 속성(배경 이미지, 위치, 크기)을 가진 div들을 아이콘으로 간주하고 수집
                icon_divs = content_box.find_elements(By.XPATH, ".//div[contains(@style, 'background-image') and contains(@style, 'background-position') and contains(@style, 'background-size')]")
                all_icon_divs.extend(icon_divs)
            
            # 3. 스프라이트 아이콘 URL 및 버전 찾기
            self.log_message(f"{get_timestamp()} 스프라이트 아이콘 URL 찾는 중...")
            sprite_url = None
            new_version = None
            for div in all_icon_divs: # 수집된 아이콘 div 중 하나에서
                style = div.get_attribute("style")
                # 정규 표현식으로 "background-image: url('/charas-VERSION.png')" 패턴 찾기
                m = re.search(r"background-image:\s*url\(['\"]?/charas-(\d+)\.png['\"]?\)", style)
                if m:
                    # URL과 버전 번호 추출
                    sprite_url = m.group(0).split("'")[1] if "'" in m.group(0) else m.group(0).split('"')[1]
                    new_version = m.group(1)
                    break # 하나 찾으면 충분
            
            if sprite_url and new_version: # URL과 버전 모두 찾았으면
                # 상대 URL인 경우 절대 URL로 변환
                if sprite_url.startswith("/"):
                    from urllib.parse import urljoin
                    sprite_url = urljoin(self.driver.current_url, sprite_url)
                
                # 로컬 버전 정보 업데이트 및 자동 전체 캐릭터 아이콘 다운로드 필요 여부 결정
                # CharacterImageManager의 현재 버전 상태를 확인하고, 새 버전이면 업데이트
                # self.char_manager.current_version은 이미 로드된 상태. 여기서 업데이트 전 값을 old_version으로 저장
                old_version_before_update = self.char_manager.get_current_version()
                version_changed = self.char_manager.update_version(new_version) # 버전 변경 시 True 반환
                
                if version_changed or need_download: # 버전이 바뀌었거나, 전체 캐릭터 아이콘 폴더가 비어있으면
                    self.log_message(f"{get_timestamp()} {'=' * 60}")
                    if version_changed:
                        self.log_message(f"{get_timestamp()} 새로운 버전이 감지되었습니다!")
                        self.log_message(f"{get_timestamp()} 이전 버전: {old_version_before_update}") # 이전 버전 표시
                        self.log_message(f"{get_timestamp()} 새로운 버전: {new_version}")
                    if need_download:
                        self.log_message(f"{get_timestamp()} 전체 캐릭터 아이콘 폴더가 없거나 비어있습니다!")
                        self.log_message(f"{get_timestamp()} 전체 캐릭터 아이콘 자동 다운로드를 시작합니다...")
                    self.log_message(f"{get_timestamp()} {'=' * 60}")
                else: # 버전 동일하고, 전체 캐릭터 아이콘 폴더도 정상이면
                    self.log_message(f"{get_timestamp()} {'=' * 60}")
                    self.log_message(f"{get_timestamp()} 버전 체크 결과:")
                    self.log_message(f"{get_timestamp()} 현재 버전({new_version})이 최신 상태입니다.")
                    self.log_message(f"{get_timestamp()} 로컬 전체 캐릭터 아이콘이 이미 존재합니다. (필요시 수동 업데이트)")
                    self.log_message(f"{get_timestamp()} {'=' * 60}")
                
                # 스프라이트 시트 처리 (다운로드, 분리, 저장)
                self.log_message(f"{get_timestamp()} 아이콘 처리 중...")
                self.char_manager.process_sprite_image(sprite_url, all_icon_divs)
            
                # 4. 모든 패널 닫기
                self.log_message(f"{get_timestamp()} 패널 닫는 중...")
                for item in items:
                    header = item.find_element(By.CLASS_NAME, "ant-collapse-header")
                    if header.get_attribute("aria-expanded") == "true": # 패널이 열려있으면
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", header)
                            time.sleep(0.1)
                            self.driver.execute_script("arguments[0].click();", header) # JS로 클릭하여 닫기
                            time.sleep(0.2)
                        except Exception: # 오류 시 무시
                            continue
                
                # 5. 화면을 맨 위로 스크롤
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.5)

                self.log_message(f"{get_timestamp()} 사이트 연결 및 아이콘 처리 완료!\n")
                
                # GUI 업데이트는 메인 스레드에서 실행 (tk.after 사용)
                self.root.after(0, lambda: [
                    self.connect_btn.config(state=tk.NORMAL), # 연결 버튼 활성화
                    self.download_all_btn.config(state=tk.NORMAL), # 수동 다운로드 버튼 활성화
                    self.capture_btn.config(state=tk.NORMAL), # 캡처 버튼 활성화
                    self.language_dropdown.config(state=tk.NORMAL), # 언어 드롭다운 활성화
                    self.server_dropdown.config(state=tk.NORMAL), # 서버 드롭다운 활성화
                    self.sorting_dropdown.config(state=tk.NORMAL) # 정렬 드롭다운 활성화
                ])

                # 사이트 연결 완료 후, 필요시 전체 캐릭터 아이콘 다운로드 실행
                if version_changed or need_download:
                    # _download_all_icons_thread를 별도 스레드로 실행 (GUI 프리징 방지)
                    # from_connect_site=True 플래그 전달
                    self.root.after(100, lambda: threading.Thread(target=self._download_all_icons_thread, args=(True,)).start())
                else:
                    # 전체 캐릭터 아이콘 다운로드 불필요 시, 연결 성공 알림만 표시
                    # self.search_btn.config(state=tk.NORMAL) # 아레나 조합 검색 버튼 활성화 -> 아직 캡처 전이므로 비활성화 유지
                    self.root.after(0, lambda: messagebox.showinfo("알림", "사이트 연결: 성공"))

        except Exception as e: # 사이트 연결 전체 과정 중 예외 발생 시
            self.log_message(f"{get_timestamp()} 사이트 연결 실패: {str(e)}\n")
            # GUI 업데이트 (메인 스레드)
            self.root.after(0, lambda: [
                messagebox.showerror("오류", "사이트 연결: 실패"), # 오류 메시지 박스
                self.connect_btn.config(state=tk.NORMAL), # 연결 버튼 다시 활성화
                self.language_dropdown.config(state=tk.NORMAL), # 언어 드롭다운 활성화
                self.download_all_btn.config(state=tk.NORMAL), # 수동 다운로드 버튼 활성화
                self.server_dropdown.config(state=tk.NORMAL), # 일관성을 위해 활성화
                self.sorting_dropdown.config(state=tk.NORMAL)  # 일관성을 위해 활성화
            ])
            if self.driver: # 드라이버가 생성되었다면
                self.driver.quit() # 드라이버 종료
                self.driver = None # 참조 제거

    def _download_all_icons_thread(self, from_connect_site=False):
        """
        'AllCharacterImageManager' 사용 전체 캐릭터 아이콘 백그라운드 스레드 다운로드,
        완료 시 통합 알림 메시지(사이트 연결 결과 + 아이콘 다운로드 결과) 표시.
        :param from_connect_site: 이 메서드가 사이트 연결 과정에서 호출되었는지 여부
        """
        # 다운로드 중에는 관련 버튼들 비활성화
        # UI 업데이트는 메인 스레드에서 하도록 root.after 사용
        def set_buttons_state(state):
            self.download_all_btn.config(state=state)
            # 검색 버튼은 다운로드 성공 시에만 활성화되도록 별도 관리
            if state == tk.DISABLED:
                self.search_btn.config(state=tk.DISABLED)
            # 사이트 연결 버튼, 캡처 버튼 등 다른 버튼은 그대로 둠

        self.root.after(0, lambda: set_buttons_state(tk.DISABLED))

        try:
            success = self.all_char_manager.download_all_icons() # 실제 다운로드 실행
            
            if success: # 성공 시
                title = "알림"
                if from_connect_site:
                    final_message = "사이트 연결: 성공\n전체 캐릭터 아이콘 다운로드: 성공"
                else:
                    final_message = "전체 캐릭터 아이콘 다운로드: 성공"
                # 다운로드 성공 시, 그리고 split_imgs가 이미 있다면 검색 버튼 활성화
                if self.split_imgs: # 이미 캡처된 이미지가 있다면 검색 버튼 활성화
                    self.root.after(0, lambda: self.search_btn.config(state=tk.NORMAL))

                self.root.after(0, lambda: messagebox.showinfo(title, final_message))
            else: # 실패 시
                title = "오류"
                if from_connect_site:
                    final_message = "사이트 연결: 성공\n전체 캐릭터 아이콘 다운로드: 실패"
                else:
                    final_message = "전체 캐릭터 아이콘 다운로드: 실패"
                self.root.after(0, lambda: messagebox.showerror(title, final_message))
        except Exception as e: # _download_all_icons_thread 자체에서 예외 발생 시
            self.log_message(f"{get_timestamp()} 전체 아이콘 다운로드 스레드 오류: {str(e)}")
            title = "오류"
            if from_connect_site:
                final_message = "사이트 연결: 성공\n전체 캐릭터 아이콘 다운로드 중 심각한 오류 발생"
            else:
                final_message = "전체 캐릭터 아이콘 다운로드 중 심각한 오류 발생"
            self.root.after(0, lambda: messagebox.showerror(title, final_message))
        finally: # 성공/실패 여부와 관계없이
            # 메인 스레드에서 다운로드 버튼 다시 활성화
            self.root.after(0, lambda: set_buttons_state(tk.NORMAL))


    def start_drag_capture(self):
        """
        "아레나 조합 캡쳐" 버튼 클릭 시 호출.
        메인 윈도우 숨김, 화면 드래그 캡처 위한 반투명 전체화면 창 생성.
        """
        self.root.withdraw()  # 메인 윈도우 숨기기
        # 메인 창이 화면에서 완전히 사라질 시간을 확보하기 위해 짧은 지연을 줌.
        # 이 지연이 없으면 메인 창이 캡처될 수 있음.
        self.root.update_idletasks() # Tkinter의 보류 중인 UI 업데이트를 강제로 처리
        time.sleep(0.2) # 0.2초 지연 (환경에 따라 조절 가능)
        self._create_capture_window()  # 캡처용 새 창 생성 및 전체 화면 캡처 시작

    def _create_capture_window(self):
        """
        화면 드래그 캡처 위한 반투명 전체화면 창 (Toplevel) 생성 및 설정.
        이 함수가 호출되는 시점에 전체 화면을 미리 캡처하여,
        드래그 중 선택 영역을 원본 밝기로 표시하는 데 사용.
        """
        # 1. 전체 화면 미리 캡처 (메인 창이 숨겨진 후 실행)
        try:
            # ImageGrab.grab()은 현재 전체 화면의 스크린샷을 PIL.Image 객체로 반환.
            self.full_screen_capture = ImageGrab.grab()
            if self.full_screen_capture is None: # 캡처 실패 시
                messagebox.showerror("오류", "전체 화면 캡처에 실패했습니다.")
                self.root.deiconify() # 숨겼던 메인 창 다시 표시
                return # 캡처 창 생성 중단
        except Exception as e: # 기타 예외 발생 시
            messagebox.showerror("오류", f"전체 화면 캡처 중 오류: {str(e)}")
            self.root.deiconify() # 메인 창 다시 표시
            return # 캡처 창 생성 중단

        # 2. 캡처용 Toplevel 창 생성 및 설정
        self.capture_window = tk.Toplevel()  # 새 최상위 창 생성
        self.capture_window.attributes('-fullscreen', True)  # 전체화면 모드로 설정
        # 창 전체의 투명도 설정 (0.0: 완전 투명, 1.0: 완전 불투명)
        # 0.3으로 설정하여 배경이 어둡게 비치도록 함.
        self.capture_window.attributes('-alpha', 0.3)
        # 창 배경색 설정. '-alpha'에 의해 반투명하게 보임.
        self.capture_window.config(bg='black')  # 검은색 배경으로 어두운 효과 강조

        # 3. 캡처 영역 선택 및 이미지 표시를 위한 Canvas 생성
        self.capture_canvas = tk.Canvas(
            self.capture_window,
            cursor="cross",  # 마우스 커서를 십자 모양으로 변경 (선택 모드 암시)
            bg='black',      # 캔버스 배경색도 창 배경과 통일 (실제로는 창 투명도에 영향 받음)
            highlightthickness=0  # 캔버스 자체의 테두선 없앰
        )
        self.capture_canvas.pack(fill=tk.BOTH, expand=True)  # 캔버스를 캡처 창에 꽉 채움

        # 4. 드래그 영역에 표시할 이미지 관련 변수 초기화
        # 드래그 중인 영역의 원본 이미지를 담을 Tkinter PhotoImage 객체
        self.tk_selected_region_image = None
        # 해당 PhotoImage를 캔버스에 표시하는 아이템의 ID
        self.canvas_selected_region_item = None
        # 드래그 영역 테두리를 표시하는 사각형 아이템의 ID (기존 코드에서 self.rect로 사용되던 변수)
        # self.rect는 _init_variables에서 None으로 초기화되어야 함. on_mouse_down에서 생성.

        # 5. 마우스 이벤트 핸들러 바인딩
        self._setup_capture_bindings() # 캡처 창에 마우스 이벤트 연결

    def _setup_capture_bindings(self):
        """
        캡처 창(Toplevel)의 Canvas 위젯에 마우스 버튼 및 드래그 이벤트 바인딩.
        이를 통해 사용자의 드래그 동작을 감지하고 처리.
        """
        # 마우스 왼쪽 버튼 누름(<ButtonPress-1>) 이벤트 발생 시 self.on_mouse_down 메서드 호출
        self.capture_window.bind('<ButtonPress-1>', self.on_mouse_down)
        # 마우스 왼쪽 버튼을 누른 채로 움직이는(<B1-Motion>) 이벤트 발생 시 self.on_mouse_drag 메서드 호출
        self.capture_window.bind('<B1-Motion>', self.on_mouse_drag)
        # 마우스 왼쪽 버튼에서 손을 떼는(<ButtonRelease-1>) 이벤트 발생 시 self.on_mouse_up 메서드 호출
        self.capture_window.bind('<ButtonRelease-1>', self.on_mouse_up)

    def on_mouse_down(self, event):
        """
        캡처 창에서 마우스 왼쪽 버튼이 눌렸을 때 호출됨.
        드래그 시작점의 화면 전체 좌표와 캔버스 로컬 좌표를 기록.
        이전에 그려진 선택 영역 이미지 및 테두리를 초기화.
        :param event: 마우스 이벤트 객체 (사용되진 않지만 Tkinter 바인딩 콜백의 표준 파라미터)
        """
        # 캔버스의 화면상 절대 위치(좌상단 기준)를 가져옴.
        # 이를 통해 화면 전체 마우스 좌표를 캔버스 로컬 좌표로 변환하는 데 사용.
        self.canvas_origin_x = self.capture_canvas.winfo_rootx()
        self.canvas_origin_y = self.capture_canvas.winfo_rooty()

        # 드래그 시작점의 화면 전체 좌표 (X, Y)
        self.start_x_screen = self.capture_window.winfo_pointerx()
        self.start_y_screen = self.capture_window.winfo_pointery()

        # 드래그 시작점의 캔버스 로컬 좌표 (X, Y)
        # 캔버스에 도형이나 이미지를 그릴 때 사용.
        self.start_x_canvas = self.start_x_screen - self.canvas_origin_x
        self.start_y_canvas = self.start_y_screen - self.canvas_origin_y

        # 이전에 그려진 빨간색 테두리 사각형(self.rect)이 있다면 삭제.
        if hasattr(self, 'rect') and self.rect:
            self.capture_canvas.delete(self.rect)
            self.rect = None # ID 참조도 None으로 초기화

        # 이전에 표시된 선택 영역 원본 이미지(self.canvas_selected_region_item)가 있다면 삭제.
        if self.canvas_selected_region_item:
            self.capture_canvas.delete(self.canvas_selected_region_item)
            self.canvas_selected_region_item = None # ID 참조도 None으로 초기화
            self.tk_selected_region_image = None    # PhotoImage 객체 참조도 해제

        # 드래그 영역을 시각적으로 표시하기 위한 빨간색 테두리 사각형 생성.
        # 처음에는 시작점과 끝점이 같으므로 점으로 보임.
        self.rect = self.capture_canvas.create_rectangle(
            self.start_x_canvas, self.start_y_canvas, # 사각형의 좌상단 x, y
            self.start_x_canvas, self.start_y_canvas, # 사각형의 우하단 x, y (초기에는 동일)
            outline='red',  # 테두리 색상
            width=2         # 테두리 두께
        )

    def on_mouse_drag(self, event):
        """
        캡처 창에서 마우스 왼쪽 버튼을 누른 채로 드래그할 때 계속 호출됨.
        현재 드래그 중인 영역을 계산하여, 해당 부분의 원본 이미지를 캔버스에 표시하고
        빨간색 테두리도 업데이트하여 사용자에게 시각적 피드백을 제공.
        :param event: 마우스 이벤트 객체 (사용되진 않지만 필요)
        """
        # on_mouse_down이 정상적으로 호출되어 start_x_screen이 설정되었는지 확인.
        # (예: 창 포커스 문제 등으로 on_mouse_down이 스킵되는 극히 드문 경우 방지)
        if not hasattr(self, 'start_x_screen'):
            return

        # 현재 마우스 포인터의 화면 전체 좌표
        cur_x_screen = self.capture_window.winfo_pointerx()
        cur_y_screen = self.capture_window.winfo_pointery()

        # 현재 마우스 포인터의 캔버스 로컬 좌표
        cur_x_canvas = cur_x_screen - self.canvas_origin_x
        cur_y_canvas = cur_y_screen - self.canvas_origin_y

        # 드래그 영역의 화면 전체 좌표 계산 (정규화: x1 < x2, y1 < y2 보장)
        # 이 좌표는 full_screen_capture에서 이미지를 crop할 때 사용됨.
        x1 = min(self.start_x_screen, cur_x_screen)
        y1 = min(self.start_y_screen, cur_y_screen)
        x2 = max(self.start_x_screen, cur_x_screen)
        y2 = max(self.start_y_screen, cur_y_screen)

        # 드래그 영역의 캔버스 로컬 좌표 계산 (정규화)
        # 이 좌표는 캔버스에 테두리나 이미지를 그릴 때 사용됨.
        cx1 = min(self.start_x_canvas, cur_x_canvas)
        cy1 = min(self.start_y_canvas, cur_y_canvas)
        cx2 = max(self.start_x_canvas, cur_x_canvas)
        cy2 = max(self.start_y_canvas, cur_y_canvas)

        # 빨간색 테두리 사각형의 좌표를 현재 드래그 영역에 맞게 업데이트.
        if self.rect:
            self.capture_canvas.coords(self.rect, cx1, cy1, cx2, cy2)

        # 드래그 영역이 유효한 크기(너비와 높이가 0보다 큼)를 가질 때만 이미지 처리.
        if x2 > x1 and y2 > y1:
            try:
                # 미리 캡처해둔 전체 화면 이미지(self.full_screen_capture)에서
                # 현재 드래그 영역(화면 좌표 x1, y1, x2, y2)에 해당하는 부분을 잘라냄 (crop).
                selected_region_pil = self.full_screen_capture.crop((x1, y1, x2, y2))

                # 잘라낸 PIL 이미지를 Tkinter에서 사용할 수 있는 PhotoImage 객체로 변환.
                # 이 객체는 캔버스 아이템에 의해 참조되어야 가비지 컬렉션되지 않음.
                self.tk_selected_region_image = ImageTk.PhotoImage(selected_region_pil)

                if self.canvas_selected_region_item is None:
                    # 아직 캔버스에 선택 영역 이미지가 없으면 새로 생성.
                    # 이미지는 캔버스의 (cx1, cy1) 위치에 그려지며, anchor='nw'는
                    # 이미지의 좌상단 모서리가 (cx1, cy1)에 위치하도록 함.
                    self.canvas_selected_region_item = self.capture_canvas.create_image(
                        cx1, cy1, anchor='nw', image=self.tk_selected_region_image
                    )
                else:
                    # 이미 캔버스에 선택 영역 이미지가 있으면, 좌표와 이미지만 업데이트.
                    self.capture_canvas.coords(self.canvas_selected_region_item, cx1, cy1)
                    self.capture_canvas.itemconfig(self.canvas_selected_region_item, image=self.tk_selected_region_image)

                # 선택된 영역 이미지를 가장 위로 가져와서 빨간 테두리보다 위에 보이도록 함.
                # (만약 테두리를 이미지보다 위에 표시하고 싶다면 이 순서를 바꾸거나 tag_lower 사용)
                if self.rect: # 테두리가 그려져 있다면
                    self.capture_canvas.tag_raise(self.canvas_selected_region_item, self.rect)

            except Exception as e: # 이미지 crop 또는 그리기 중 예외 발생 시
                self.log_message(f"{get_timestamp()} Error during drag (cropping/drawing): {e}") # 디버깅용
                # 오류 발생 시 이전에 표시된 이미지가 있다면 삭제.
                if self.canvas_selected_region_item:
                    self.capture_canvas.delete(self.canvas_selected_region_item)
                    self.canvas_selected_region_item = None
                self.tk_selected_region_image = None # PhotoImage 참조도 해제
        else:
            # 드래그 영역의 크기가 유효하지 않으면(예: 너비나 높이가 0이거나 음수)
            # 이전에 표시된 선택 영역 이미지가 있다면 삭제.
            if self.canvas_selected_region_item:
                self.capture_canvas.delete(self.canvas_selected_region_item)
                self.canvas_selected_region_item = None
            self.tk_selected_region_image = None

    def on_mouse_up(self, event):
        """
        캡처 창에서 마우스 왼쪽 버튼을 떼었을 때 호출됨.
        최종 드래그 영역의 화면 전체 좌표를 self.capture_coords에 저장.
        캡처 창을 닫고, 메인 창을 다시 표시한 후, 캡처 후 처리 로직(after_capture)을 호출.
        :param event: 마우스 이벤트 객체 (사용되진 않지만 필요)
        """
        # on_mouse_down이 정상적으로 호출되었는지 확인.
        if not hasattr(self, 'start_x_screen'):
            self.capture_window.destroy() # 예외 상황이므로 캡처 창 즉시 닫음
            self.root.deiconify()         # 메인 창 다시 표시
            # after_capture 호출 시 플래그를 False로 하여 일반 캡처 시도 (또는 오류 처리)
            self.after_capture(use_full_screen_capture=False)
            return

        # 마우스 버튼을 뗀 위치의 화면 전체 좌표
        end_x_screen = self.capture_window.winfo_pointerx()
        end_y_screen = self.capture_window.winfo_pointery()

        # 최종 캡처 영역의 화면 전체 좌표 계산 및 저장 (정규화).
        # 이 좌표는 after_capture에서 이미지를 잘라내는 데 사용됨.
        self.capture_coords = (
            min(self.start_x_screen, end_x_screen),
            min(self.start_y_screen, end_y_screen),
            max(self.start_x_screen, end_x_screen),
            max(self.start_y_screen, end_y_screen)
        )

        self.capture_window.destroy()  # 캡처 창 닫기
        self.root.deiconify()          # 메인 애플리케이션 창 다시 표시
        # 캡처 후 처리 함수 호출. use_full_screen_capture=True로 전달하여
        # 미리 캡처한 전체 화면 이미지를 사용하도록 지시.
        self.after_capture(use_full_screen_capture=True)

    # 파라미터 'use_full_screen_capture' 추가됨
    def after_capture(self, use_full_screen_capture=False):
        """
        화면 캡처 완료 후 호출됨.
        use_full_screen_capture 플래그에 따라 미리 캡처된 이미지 또는
        새로 화면을 캡처하여 최종 이미지를 얻고, 아이콘 분할 및 미리보기 표시.
        :param use_full_screen_capture: True이면 self.full_screen_capture 사용,
                                       False이면 ImageGrab.grab(bbox) 사용.
        """
        try:
            img = None # 최종 캡처될 이미지를 담을 변수
            if use_full_screen_capture and \
               hasattr(self, 'full_screen_capture') and \
               self.full_screen_capture and \
               hasattr(self, 'capture_coords') and \
               self.capture_coords:
                # 미리 캡처된 전체 화면 이미지에서 최종 선택 영역(self.capture_coords)을 잘라냄.
                img = self.full_screen_capture.crop(self.capture_coords)
            else:
                # use_full_screen_capture가 False이거나 필요한 변수가 없는 경우 (fallback).
                # 또는, on_mouse_up에서 비정상적으로 종료된 경우.
                if not hasattr(self, 'capture_coords') or not self.capture_coords:
                    self.log_message(f"{get_timestamp()} 캡처 좌표가 설정되지 않았습니다.\n");
                    messagebox.showerror("오류", "캡처 좌표가 설정되지 않았습니다.")
                    self._reset_capture_state_and_ui() # 관련 상태 초기화
                    return
                # 지정된 영역(bbox=self.capture_coords)만 새로 캡처.
                img = ImageGrab.grab(bbox=self.capture_coords)

            # 캡처된 이미지가 유효한지 확인 (None이 아니고, 너비와 높이가 0보다 큰지).
            if img is None or img.size[0] == 0 or img.size[1] == 0:
                self.log_message(f"{get_timestamp()} 이미지 캡처에 실패했습니다. 다시 시도해주세요.\n")
                messagebox.showerror("오류", "이미지 캡처에 실패했습니다.\n\n다시 시도해주세요.")
                self._reset_capture_state_and_ui() # 관련 상태 초기화
                return

            self.captured_img = img  # 최종 캡처된 이미지를 클래스 변수에 저장
            self.split_and_preview() # 캡처된 이미지에서 아이콘 분할 및 GUI에 미리보기 표시

            # 분할된 이미지가 성공적으로 생성되었으면 검색/테스트 버튼 활성화.
            if self.split_imgs:
                self.search_btn.config(state=tk.NORMAL)
                self.test_btn.config(state=tk.NORMAL)
            else: # 분할 실패 시 버튼 비활성화.
                self.search_btn.config(state=tk.DISABLED)
                self.test_btn.config(state=tk.DISABLED)

        except Exception as e: # 캡처 또는 후처리 중 예외 발생 시
            self.log_message(f"{get_timestamp()} 이미지 캡처 후 처리 중 오류가 발생했습니다. 다시 시도해주세요.\n");
            messagebox.showerror("오류", f"이미지 캡처 후 처리 중 오류가 발생했습니다.\n\n{str(e)}\n\n다시 시도해주세요.")
            self._reset_capture_state_and_ui() # 관련 상태 초기화
        finally:
            # 사용된 전체 화면 캡처 이미지(self.full_screen_capture)가 있다면 메모리에서 해제.
            if hasattr(self, 'full_screen_capture'):
                del self.full_screen_capture

            self.tk_selected_region_image = None
            self.canvas_selected_region_item = None

    def _reset_capture_state_and_ui(self):
        """
        캡처 관련 작업 실패 또는 완료 후 관련 상태를 초기화하고 UI 버튼 상태를 업데이트하는 헬퍼 함수.
        """
        # 검색 및 테스트 버튼 비활성화
        if hasattr(self, 'search_btn'): self.search_btn.config(state=tk.DISABLED)
        if hasattr(self, 'test_btn'): self.test_btn.config(state=tk.DISABLED)

        # 캡처 이미지 및 분할 이미지 관련 변수 초기화
        self.captured_img = None
        self.split_imgs = []

        # 미리보기 프레임의 모든 자식 위젯(이전 미리보기 이미지들) 삭제
        if hasattr(self, 'split_preview_frame'):
            for widget in self.split_preview_frame.winfo_children():
                widget.destroy()

    def split_and_preview(self):
        """
        캡처된 이미지(self.captured_img)에서 OpenCV를 사용하여 둥근 모서리 사각형 모양의
        캐릭터 아이콘을 자동으로 감지하고, 각 아이콘을 분할하여 GUI에 미리보기로 표시.
        """
        # 기존 미리보기 이미지들 삭제 (이전 캡처 결과가 남아있지 않도록)
        if hasattr(self, 'split_preview_frame'): # split_preview_frame이 생성되었는지 확인
            for widget in self.split_preview_frame.winfo_children():
                widget.destroy()
        self.split_imgs = []  # 분할된 이미지들을 저장할 리스트 초기화

        if not self.captured_img:  # 캡처된 이미지가 없으면 (예: 캡처 실패) 함수 종료
            return

        # 아이콘 자동 감지 내부 함수 정의
        def find_rounded_rect_icons(pil_img):
            """
            PIL 이미지 입력, OpenCV 사용 둥근 모서리 사각형 아이콘 찾기,
            경계 상자(x, y, w, h) 리스트 반환.
            """
            img = np.array(pil_img)  # PIL 이미지를 OpenCV에서 처리 가능한 NumPy 배열로 변환
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 그레이스케일로 변환
            blur = cv2.GaussianBlur(gray, (5, 5), 0)  # 가우시안 블러로 노이즈 제거 (5x5 커널)
            edged = cv2.Canny(blur, 30, 150)  # Canny 엣지 검출 (임계값 30, 150)

            # 엣지 이미지에서 윤곽선(contours) 찾기
            # RETR_EXTERNAL: 가장 바깥쪽 윤곽선만 찾음. CHAIN_APPROX_SIMPLE: 윤곽선 꼭짓점만 저장하여 메모리 절약.
            contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            icon_boxes = []  # 감지된 아이콘의 경계 상자를 저장할 리스트
            for cnt in contours:  # 찾은 모든 윤곽선에 대해
                # 윤곽선을 다각형으로 근사화 (Douglas-Peucker 알고리즘). 두 번째 인자는 근사 정확도.
                approx = cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)
                area = cv2.contourArea(cnt)  # 윤곽선의 면적 계산
                if len(approx) == 4 and area > 1000:  # 근사화된 다각형의 꼭짓점이 4개(사각형)이고, 면적이 1000 이상이면
                    x, y, w, h = cv2.boundingRect(approx)  # 경계 사각형 좌표(좌상단 x,y 와 너비,높이) 얻기
                    aspect = w / h  # 가로/세로 비율 계산
                    if 0.8 < aspect < 1.2:  # 비율이 정사각형에 가까우면 (0.8 ~ 1.2)
                        icon_boxes.append((x, y, w, h))  # 아이콘 후보로 추가
            # 감지된 아이콘들을 좌상단 좌표 기준으로 정렬 (x좌표 우선, 그 다음 y좌표)
            icon_boxes = sorted(icon_boxes, key=lambda b: (b[0], b[1]))
            return icon_boxes # 정렬된 아이콘 경계 상자 리스트 반환

        # 캡처된 이미지에서 아이콘 감지 실행
        icon_boxes = find_rounded_rect_icons(self.captured_img)
        if not icon_boxes:  # 감지된 아이콘이 없으면
            self.log_message(f"{get_timestamp()} 둥근 사각형 모양의 아이콘을 감지하지 못했습니다.")
            return

        # 감지된 각 아이콘에 대해
        for i, (x, y, w, h) in enumerate(icon_boxes):
            crop = self.captured_img.crop((x, y, x + w, y + h))  # 원본 캡처 이미지에서 아이콘 영역 잘라내기
            self.split_imgs.append(crop)  # 분할 이미지 리스트에 추가
            self._add_preview_image(crop, i)  # GUI에 미리보기 이미지 추가

    def _add_preview_image(self, crop, index):
        """
        분할 단일 캐릭터 아이콘 이미지 받아 GUI 미리보기 프레임 표시.
        :param crop: 분할된 캐릭터 아이콘 PIL.Image 객체
        """
        preview = crop.resize((50, 50))  # GUI 표시용 크기(50x50)로 리사이즈
        # PIL 이미지를 Tkinter에서 사용할 수 있는 PhotoImage 객체로 변환
        # 이 객체는 Label 위젯 등에 의해 참조가 유지되어야 가비지 컬렉션되지 않음 (lbl.image = img_tk)
        img_tk = ImageTk.PhotoImage(preview)
        lbl = tk.Label(self.split_preview_frame, image=img_tk)  # 이미지 레이블 생성
        lbl.image = img_tk  # PhotoImage 객체에 대한 참조 유지
        lbl.pack(side=tk.LEFT, padx=2)  # 미리보기 프레임 왼쪽에 차례로 배치 (좌우 여백 2픽셀)

    def start_search(self):
        """
        "아레나 조합 검색" 버튼 클릭 시 호출.
        설정 임계값 확인, 유효하면 'run_automation' 메서드 별도 스레드 실행.
        """
        try:
            threshold = self.match_threshold.get()  # 현재 설정된 임계값 가져오기
            if not (MIN_THRESHOLD <= threshold <= MAX_THRESHOLD):  # 임계값이 유효 범위(0.01~1.00)인지 확인
                messagebox.showerror("오류", f"임계값은 {MIN_THRESHOLD}에서 {MAX_THRESHOLD} 사이의 값만 입력 가능합니다.")
                return
            # run_automation을 별도 스레드에서 실행 (GUI 프리징 방지). 분할된 이미지 리스트 전달.
            threading.Thread(target=self.run_automation, args=(self.split_imgs,)).start()
        except Exception as e: # 임계값 가져오는 중 오류 (예: tk.DoubleVar 설정 문제)
            messagebox.showerror("오류", f"임계값 설정 중 오류가 발생했습니다: {str(e)}")
            return

    def download_all_icons(self):
        """
        "(수동) 전체 캐릭터 아이콘 다운로드" 버튼 클릭 시 호출.
        사용자 다운로드 필요성 안내/확인 후, 실제 다운로드 작업 시작.
        """
        # 사용자에게 표시할 안내 메시지
        # 자동 다운로드 조건, 수동 다운로드 권장 경우, 파일 처리 과정 등을 설명
        message = (
            " • 이 작업은 사이트 연결 버튼을 처음 클릭 하거나, 새로운 버전이 감지되면 자동으로 다운로드됩니다.\n\n"
            "※ 다음의 경우에만 전체 캐릭터 아이콘 다운로드를 권장합니다:\n"
            "  - 다운로드된 아이콘 파일이 손상된 경우\n"
            "  - 아이콘 파일이 누락되거나 오류가 발생한 경우\n"
            "  - character_unit_icon_all 폴더가 없거나 비어있는 경우\n"
            "  - character_unit_icon_all 폴더에 JPG 파일이 하나도 없는 경우\n\n"
            "※ 파일 처리 과정:\n"
            "  - WebP 파일을 다운로드 후 JPG로 변환합니다.\n"
            "  - 변환 완료 후 원본 WebP 파일은 자동으로 삭제됩니다.\n"
            "  - 최종적으로 JPG 파일만 저장됩니다.\n\n"
            "전체 캐릭터 아이콘을 다시 다운로드 하시겠습니까?"
        )
        
        # 사용자에게 예/아니오 질문 메시지 박스 표시
        if messagebox.askyesno("전체 캐릭터 아이콘 다운로드 안내", message):
            # '예' 선택 시, _download_all_icons_thread를 별도 스레드에서 실행 (from_connect_site=False 기본값 사용)
            threading.Thread(target=self._download_all_icons_thread).start()
        else: # '아니오' 선택 시
            self.log_message(f"{get_timestamp()} 전체 캐릭터 아이콘 다운로드가 취소되었습니다.\n")

    def get_3star_jpg(self, jpg_file):
        """
        주어진 JPG 파일(Path 객체) ★6 캐릭터 아이콘일 경우 (파일명 패턴 'xxxx6x.jpg'),
        해당 캐릭터 ★3 아이콘 파일명('xxxx3x.jpg') 생성,
        파일 실제 존재 시 해당 Path 객체 반환.
        :param jpg_file: 분석할 ★6 캐릭터 아이콘의 Path 객체
        :return: 대응하는 ★3 아이콘 Path 객체 또는 None
        """
        name = jpg_file.name  # 파일명 문자열 가져오기
        
        # 파일명 길이 및 ★6 패턴 확인 (예: "100161.jpg")
        if len(name) >= 7 and name[4] == '6': # 5번째 문자(인덱스 4)가 '6'이면
            new_name = name[:4] + '3' + name[5:]  # '6'을 '3'으로 변경하여 ★3 파일명 생성
            # 생성된 ★3 파일명으로 AllCharacterImageManager의 이미지 디렉토리 내에서 경로 객체 생성
            group_jpg_path = self.all_char_manager.images_dir / new_name
            
            if group_jpg_path.exists():  # 해당 ★3 아이콘 파일이 존재하면
                return group_jpg_path  # 경로 반환
        return None  # 조건에 맞지 않거나 파일이 없으면 None 반환

    def _get_cached_image(self, img_path, size=PROCESSING_SIZE):
        """
        지정 경로 이미지 로드, 지정 크기 전처리 후 결과 캐시 저장 또는
        이미 캐시된 경우 캐시에서 반환.
        캐싱 통해 반복적 파일 I/O 및 이미지 처리 오버헤드 감소.
        전처리 과정: 리사이즈, RGB 변환, NumPy 배열 변환, 그레이스케일 변환, ROI 추출.
        :param img_path: 로드할 이미지의 파일 경로 (Path 객체 또는 문자열)
        :param size: 전처리 시 리사이즈할 목표 크기 (기본값: PROCESSING_SIZE)
        :return: {'rgb': PIL RGB 이미지, 'gray': NumPy 그레이스케일 전체 이미지, 'roi': NumPy 그레이스케일 ROI} 딕셔너리.
                 실패 시 None.
        """
        cache_key = f"{img_path}_{size[0]}x{size[1]}"  # 캐시 키 생성 (파일경로 + 크기)
        if cache_key not in self.image_cache:  # 캐시에 해당 키가 없으면 (처음 로드하는 경우)
            try:
                # 이미지 로드, 리사이즈(LANCZOS 고품질 필터), RGB 변환
                img = Image.open(img_path).resize(size, Image.LANCZOS).convert('RGB')
                img_np = np.array(img)  # NumPy 배열로 변환
                img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)  # 그레이스케일로 변환
                # 그레이스케일 이미지에서 ROI_BOUNDS 좌표를 사용하여 관심 영역(ROI) 추출
                # ROI_BOUNDS는 (y_start, y_end, x_start, x_end) 순서
                roi = img_gray[
                    ROI_BOUNDS[0]:ROI_BOUNDS[1],  # Y축 슬라이싱
                    ROI_BOUNDS[2]:ROI_BOUNDS[3]   # X축 슬라이싱
                ]
                # 처리된 이미지들을 딕셔너리 형태로 캐시에 저장
                self.image_cache[cache_key] = {
                    'rgb': img,  # 리사이즈된 RGB PIL 이미지
                    'gray': img_gray,  # 리사이즈된 그레이스케일 NumPy 배열
                    'roi': roi  # ROI 부분의 그레이스케일 NumPy 배열
                }
            except Exception as e: # 이미지 로드 또는 처리 중 예외 발생 시
                self.log_message(f"이미지 캐싱 실패: {img_path} - {str(e)}")
                return None  # 실패 시 None 반환
        return self.image_cache[cache_key]  # 캐시된 이미지 정보 딕셔너리 반환

    def ssim_similarity(self, img1, img2):
        """
        두 NumPy 배열 이미지(img1, img2, 보통 ROI 영역) 간 구조적 유사도(SSIM) 계산.
        (* SSIM 값 -1 ~ 1, 1 가까울수록 유사도 높음.)
        :param img1: 첫 번째 이미지 (NumPy 배열, 그레이스케일)
        :param img2: 두 번째 이미지 (NumPy 배열, 그레이스케일)
        :return: SSIM 점수 (float). 이미지 크기가 다르면 0.0 반환.
        """
        if img1.shape != img2.shape:  # 두 이미지의 형태(크기, 채널 수)가 다르면
            return 0.0  # 비교 불가, 0.0 반환
            
        # skimage.metrics.ssim 함수를 사용하여 SSIM 계산
        return ssim(img1, img2)

    def _find_best_official_match(self, split_img_roi):
        """
        캡처 후 분할 아이콘 ROI(split_img_roi)와 가장 유사한
        로컬 저장 공식 캐릭터 아이콘('AllCharacterImageManager' 관리 JPG 파일) 찾기.
        유사도 비교 병렬 처리.
        :param split_img_roi: 비교 대상 분할 아이콘의 ROI (NumPy 그레이스케일 배열)
        :return: (최고 유사도 점수, 최고점 파일의 Path 객체) 튜플
        """
        best_score = 0  # 최고 점수 초기화
        best_official_file = None  # 최고점 파일 경로 초기화
        
        # CPU 코어 수에 기반한 최대 작업자 수 설정 (병렬 처리용)
        max_workers = MAX_WORKERS # 정의된 상수 사용
        
        # 병렬 비교를 위한 작업 목록 생성
        comparison_tasks = []
        # AllCharacterImageManager의 이미지 디렉토리 내 모든 JPG 파일 순회
        for jpg_file in self.all_char_manager.images_dir.glob("*.jpg"):
            try:
                # 파일명이 'xxxx1x.jpg' 패턴(1성 캐릭터)이면 비교에서 제외 (아이콘 모양이 다를 수 있음)
                if len(jpg_file.name) >= 7 and jpg_file.name[4] == '1':
                    continue
                    
                # 해당 JPG 파일의 캐시된 ROI 가져오기 (없으면 로드 및 전처리)
                cache = self._get_cached_image(jpg_file) # 기본 PROCESSING_SIZE (32x32) 사용
                if cache is None:  # 캐싱 실패 시 건너뛰기
                    continue
                comparison_tasks.append((jpg_file, cache['roi'])) # (파일 경로, ROI) 튜플을 작업 목록에 추가
            except Exception: # 파일 처리 중 예외 발생 시
                continue
        
        # ThreadPoolExecutor를 사용하여 유사도 계산 병렬 처리
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 각 비교 작업을 스레드 풀에 제출. future 객체와 (파일 경로, ROI) 태스크를 매핑.
            future_to_task = {
                executor.submit(self.ssim_similarity, split_img_roi, task[1]): task 
                for task in comparison_tasks
            }
            
            # 완료되는 작업 순서대로 결과 처리
            for future in as_completed(future_to_task):
                task = future_to_task[future] # 완료된 future에 해당하는 태스크 정보
                try:
                    score = future.result() # 작업 결과 (SSIM 점수) 가져오기
                    if score > best_score: # 현재까지의 최고 점수보다 높으면
                        best_score = score
                        best_official_file = task[0] # 최고점 파일 경로 업데이트
                except Exception: # 유사도 계산 중 예외 발생 시 (드묾)
                    continue
        
        return best_score, best_official_file # 최종 최고 점수와 파일 경로 반환

    def _get_group_jpgs(self, best_official_file):
        """
        '_find_best_official_match'에서 찾은 가장 유사한 공식 아이콘(best_official_file)을 기반으로,
        관련된 그룹 아이콘 파일(예: 같은 캐릭터의 다른 별 등급 아이콘)들의 목록 반환.
        주로 ★6 아이콘 매칭 시, 비교 위해 ★3 아이콘 찾거나,
        일반 아이콘 매칭 시 해당 캐릭터 ID 모든 아이콘 가져오는 데 사용.
        :param best_official_file: 가장 유사한 것으로 판단된 공식 아이콘의 Path 객체
        :return: 관련된 그룹 아이콘 파일 Path 객체들의 리스트
        """
        if not best_official_file: # 입력 파일이 없으면 빈 리스트 반환
            return []
            
        # 파일명이 ★6 패턴 ('xxxx6x.jpg')인지 확인
        if re.match(r"^\d{4}6\d\.jpg$", best_official_file.name): # Python re.match는 문자열 시작부터 일치 확인
            # ★6이면, 대응하는 ★3 아이콘 찾기
            group_jpg_path = self.get_3star_jpg(best_official_file)
            return [group_jpg_path] if group_jpg_path else [] # 찾았으면 리스트에 담아 반환, 없으면 빈 리스트
        else: # ★6 패턴이 아니면 (★3 또는 기타)
            char_id = best_official_file.name[:4] # 파일명 앞 4자리 (캐릭터 ID) 추출
            if char_id: # ID가 유효하면
                # 해당 캐릭터 ID로 시작하는 모든 JPG 파일 목록을 glob으로 찾아 리스트로 반환
                group_jpgs = list(self.all_char_manager.images_dir.glob(f"{char_id}*.jpg"))
                return group_jpgs
        return [] # 어느 경우도 아니면 빈 리스트 반환

    def _perform_match_for_single_icon(self, split_img, version_dir):
        """
        단일 분할 이미지에 대해 다단계 아이콘 매칭을 수행하고 관련 정보를 반환하는 공통 함수.
        이 매칭 과정은 다음의 주요 단계 포함:
        1.  분할된 아이콘 ROI vs 로컬에 저장된 공식 인게임 캐릭터 아이콘(JPG) 비교 (1차 식별).
        2.  1차 식별된 아이콘이 ★6일 경우, 웹사이트 검색 정확도 향상을 위해 해당 캐릭터의 ★3 아이콘으로 내부적으로 변환.
        3.  1차 식별된 아이콘(또는 ★6에서 변환된 ★3 아이콘) vs pcrdfans.com 웹사이트의 스프라이트 아이콘(PNG) 비교 (최종 후보 식별).
        결과는 점수 내림차순으로 정렬된 스프라이트 후보 목록을 포함.
        :param split_img: 분석할 분할된 캐릭터 아이콘 PIL.Image 객체
        :param version_dir: pcrdfans 스프라이트 아이콘이 저장된 최신 버전 디렉토리 Path 객체
        :return: 매칭 결과를 담은 딕셔너리:
            {
                "split_img_obj": 원본 분할 PIL.Image 객체,
                "official_match": (1단계 매칭된 인게임 파일 Path, 최고 유사도 점수) 튜플,
                "used_3star_if_6star": 1단계 매칭이 ★6일 경우 변환된 ★3 아이콘 Path 또는 None,
                "all_sprite_candidates": [ (스프라이트 PNG 파일 Path, 점수, 기준 그룹 JPG Path, 스프라이트 메타데이터 dict), ... ] (점수 내림차순 정렬)
            }
        """
        # 1. 분할 이미지 전처리 (ROI 추출)
        split_img_resized = split_img.resize(PROCESSING_SIZE, Image.LANCZOS).convert('RGB')
        split_img_np = np.array(split_img_resized)
        split_img_gray = cv2.cvtColor(split_img_np, cv2.COLOR_RGB2GRAY)
        split_img_roi = split_img_gray[ROI_BOUNDS[0]:ROI_BOUNDS[1], ROI_BOUNDS[2]:ROI_BOUNDS[3]]

        # 2. 1단계 매칭: 인게임 아이콘(AllCharacterImageManager의 JPG)과 비교
        best_official_score, best_official_file = self._find_best_official_match(split_img_roi)

        # 3. 그룹 아이콘 처리 및 ★6 -> ★3 변환 정보
        group_jpgs = self._get_group_jpgs(best_official_file)
        
        used_3star_jpg = None
        if best_official_file and re.match(r"^\d{4}6\d\.jpg$", best_official_file.name):
            used_3star_jpg = self.get_3star_jpg(best_official_file)

        # 4. 2단계 매칭: 스프라이트 아이콘(CharacterImageManager의 PNG)과 비교
        all_sprite_match_candidates = []
        
        comparison_tasks = []
        for group_jpg in group_jpgs:
            group_cache = self._get_cached_image(group_jpg)
            if group_cache is None: 
                continue
            
            for char_file in version_dir.glob("*.png"):
                char_cache = self._get_cached_image(char_file)
                if char_cache is None: 
                    continue
                
                sprite_metadata = self.char_manager.metadata.get(version_dir.name, {}).get(char_file.name)
                if sprite_metadata is None: # 메타데이터가 없는 경우, 이 아이콘은 비교에서 제외
                    self.log_message(f"{get_timestamp()} 경고: {char_file.name}에 대한 메타데이터 없음. 비교 건너뜀.")
                    continue

                comparison_tasks.append(
                    (group_cache['roi'], char_cache['roi'], char_file, group_jpg, sprite_metadata)
                )

        # CPU 코어 수에 기반한 최대 작업자 수 설정 (병렬 처리용)
        max_workers = MAX_WORKERS
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task_info = {
                executor.submit(self.ssim_similarity, task[0], task[1]): (task[2], task[3], task[4])
                for task in comparison_tasks
            }
            for future in as_completed(future_to_task_info):
                char_file, group_jpg, sprite_metadata = future_to_task_info[future]
                try:
                    score = future.result()
                    all_sprite_match_candidates.append((char_file, score, group_jpg, sprite_metadata))
                except Exception as e:
                    self.log_message(f"{get_timestamp()} 스프라이트 유사도 계산 중 오류: {char_file.name} vs {group_jpg.name} - {str(e)}")
                    continue
        
        all_sprite_match_candidates.sort(key=lambda x: x[1], reverse=True)

        return {
            "split_img_obj": split_img,
            "official_match": (best_official_file, best_official_score),
            "used_3star_if_6star": used_3star_jpg,
            "all_sprite_candidates": all_sprite_match_candidates
        }

    def _process_single_image(self, split_img, version_dir):
        """
        단일 분할 이미지(split_img) 대한 상세 유사도 비교 정보(딕셔너리) 생성.
        주로 "유사도 비교 테스트" 창 표시 데이터 준비 시 사용.
        내부적으로 `_perform_match_for_single_icon` 공통 함수를 호출하여 매칭 수행.
        :param split_img: 분석할 분할된 캐릭터 아이콘 PIL.Image 객체
        :param version_dir: pcrdfans 스프라이트 아이콘이 저장된 최신 버전 디렉토리 Path 객체
        :return: 상세 비교 결과 딕셔너리. 실패 시 None.
                 딕셔너리 구조: {"split_img": 원본 분할 이미지,
                               "official": (최고점 인게임 파일 Path, 점수),
                               "sprites": [(스프라이트 파일 Path, 점수, 기준 그룹 JPG Path), ...],
                               "used_3star_jpg": 사용된 ★3 파일 Path 또는 None}
        """
        try:
            # 공통 매칭 함수 호출
            match_results = self._perform_match_for_single_icon(split_img, version_dir)
            
            official_file, official_score = match_results["official_match"]
            used_3star_jpg = match_results["used_3star_if_6star"]
            all_sprite_candidates = match_results["all_sprite_candidates"] # (sprite_file, score, base_group_jpg, sprite_metadata)

            # _process_single_image는 상위 3개의 (스프라이트 파일 Path, 점수, 기준 그룹 JPG Path)를 반환해야 함
            top_3_sprites_for_test = []
            for candidate in all_sprite_candidates[:3]: # 상위 3개
                sprite_file, score, base_group_jpg, _ = candidate
                top_3_sprites_for_test.append((sprite_file, score, base_group_jpg))
            
            return {
                "split_img": match_results["split_img_obj"], # 원본 분할 이미지
                "official": (official_file, official_score), # (1단계 매칭 파일, 점수)
                "sprites": top_3_sprites_for_test, # 3단계 매칭 결과 상위 3개 리스트
                "used_3star_jpg": used_3star_jpg # ★6 -> ★3 변환 시 사용된 ★3 파일 경로
            }
        except Exception as e: # 전체 _process_single_image 과정 중 예외 발생 시
            self.log_message(f"분할 이미지 처리 중 오류 발생 (_process_single_image): {str(e)}")
            return None # 실패 시 None 반환

    def _collect_similarity_results(self):
        """
        현재 self.split_imgs 모든 분할 이미지 대해
        '_process_single_image' 호출, 유사도 비교 결과 수집.
        주로 "유사도 비교 테스트" 창 표시 데이터 일괄 준비 시 사용.
        결과 수집 병렬 처리.
        :return: 각 분할 이미지에 대한 _process_single_image 결과 딕셔너리들의 리스트.
                 결과가 없는 항목은 None으로 채워질 수 있음.
        """
        # pcrdfans 스프라이트 아이콘이 저장된 최신 버전 디렉토리 가져오기
        version_dir = self.char_manager.get_latest_version_dir()
        if not version_dir: # 버전 디렉토리 없으면 빈 리스트 반환
            return []

        self.image_cache.clear() # 새 비교 시작 전 이미지 캐시 초기화
        results = [None] * len(self.split_imgs) # 결과 저장용 리스트 (분할 이미지 수만큼 None으로 초기화)
        
        max_workers = MAX_WORKERS # 병렬 작업자 수
        
        # ThreadPoolExecutor를 사용하여 모든 분할 이미지에 대해 _process_single_image 병렬 실행
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 각 작업을 스레드 풀에 제출. future 객체와 해당 분할 이미지의 인덱스 매핑.
            future_to_idx = {
                executor.submit(self._process_single_image, split_img, version_dir): idx
                for idx, split_img in enumerate(self.split_imgs)
            }
            # 완료되는 작업 순서대로 결과 처리
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future] # 완료된 future에 해당하는 원본 인덱스
                try: # future.result()에서 예외가 발생할 수 있으므로 try-except 추가
                    result = future.result() # 작업 결과 (딕셔너리 또는 None) 가져오기
                    if result: # 유효한 결과가 있으면
                        results[idx] = result # 해당 인덱스 위치에 결과 저장
                except Exception as e:
                    self.log_message(f"분할 이미지 {idx} 처리 중 병렬 작업 오류: {str(e)}")
                    # results[idx]는 None으로 유지됨
        return results # 모든 분할 이미지에 대한 결과 리스트 반환

    def run_automation(self, split_imgs):
        """
        "아레나 조합 검색" 핵심 자동화 로직 수행.
        캡처 분할 이미지들(split_imgs)을 분석하여 가장 유사한 캐릭터 아이콘을 식별하고,
        pcrdfans.com 웹사이트에서 해당 아이콘들을 자동으로 클릭한 후 최종 검색 실행.

        :param split_imgs: 캡처 후 분할된 캐릭터 아이콘 PIL.Image 객체들의 리스트.
        """
        # Selenium WebDriver가 유효한지 먼저 확인.
        if not self._check_driver_status(): # Selenium 드라이버 상태 확인
            self.log_message(f"{get_timestamp()} 사이트 연결이 끊어져 있습니다. [사이트 연결] 버튼을 클릭해 주세요.\n")
            messagebox.showerror("오류", "사이트 연결이 끊어져 있습니다.\n\n[사이트 연결] 버튼을 클릭해 주세요.")
            return

        try:
            # GUI에서 설정된 현재 유사도 임계값 가져옴.
            MATCH_THRESHOLD = self.match_threshold.get()
            self.log_message(f"{get_timestamp()} 이미지 비교 중... (임계값: {MATCH_THRESHOLD}) 잠시만 기다려주세요.")
            
            # 웹페이지를 최상단으로 스크롤하여 이후 요소 조작의 기준점을 맞춥니다.
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.1) # 스크롤 동작을 위한 약간의 대기

            # pcrdfans.com에서 이전에 선택된 캐릭터가 있다면 "선택 초기화" 버튼을 클릭하여 모두 해제.
            self.log_message(f"{get_timestamp()} 선택된 아이콘 초기화 중...")
            reset_button = self.driver.find_element(By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-btn-sm')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", reset_button) # 초기화 버튼이 보이도록 스크롤
            time.sleep(0.1)
            self.driver.execute_script("arguments[0].click();", reset_button) # JavaScript로 클릭 실행
            time.sleep(0.5) # 초기화가 적용될 시간 충분히 대기.
            
            # 로컬에 저장된 pcrdfans.com 스프라이트 아이콘의 최신 버전 디렉토리 가져옴.
            version_dir = self.char_manager.get_latest_version_dir()
            if not version_dir: # 스프라이트 아이콘이 없으면 진행 불가
                self.log_message(f"{get_timestamp()} 저장된 이미지가 없습니다. [사이트 연결] 버튼을 클릭해 해주세요.\n")
                messagebox.showerror("오류", "저장된 이미지가 없습니다.\n\n[사이트 연결] 버튼을 클릭해 주세요.")
                return

            # 새로운 이미지 비교를 시작하기 전에 이전 이미지 캐시 비움.
            self.image_cache.clear()
            
            # pcrdfans.com 웹페이지의 모든 캐릭터 선택 패널(아코디언) 확장.
            # 모든 캐릭터 아이콘 div 요소가 DOM에 로드되어 Selenium으로 찾을 수 있게 하기 위함.
            self.log_message(f"{get_timestamp()} 모든 패널 확장 중...")
            collapse_root = self.driver.find_element(By.CLASS_NAME, "ant-collapse-icon-position-left") # 패널들의 루트 요소
            items = collapse_root.find_elements(By.CLASS_NAME, "ant-collapse-item") # 각 패널 아이템
            
            for item in items: # 각 패널에 대해
                header = item.find_element(By.CLASS_NAME, "ant-collapse-header") # 패널 헤더
                if header.get_attribute("aria-expanded") == "false": # 패널이 닫혀있으면
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", header) # 헤더가 보이도록 스크롤
                        time.sleep(0.1)
                        self.driver.execute_script("arguments[0].click();", header) # JS로 클릭하여 확장
                        time.sleep(0.2) # 패널이 완전히 확장될 때까지 대기
                    except Exception: # 클릭 중 오류 발생 시 (예: 다른 요소에 가려짐) 다음 패널로 진행
                        continue
            
            # 모든 패널 확장 후, 다시 페이지 최상단으로 스크롤.
            self.driver.execute_script("window.scrollTo(0, 0);")
            
            # 최종적으로 웹사이트에서 클릭할 스프라이트 아이콘의 메타데이터를 저장할 리스트.
            # (메타데이터 dict, 기준 인게임 JPG 파일명, 대상 스프라이트 PNG 파일명) 튜플 형태.
            all_sprite_metadata_to_click = []
            
            # 사용자가 캡처한 각 분할 이미지에 대해 유사도 비교 수행.
            for idx, split_img in enumerate(split_imgs):
                self.log_message(f"{get_timestamp()} 분할 이미지 {idx + 1} 처리 중...")
                # 다단계 아이콘 매칭 함수를 호출하여 최적의 인게임 아이콘 및 스프라이트 아이콘 후보를 찾음.
                match_results = self._perform_match_for_single_icon(split_img, version_dir)
                official_file, official_score = match_results["official_match"] # 1단계: 인게임 아이콘 매칭 결과
                
                # 1단계 매칭 결과가 없거나 점수가 임계값 미만이면 다음 분할 이미지로 넘어감.
                if not official_file or official_score < MATCH_THRESHOLD:
                    self.log_message(f"{get_timestamp()} 유사한 인게임 아이콘을 찾지 못했습니다. (점수: {official_score:.4f})")
                    continue
                
                sprite_candidates = match_results["all_sprite_candidates"] # 3단계: 스프라이트 아이콘 매칭 후보 리스트
                
                if sprite_candidates: # 스프라이트 아이콘 후보가 있다면
                    # 가장 점수가 높은 후보 선택.
                    best_sprite_file, best_sprite_score, best_group_jpg, best_sprite_metadata = sprite_candidates[0]
                    
                    # 최고점 스프라이트 아이콘의 점수가 임계값 이상이고 메타데이터가 유효하면 클릭 대상에 추가.
                    if best_sprite_score >= MATCH_THRESHOLD and best_sprite_metadata:
                        self.log_message(f"{get_timestamp()} 유사한 스프라이트 아이콘을 찾았습니다: {best_sprite_file.name} (점수: {best_sprite_score:.4f}, 기준: {best_group_jpg.name})")
                        all_sprite_metadata_to_click.append((best_sprite_metadata, best_group_jpg.name, best_sprite_file.name))
                    else:
                        self.log_message(f"{get_timestamp()} 유사한 스프라이트 아이콘을 찾지 못했습니다. (최고 점수: {best_sprite_score:.4f})")
                else:
                    self.log_message(f"{get_timestamp()} 유사한 스프라이트 아이콘 후보가 없습니다.")

            # 웹사이트에서 이미 클릭한 아이콘의 div_style을 추적하여 중복 클릭 방지.
            found_divs = set()
            # 클릭해야 할 아이콘 메타데이터 목록의 복사본을 만들어 순회 중 제거가 가능하도록 함.
            remaining_metadata_tuples = all_sprite_metadata_to_click.copy()
            
            # pcrdfans.com의 각 캐릭터 패널을 다시 순회하며, 위에서 식별된 아이콘들 클릭.
            for item in items: # 각 패널 아이템
                if not remaining_metadata_tuples: # 더 이상 클릭할 아이콘이 없으면 루프 종료
                    break
                    
                content_box = item.find_element(By.CLASS_NAME, "ant-collapse-content-box") # 패널 내용 영역
                # 현재 패널 내의 모든 아이콘 div 요소들을 가져옴.
                panel_divs = content_box.find_elements(By.XPATH, ".//div[contains(@style, 'background-image')]")
                
                # 현재 패널에서 찾아야 할 아이콘들만 필터링 (이미 찾은 아이콘 제외).
                current_panel_targets = []
                for metadata_tuple in remaining_metadata_tuples: 
                    metadata_dict = metadata_tuple[0]
                    div_style = metadata_dict['div_style'] # 클릭 대상 아이콘의 div 스타일
                    if div_style not in found_divs: # 아직 클릭되지 않은 아이콘이면
                        current_panel_targets.append(metadata_tuple)
                
                if current_panel_targets: # 현재 패널에서 찾아야 할 아이콘이 있다면
                    for div_element in panel_divs: # 패널 내 모든 div 요소에 대해
                        if not current_panel_targets: # 현재 패널에서 찾을 아이콘이 더 없으면 내부 루프 종료
                            break
                        current_div_style = div_element.get_attribute("style") # 현재 div의 스타일
                        
                        # 찾아야 할 아이콘 목록(복사본) 순회.
                        for target_tuple in list(current_panel_targets):
                            target_metadata_dict = target_tuple[0]
                            target_div_style = target_metadata_dict['div_style'] # 목표 아이콘의 div 스타일
                            
                            # 현재 div의 스타일과 목표 아이콘의 스타일이 일치하고, 아직 클릭되지 않았다면
                            if target_div_style == current_div_style and target_div_style not in found_divs:
                                try:
                                    # 해당 div를 화면 중앙으로 스크롤하고 JavaScript로 클릭.
                                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", div_element) 
                                    time.sleep(0.1) 
                                    self.driver.execute_script("arguments[0].click();", div_element) 
                                    time.sleep(0.2) # 클릭 반영 대기
                                    found_divs.add(target_div_style) # 클릭된 div 스타일을 기록
                                    # 전체 남은 목록과 현재 패널 목표 목록에서 해당 아이콘 제거
                                    if target_tuple in remaining_metadata_tuples:
                                        remaining_metadata_tuples.remove(target_tuple)
                                    if target_tuple in current_panel_targets:
                                        current_panel_targets.remove(target_tuple)

                                    self.log_message(f"{get_timestamp()} {target_tuple[1]}와 유사한 {target_tuple[2]} 스프라이트 아이콘 클릭 완료")
                                    break # 현재 div에 대한 목표 아이콘 찾았으므로 다음 div로
                                except Exception as e:
                                    self.log_message(f"{get_timestamp()} div 클릭 실패: {str(e)}")
                
                # 현재 패널 처리가 끝나면, 다시 패널을 닫아 화면 정리.
                header = item.find_element(By.CLASS_NAME, "ant-collapse-header")
                if header.get_attribute("aria-expanded") == "true": # 패널이 열려있다면
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", header) 
                        time.sleep(0.1)
                        self.driver.execute_script("arguments[0].click();", header) # 클릭하여 닫기
                        time.sleep(0.2) 
                    except Exception: 
                        continue # 패널 닫기 실패 시 무시하고 계속
            
            # 모든 패널 순회 후에도 클릭하지 못한 아이콘이 있다면 로그 남김.
            if remaining_metadata_tuples: 
                self.log_message(f"{get_timestamp()} {len(remaining_metadata_tuples)}개의 div를 찾지 못했습니다.")
                for meta_tuple in remaining_metadata_tuples:
                    self.log_message(f"  - 찾지 못한 아이콘 기준 JPG: {meta_tuple[1]}, 대상 스프라이트: {meta_tuple[2]}")

            self.log_message(f"{get_timestamp()} 모든 아이콘을 클릭했습니다! (임계값: {MATCH_THRESHOLD})\n")
            
            # 모든 아이콘 선택 완료 후, 웹사이트의 "검색" 버튼 클릭.
            try:
                self.log_message(f"{get_timestamp()} 검색 버튼 클릭 중...")
                search_button_element = self.driver.find_element(By.CSS_SELECTOR, 'button.ant-btn.battle_search_button.ant-btn-primary')
                self.driver.execute_script("arguments[0].scrollIntoView(true);", search_button_element) # 검색 버튼 보이도록 스크롤
                time.sleep(0.2)
                self.driver.execute_script("arguments[0].click();", search_button_element) # JS로 클릭
                self.log_message(f"{get_timestamp()} 검색이 성공적으로 완료되었습니다!\n")
            except Exception as e:
                self.log_message(f"{get_timestamp()} 검색 버튼 클릭 중 오류 발생: {str(e)}\n")
                messagebox.showerror("오류", f"검색 버튼 클릭 중 오류가 발생했습니다: {str(e)}")
            
            # 최종적으로 화면을 다시 최상단으로 스크롤.
            self.driver.execute_script("window.scrollTo(0, 0);")
            
        except Exception as e: # 자동화 전체 과정에서 예외 발생 시
            if self.driver: # 드라이버가 아직 유효하다면 화면 스크롤 시도
                 self.driver.execute_script("window.scrollTo(0, 0);")
            
            self.log_message(f"{get_timestamp()} 오류 발생: {str(e)}\n")
            import traceback # 상세한 오류 추적을 위해 traceback 모듈 임포트
            self.log_message(traceback.format_exc()) # 발생한 예외의 전체 스택 트레이스를 로그에 기록
            messagebox.showerror("오류", f"자동화 중 오류가 발생했습니다: {str(e)}")

    def test_similarity(self):
        """
        "유사도 비교 테스트" 버튼 클릭 시 호출.
        캡처 분할 이미지 여부, 아이콘 버전 디렉토리 여부 확인 후,
        '_run_similarity_test' 메서드 별도 스레드 실행.
        """
        if not self.split_imgs: # 분할된 이미지가 없으면
            self.log_message(f"{get_timestamp()} 아레나 조합이 캡쳐되지 않았습니다..\n")
            messagebox.showwarning("경고", "아레나 조합이 캡쳐되지 않았습니다.")
            return
            
        version_dir = self.char_manager.get_latest_version_dir() # pcrdfans 아이콘 버전 디렉토리
        if not version_dir: # 없으면 (사이트 연결 및 아이콘 처리 안된 상태)
            self.log_message(f"{get_timestamp()} character_images 폴더가 없습니다. 사이트 연결을 먼저 실행해주세요.\n")
            messagebox.showwarning("경고", "character_images 폴더가 없습니다.\n\n사이트 연결을 먼저 실행해주세요.")
            return

        self.test_btn.config(state=tk.DISABLED) # 테스트 중 버튼 비활성화
        self.log_message(f"{get_timestamp()} 유사도 비교 테스트 시작...")
        # _run_similarity_test를 별도 스레드에서 실행 (GUI 프리징 방지)
        threading.Thread(target=self._run_similarity_test).start()

    def _run_similarity_test(self):
        """
        별도의 스레드에서 유사도 비교 테스트 실제로 수행.
        각 분할 이미지에 대해 상세한 유사도 분석(1단계, 2단계, 3단계)을 수행하고,
        그 과정을 메인 창의 로그 텍스트 박스에 실시간으로 출력.
        모든 분석이 끝나면 '_create_test_window'를 호출하여 결과를 별도 창에 시각화.
        '_collect_similarity_results'를 호출하여 데이터를 미리 수집하고,
        이 데이터를 로그 출력과 결과 창 생성에 모두 사용.
        """
        try:
            self.log_message(f"{get_timestamp()} 이미지 캐시 초기화 중...")
            self.image_cache.clear() # 새 테스트 시작 전 이미지 캐시 비우기
            
            self.log_message(f"{get_timestamp()} 분할 이미지 처리 및 상세 분석 시작...\n")
            
            # 유사도 결과 데이터 한번만 수집
            all_similarity_results_data = self._collect_similarity_results()
            
            # 수집된 데이터를 기반으로 로그 텍스트 생성 및 출력
            log_output_text = self._format_similarity_test_results(all_similarity_results_data)
            self.root.after(0, lambda: self.log_message(log_output_text)) # 메인 스레드에서 로그 업데이트

            self.log_message(f"{get_timestamp()} 모든 분할 이미지 상세 분석 완료!")
            self.log_message(f"{get_timestamp()} 유사도 비교 테스트 결과 창 생성...\n")
            
            # 모든 분석 완료 후, 메인 스레드에서 _create_test_window 호출하여 결과 창 띄우기
            # 수집된 데이터를 _create_test_window에 전달
            self.root.after(0, lambda: self._create_test_window(all_similarity_results_data))
            
        except Exception as e: # _run_similarity_test 전체 과정 중 예외 발생 시
            self.log_message(f"{get_timestamp()} 유사도 테스트 중 오류 발생: {str(e)}")
            # 예외 발생 시에도 test_btn은 finally에서 활성화되도록 함
        finally: # 성공/실패 여부와 관계없이
            # 메인 스레드에서 테스트 버튼 다시 활성화
            self.root.after(0, lambda: self.test_btn.config(state=tk.NORMAL))

    def _format_similarity_test_results(self, all_similarity_results):
        """
        '_collect_similarity_results'에서 수집된 유사도 비교 결과 데이터(리스트)를
        가독성 있는 문자열로 포맷팅.
        :param all_similarity_results: _collect_similarity_results의 반환값
        :return: 포맷팅된 결과 문자열
        """
        version_dir = self.char_manager.get_latest_version_dir() # pcrdfans 아이콘 버전
        version = version_dir.name if version_dir else "unknown" # 버전명 또는 "unknown"
        threshold = self.match_threshold.get() # 현재 임계값
        
        result_lines = [ # 결과 문자열 라인들을 담을 리스트
            f"{get_timestamp()} 유사도 비교 테스트 결과 (임계값: {threshold:.2f}, 버전: {version})",
            "=" * 60, # 구분선
            "" # 빈 줄
        ]
        
        # 각 분할 이미지의 결과(result 딕셔너리)에 대해
        for idx, result in enumerate(all_similarity_results, 1): # 인덱스 1부터 시작
            if result is None: # _collect_similarity_results에서 None으로 채워진 경우
                result_lines.append(f"[분할 이미지 {idx}] - 결과 없음")
                result_lines.extend(["=" * 60, ""])
                continue

            official_file, official_score = result["official"] # 1단계 매칭 결과
            used_3star_jpg = result["used_3star_jpg"] # ★6 -> ★3 변환 결과
            sprites = result["sprites"] # 3단계 매칭 결과 (상위 3개 리스트)
            
            # 캐릭터 ID 및 해당 ID의 모든 로컬 JPG 파일 정보 수집
            char_id = ""
            found_files_for_format = [] # 이름 충돌 피하기 위해 _for_format 접미사
            if official_file:
                char_id = official_file.name[:4]
                found_files_for_format = [f.name for f in self.all_char_manager.images_dir.glob(f"{char_id}*.jpg")]
            
            # 분할 이미지 헤더
            result_lines.extend([
                f"[분할 이미지 {idx}]",
                "-" * 50, # 구분선
                "1단계 (인게임 아이콘):",
                f" • 최고 유사도: {official_score:.4f}",
                f" • 매칭 파일: {official_file.name if official_file else 'None'}",
                f" • 캐릭터 ID: {char_id if char_id else 'N/A'}",
                " • 발견된 파일들:"
            ])
            
            # 발견된 로컬 JPG 파일 목록 추가
            if found_files_for_format:
                for file_name in sorted(found_files_for_format):
                    result_lines.append(f"  - {file_name}")
            else:
                result_lines.append("  (발견된 파일 없음)")
            
            # 매칭된 인게임 아이콘이 ★6인지 여부
            if official_file and re.match(r"^\d{4}6\d\.jpg$", official_file.name):
                result_lines.append(" • ★6 아이콘 감지됨")
            
            # 2단계: ★6 -> ★3 전환 결과
            result_lines.extend(["", "2단계 (★6 → ★3 전환):"])
            if official_file and re.match(r"^\d{4}6\d\.jpg$", official_file.name): # ★6이면
                result_lines.append(f" • 전환 {'성공' if used_3star_jpg else '실패'}: {used_3star_jpg.name if used_3star_jpg else 'None'}")
            elif official_file and re.match(r"^\d{4}3\d\.jpg$", official_file.name): # ★3이면
                result_lines.append(" • ★3 아이콘입니다 (전환 불필요).")
            elif official_file: # ★6도 ★3도 아니면
                result_lines.append(" • ★3 또는 ★6 아이콘이 아닙니다.")
            else: # 1단계 매칭 파일 없으면
                result_lines.append(" • 1단계 매칭된 인게임 아이콘 없음 (전환 불가).")
            
            # 3단계: 스프라이트 아이콘 매칭 결과 (상위 1개만 간단히 표시)
            result_lines.extend(["", "3단계 (스프라이트 아이콘):"])
            if sprites: # 매칭 결과 있으면
                best_sprite_tuple = sprites[0] # (스프라이트 파일 Path, 점수, 기준 그룹 JPG Path)
                result_lines.extend([
                    f" • 최고 유사도: {best_sprite_tuple[1]:.4f}",
                    f" • 매칭 파일: {best_sprite_tuple[0].name}",
                    f" • 기준 파일: {best_sprite_tuple[2].name}\n" # 기준 그룹 JPG도 표시
                ])
            else: # 매칭 결과 없음
                result_lines.append(" • 유사한 스프라이트 아이콘을 찾지 못함.\n")

            result_lines.extend(["=" * 60, ""]) # 각 분할 이미지 결과 후 구분선
        
        return "\n".join(result_lines) # 모든 라인을 합쳐 하나의 문자열로 반환

    def _create_test_window(self, all_similarity_results_data):
        """
        유사도 비교 테스트 결과를 시각적으로 보여주는 별도의 Toplevel 창을 생성하고 설정.
        이 창에는 원본 캡처 이미지 미리보기와 함께, 각 분할 이미지별 상세 비교 결과를
        표(테이블) 형태로 표시 (분할 이미지, 1단계 매칭, ★6 -> ★3 변환, 3단계 매칭 상위 3개).
        """
        # 1. 원본 캡처 이미지 리사이즈 (창 크기에 맞게)
        if not self.captured_img: # 혹시 캡처 이미지가 없다면 (이론상 여기까지 오면 있어야 함)
            messagebox.showerror("오류", "원본 캡처 이미지가 없습니다.")
            return

        original_width, original_height = self.captured_img.size
        aspect_ratio = original_width / original_height if original_height > 0 else 1 # 0으로 나누기 방지
        new_width = min(MAX_PREVIEW_WIDTH, original_width) # 최대 너비 제한
        new_height = int(new_width / aspect_ratio) if aspect_ratio > 0 else int(new_width) # 0으로 나누기 방지
        # 리사이즈된 원본 캡처 이미지 (LANCZOS 고품질 필터)
        self.capture_preview = self.captured_img.resize(
            (new_width, new_height),
            Image.LANCZOS
        )
        
        # 2. 테스트 창에 표시할 이미지들 미리 로드 및 캐싱 (PhotoImage 객체 생성 오버헤드 줄이기 위함)
        self.preview_cache = {} # 테스트 창 전용 미리보기 이미지 캐시 (PhotoImage 아님, PIL Image)
        
        for idx, result in enumerate(all_similarity_results_data): # 각 분할 이미지 결과에 대해
            if result is None: continue # 결과 없으면 건너뛰기

            # 분할 이미지 자체를 PREVIEW_SIZE로 리사이즈하여 캐시
            split_img = result["split_img"]
            self.preview_cache[f"split_{idx}"] = split_img.resize(
                PREVIEW_SIZE, # (50,50)
                Image.LANCZOS
            )
            
            # 1단계 매칭된 인게임 아이콘(official_file) 리사이즈하여 캐시
            official_file, _ = result["official"]
            if official_file:
                try:
                    self.preview_cache[f"official_{idx}"] = Image.open(
                        official_file
                    ).resize(PREVIEW_SIZE, Image.LANCZOS)
                except FileNotFoundError: # 파일 못찾으면 캐시에 안넣음
                    pass 
            
            # 3단계 매칭된 스프라이트 아이콘들(상위 3개) 리사이즈하여 캐시
            for i, (sprite_file, _, _) in enumerate(result["sprites"]):
                if sprite_file: # sprite_file이 None이 아닐 때만 처리
                    try:
                        self.preview_cache[f"sprite_{idx}_{i}"] = Image.open(
                            sprite_file
                        ).resize(PREVIEW_SIZE, Image.LANCZOS)
                    except FileNotFoundError:
                        pass
        
        # 3. Toplevel 창 생성 및 설정
        test_window = tk.Toplevel(self.root) # 메인 윈도우의 자식 창으로 생성
        test_window.title("유사도 비교 테스트 결과")
        
        # 창을 화면 중앙에 위치시키기
        screen_width = test_window.winfo_screenwidth()
        screen_height = test_window.winfo_screenheight()
        x = (screen_width // 2) - (TEST_WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (TEST_WINDOW_HEIGHT // 2)
        test_window.geometry(f"{TEST_WINDOW_WIDTH}x{TEST_WINDOW_HEIGHT}+{x}+{y}") # 창 크기 및 위치

        # 4. 창 내부 UI 구성
        main_frame = tk.Frame(test_window) # 모든 내용을 담을 메인 프레임
        main_frame.pack(expand=True, fill='both', padx=10, pady=10) # 창에 꽉 채움 (여백 포함)

        # 원본 캡처 이미지 미리보기 표시
        self._show_original_image(main_frame)
        
        # 유사도 비교 결과 테이블 표시
        self._show_result_table(main_frame, all_similarity_results_data)

    def _show_original_image(self, main_frame):
        """
        테스트 결과 창의 상단에 원본 캡처 이미지 미리보기 표시.
        :param main_frame: 이미지를 표시할 부모 프레임
        """
        capture_frame = tk.Frame(main_frame) # 원본 이미지용 프레임
        capture_frame.pack(fill='x', pady=(0, 20)) # 가로로 채우고 아래쪽 여백
        tk.Label(capture_frame, text="사용자 지정 아레나 조합 캡쳐 (원본)").pack() # 제목 레이블
        
        # 리사이즈된 원본 캡처 이미지를 Tkinter용 PhotoImage로 변환
        capture_tk = ImageTk.PhotoImage(self.capture_preview)
        capture_label = tk.Label(capture_frame, image=capture_tk) # 이미지 레이블
        capture_label.image = capture_tk  # 가비지 컬렉션 방지용 참조 유지
        capture_label.pack() # 배치

    def _show_result_table(self, main_frame, all_similarity_results):
        """
        테스트 결과 창에 유사도 비교 결과를 테이블(표) 형태로 표시.
        Tkinter의 grid 레이아웃 매니저를 사용하여 표를 구성.
        :param main_frame: 테이블을 표시할 부모 프레임
        :param all_similarity_results: _collect_similarity_results의 반환값
        """
        result_frame = tk.Frame(main_frame) # 결과 테이블용 프레임
        result_frame.pack(fill='both', expand=True) # 부모 프레임에 꽉 채움
        tk.Label(result_frame, text="유사 이미지 감지 결과 (상위 3개)").pack(pady=(0, 10)) # 테이블 제목

        # 실제 테이블(표)을 담을 프레임
        table_frame = tk.Frame(result_frame)
        table_frame.pack(fill='both', expand=True)
        
        # 테이블 헤더(행 제목) 설정
        self._setup_table_headers(table_frame, all_similarity_results)
        
        # 테이블 내용(각 셀) 채우기
        self._show_table_content(table_frame, all_similarity_results)
        
        # 테이블의 grid 레이아웃 행/열 크기 조절 설정
        self._configure_table_grid(table_frame, all_similarity_results)

    def _setup_table_headers(self, table_frame, all_similarity_results):
        """
        테스트 결과 테이블의 행 제목(첫 번째 열) 설정.
        :param table_frame: 테이블을 담고 있는 프레임
        :param all_similarity_results: (사용 안됨 - 열 개수 결정에 필요할 수 있으나 현재는 고정 헤더)
        """
        row_labels = [ # 행 제목 문자열 리스트
            "분할 이미지",    # 0행
            "인게임 아이콘",  # 1행 (1단계 매칭)
            "★6 → ★3 전환", # 2행
            "유사도 1위",     # 3행 (3단계 매칭 1위)
            "유사도 2위",     # 4행 (3단계 매칭 2위)
            "유사도 3위"      # 5행 (3단계 매칭 3위)
        ]
        
        # 각 행 제목에 대해
        for row_idx, label_text in enumerate(row_labels):
            # 각 제목을 담을 프레임 생성 (셀 역할, 가운데 정렬을 위함)
            label_frame = tk.Frame(table_frame)
            # grid로 배치: row_idx 행, 0번 열. padx/pady는 여백. sticky='nsew'는 셀 내용이 셀 크기에 맞춰 확장되도록.
            label_frame.grid(row=row_idx, column=0, padx=5, pady=2, sticky='nsew')
            label_widget = tk.Label(label_frame, text=label_text, anchor="center", justify="center") # 레이블 생성 (가운데 정렬)
            label_widget.pack(expand=True, fill="both") # 레이블을 프레임(셀)에 꽉 채움

    def _show_table_content(self, table_frame, all_similarity_results):
        """
        테스트 결과 테이블의 내용(각 셀 데이터) 채움.
        각 행(분할 이미지, 인게임 아이콘 등)별로 별도 메서드를 호출하여 처리.
        :param table_frame: 테이블을 담고 있는 프레임
        :param all_similarity_results: _collect_similarity_results의 반환값
        """
        # 0행: 분할 이미지 미리보기 표시
        self._show_split_images_row(table_frame, all_similarity_results)
        
        # 1행: 1단계 매칭된 인게임 아이콘 및 점수 표시
        self._show_official_icons_row(table_frame, all_similarity_results)
        
        # 2행: ★6 -> ★3 변환 결과 아이콘 표시
        self._show_star_conversion_row(table_frame, all_similarity_results)
        
        # 3행, 4행, 5행: 3단계 매칭된 스프라이트 아이콘 상위 3개 및 점수 표시
        self._show_similarity_result_rows(table_frame, all_similarity_results)

    def _show_split_images_row(self, table_frame, all_similarity_results):
        """
        테이블의 0행 (분할 이미지 행) 채움.
        각 열에는 해당 분할 이미지의 미리보기와 "아이콘 X" 텍스트 표시.
        :param table_frame: 테이블 프레임
        :param all_similarity_results: 결과 데이터
        """
        # 각 분할 이미지 결과(result)에 대해 (col은 0부터 시작)
        for col_idx, result in enumerate(all_similarity_results):
            if result is None: continue # 결과 없으면 건너뛰기

            # 현재 셀을 위한 프레임 생성 및 grid 배치 (0행, col_idx+1 열 - 0열은 행 제목용)
            cell_frame = tk.Frame(table_frame)
            cell_frame.grid(row=0, column=col_idx + 1, padx=10, pady=2, sticky='nsew')
            
            # 캐시에서 해당 분할 이미지(리사이즈된 PIL Image) 가져오기
            split_preview_img = self.preview_cache.get(f"split_{col_idx}")
            if split_preview_img: # 캐시에 있으면
                split_tk = ImageTk.PhotoImage(split_preview_img) # Tkinter용 PhotoImage로 변환
                split_label = tk.Label(cell_frame, image=split_tk)
                split_label.image = split_tk # 참조 유지
                split_label.pack() # 셀 프레임에 이미지 배치
            
            # 아이콘 번호 텍스트 레이블 (예: "아이콘 1")
            icon_name_label = tk.Label(cell_frame, text=f"아이콘 {col_idx + 1}", 
                                     anchor='center', justify='center') # 가운데 정렬
            icon_name_label.pack() # 이미지 아래에 배치

    def _show_official_icons_row(self, table_frame, all_similarity_results):
        """
        테이블의 1행 (인게임 아이콘 행 - 1단계 매칭 결과) 채움.
        각 열에는 매칭된 인게임 아이콘 미리보기, 파일명, 유사도 점수 표시.
        :param table_frame: 테이블 프레임
        :param all_similarity_results: 결과 데이터
        """
        for col_idx, result in enumerate(all_similarity_results):
            if result is None: continue

            official_file, official_score = result["official"] # 1단계 매칭 파일과 점수
            # 현재 셀용 프레임 생성 및 배치 (1행, col_idx+1 열)
            cell_frame = tk.Frame(table_frame)
            cell_frame.grid(row=1, column=col_idx + 1, padx=10, pady=2, sticky='nsew')
            
            if official_file: # 매칭된 파일이 있으면
                # 캐시에서 해당 인게임 아이콘 이미지 가져오기
                official_img = self.preview_cache.get(f"official_{col_idx}")
                if official_img:
                    official_tk = ImageTk.PhotoImage(official_img)
                    label_img = tk.Label(cell_frame, image=official_tk)
                    label_img.image = official_tk
                    label_img.pack() # 이미지 배치
                
                # 파일명과 유사도 점수 텍스트 레이블
                name_label = tk.Label(cell_frame, 
                    text=f"{official_file.name}\n유사도: {official_score:.4f}")
                name_label.pack() # 이미지 아래에 배치
            else: # 매칭된 파일 없으면
                name_label = tk.Label(cell_frame, text="(유사한 인게임 아이콘 없음)")
                name_label.pack(expand=True) # expand=True 추가하여 텍스트가 셀 중앙에 오도록 유도

    def _show_star_conversion_row(self, table_frame, all_similarity_results):
        """
        테이블의 2행 (★6 -> ★3 변환 결과 행) 채움.
        1단계에서 매칭된 아이콘이 ★6이면, 변환된 ★3 아이콘 미리보기와 정보 표시.
        :param table_frame: 테이블 프레임
        :param all_similarity_results: 결과 데이터
        """
        for col_idx, result in enumerate(all_similarity_results):
            if result is None: continue

            official_file, _ = result["official"] # 1단계 매칭 파일
            # 현재 셀용 프레임 생성 및 배치 (2행, col_idx+1 열)
            cell_frame = tk.Frame(table_frame)
            cell_frame.grid(row=2, column=col_idx + 1, padx=10, pady=2, sticky='nsew')
            
            # 1단계 매칭 파일이 ★6 패턴인지 확인
            if official_file and len(official_file.name) >= 7 and official_file.name[4] == '6':
                # 대응하는 ★3 아이콘 파일명 생성 및 경로 객체 만들기
                new_name = official_file.name[:4] + '3' + official_file.name[5:]
                three_star_jpg_path = self.all_char_manager.images_dir / new_name
                
                if three_star_jpg_path.exists(): # ★3 파일이 실제로 존재하면
                    try:
                        # ★3 아이콘 이미지 로드 및 리사이즈
                        img = Image.open(three_star_jpg_path).resize(PREVIEW_SIZE, Image.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img)
                        img_label = tk.Label(cell_frame, image=img_tk)
                        img_label.image = img_tk
                        img_label.pack() # 이미지 배치
                        
                        msg = f"{new_name}\n★6 → ★3" # 표시할 메시지
                        name_label = tk.Label(cell_frame, text=msg, fg='blue') # 파란색 텍스트
                        name_label.pack()
                    except Exception as e: # 이미지 로딩 실패 시
                        msg = f"{new_name}\n★6 → ★3\n(이미지 로딩 실패)"
                        name_label = tk.Label(cell_frame, text=msg, fg='red') # 빨간색 텍스트
                        name_label.pack(expand=True)
                else: # ★3 파일 존재 안 함
                    msg = f"{new_name}\n★6 → ★3\n({new_name} 없음)"
                    name_label = tk.Label(cell_frame, text=msg, fg='red')
                    name_label.pack(expand=True)
            else: # 1단계 매칭 파일이 ★6이 아니거나 없으면
                name_label = tk.Label(cell_frame, text="") # 빈 텍스트 (아무것도 표시 안 함)
                name_label.pack(expand=True)

    def _show_similarity_result_rows(self, table_frame, all_similarity_results):
        """
        테이블의 3, 4, 5행 (3단계 스프라이트 아이콘 매칭 결과 상위 1~3위) 채움.
        각 열에는 매칭된 스프라이트 아이콘 미리보기, 파일명, 유사도 점수 표시.
        :param table_frame: 테이블 프레임
        :param all_similarity_results: 결과 데이터
        """
        for i in range(3): # 상위 1위, 2위, 3위에 대해 (i = 0, 1, 2)
            row_idx_in_table = 3 + i # 테이블에서의 실제 행 인덱스 (3, 4, 5)
            for col_idx, result in enumerate(all_similarity_results): # 각 분할 이미지 결과에 대해
                if result is None: continue

                sprites_matched = result["sprites"] # 3단계 매칭 결과 리스트 (상위 3개)
                # 현재 셀용 프레임 생성 및 배치
                cell_frame = tk.Frame(table_frame)
                cell_frame.grid(row=row_idx_in_table, column=col_idx + 1, padx=10, pady=2, sticky='nsew')
                
                if i < len(sprites_matched) and sprites_matched[i] and sprites_matched[i][0]: # 현재 순위(i)에 해당하는 매칭 결과가 있고, 파일 경로가 유효하면
                    # (스프라이트 파일 Path, 점수, 기준 그룹 JPG Path)
                    sprite_file, sprite_score, _ = sprites_matched[i]
                    # 캐시에서 해당 스프라이트 아이콘 이미지 가져오기
                    sprite_img_preview = self.preview_cache.get(f"sprite_{col_idx}_{i}")
                    if sprite_img_preview:
                        sprite_tk = ImageTk.PhotoImage(sprite_img_preview)
                        label_img = tk.Label(cell_frame, image=sprite_tk)
                        label_img.image = sprite_tk
                        label_img.pack() # 이미지 배치
                    
                    # 파일명과 유사도 점수 텍스트 레이블
                    name_label = tk.Label(cell_frame, 
                        text=f"{sprite_file.name}\n유사도: {sprite_score:.4f}")
                    name_label.pack() # 이미지 아래에 배치
                else: # 해당 순위의 매칭 결과가 없으면 (예: 상위 1개만 매칭됨)
                    name_label = tk.Label(cell_frame, text="(유사한 스프라이트 아이콘 없음)")
                    name_label.pack(expand=True)

    def _configure_table_grid(self, table_frame, all_similarity_results):
        """
        테스트 결과 테이블의 grid 레이아웃에서 각 행과 열의 크기 조절 방식 설정.
        모든 셀이 동일한 가중치(weight=1)를 갖도록 하여 창 크기 변경 시 균등하게 조절되도록 함.
        :param table_frame: 테이블 프레임
        :param all_similarity_results: (열 개수 결정에 사용)
        """
        # 열 설정: 0번 열(행 제목) + 각 분할 이미지 결과 열들
        num_data_columns = len(all_similarity_results) if all_similarity_results else 0
        for col_idx in range(num_data_columns + 1): # 총 열 개수만큼 반복
            table_frame.grid_columnconfigure(col_idx, weight=1) # 해당 열의 가중치를 1로 설정
            
        # 행 설정: 총 6개의 데이터 행 (0~5행)
        for row_idx in range(6): # 0~5행 (데이터가 있는 행들)
            table_frame.grid_rowconfigure(row_idx, weight=1) # 해당 행의 가중치를 1로 설정

    def __del__(self):
        """
        ArenaDeckApp 객체가 소멸될 때 (보통 프로그램 종료 시) 호출되는 소멸자.
        Selenium WebDriver가 실행 중이면 안전하게 종료.
        """
        if hasattr(self, 'driver') and self.driver: # 드라이버 객체가 존재하면 (None이 아니면)
            try:
                self.driver.quit() # WebDriver와 연결된 모든 브라우저 창을 닫고 세션을 종료
                self.driver = None # 명시적으로 None 할당
            except Exception as e:
                self.log_message(f"{get_timestamp()} Error quitting WebDriver in __del__: {e}") # 디버깅용
                pass

if __name__ == "__main__":
    # 이 스크립트가 직접 실행될 때 (모듈로 임포트된 경우가 아닐 때)
    root = tk.Tk()  # Tkinter의 메인 윈도우(루트 윈도우) 생성
    app = ArenaDeckApp(root)  # ArenaDeckApp 클래스의 인스턴스 생성 (root 윈도우 전달)
    root.mainloop()  # Tkinter 이벤트 루프 시작. 이 호출은 GUI 창이 닫힐 때까지 프로그램을 대기 상태로 유지하며 사용자 이벤트 처리.