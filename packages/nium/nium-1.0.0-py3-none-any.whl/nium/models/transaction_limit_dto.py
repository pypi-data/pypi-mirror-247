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

from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, validator

class TransactionLimitDTO(BaseModel):
    """
    TransactionLimitDTO
    """
    additional_percentage: Union[StrictFloat, StrictInt] = Field(..., alias="additionalPercentage", description="This field contains the threshold percentage which is calculated on the value as a threshold or margin which is to be allowed for authorization when a transaction exceeds the specified limits. The format is Decimal(3,4).")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the timestamp of limit generation.")
    masked_card_number: Optional[StrictStr] = Field(None, alias="maskedCardNumber", description="This is the 16-digit masked card number in format 1234-56xx-xxxx-3456.")
    status: StrictStr = Field(..., description="This field defines whether a particular limit is active or not. It can accept one of the two values: Active or Inactive.")
    type: StrictStr = Field(..., description="This field accepts the limit type to be set. It can take the following values: PER_TRANSACTION_AMOUNT_LIMIT DAILY_AMOUNT_LIMIT MONTHLY_AMOUNT_LIMIT LIFETIME_AMOUNT_LIMIT LIFETIME_COUNT_LIMIT TRANSACTION_DURATION_LIMIT")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="This field contains the timestamp of limit updation.")
    value: StrictStr = Field(..., description="This field accepts the values for each card-level limits. It accepts a date range in the yyyymmdd-yyyymmdd format and UTC +00 time zone as a string when type is TRANSACTION_DURATION_LIMIT. Otherwise, it accepts the limit value.")
    __properties = ["additionalPercentage", "createdAt", "maskedCardNumber", "status", "type", "updatedAt", "value"]

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Active', 'Inactive'):
            raise ValueError("must be one of enum values ('Active', 'Inactive')")
        return value

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('PER_TRANSACTION_AMOUNT_LIMIT', 'DAILY_AMOUNT_LIMIT', 'MONTHLY_AMOUNT_LIMIT', 'LIFETIME_AMOUNT_LIMIT', 'LIFETIME_COUNT_LIMIT', 'TRANSACTION_DURATION_LIMIT'):
            raise ValueError("must be one of enum values ('PER_TRANSACTION_AMOUNT_LIMIT', 'DAILY_AMOUNT_LIMIT', 'MONTHLY_AMOUNT_LIMIT', 'LIFETIME_AMOUNT_LIMIT', 'LIFETIME_COUNT_LIMIT', 'TRANSACTION_DURATION_LIMIT')")
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
    def from_json(cls, json_str: str) -> TransactionLimitDTO:
        """Create an instance of TransactionLimitDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionLimitDTO:
        """Create an instance of TransactionLimitDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionLimitDTO.parse_obj(obj)

        _obj = TransactionLimitDTO.parse_obj({
            "additional_percentage": obj.get("additionalPercentage"),
            "created_at": obj.get("createdAt"),
            "masked_card_number": obj.get("maskedCardNumber"),
            "status": obj.get("status"),
            "type": obj.get("type"),
            "updated_at": obj.get("updatedAt"),
            "value": obj.get("value")
        })
        return _obj


