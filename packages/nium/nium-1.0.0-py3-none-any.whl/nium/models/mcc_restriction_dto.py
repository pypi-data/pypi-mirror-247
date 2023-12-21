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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, validator

class MCCRestrictionDTO(BaseModel):
    """
    MCCRestrictionDTO
    """
    channel_strategy: Optional[StrictStr] = Field(None, alias="channelStrategy", description="This field accepts the two values: WHITE_LIST BLACK_LIST If this field is not passed then the default value will be WHITE_LIST. If the WHITE_LIST is selected along with the Active status, it means mcc whitelisting is active for the provided list.")
    description: StrictStr = Field(..., description="This field accepts the description for enabling or disabling the mcc restriction.")
    merchant_category_codes: conlist(StrictStr) = Field(..., alias="merchantCategoryCodes", description="This array accepts the list of 4-digit mcc codes.")
    status: Optional[StrictStr] = Field(None, description="This field accepts the status and values for this field can be: Active or Inactive. The default value of this field is Active.")
    __properties = ["channelStrategy", "description", "merchantCategoryCodes", "status"]

    @validator('channel_strategy')
    def channel_strategy_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('BLACK_LIST', 'WHITE_LIST'):
            raise ValueError("must be one of enum values ('BLACK_LIST', 'WHITE_LIST')")
        return value

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Active', 'Inactive'):
            raise ValueError("must be one of enum values ('Active', 'Inactive')")
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
    def from_json(cls, json_str: str) -> MCCRestrictionDTO:
        """Create an instance of MCCRestrictionDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> MCCRestrictionDTO:
        """Create an instance of MCCRestrictionDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return MCCRestrictionDTO.parse_obj(obj)

        _obj = MCCRestrictionDTO.parse_obj({
            "channel_strategy": obj.get("channelStrategy"),
            "description": obj.get("description"),
            "merchant_category_codes": obj.get("merchantCategoryCodes"),
            "status": obj.get("status")
        })
        return _obj


