from datetime import datetime, timedelta

from pydantic import ValidationError
from tradelink._src.Requester import Requester
from tradelink._src.utils.logging import get_logger
from tradelink._src.models.Portfolio import (
    PortfolioModel,
    TradeLinkStep,
)


class Portfolio:
    id: str
    step: TradeLinkStep
    start_date: datetime | None = None
    end_date: datetime | None = None
    requester: Requester

    cached_portfolio: PortfolioModel
    cache_updated_at: None | datetime = None

    def __init__(
        self,
        _id: str,
        step: TradeLinkStep = TradeLinkStep.day,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ):
        self.id = _id
        self.step = step
        self.start_date = start_date
        self.end_date = end_date
        self.requester = Requester()
        self._logger = get_logger(__name__)

    async def _update_cache_if_stale(self) -> None:
        if not self.cache_updated_at:
            await self.update_info()
        else:
            if (
                self.cache_updated_at
                and datetime.utcnow() - self.cache_updated_at
                > timedelta(hours=1)
            ):
                await self.update_info()

        if not self.cached_portfolio:
            self._logger.error(
                f"Can't get total return of the portfolio {self.id}"
            )
            raise ValueError(
                f"Can't get total return of the portfolio {self.id}"
            )

    async def update_info(self) -> "Portfolio":
        self._logger.debug(f"Started updating portfolio {self.id}")
        try:
            response = await self.requester.get_portfolio(self.id, self.step)
        except ValidationError:
            self._logger.error(f"Failed to update info of portfolio {self.id}")
            return self

        if isinstance(response, str):
            self._logger.error(f"Failed to update info of portfolio {self.id}")
            return self

        self.cached_portfolio = response
        self.cache_updated_at = datetime.utcnow()

        self._logger.info(f"Succesfully updated portfolio {self.id}")
        return self

    async def get_total_return(self) -> float:
        """In percents"""
        await self._update_cache_if_stale()
        return self.cached_portfolio.extended.lastProfit * 100

    async def get_total_volume(self) -> float:
        """Absolute value"""
        await self._update_cache_if_stale()
        return self.cached_portfolio.extended.feeStat.volume
