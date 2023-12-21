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

class RenewCardRequest(BaseModel):
    """
    A card can be renewed using the Renew Card API on or before 45 days from the date of expiry  # noqa: E501
    """
    card_expiry: Optional[StrictStr] = Field(None, alias="cardExpiry", description="Expiry date for the renewed card to be set in MMyy format. This field is conditional This field is mandatory for virtual and virtual upgraded to physical cards. This field is optional for a physical card. This field value should be between 2 to 5 years")
    use_current_address: Optional[StrictBool] = Field(None, alias="useCurrentAddress", description="Flag to check if the address details for the renew card should be taken from the card being renewed or is being given afresh. This flag should only be passed for physical cards. It can take either true or false For virtual cards this flag is null.")
    delivery: Optional[Address] = None
    email: Optional[constr(strict=True, max_length=60, min_length=0)] = Field(None, description="Email Address to be mapped to the renewed card.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="Mobile country code to be mapped to the renewed card, it is two-letter ISO2 country code.")
    mobile: Optional[constr(strict=True)] = Field(None, description="Mobile number to be mapped to the renewed card")
    __properties = ["cardExpiry", "useCurrentAddress", "delivery", "email", "countryCode", "mobile"]

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
    def from_json(cls, json_str: str) -> RenewCardRequest:
        """Create an instance of RenewCardRequest from a JSON string"""
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
    def from_dict(cls, obj: dict) -> RenewCardRequest:
        """Create an instance of RenewCardRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RenewCardRequest.parse_obj(obj)

        _obj = RenewCardRequest.parse_obj({
            "card_expiry": obj.get("cardExpiry"),
            "use_current_address": obj.get("useCurrentAddress"),
            "delivery": Address.from_dict(obj.get("delivery")) if obj.get("delivery") is not None else None,
            "email": obj.get("email"),
            "country_code": obj.get("countryCode"),
            "mobile": obj.get("mobile")
        })
        return _obj


