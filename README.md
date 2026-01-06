# 대중교통 API 테스트 백엔드

FastAPI를 사용한 지하철, 버스, SK 대중교통 API 통신 테스트 백엔드

## 개발 환경

- Python 3.12
- FastAPI
- Docker
- PyCharm

## API 키
각자 발급받은 API키를 .env로 넣으시면 됩니다.

## 설치 및 실행

### 로컬 환경에서 실행

1. 가상 환경 생성 및 활성화 (선택사항)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정 (선택사항)
```bash
# .env 파일은 선택사항입니다 (코드에 API 키 기본값이 설정되어 있음) -> 수정하여서 추가 하셔야 합니다.
# 환경 변수를 사용하려면 .env 파일을 생성하세요:
# SUBWAY_API_KEY=your_key_here
# BUS_API_KEY=your_key_here
# SK_API_KEY=your_key_here
```

4. 서버 실행
```bash
python main.py
# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker를 사용한 실행

1. Docker 이미지 빌드
```bash
docker build -t transport-api .
```

2. Docker 컨테이너 실행
```bash
docker run -d -p 8000:8000 --name transport-api transport-api
```

3. 환경 변수를 사용하려면 (선택사항)
```bash
# .env 파일이 있는 경우
docker run -d -p 8000:8000 --env-file .env --name transport-api transport-api
```

## API 엔드포인트

### Swagger UI
서버 실행 후 브라우저에서 다음 주소로 접속하세요:
- **Swagger UI (API 테스트)**: http://localhost:8000/docs
- **API 루트**: http://localhost:8000
- **ReDoc (API 문서)**: http://localhost:8000/redoc

**중요**: 브라우저에서는 `localhost` 또는 `127.0.0.1`을 사용하세요. `0.0.0.0`은 서버 설정용 주소입니다.

### API 엔드포인트

1. **지하철 실시간 위치**
   - `GET /api/subway/realtime`
   - 파라미터:
     - `line`: 지하철 호선명 (예: "1호선", "2호선")
     - `start_index`: 시작 인덱스 (기본값: 0)
     - `end_index`: 종료 인덱스 (기본값: 5)

2. **버스 실시간 위치**
   - `GET /api/bus/realtime`
   - 파라미터:
     - `bus_route_id`: 버스 노선 ID (예: "100100118")

3. **SK 대중교통 경로 탐색**
   - `GET /api/sk/route`
   - 파라미터:
     - `start_x`: 출발지 경도
     - `start_y`: 출발지 위도
     - `end_x`: 도착지 경도
     - `end_y`: 도착지 위도
     - `count`: 결과 개수 (기본값: 5)
     - `lang`: 언어 코드 (0: 한국어, 1: 영어)

4. **헬스 체크**
   - `GET /health`

## 사용 예시

### Swagger UI 사용
1. 서버 실행 후 브라우저에서 http://localhost:8000/docs 접속
2. 각 API 엔드포인트를 클릭하여 테스트
3. "Try it out" 버튼을 클릭하여 파라미터 입력
4. "Execute" 버튼을 클릭하여 API 호출

### curl 예시
```bash
# 지하철 실시간 위치 조회
curl "http://localhost:8000/api/subway/realtime?line=1호선&start_index=0&end_index=5"

# 버스 실시간 위치 조회
curl "http://localhost:8000/api/bus/realtime?bus_route_id=100100118"

