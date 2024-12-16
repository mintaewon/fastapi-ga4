from fastapi import FastAPI
from app.routers import ga4

def create_app():
    app = FastAPI(title="GA4 Data Collector")

    # 라우터 등록
    app.include_router(ga4.router, prefix="/ga4", tags=["GA4"])
    # app.include_router(health.router, prefix="/health", tags=["Health"])

    return app