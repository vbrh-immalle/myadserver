from dataclasses import dataclass

@dataclass
class Ad:
    afbeelding: str
    link: str


@dataclass
class CeoResellerInfo:
    reseller: str
    afbeelding: str
    link: str
    aantal_views: int
    aantal_clicks: int
    CTR: float


@dataclass
class ResellerInfo:
    afbeelding: str
    link: str
    aantal_views: int
    aantal_clicks: int
    CTR: float
