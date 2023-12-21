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
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, validator
from nium.models.fee_response_dto import FeeResponseDTO

class ClientFeeDetailsResponseDTO(BaseModel):
    """
    ClientFeeDetailsResponseDTO
    """
    default: Optional[StrictBool] = None
    fees: Optional[conlist(FeeResponseDTO)] = Field(None, description="This is an array which contains the fees details.")
    segment: Optional[StrictStr] = Field(None, description="This field contains the fee segment associated with a client.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status and the possible values are: Active Inactive")
    __properties = ["default", "fees", "segment", "status"]

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
    def from_json(cls, json_str: str) -> ClientFeeDetailsResponseDTO:
        """Create an instance of ClientFeeDetailsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in fees (list)
        _items = []
        if self.fees:
            for _item in self.fees:
                if _item:
                    _items.append(_item.to_dict())
            _dict['fees'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ClientFeeDetailsResponseDTO:
        """Create an instance of ClientFeeDetailsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ClientFeeDetailsResponseDTO.parse_obj(obj)

        _obj = ClientFeeDetailsResponseDTO.parse_obj({
            "default": obj.get("default"),
            "fees": [FeeResponseDTO.from_dict(_item) for _item in obj.get("fees")] if obj.get("fees") is not None else None,
            "segment": obj.get("segment"),
            "status": obj.get("status")
        })
        return _obj


