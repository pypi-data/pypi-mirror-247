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

class TermsAndConditionsResponseDTO(BaseModel):
    """
    TermsAndConditionsResponseDTO
    """
    created_at: Optional[StrictStr] = Field(None, alias="createdAt", description="This field contains the date and time of the TnC version creation.")
    description: Optional[StrictStr] = Field(None, description="This field contains the HTML format of the TnC.")
    name: Optional[StrictStr] = Field(None, description="This field contains the name of the TnC to be presented to the customer.")
    version_id: Optional[StrictStr] = Field(None, alias="versionId", description="This field contains the version number of the TnC.")
    __properties = ["createdAt", "description", "name", "versionId"]

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
    def from_json(cls, json_str: str) -> TermsAndConditionsResponseDTO:
        """Create an instance of TermsAndConditionsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TermsAndConditionsResponseDTO:
        """Create an instance of TermsAndConditionsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TermsAndConditionsResponseDTO.parse_obj(obj)

        _obj = TermsAndConditionsResponseDTO.parse_obj({
            "created_at": obj.get("createdAt"),
            "description": obj.get("description"),
            "name": obj.get("name"),
            "version_id": obj.get("versionId")
        })
        return _obj


