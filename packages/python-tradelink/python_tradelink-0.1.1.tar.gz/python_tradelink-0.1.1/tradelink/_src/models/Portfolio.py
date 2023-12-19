from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from tradelink._src.models.Extended import Extended


class PortfolioModel(BaseModel):
    extended: Extended

    # Other
    createdAt: datetime
    startDate: datetime
    updatedAt: datetime
    views: int
    ctx: str
    disqualified: bool
    userId: str
    name: str
    keyId: str
    keyIds: list[str]
    public: bool
    inRating: bool
    unlisted: bool
    showPositions: bool
    jet: Optional[dict[str, list[Optional[dict[str, datetime]]] | bool]]
    description: str
    marketDirection: None | str
    speed: None | str
    managementType: None | str
    positionType: None | str
    riskType: None | str
    portfolioId: str
    rank: int
    rankDelta: int
    stars: int
    

class TradeLinkStep(Enum):
    week = "week"
    day = "day"
    hour = "hour"
