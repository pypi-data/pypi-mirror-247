from typing import Optional
from pydantic import BaseModel


class ListElement(BaseModel):
    timestamp: int  # Should be converted to the datetime
    value: float


class OrderElement(BaseModel):
    abs: int | float
    rel: int | float


class SymbolElement(BaseModel):
    symbol: str
    volume: dict[str, float]
    pnl: dict[str, float]
    qty: dict[str, int | float]
    direction: dict[str, OrderElement | float]


class FeeStats(BaseModel):
    paid: float
    rebate: float
    total: float
    fundingP: float
    fundingN: float
    fundingNet: float
    volume: float
    refs: float
    wths: float
    deps: float
    stake: float
    unstake: float
    unstakeFee: float
    optionVol: float
    optionFeeN: float
    optionFeeP: float


class User(BaseModel):
    links: list[Optional[dict[str, str]]]
    name: str
    avatar: None | str


class Orders(BaseModel):
    withRealizedPnl: bool
    type: dict[str, OrderElement]
    direction: dict[str, OrderElement | float]
    volume: dict[str, float]
    distribution: dict[str, list[OrderElement]]
    symbols: list[Optional[SymbolElement]]


class Extended(BaseModel):
    # Charts
    chart_balances: list[ListElement]
    chart_balancesR: list[ListElement]
    chart_profits: list[ListElement]
    chart_profitsR: list[ListElement]
    chart_monthly: list[ListElement]
    chart_weekly: list[ListElement]
    chart_daily: list[ListElement]
    chart_dailyPnL: list[ListElement]
    chart_indexDaily: list[ListElement]
    chart_indexWeekly: list[ListElement]
    chart_indexMonthly: list[ListElement]
    chart_maxDDHistory: list[ListElement]
    chart_maxDDDHistory: list[ListElement]
    chart_monthDDHistory: list[ListElement]

    chart_icp: list[ListElement]
    chart_longPositions: list[ListElement]
    chart_shortPositions: list[ListElement]
    chart_longPositionsIcp: list[ListElement]
    chart_shortPositionsIcp: list[ListElement]

    lastMonthlyProfit: ListElement
    lastWeeklyProfit: ListElement
    lastDailyProfit: ListElement
    lastMonthlyNetProfit: ListElement
    lastWeeklyNetProfit: ListElement
    lastDailyNetProfit: ListElement

    # Indicators
    feeStat: FeeStats
    weeklyFeeStat: FeeStats
    sourceFor: list[str]
    orders: Orders
    user: User
    tournament: dict[str, bool]

    activeDays: int
    ohr: float
    cagr: float
    trackingDays: int
    tradingDays: int
    maxDD: float
    maxDDDuration: int
    firstTrade: int  # Should be converted to the datetime
    winningDays: int
    losingDays: int
    breakevenDays: int
    winrate: float
    totalProfit: float
    totalLoss: float
    netProfit: float
    lastProfit: float
    lastWeekBalance: float
    lastWeekProfit: float
    lastWeekAverageMonthlyProfit: float
    averageMonthlyProfit: float
    averageDailyProfit: float
    averageProfit: float
    averageLoss: float
    profitRatio: float
    recoveryFactor: float
    expectedValue: float
    kSortino: float
    kSharp: float
    kCalmar: float
    betaRatio: float
    ADL: float
    volatility: float
    rSquared: float
    informationRatio: float
    treynorRatio: float
    sterlingRatio: float
    schwagerRatio: float
    safetyFirstRatio: float
    averageBalance: float
    firstBalance: float
    maxBalance: float
    minBalance: float
    lastBalance: float
    maxIcp: float
    avgIcp: float
    lastMonthGrowth: float
    lastQuarterGrowth: float
    lastYearGrowth: float
    growthRate: float
    VaR: float
    maxdddRatio: float
    betaRating: float
    usedMarkets: int
    totalTrades: int

    # Other
    keyId: str
    stockName: str
    stockNames: list[str]
    accountIds: list[str]
    baseAsset: str
    keyName: str
    keyStatus: bool
    active: bool
    progressPercent: int
    firstValidDataDate: str
    lastValidDataDate: str
    updatedAt: None | str
    startDate: str
    endDate: str
    beginMoment: str
    selfPower: None | float
    selfProfitRate: float
    integralEvaluation: float
    riskFreeRate: float
