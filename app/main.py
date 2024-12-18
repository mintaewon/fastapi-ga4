from fastapi import FastAPI
from app.routers import ga4

def create_app():
    app = FastAPI(title="GA4 Data Collector")

    @app.get("/", tags=["Health"])
    async def health_check():
        return {"status": "healthy"} 

    # 라우터 등록
    app.include_router(ga4.router, prefix="/api/google/ga4", tags=["GA4"])

    return app