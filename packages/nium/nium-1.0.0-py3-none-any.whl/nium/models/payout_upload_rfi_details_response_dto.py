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

class PayoutUploadRfiDetailsResponseDTO(BaseModel):
    """
    PayoutUploadRfiDetailsResponseDTO
    """
    compliance_id: Optional[StrictStr] = Field(None, alias="complianceId")
    remarks: Optional[StrictStr] = None
    status: Optional[StrictStr] = None
    __properties = ["complianceId", "remarks", "status"]

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
    def from_json(cls, json_str: str) -> PayoutUploadRfiDetailsResponseDTO:
        """Create an instance of PayoutUploadRfiDetailsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PayoutUploadRfiDetailsResponseDTO:
        """Create an instance of PayoutUploadRfiDetailsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PayoutUploadRfiDetailsResponseDTO.parse_obj(obj)

        _obj = PayoutUploadRfiDetailsResponseDTO.parse_obj({
            "compliance_id": obj.get("complianceId"),
            "remarks": obj.get("remarks"),
            "status": obj.get("status")
        })
        return _obj


