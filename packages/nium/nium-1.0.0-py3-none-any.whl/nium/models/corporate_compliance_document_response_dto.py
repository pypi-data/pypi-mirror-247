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

class CorporateComplianceDocumentResponseDTO(BaseModel):
    """
    CorporateComplianceDocumentResponseDTO
    """
    case_id: Optional[StrictStr] = Field(None, alias="caseId", description="This field contains the case ID of the corporate customer.")
    client_id: Optional[StrictStr] = Field(None, alias="clientId", description="This field contains the client ID of the corporate customer.")
    remarks: Optional[StrictStr] = Field(None, description="This field contains the uploaded document remarks of the corporate customer.")
    status: Optional[StrictStr] = Field(None, description="This field contains the uploaded document status of the corporate customer.")
    __properties = ["caseId", "clientId", "remarks", "status"]

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
    def from_json(cls, json_str: str) -> CorporateComplianceDocumentResponseDTO:
        """Create an instance of CorporateComplianceDocumentResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateComplianceDocumentResponseDTO:
        """Create an instance of CorporateComplianceDocumentResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateComplianceDocumentResponseDTO.parse_obj(obj)

        _obj = CorporateComplianceDocumentResponseDTO.parse_obj({
            "case_id": obj.get("caseId"),
            "client_id": obj.get("clientId"),
            "remarks": obj.get("remarks"),
            "status": obj.get("status")
        })
        return _obj


