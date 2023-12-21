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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class CustomerDataExternalRequestDTO(BaseModel):
    """
    CustomerDataExternalRequestDTO
    """
    country_code: StrictStr = Field(..., alias="countryCode", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country prefix code to the customer’s mobile number.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field accepts the previously generated unique customer identifier of customer.")
    email: StrictStr = Field(..., description="This field accepts the unique email address of the customer. Maximum character limit: 60")
    mobile: StrictStr = Field(..., description="This field accepts the mobile number of the customer without the country prefix code. Maximum character limit: 20")
    native_language_name: Optional[StrictStr] = Field(None, alias="nativeLanguageName", description="This field accepts the customer's name in native language. Maximum character limit: 40")
    segment: Optional[StrictStr] = Field(None, description="This field accepts the fee segment associated with a client. Maximum character limit: 64")
    upgrade_request: Optional[StrictBool] = Field(None, alias="upgradeRequest")
    __properties = ["countryCode", "customerHashId", "email", "mobile", "nativeLanguageName", "segment", "upgradeRequest"]

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
    def from_json(cls, json_str: str) -> CustomerDataExternalRequestDTO:
        """Create an instance of CustomerDataExternalRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerDataExternalRequestDTO:
        """Create an instance of CustomerDataExternalRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerDataExternalRequestDTO.parse_obj(obj)

        _obj = CustomerDataExternalRequestDTO.parse_obj({
            "country_code": obj.get("countryCode"),
            "customer_hash_id": obj.get("customerHashId"),
            "email": obj.get("email"),
            "mobile": obj.get("mobile"),
            "native_language_name": obj.get("nativeLanguageName"),
            "segment": obj.get("segment"),
            "upgrade_request": obj.get("upgradeRequest")
        })
        return _obj


