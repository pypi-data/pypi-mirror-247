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

    time_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"

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

    async def get_last_valid_data_date(self) -> datetime:
        await self._update_cache_if_stale()
        return datetime.strptime(
            self.cached_portfolio.extended.lastValidDataDate, self.time_format
        )

    async def get_start_date(self) -> datetime:
        await self._update_cache_if_stale()
        return datetime.strptime(
            self.cached_portfolio.extended.startDate, self.time_format
        )

    async def get_end_date(self) -> datetime:
        await self._update_cache_if_stale()
        return datetime.strptime(
            self.cached_portfolio.extended.endDate, self.time_format
        )

    async def get_unrpnl_deposit_of_the_first_point(self) -> float:
        """Absolute unrealized value"""
        await self._update_cache_if_stale()

        if (
            self.cached_portfolio.extended.chart_balances
            and self.cached_portfolio.extended.chart_profits
            and self.cached_portfolio.extended.chart_balances[0]
            and self.cached_portfolio.extended.chart_profits[0]
        ):
            return self.cached_portfolio.extended.chart_balances[0].value / (
                1 + self.cached_portfolio.extended.chart_profits[0].value
            )
        else:
            return 0

    async def get_total_deposits(self) -> float:
        """Absolute value"""
        await self._update_cache_if_stale()

        return self.cached_portfolio.extended.feeStat.deps

    async def get_total_withdraws(self) -> float:
        """Absolute value"""
        await self._update_cache_if_stale()

        return self.cached_portfolio.extended.feeStat.wths

    async def get_unrpnl_last_balance(self) -> float:
        """Absolute value"""
        await self._update_cache_if_stale()

        if (
            self.cached_portfolio.extended.chart_balances
            and self.cached_portfolio.extended.chart_balances[0]
        ):
            return self.cached_portfolio.extended.chart_balances[-1].value
        else:
            return 0

    async def get_unrpnl_last_netpnl(self) -> float:
        """Absolute value"""
        await self._update_cache_if_stale()

        return sum(
            [x.value for x in self.cached_portfolio.extended.chart_dailyPnL]
        )
