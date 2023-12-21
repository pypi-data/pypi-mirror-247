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
from pydantic import BaseModel, Field, constr, validator
from nium.models.address import Address

class UpdateContactInfoRequestDTO(BaseModel):
    """
    UpdateContactInfoRequestDTO
    """
    email: Optional[constr(strict=True, max_length=60, min_length=0)] = Field(None, description="Card holder Email")
    country_code: Optional[constr(strict=True, max_length=2, min_length=2)] = Field(None, alias="countryCode", description="Mobile Country Code ISO 2")
    mobile: Optional[constr(strict=True)] = Field(None, description="Card holder mobile number")
    delivery: Optional[Address] = None
    name_on_card: Optional[constr(strict=True)] = Field(None, alias="nameOnCard", description="This field can be used to print the customer name. The value sent in this field will be updated on the card.If this field is left empty, line 1 will not be printed on the card. This field accepts alphanumeric characters along with space(s) The maximum character limit is 26.")
    __properties = ["email", "countryCode", "mobile", "delivery", "nameOnCard"]

    @validator('mobile')
    def mobile_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"\d{0,30}", value):
            raise ValueError(r"must validate the regular expression /\d{0,30}/")
        return value

    @validator('name_on_card')
    def name_on_card_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z\s]{1,26}$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z\s]{1,26}$/")
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
    def from_json(cls, json_str: str) -> UpdateContactInfoRequestDTO:
        """Create an instance of UpdateContactInfoRequestDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> UpdateContactInfoRequestDTO:
        """Create an instance of UpdateContactInfoRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateContactInfoRequestDTO.parse_obj(obj)

        _obj = UpdateContactInfoRequestDTO.parse_obj({
            "email": obj.get("email"),
            "country_code": obj.get("countryCode"),
            "mobile": obj.get("mobile"),
            "delivery": Address.from_dict(obj.get("delivery")) if obj.get("delivery") is not None else None,
            "name_on_card": obj.get("nameOnCard")
        })
        return _obj


