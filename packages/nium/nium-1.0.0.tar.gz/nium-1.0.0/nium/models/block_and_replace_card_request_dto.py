# coding: utf-8

"""
    NIUM Platform

    NIUM Platform

    Contact: experience@nium.com
    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, constr, validator
from nium.models.address import Address

class BlockAndReplaceCardRequestDTO(BaseModel):
    """
    A card can be blocked and replaced using the Block And Replace Card API  # noqa: E501
    """
    reason: StrictStr = Field(..., description="This field accepts the reason for card block. The possible values are: fraud lost stolen damaged")
    replace_card: StrictBool = Field(..., alias="replaceCard", description="A Flag that specifies whether to replace card or not")
    plastic_id: Optional[StrictStr] = Field(None, alias="plasticId", description="Pre-defined plastic Id defined at NIUM and communicated to client. It is used to determine the card design")
    card_expiry: Optional[StrictStr] = Field(None, alias="cardExpiry", description="Expiry date to be set for virtual and virtual physical cards. For physical cards do not send this field. This field is in MMYY format. For virtual cards, the last acceptable date is the year-end of the 5th year from now. Card will be valid till the last day of the month and year of expiry.")
    use_current_address: Optional[StrictBool] = Field(None, alias="useCurrentAddress", description="Boolean \"useCurrentAddress\" specifies whether to use existing address in the system or new address passed in address object")
    delivery: Optional[Address] = None
    email: Optional[StrictStr] = Field(None, description="Card holder Email")
    country_code: Optional[constr(strict=True, max_length=2, min_length=2)] = Field(None, alias="countryCode", description="Country is two-letter ISO2 country code for mobile")
    mobile: Optional[constr(strict=True)] = Field(None, description="Mobile field is where the recipient's mobile phone number. This field is mandatory when useBillingAddress is true")
    __properties = ["reason", "replaceCard", "plasticId", "cardExpiry", "useCurrentAddress", "delivery", "email", "countryCode", "mobile"]

    @validator('reason')
    def reason_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('fraud, lost, stolen, damaged'):
            raise ValueError("must be one of enum values ('fraud, lost, stolen, damaged')")
        return value

    @validator('mobile')
    def mobile_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"\d{0,30}", value):
            raise ValueError(r"must validate the regular expression /\d{0,30}/")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BlockAndReplaceCardRequestDTO:
        """Create an instance of BlockAndReplaceCardRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of delivery
        if self.delivery:
            _dict['delivery'] = self.delivery.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BlockAndReplaceCardRequestDTO:
        """Create an instance of BlockAndReplaceCardRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BlockAndReplaceCardRequestDTO.parse_obj(obj)

        _obj = BlockAndReplaceCardRequestDTO.parse_obj({
            "reason": obj.get("reason"),
            "replace_card": obj.get("replaceCard"),
            "plastic_id": obj.get("plasticId"),
            "card_expiry": obj.get("cardExpiry"),
            "use_current_address": obj.get("useCurrentAddress"),
            "delivery": Address.from_dict(obj.get("delivery")) if obj.get("delivery") is not None else None,
            "email": obj.get("email"),
            "country_code": obj.get("countryCode"),
            "mobile": obj.get("mobile")
        })
        return _obj


