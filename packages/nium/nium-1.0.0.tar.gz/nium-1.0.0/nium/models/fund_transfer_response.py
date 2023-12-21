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

class FundTransferResponse(BaseModel):
    """
    FundTransferResponse
    """
    message: Optional[StrictStr] = Field(None, description="This field provides the message in case of errors. In case of success, it is null.")
    status: Optional[StrictStr] = Field(None, description="The status value can be Pending or Approved.")
    system_reference_number: Optional[StrictStr] = Field(None, alias="systemReferenceNumber", description="Unique auth code generated for the transaction by the card issuance platform.")
    __properties = ["message", "status", "systemReferenceNumber"]

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('ACTIVE', 'INACTIVE', 'BLOCKED', 'SUSPENDED', 'UPLOADED', 'APPROVED', 'REJECTED', 'FAILED', 'SUCCESS', 'FAILURE', 'PARTIALLY SUCCESS', 'SYNC', 'NOT SYNC', 'PENDING', 'REQUIRES_ACTION', 'CLEAR', 'DECLINED', 'ACCOUNT_BLOCKED', 'AMOUNT_BLOCKED'):
            raise ValueError("must be one of enum values ('ACTIVE', 'INACTIVE', 'BLOCKED', 'SUSPENDED', 'UPLOADED', 'APPROVED', 'REJECTED', 'FAILED', 'SUCCESS', 'FAILURE', 'PARTIALLY SUCCESS', 'SYNC', 'NOT SYNC', 'PENDING', 'REQUIRES_ACTION', 'CLEAR', 'DECLINED', 'ACCOUNT_BLOCKED', 'AMOUNT_BLOCKED')")
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
    def from_json(cls, json_str: str) -> FundTransferResponse:
        """Create an instance of FundTransferResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FundTransferResponse:
        """Create an instance of FundTransferResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FundTransferResponse.parse_obj(obj)

        _obj = FundTransferResponse.parse_obj({
            "message": obj.get("message"),
            "status": obj.get("status"),
            "system_reference_number": obj.get("systemReferenceNumber")
        })
        return _obj


