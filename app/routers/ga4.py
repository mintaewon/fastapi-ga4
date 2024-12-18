from fastapi import APIRouter, HTTPException
from app.services.ga4_service import GA4Report
from app.schemas.ga4 import GA4RequestSchema, GA4ResponseSchema, GA4RealtimeRequestSchema, GA4RealtimeResponseSchema

router = APIRouter()

@router.post("/report/batch-run-report", response_model=GA4ResponseSchema)
async def get_ga4_batch_run_report_data(request: GA4RequestSchema):
    """
    GA4 데이터를 수집하는 엔드포인트

    --INPUT Data (JSON)--
    property_id: 프로퍼티 ID (290659783)
    start_date: 조회 시작 날짜 (YYYY-MM-DD)
    end_date: 조회 종료 날짜 (YYYY-MM-DD)
    dimensions_list: 수집할 demension 목록 (ex: ['date', 'country', 'city'])
    metrics_list: 수집할 metric 목록 (ex: ['sessions'])

    --OUTPUT Data (JSON)--
    status: 성공여부
    data: 수집된 데이터
    """
    try:
        ga4 = GA4Report()
        data = []
        while True:
            temp_data = await ga4.fetch_ga4_data(property_id=request.property_id, start_date=request.start_date, end_date=request.end_date, dimensions_list=request.dimensions_list, metrics_list=request.metrics_list, limit=request.limit, offset=request.offset)
            data.extend(temp_data)
            if len(temp_data) < request.limit:
                break
            request.offset += request.limit
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/report/realtime-run-report", response_model=GA4RealtimeResponseSchema)
async def get_ga4_realtime_run_report_data(request: GA4RealtimeRequestSchema):
    """
    GA4 Real Time Report 데이터를 수집하는 엔드포인트

    --INPUT Data (JSON)--
    property_id: 프로퍼티 ID (290659783)
    dimensions_list: 수집할 demension 목록 (ex: ['country', 'city'])
    metrics_list: 수집할 metric 목록 (ex: ['activeUsers'])

    --OUTPUT Data (JSON)--
    status: 성공여부
    data: 수집된 데이터
    """
    ga4 = GA4Report()
    data = await ga4.fetch_ga4_realtime_data(property_id=request.property_id, metrics_list=request.metrics_list, dimensions_list=request.dimensions_list)
    return {"status": "success", "data": data}

