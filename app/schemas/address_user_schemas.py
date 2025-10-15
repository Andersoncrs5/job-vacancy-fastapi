from datetime import datetime, date
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

    def to_entity(self):
        from app.configs.db.database import AddressUserEntity

        return AddressUserEntity(
            street = self.street,
            number = self.number,
            complement = self.complement,
            district = self.district,
            city = self.city,
            state = self.state,
            country = self.country,
            zipcode = self.zipcode,
            address_type = self.address_type,
            is_visible = self.is_visible,
            is_default = self.is_default,
        )
    
class UpdateAddressUserDTO(ORJSONModel):
    street: str | None
    number: str | None
    complement: str | None
    district: str | None
    city: str | None
    state: str | None
    country: str | None
    zipcode: str | None
    address_type: AddressTypeEnum | None
    is_default: bool | None
    is_visible: bool | None