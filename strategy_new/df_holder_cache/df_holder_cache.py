from typing import Dict, Optional
from src.common.adapter.out.upbit_df_holder import UpbitDfHolder


class DfHolderCache:
    """UpbitDfHolder 캐시 관리자"""

    _instance: Optional["DfHolderCache"] = None

    @classmethod
    def get_instance(cls, timezone: Optional[str] = None) -> "DfHolderCache":
        """
        싱글톤 인스턴스 반환
        최초 호출 시에만 timezone이 필요
        """
        if not cls._instance:
            if timezone is None:
                raise ValueError("timezone must be provided for initial creation")
            cls._instance = cls(timezone)
        return cls._instance

    def __init__(self, timezone: str):
        """
        private 생성자
        get_instance()를 통해서만 인스턴스 생성 가능
        """
        if DfHolderCache._instance:
            raise RuntimeError("Use get_instance() instead")

        self._holders: Dict[str, UpbitDfHolder] = {}
        self._timezone: str = timezone

    def get_holder(self, ticker: str) -> UpbitDfHolder:
        """UpbitDfHolder 조회 또는 생성"""
        if ticker not in self._holders:
            self._holders[ticker] = UpbitDfHolder(ticker=ticker, timezone=self._timezone)
        return self._holders[ticker]

    def refresh_data(self, ticker: Optional[str] = None) -> None:
        """
        데이터 새로고침
        ticker가 None이면 모든 티커 새로고침
        """
        if ticker:
            if ticker in self._holders:
                self._holders[ticker].refresh_data()
        else:
            for holder in self._holders.values():
                holder.refresh_data()

    def clear(self) -> None:
        """캐시 초기화"""
        self._holders.clear()

    @property
    def timezone(self) -> str:
        """현재 설정된 timezone 반환"""
        return self._timezone
