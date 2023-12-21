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

class UploadRfiDetailsResponseDto(BaseModel):
    """
    UploadRfiDetailsResponseDto
    """
    compliance_id: Optional[StrictStr] = Field(None, alias="complianceId", description="This field contains the unique compliance ID for the customer.")
    rfi_id: Optional[StrictStr] = Field(None, alias="rfiId", description="This field contains the unique RFI ID. This is for future use. Currently, the value shall be null.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status and following are the valid values for compliance status: • IN_PROGRESS • ACTION_REQUIRED • RFI_REQUESTED • RFI_RESPONDED • COMPLETED • REJECT • ERROR In case of successful response to RFI, expected status is RFI_RESPONDED.")
    __properties = ["complianceId", "rfiId", "status"]

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
    def from_json(cls, json_str: str) -> UploadRfiDetailsResponseDto:
        """Create an instance of UploadRfiDetailsResponseDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UploadRfiDetailsResponseDto:
        """Create an instance of UploadRfiDetailsResponseDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UploadRfiDetailsResponseDto.parse_obj(obj)

        _obj = UploadRfiDetailsResponseDto.parse_obj({
            "compliance_id": obj.get("complianceId"),
            "rfi_id": obj.get("rfiId"),
            "status": obj.get("status")
        })
        return _obj


