# Week 11 실습
## 오늘 한 것
- PyInstaller 설치 및 빌드
- resource_path() 함수 추가
- --add-data 옵션으로 에셋 포함
- .exe 실행 확인
## resource_path() 를 써야 하는 이유
exe 파일 실행 할 때 이미지, 사운드 파일 경로를 제대로 찾기 하기 위해서
## 빌드 명령어
-pyinstaller --onefile Game.py

-pyinstaller --onefile --windowed Game.py

-pyinstaller --onefile --windowed ^
--add-data "sprite;sprite" ^
--add-data "sound;sound" ^
--name=Game Game.py
## AI 활용 내역
...