# SK 경로 탐색
curl "http://localhost:8000/api/sk/route?start_x=126.9780&start_y=37.5665&end_x=127.0276&end_y=37.4979"
```

## API 테스트 가이드

### 1. 지하철 실시간 위치 API
**파라미터 예시:**
- `line`: `1호선`, `2호선`, `3호선`, `4호선`, `5호선`, `6호선`, `7호선`, `8호선`, `9호선`
- `start_index`: `0` (기본값)
- `end_index`: `5` (기본값)

**테스트 예시:**
- line: `1호선`
- start_index: `0`
- end_index: `5`

**참고**: 인증키가 유효하지 않으면 "인증키가 유효하지 않습니다" 오류가 발생합니다. 서울시 공공데이터포털(data.seoul.go.kr)에서 인증키를 발급받아야 합니다.

### 2. 버스 실시간 위치 API
**파라미터 예시:**
- `bus_route_id`: 버스 노선 ID (예: `100100118`, `100100119` 등)
  - 실제 노선 ID는 서울시 버스정보 시스템에서 확인 필요
- `service_key`: 선택사항 (비워두면 기본 인증키 사용)

**테스트 예시:**
- bus_route_id: `100100118`

**참고**: "SERVICE KEY IS NOT REGISTERED ERROR" 오류가 발생하면 인증키가 등록되지 않았거나 유효하지 않습니다.

### 3. SK 대중교통 경로 탐색 API
**파라미터 예시 (서울 지역 좌표):**
- `start_x` (경도): 서울 지역 경도 (126.9xxx ~ 127.1xxx)
- `start_y` (위도): 서울 지역 위도 (37.4xxx ~ 37.7xxx)
- `end_x` (경도): 서울 지역 경도
- `end_y` (위도): 서울 지역 위도
- `count`: `1` ~ `10` (기본값: 5)
- `lang`: `0` (한국어) 또는 `1` (영어)

**서울 주요 지역 좌표 (WGS84):**
- 서울역: 경도 `126.9716`, 위도 `37.5547`
- 강남역: 경도 `127.0276`, 위도 `37.4979`
- 명동: 경도 `126.9850`, 위도 `37.5636`
- 종로: 경도 `126.9780`, 위도 `37.5665`
- 잠실: 경도 `127.1000`, 위도 `37.5133`

**테스트 예시 (서울역 → 강남역):**
- start_x: `126.9716`
- start_y: `37.5547`
- end_x: `127.0276`
- end_y: `37.4979`
- count: `5`
- lang: `0`

**참고**: 
- 좌표는 WGS84 좌표계를 사용합니다
- 서비스 지역이 아니라는 오류가 발생하면 좌표가 잘못되었거나 서비스 지역이 아닐 수 있습니다
- SK API는 전국 대중교통을 지원하지만, 일부 지역은 제한될 수 있습니다

## 인증키 오류 해결 방법

### 지하철/버스 API 인증키가 작동하지 않는 경우:

1. **인증키 발급 확인**
   - 서울시 공공데이터포털: https://data.seoul.go.kr
   - 서울시 버스정보 API: http://data.seoul.go.kr/dataList/OA-12764/F/1/datasetView.do
   - 로그인 후 "인증키 신청" 또는 "마이페이지 > 인증키 관리"에서 확인

2. **인증키 활성화 시간**
   - 발급 직후 즉시 사용 불가능할 수 있음
   - 최대 1-2시간 후 활성화
   - 발급 후 시간이 지난 후 다시 시도

3. **인증키 확인 사항**
   - 인증키를 정확히 복사했는지 확인 (공백, 특수문자 포함)
   - 대소문자 구분 확인
   - 인증키가 만료되지 않았는지 확인

4. **인증키 테스트 방법**
   - 브라우저에서 직접 URL 테스트:
     - 지하철: `http://swopenapi.seoul.go.kr/api/subway/{인증키}/json/realtimePosition/0/5/1호선`
     - 버스: `http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid?serviceKey={인증키}&busRouteId=100100118&resultType=json`

5. **환경 변수로 인증키 설정**
   - `.env` 파일 생성 (프로젝트 루트에)
   - 다음 내용 추가:
     ```
     SUBWAY_API_KEY=발급받은_지하철_인증키
     BUS_API_KEY=발급받은_버스_인증키
     SK_API_KEY=발급받은_SK_인증키
     ```
   - 서버 재시작 필요

## 참고사항

- 각 API의 실제 엔드포인트와 파라미터는 API 제공자의 문서를 참고하세요
- API 키는 환경 변수나 .env 파일을 통해 관리하는 것을 권장합니다
- 실제 사용 시 API 제공자의 정책과 제한사항을 확인하세요
- 제공된 인증키가 샘플/테스트 키일 수 있으며, 실제 사용하려면 각 서비스에서 발급받아야 합니다