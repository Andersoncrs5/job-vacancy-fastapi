from datetime import datetime, date
from pydantic import Field
from app.configs.orjson.orjson_config import ORJSONModel
from app.configs.db.enums import AddressTypeEnum

class AddressEnterpriseOUT(ORJSONModel):
    enterprise_id: int
    street: str
    number: str
    complement: str | None
    district: str | None
    city: str
    state: str
    country: str
    zipcode: str
    address_type: AddressTypeEnum
    is_default: bool
    is_public: bool
    created_at: datetime
    updated_at: datetime

class CreateAddressEnterpriseDTO(ORJSONModel):
    street: str = Field(..., min_length=3, max_length=75, description="Street name (3 to 75 characters)")
    number: str = Field(..., max_length=50, description="House/building number (up to 50 characters)")
    complement: str | None = Field(None, max_length=500, description="Additional address details (up to 500 characters)")
    district: str | None = Field(None, max_length=100, description="District or neighborhood (up to 100 characters)")
    city: str = Field(..., max_length=100, description="City name (up to 100 characters)")
    state: str = Field(..., max_length=100, description="State name (up to 100 characters)")
    country: str = Field(..., max_length=100, description="Country name (up to 100 characters)")
    zipcode: str = Field(..., max_length=20, description="Postal code (up to 20 characters)")
    is_public: bool = Field(True, description="Whether the address is publicly visible")
    address_type: AddressTypeEnum = Field(..., description="Type of address (e.g., commercial, residential)")
    is_default: bool = Field(True, description="Marks this as the default address")

    def to_entity(self):
        from app.configs.db.database import AddressEnterpriseEntity
        return AddressEnterpriseEntity(**self.model_dump())
    
class UpdateAddressEnterpriseDTO(ORJSONModel):
    street: str | None = Field(None, max_length=75, description="Street name (up to 75 characters)")
    number: str | None = Field(None, max_length=50, description="House/building number (up to 50 characters)")
    complement: str | None = Field(None, max_length=500, description="Additional address details")
    district: str | None = Field(None, max_length=100, description="District or neighborhood")
    city: str | None = Field(None, max_length=100, description="City name")
    state: str | None = Field(None, max_length=100, description="State name")
    country: str | None = Field(None, max_length=100, description="Country name")
    zipcode: str | None = Field(None, max_length=20, description="Postal code")
    address_type: AddressTypeEnum | None = Field(None, description="Type of address")
    is_default: bool | None = Field(None, description="Marks this as the default address")
    is_public: bool | None = Field(None, description="Whether the address is publicly visible")