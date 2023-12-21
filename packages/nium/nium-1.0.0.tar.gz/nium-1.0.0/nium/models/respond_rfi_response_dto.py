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

class RespondRfiResponseDTO(BaseModel):
    """
    RespondRfiResponseDTO
    """
    case_id: Optional[StrictStr] = Field(None, alias="caseId", description="This field contains the compliance case Id of the customer.")
    client_id: Optional[StrictStr] = Field(None, alias="clientId", description="This field contains the NIUM client Id of the customer.")
    status: Optional[StrictStr] = Field(None, description="This field contains the compliance status of the corporate customer after the RFI is responded. On successful response to RFI, possible value is RFI_RESPONDED.")
    __properties = ["caseId", "clientId", "status"]

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
    def from_json(cls, json_str: str) -> RespondRfiResponseDTO:
        """Create an instance of RespondRfiResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RespondRfiResponseDTO:
        """Create an instance of RespondRfiResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RespondRfiResponseDTO.parse_obj(obj)

        _obj = RespondRfiResponseDTO.parse_obj({
            "case_id": obj.get("caseId"),
            "client_id": obj.get("clientId"),
            "status": obj.get("status")
        })
        return _obj


