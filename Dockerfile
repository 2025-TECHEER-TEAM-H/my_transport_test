# Dockerfile: Docker 이미지를 빌드하기 위한 설정 파일
# 이 파일의 지시사항에 따라 Docker 컨테이너 이미지가 생성됩니다

# 베이스 이미지: Python 3.12 공식 이미지 (slim 버전 - 용량 최소화)
# slim 버전은 최소한의 패키지만 포함하여 이미지 크기를 줄임
FROM python:3.12-slim

# 작업 디렉토리 설정 (컨테이너 내부의 작업 공간)
# 이후 모든 명령은 /app 디렉토리에서 실행됨
WORKDIR /app

# 시스템 패키지 업데이트 및 캐시 정리
# && : 명령을 연속으로 실행 (앞 명령이 성공하면 다음 명령 실행)
# --no-install-recommends: 불필요한 권장 패키지 설치 제외
# rm -rf /var/lib/apt/lists/*: 패키지 목록 캐시 삭제 (이미지 크기 감소)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
# requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt .
# --no-cache-dir: pip 캐시를 저장하지 않음 (이미지 크기 감소)
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
# 현재 디렉토리의 main.py 파일을 컨테이너의 /app 디렉토리로 복사
COPY main.py .

# 포트 노출 선언 (실제로 포트를 열지는 않음, 문서화 목적)
# docker run -p 옵션으로 포트 매핑이 필요함
EXPOSE 8000

# 컨테이너 실행 시 자동으로 실행될 명령
# uvicorn 서버를 실행하여 FastAPI 애플리케이션 시작
# --host 0.0.0.0: 모든 네트워크 인터페이스에서 접근 가능
# --port 8000: 8000번 포트에서 서버 실행
# --reload: 코드 변경 시 자동 재시작 (개발 모드, 프로덕션에서는 제거 권장)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
