import webbrowser  # 맨 위에 추가
import os
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from dotenv import load_dotenv
# .env 파일에 기록된 환경 변수들을 로드합니다.
load_dotenv()

app = FastAPI(
    title="대중교통 API 테스트",
    description="환경 변수를 활용한 대중교통 API 통합 백엔드",
    version="1.1.0"
)

# 환경 변수에서 키를 읽어옵니다.
# 만약 .env 파일이 없거나 설정이 안 되어 있으면 None이 할당됩니다.
SUBWAY_API_KEY = os.getenv("SUBWAY_API_KEY")
BUS_API_KEY = os.getenv("BUS_API_KEY")
SK_API_KEY = os.getenv("SK_API_KEY")

@app.get("/")
async def root():
    return {
        "message": "환경 변수 설정이 완료된 서버입니다.",
        "status": "ready",
        "keys_loaded": {
            "subway": SUBWAY_API_KEY is not None,
            "bus": BUS_API_KEY is not None,
            "sk": SK_API_KEY is not None
        }
    }

@app.get("/api/subway/realtime")
async def get_subway_realtime(
    line: str = Query(..., description="지하철 호선 (예: 1호선)", examples=["1호선"]),
    start_index: int = 0,
    end_index: int = 5
):
    if not SUBWAY_API_KEY:
        raise HTTPException(status_code=500, detail="SUBWAY_API_KEY가 설정되지 않았습니다.")

    url = f"http://swopenapi.seoul.go.kr/api/subway/{SUBWAY_API_KEY}/json/realtimePosition/{start_index}/{end_index}/{line}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        return JSONResponse(content=response.json())

@app.get("/api/bus/realtime")
async def get_bus_realtime(
    bus_route_id: str = Query(..., examples=["100100118"])
):
    if not BUS_API_KEY:
        raise HTTPException(status_code=500, detail="BUS_API_KEY가 설정되지 않았습니다.")

    # 특수문자가 포함된 키의 인코딩 깨짐 방지를 위해 직접 결합
    base_url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid"
    url = f"{base_url}?serviceKey={BUS_API_KEY}&busRouteId={bus_route_id}&resultType=json"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        return JSONResponse(content=response.json())

@app.get("/api/sk/route")
async def get_sk_route(
    start_x: float = 126.9780, start_y: float = 37.5665,
    end_x: float = 127.0276, end_y: float = 37.4979
):
    if not SK_API_KEY:
        raise HTTPException(status_code=500, detail="SK_API_KEY가 설정되지 않았습니다.")

    url = "https://apis.openapi.sk.com/transit/routes"
    headers = {"appKey": SK_API_KEY, "Content-Type": "application/json"}
    payload = {"startX": start_x, "startY": start_y, "endX": end_x, "endY": end_y, "count": 5}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        return JSONResponse(content=response.json())

if __name__ == "__main__":
    import uvicorn
    from threading import Timer

    # 서버가 뜰 시간을 벌어주기 위해 1.5초 뒤에 브라우저 실행
    # 주소를 127.0.0.1로 고정하여 바로 접속되게 함
    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8000/docs")).start()

    # 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000)