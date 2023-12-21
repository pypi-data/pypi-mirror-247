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
from pydantic import BaseModel, StrictStr, validator

class TypedErrorErrorCodes(BaseModel):
    """
    TypedErrorErrorCodes
    """
    code: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    field: Optional[StrictStr] = None
    __properties = ["code", "description", "field"]

    @validator('code')
    def code_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INVALID_CLIENT_HASH_ID', 'INVALID_CUSTOMER_HASH_ID', 'INVALID_WALLET_HASH_ID', 'INVALID_CARD_HASH_ID', 'CARD_IS_PERMANENTLY_BLOCKED', 'CARD_EXPIRED', 'VALIDATION_ERROR', 'UNAUTHORIZED', 'FORBIDDEN', 'BAD_REQUEST'):
            raise ValueError("must be one of enum values ('INVALID_CLIENT_HASH_ID', 'INVALID_CUSTOMER_HASH_ID', 'INVALID_WALLET_HASH_ID', 'INVALID_CARD_HASH_ID', 'CARD_IS_PERMANENTLY_BLOCKED', 'CARD_EXPIRED', 'VALIDATION_ERROR', 'UNAUTHORIZED', 'FORBIDDEN', 'BAD_REQUEST')")
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
    def from_json(cls, json_str: str) -> TypedErrorErrorCodes:
        """Create an instance of TypedErrorErrorCodes from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TypedErrorErrorCodes:
        """Create an instance of TypedErrorErrorCodes from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TypedErrorErrorCodes.parse_obj(obj)

        _obj = TypedErrorErrorCodes.parse_obj({
            "code": obj.get("code"),
            "description": obj.get("description"),
            "field": obj.get("field")
        })
        return _obj


