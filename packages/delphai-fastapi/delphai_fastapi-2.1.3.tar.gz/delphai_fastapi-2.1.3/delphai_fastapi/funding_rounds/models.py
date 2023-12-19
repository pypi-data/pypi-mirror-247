from datetime import datetime, date
from typing import Dict, List, Optional
from enum import Enum

from fastapi_camelcase import CamelModel
from pydantic import Field

from ..types import ObjectId


class FundingAmountType(str, Enum):
    ORIGINAL = "original"
    CONVERTED = "converted"


class FundingAmountEntry(CamelModel):
    currency: str = Field(description="Currency of funding number", example="EUR")
    value: int = Field(description="Funding number")
    type: FundingAmountType


class Investor(CamelModel):
    name: str = Field(..., description="Investor name")
    company_id: Optional[ObjectId] = Field(description="Internal Investor company ID")


class FundingRound(CamelModel):
    id: ObjectId = Field(..., description="Internal FundingRound ID")
    company_id: ObjectId = Field(..., description="Internal company ID")
    amounts: Optional[Dict[str, FundingAmountEntry]] = Field(
        description="Original and converted funding numbers with currencies"
    )
    stage: Optional[str] = Field(description="Funding round stage", example="Series A")
    date: date  # = Field(..., description="Date when the funding round was closed") # doesn't work for some reason
    updated_at: Optional[datetime] = Field(
        description="Date and time when the funding round was updated in delphai"
    )
    investors: Optional[List[Investor]] = Field(
        description="List of investors in the funding round"
    )


class FundingRounds(CamelModel):
    results: List[FundingRound]
    total: int = Field(..., description="Number of results")
