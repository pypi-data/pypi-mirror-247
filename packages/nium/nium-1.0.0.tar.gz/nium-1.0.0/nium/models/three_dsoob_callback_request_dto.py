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

class ThreeDSOOBCallbackRequestDTO(BaseModel):
    """
    ThreeDSOOBCallbackRequestDTO
    """
    auth_transaction_id: StrictStr = Field(..., alias="authTransactionId")
    reference_number: StrictStr = Field(..., alias="referenceNumber")
    status_code: StrictStr = Field(..., alias="statusCode")
    status: Optional[StrictStr] = None
    __properties = ["authTransactionId", "referenceNumber", "statusCode", "status"]

    @validator('status_code')
    def status_code_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('SSS000', 'VCL001', 'VCL002', 'VCU001', 'VCU601', 'VCU602', 'VCU603', 'VCU701', 'VWA001', 'VCF001', 'VCT001', 'VCD001', 'VII001', 'VII002', 'UAS001', 'ISE999'):
            raise ValueError("must be one of enum values ('SSS000', 'VCL001', 'VCL002', 'VCU001', 'VCU601', 'VCU602', 'VCU603', 'VCU701', 'VWA001', 'VCF001', 'VCT001', 'VCD001', 'VII001', 'VII002', 'UAS001', 'ISE999')")
        return value

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
    def from_json(cls, json_str: str) -> ThreeDSOOBCallbackRequestDTO:
        """Create an instance of ThreeDSOOBCallbackRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ThreeDSOOBCallbackRequestDTO:
        """Create an instance of ThreeDSOOBCallbackRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ThreeDSOOBCallbackRequestDTO.parse_obj(obj)

        _obj = ThreeDSOOBCallbackRequestDTO.parse_obj({
            "auth_transaction_id": obj.get("authTransactionId"),
            "reference_number": obj.get("referenceNumber"),
            "status_code": obj.get("statusCode"),
            "status": obj.get("status")
        })
        return _obj


