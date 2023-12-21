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



from pydantic import BaseModel, Field, StrictStr, validator

class ChannelActionRequestDTO(BaseModel):
    """
    ChannelActionRequestDTO
    """
    action: StrictStr = Field(..., description="Block or unblock the channel at a card level. Valid values are BLOCK and UNBLOCK. One channel can be blocked at a time.")
    channel: StrictStr = Field(..., description="Channel which needs to be restricted.The valid values are IN_STORE, ONLINE, ATM, CROSS_BORDER, MAG_STRIPE.")
    __properties = ["action", "channel"]

    @validator('action')
    def action_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('BLOCK', 'UNBLOCK'):
            raise ValueError("must be one of enum values ('BLOCK', 'UNBLOCK')")
        return value

    @validator('channel')
    def channel_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('IN_STORE', 'ONLINE', 'ATM', 'CROSS_BORDER', 'MAG_STRIPE'):
            raise ValueError("must be one of enum values ('IN_STORE', 'ONLINE', 'ATM', 'CROSS_BORDER', 'MAG_STRIPE')")
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
    def from_json(cls, json_str: str) -> ChannelActionRequestDTO:
        """Create an instance of ChannelActionRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ChannelActionRequestDTO:
        """Create an instance of ChannelActionRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ChannelActionRequestDTO.parse_obj(obj)

        _obj = ChannelActionRequestDTO.parse_obj({
            "action": obj.get("action"),
            "channel": obj.get("channel")
        })
        return _obj


