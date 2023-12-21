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

class TransactionChannelResponseDTO(BaseModel):
    """
    TransactionChannelResponseDTO
    """
    channel: Optional[StrictStr] = Field(None, description="This field contains the individual channel name.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status of the individual channel.")
    __properties = ["channel", "status"]

    @validator('channel')
    def channel_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('IN_STORE', 'ONLINE', 'ATM', 'CROSS_BORDER', 'MAG_STRIPE', 'MCC'):
            raise ValueError("must be one of enum values ('IN_STORE', 'ONLINE', 'ATM', 'CROSS_BORDER', 'MAG_STRIPE', 'MCC')")
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
    def from_json(cls, json_str: str) -> TransactionChannelResponseDTO:
        """Create an instance of TransactionChannelResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionChannelResponseDTO:
        """Create an instance of TransactionChannelResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionChannelResponseDTO.parse_obj(obj)

        _obj = TransactionChannelResponseDTO.parse_obj({
            "channel": obj.get("channel"),
            "status": obj.get("status")
        })
        return _obj


