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

class OOBCallbackResponseDTO(BaseModel):
    """
    OOBCallbackResponseDTO
    """
    status: Optional[StrictStr] = None
    __properties = ["status"]

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('ACTIVE', 'INACTIVE', 'BLOCKED', 'P_BLOCK', 'SUSPEND', 'PENDING', 'APPROVED', 'REJECTED', 'UPLOADED', 'REVIEWED', 'FAILED', 'SUCCESS', 'ASSIGNED', 'UNASSIGNED', 'TEMP_BLOCK', 'All', 'ARCHIVED', 'VIRTUAL_ACTIVE', 'CLOSED', 'RENEWED', 'DAMAGED', 'DO_NOT_HONOUR', 'LOST_CARD', 'REFER_TO_ISSUER', 'CARD_PIN_BLOCKED', 'CARD_VOIDED', 'CARD_DESTROYED', 'STOLEN_CARD', 'CARD_EXPIRED', 'FRAUD', 'TEMP_BLOCK'):
            raise ValueError("must be one of enum values ('ACTIVE', 'INACTIVE', 'BLOCKED', 'P_BLOCK', 'SUSPEND', 'PENDING', 'APPROVED', 'REJECTED', 'UPLOADED', 'REVIEWED', 'FAILED', 'SUCCESS', 'ASSIGNED', 'UNASSIGNED', 'TEMP_BLOCK', 'All', 'ARCHIVED', 'VIRTUAL_ACTIVE', 'CLOSED', 'RENEWED', 'DAMAGED', 'DO_NOT_HONOUR', 'LOST_CARD', 'REFER_TO_ISSUER', 'CARD_PIN_BLOCKED', 'CARD_VOIDED', 'CARD_DESTROYED', 'STOLEN_CARD', 'CARD_EXPIRED', 'FRAUD', 'TEMP_BLOCK')")
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
    def from_json(cls, json_str: str) -> OOBCallbackResponseDTO:
        """Create an instance of OOBCallbackResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OOBCallbackResponseDTO:
        """Create an instance of OOBCallbackResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OOBCallbackResponseDTO.parse_obj(obj)

        _obj = OOBCallbackResponseDTO.parse_obj({
            "status": obj.get("status")
        })
        return _obj


