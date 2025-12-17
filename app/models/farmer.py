from pydantic import BaseModel, Field, field_validator
from datetime import date


class FarmerDetails(BaseModel):
    """Farmer and crop information"""
    farmer_name: str = Field(..., min_length=1, max_length=100)
    crop_name: str = Field(..., min_length=1, max_length=100)
    season: str = Field(..., pattern="^(Kharif|Rabi|Summer|Other)$")
    total_acres: float = Field(..., gt=0)
    sowing_date: date
    harvest_date: date
    village: str = Field(..., min_length=1, max_length=100)
    taluka: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)

    @field_validator('harvest_date')
    def validate_harvest_date(cls, v, info):
        if 'sowing_date' in info.data and v <= info.data['sowing_date']:
            raise ValueError('Harvest date must be after sowing date')
        return v
