from typing import List

from fastapi import APIRouter, HTTPException
from app.services.ga4_service import GA4Report

router = APIRouter()

@router.post("/get-ga4-data")
async def get_ga4_data(property_id: str, start_date: str, end_date: str, metrics_list: List[str], dimensions_list: List[str], limit: int = 100000, offset: int = 0):
    """
    GA4 데이터를 수집하는 엔드포인트
    :param start_date: 조회 시작 날짜 (YYYY-MM-DD)
    :param end_date: 조회 종료 날짜 (YYYY-MM-DD)
    :param metrics: 수집할 메트릭
    :param dimensions: 수집할 차원
    :return: 수집된 데이터
    """
    try:
        ga4 = GA4Report()
        data = await ga4.fetch_ga4_data(property_id=property_id, start_date=start_date, end_date=end_date, metrics_list=metrics_list, dimensions_list=dimensions_list, limit=limit, offset=offset)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
