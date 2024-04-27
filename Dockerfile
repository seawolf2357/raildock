# 공식 Python 이미지를 Docker Hub에서 사용합니다.
FROM python:3.10-slim

# 컨테이너 내부의 작업 디렉토리 설정
WORKDIR /app

# 로컬 코드를 컨테이너의 작업 디렉토리로 복사
COPY . /app

RUN pip install fastapi aiohttp uvicorn httpx

# Python 종속성 설치

# Docker에게 컨테이너가 런타임에 포트 80을 사용한다고 알림
EXPOSE 8080

# Uvicorn 서버를 포트 80에서 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

