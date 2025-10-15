from datetime import datetime, date

from pydantic import Field

from app.configs.orjson.orjson_config import ORJSONModel
from app.configs.db.enums import AddressTypeEnum

class AddressUserOUT(ORJSONModel):
    id: int
    user_id: int
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
    is_visible: bool
    created_at: datetime
    updated_at: datetime

class CreateAddressUserDTO(ORJSONModel):
    street: str = Field(..., min_length=3, max_length=255, description="Street name (3–255 characters)")
    number: str | None = Field(None, max_length=50, description="House/building number (up to 50 characters)")
    complement: str | None = Field(None, max_length=500, description="Additional address details (optional)")
    district: str | None = Field(None, max_length=100, description="District or neighborhood (up to 100 characters)")
    city: str = Field(..., max_length=100, description="City name (up to 100 characters)")
    state: str = Field(..., max_length=100, description="State name (up to 100 characters)")
    country: str = Field("Brasil", max_length=100, description="Country name (default = Brasil)")
    zipcode: str | None = Field(None, max_length=20, description="Postal code (up to 20 characters)")
    address_type: AddressTypeEnum = Field(..., description="Type of address (e.g., RESIDENTIAL, COMMERCIAL)")
    is_default: bool = Field(False, description="Marks this as the default address")
    is_visible: bool = Field(False, description="Whether the address is publicly visible")

    def to_entity(self):
        from app.configs.db.database import AddressUserEntity
        return AddressUserEntity(**self.model_dump())

class UpdateAddressUserDTO(ORJSONModel):
    street: str | None = Field(None, max_length=255, description="Street name (optional, up to 255 characters)")
    number: str | None = Field(None, max_length=50, description="House/building number (optional)")
    complement: str | None = Field(None, max_length=500, description="Additional address details (optional)")
    district: str | None = Field(None, max_length=100, description="District or neighborhood (optional)")
    city: str | None = Field(None, max_length=100, description="City name (optional)")
    state: str | None = Field(None, max_length=100, description="State name (optional)")
    country: str | None = Field(None, max_length=100, description="Country name (optional)")
    zipcode: str | None = Field(None, max_length=20, description="Postal code (optional)")
    address_type: AddressTypeEnum | None = Field(None, description="Type of address (optional)")
    is_default: bool | None = Field(None, description="Marks this as the default address (optional)")
    is_visible: bool | None = Field(None, description="Whether the address is publicly visible (optional)")