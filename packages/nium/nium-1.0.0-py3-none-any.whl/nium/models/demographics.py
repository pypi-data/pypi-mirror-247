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
from pydantic import BaseModel, Field, StrictStr
from nium.models.address import Address

class Demographics(BaseModel):
    """
    Demographic details  # noqa: E501
    """
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field contains the first name of the card holder.")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field contains the middle name of the card holder.")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field contains the last name of the card holder.")
    email: Optional[StrictStr] = Field(None, description="This field contains the email ID of the card holder.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field contains the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for identifying the country prefix to a mobile number.")
    mobile: Optional[StrictStr] = Field(None, description="This field contains the mobile number of the card holder.")
    current_delivery_address: Optional[Address] = Field(None, alias="currentDeliveryAddress")
    __properties = ["firstName", "middleName", "lastName", "email", "countryCode", "mobile", "currentDeliveryAddress"]

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
    def from_json(cls, json_str: str) -> Demographics:
        """Create an instance of Demographics from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of current_delivery_address
        if self.current_delivery_address:
            _dict['currentDeliveryAddress'] = self.current_delivery_address.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Demographics:
        """Create an instance of Demographics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Demographics.parse_obj(obj)

        _obj = Demographics.parse_obj({
            "first_name": obj.get("firstName"),
            "middle_name": obj.get("middleName"),
            "last_name": obj.get("lastName"),
            "email": obj.get("email"),
            "country_code": obj.get("countryCode"),
            "mobile": obj.get("mobile"),
            "current_delivery_address": Address.from_dict(obj.get("currentDeliveryAddress")) if obj.get("currentDeliveryAddress") is not None else None
        })
        return _obj


