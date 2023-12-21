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

class BankRoutingInfo(BaseModel):
    """
    BankRoutingInfo
    """
    type: Optional[StrictStr] = Field(None, description="This field accepts the routing code type.")
    value: Optional[StrictStr] = Field(None, description="This field accepts the routing code value 1.  for example  ADCBINBB or ADCBINBB123 for SWIFT,  SBIN0000058 for IFSC,  100000 for SORT CODE,  111000025 for ACH CODE,  012515 for BSB CODE,  151 for BANK CODE.")
    __properties = ["type", "value"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('IFSC', 'SWIFT', 'ACH_CODE', 'BSB_CODE', 'SORT_CODE', 'BANK_CODE', 'LOCATION_ID', 'BRANCH_CODE', 'TRANSIT_NUMBER', 'BRANCH_NAME', 'CNAPS', 'WALLET'):
            raise ValueError("must be one of enum values ('IFSC', 'SWIFT', 'ACH_CODE', 'BSB_CODE', 'SORT_CODE', 'BANK_CODE', 'LOCATION_ID', 'BRANCH_CODE', 'TRANSIT_NUMBER', 'BRANCH_NAME', 'CNAPS', 'WALLET')")
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
    def from_json(cls, json_str: str) -> BankRoutingInfo:
        """Create an instance of BankRoutingInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BankRoutingInfo:
        """Create an instance of BankRoutingInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BankRoutingInfo.parse_obj(obj)

        _obj = BankRoutingInfo.parse_obj({
            "type": obj.get("type"),
            "value": obj.get("value")
        })
        return _obj


