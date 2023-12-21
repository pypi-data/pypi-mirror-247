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
from pydantic import BaseModel, Field, StrictStr

class CustomFeeResponseDTO(BaseModel):
    """
    CustomFeeResponseDTO
    """
    message: Optional[StrictStr] = Field(None, description="This field contains further details regarding the status of the fee.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status such as success if the fee is levied successfully.")
    system_reference_number: Optional[StrictStr] = Field(None, alias="systemReferenceNumber", description="This field contains the unique system reference number.")
    __properties = ["message", "status", "systemReferenceNumber"]

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
    def from_json(cls, json_str: str) -> CustomFeeResponseDTO:
        """Create an instance of CustomFeeResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomFeeResponseDTO:
        """Create an instance of CustomFeeResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomFeeResponseDTO.parse_obj(obj)

        _obj = CustomFeeResponseDTO.parse_obj({
            "message": obj.get("message"),
            "status": obj.get("status"),
            "system_reference_number": obj.get("systemReferenceNumber")
        })
        return _obj


