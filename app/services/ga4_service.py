from google.api_core.retry import Retry
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    FilterExpressionList,
    Metric,
    NumericValue,
    RunReportRequest,
    RunRealtimeReportRequest,
)

class BaseInfo:
    def __init__(self):
        self.retry = Retry(
        initial=1.0,  # 첫 시도 후 대기 시간 (초)
        maximum=20.0,  # 최대 대기 시간 (초)
        multiplier=2.0,  # 대기 시간 증가 배율
        deadline=100.0  # 전체 재시도 제한 시간 (초)
        )


class GA4Report(BaseInfo):
    def __init__(self):
        super().__init__()

    def _get_client(self):
        client = BetaAnalyticsDataClient()
        return client

    async def fetch_ga4_data(self, property_id: str, start_date: str, end_date: str, metrics_list: list, dimensions_list: list, limit=100000, offset=0):
        """
        GA4 데이터를 호출하는 함수
        :param start_date: 조회 시작 날짜
        :param end_date: 조회 종료 날짜
        :param metrics_list: 수집할 메트릭 (배열)
        :param dimensions_list: 수집할 차원 (배열)
        :return: GA4 데이터
        """
        client = self._get_client()
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dl) for dl in dimensions_list],
            metrics=[Metric(name=ml) for ml in metrics_list],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            limit = limit,
            offset = offset,
        )
        response = client.run_report(request=request, retry=self.retry)
        result = [
            {dimension.name: row.dimension_values[i].value for i, dimension in enumerate(response.dimension_headers)}
            | {metric.name: row.metric_values[i].value for i, metric in enumerate(response.metric_headers)}
            for row in response.rows
        ]
        return result
    
    async def fetch_ga4_realtime_data(self, property_id: str, metrics_list: list, dimensions_list: list, limit=100000, offset=0):
        client = self._get_client()
        request = RunRealtimeReportRequest(
            property=f"properties/{property_id}",
            metrics=[Metric(name=ml) for ml in metrics_list],
            dimensions=[Dimension(name=dl) for dl in dimensions_list],
        )
        response = client.run_realtime_report(request=request, retry=self.retry)
        result = [
            {dimension.name: row.dimension_values[i].value for i, dimension in enumerate(response.dimension_headers)}
            | {metric.name: row.metric_values[i].value for i, metric in enumerate(response.metric_headers)}
            for row in response.rows
        ]
        return result
