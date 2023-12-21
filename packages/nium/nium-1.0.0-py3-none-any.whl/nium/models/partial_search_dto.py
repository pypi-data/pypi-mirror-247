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
from pydantic import BaseModel, Field, StrictStr, validator

class PartialSearchDTO(BaseModel):
    """
    PartialSearchDTO
    """
    country_code: Optional[StrictStr] = Field(None, description="This field accepts the [2-letter ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for which routing code search is initiated.")
    currency_code: Optional[StrictStr] = Field(None, description="This field accepts the [3-letter ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for which routing code search is to be initiated.")
    payout_method: Optional[StrictStr] = Field(None, description="This field can accept the different modes of payout. This field can accept one of the following values: 1.LOCAL 2.SWIFT Default value of the parameter is LOCAL.")
    routing_code_type: StrictStr = Field(..., description="This field determines the routing code type for the search. The possible values are: IFSC SWIFT ACH CODE BSB CODE SORT CODE BANK CODE LOCATION ID BRANCH CODE BRANCH NAME TRANSIT NUMBER")
    search_key: StrictStr = Field(..., description="This field accepts the key on which the search is initiated. The possible values for search key are: bank_name branch_name")
    search_value: StrictStr = Field(..., description="This field accepts the partial or full value of the search key on which the search is initiated, for example, if search_key is bank_name, search_value could be DBS.")
    __properties = ["country_code", "currency_code", "payout_method", "routing_code_type", "search_key", "search_value"]

    @validator('routing_code_type')
    def routing_code_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('IFSC', 'SWIFT', 'ACH CODE', 'BSB CODE', 'SORT CODE', 'BANK CODE', 'LOCATION ID', 'BRANCH CODE', 'BRANCH NAME', 'TRANSIT NUMBER'):
            raise ValueError("must be one of enum values ('IFSC', 'SWIFT', 'ACH CODE', 'BSB CODE', 'SORT CODE', 'BANK CODE', 'LOCATION ID', 'BRANCH CODE', 'BRANCH NAME', 'TRANSIT NUMBER')")
        return value

    @validator('search_key')
    def search_key_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('bank_name', 'branch_name'):
            raise ValueError("must be one of enum values ('bank_name', 'branch_name')")
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
    def from_json(cls, json_str: str) -> PartialSearchDTO:
        """Create an instance of PartialSearchDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PartialSearchDTO:
        """Create an instance of PartialSearchDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PartialSearchDTO.parse_obj(obj)

        _obj = PartialSearchDTO.parse_obj({
            "country_code": obj.get("country_code"),
            "currency_code": obj.get("currency_code"),
            "payout_method": obj.get("payout_method"),
            "routing_code_type": obj.get("routing_code_type"),
            "search_key": obj.get("search_key"),
            "search_value": obj.get("search_value")
        })
        return _obj


