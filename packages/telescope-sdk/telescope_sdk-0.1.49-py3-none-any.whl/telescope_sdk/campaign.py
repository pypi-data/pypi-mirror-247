from enum import Enum
from typing import List, Optional
from telescope_sdk.common import UserFacingDataType
from pydantic import BaseModel
from telescope_sdk.company import CompanySizeRange, FoundedYearRange, RevenueRange


class CampaignStatus(str, Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'ERROR'


class ExampleCompany(BaseModel):
    id: str
    name: str


class LocationType(str, Enum):
    city = 'city'
    state = 'state'


class LocationFilter(BaseModel):
    type: LocationType
    name: str


class IdealCustomerProfile(BaseModel):
    id: str
    owner_id: str
    campaign_id: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str] = None
    example_companies: List[ExampleCompany]
    job_titles: List[str]
    keywords: List[str] = None
    negative_keywords: List[str] = None
    country_codes: List[List[str]] = None
    employee_country_codes: List[List[str]] = None
    industries: List[str] = None
    company_size_range: CompanySizeRange = None
    company_types: List[str] = None
    founded_year_range: Optional[FoundedYearRange] = None
    require_email: Optional[bool] = False
    hq_location_filters: Optional[List[LocationFilter]] = None
    employee_location_filters: Optional[List[LocationFilter]] = None
    company_revenue_range: Optional[RevenueRange] = None
    only_show_verified_emails: Optional[bool] = False
    hide_companies_in_another_campaign: Optional[bool] = False
    hide_leads_in_another_campaign: Optional[bool] = False


class Campaign(UserFacingDataType):
    name: str
    status: CampaignStatus
    sequence_id: Optional[str] = None
    outreach_enabled: Optional[bool] = None
    replenish: bool
    icp: IdealCustomerProfile
