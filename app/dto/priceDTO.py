from typing import List
from pydantic import BaseModel, Field, model_validator

class PriceListDTO(BaseModel):
    priceList: List[float] = Field(..., 
                                   min_items=60,
                                   description="A list of positive float numbers with a minimum size of 60.")
    
    @model_validator(mode="before")
    def validate_price_list(cls, values):
        price_list = values.get("priceList")
        if len(price_list) < 60:
            raise ValueError("The priceList must contain at least 60 elements.")
        if any(price <= 0 for price in price_list):
            raise ValueError("All numbers in the priceList must be positive.")
        return values
    

    class Config:
        schema_extra = {
            "example": {
                "priceList": [100.5, 200.75, 300.0, 150.25, 125.0] * 12
            }
        }
