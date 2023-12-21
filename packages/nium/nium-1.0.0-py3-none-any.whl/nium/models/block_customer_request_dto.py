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

class BlockCustomerRequestDTO(BaseModel):
    """
    BlockCustomerRequestDTO
    """
    action: StrictStr = Field(..., description="This field accepts the action type of block/unblock. The possible values are: • TEMPORARY_BLOCK • PERMANENT_BLOCK • UNBLOCK")
    comment: Optional[StrictStr] = Field(None, description="This field accepts comment which describes the action or reason. Maximum character limit: 255")
    reason: StrictStr = Field(..., description="This field accepts the reason for block/unblock for customer. Following are the valid values with respect to action: => PERMANENT_BLOCK: • CUSTOMER_REQUEST • CLIENT_REQUEST • DECEASED • ACCOUNT_CLOSURE • SUSPICIOUS_ACTIVITY • FRAUDULENT_ACTIVITY • POTENTIAL_SANCTION • SANCTIONED_CUSTOMER • BLACKLISTED_CUSTOMER => TEMPORARY_BLOCK: • CUSTOMER_REQUEST • CLIENT_REQUEST • SUSPICIOUS_ACTIVITY • POTENTIAL_SANCTION => UNBLOCK: • CUSTOMER_REQUEST • CLIENT_REQUEST")
    __properties = ["action", "comment", "reason"]

    @validator('action')
    def action_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('TEMPORARY_BLOCK', 'PERMANENT_BLOCK', 'UNBLOCK'):
            raise ValueError("must be one of enum values ('TEMPORARY_BLOCK', 'PERMANENT_BLOCK', 'UNBLOCK')")
        return value

    @validator('reason')
    def reason_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('CUSTOMER_REQUEST', 'CLIENT_REQUEST', 'DECEASED', 'ACCOUNT_CLOSURE', 'SUSPICIOUS_ACTIVITY', 'FRAUDULENT_ACTIVITY', 'POTENTIAL_SANCTION', 'SANCTIONED_CUSTOMER', 'BLACKLISTED_CUSTOMER', 'NO_OBJECTION'):
            raise ValueError("must be one of enum values ('CUSTOMER_REQUEST', 'CLIENT_REQUEST', 'DECEASED', 'ACCOUNT_CLOSURE', 'SUSPICIOUS_ACTIVITY', 'FRAUDULENT_ACTIVITY', 'POTENTIAL_SANCTION', 'SANCTIONED_CUSTOMER', 'BLACKLISTED_CUSTOMER', 'NO_OBJECTION')")
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
    def from_json(cls, json_str: str) -> BlockCustomerRequestDTO:
        """Create an instance of BlockCustomerRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BlockCustomerRequestDTO:
        """Create an instance of BlockCustomerRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BlockCustomerRequestDTO.parse_obj(obj)

        _obj = BlockCustomerRequestDTO.parse_obj({
            "action": obj.get("action"),
            "comment": obj.get("comment"),
            "reason": obj.get("reason")
        })
        return _obj


