# PBL_Team4

메리테일의 코드 저장소 (제출용)

## 코드 조각 설명

### 1. chat_prompt.py: ChatGPT API를 파인튜닝하여서 유저에게 맞는 적절한 동화를 생성할 수 있도록 하는 파이썬 코드

- 실제 개발 내용이 아닌 간단한 구현 및 재현만을 위한 코드 스니펫

### 2. whisper_chat.py: Whisper API를 이용한 STT 모듈

- 피봇 전 서비스를 위해 작성되었던 코드

### 3. serving/app/main.py: FastAPI를 이용한 기본 인퍼런스 서버

### 4. seving/app/api/router/predict.py: TTS를 위한 모델 파트

- 해당 코드에서는 허깅페이스 허브의 TensorflowTTS 모델을 로드하여 사용하고 있음
- pt 파일은 깃허브에 업로드하지 않았음

### 5. serving/request_test.py: 현장 시연을 위한 간단한 인퍼런스 테스트용 파이썬 파일

- argparse로 텍스트를 커맨드 상에서 주입할 수 있게 하였음
- 간단한 구현으로 인해 결과는 인퍼런스 서버 내에 저장되므로 해당 결과를 가져오는 scp 명령어 추가
- 해당 인퍼런스 서버는 학교 측에서 지원해준 것으로, 비밀번호가 걸려있음

### 6. korean_dict.txt / transcript.v.1.4.txt: KSS용 메타데이터

### 7. message.json: 실제 유저의 응답은 암호화되어 저장됨
