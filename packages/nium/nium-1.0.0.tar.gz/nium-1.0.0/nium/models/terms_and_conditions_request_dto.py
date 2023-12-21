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



from pydantic import BaseModel, Field, StrictBool, StrictStr

class TermsAndConditionsRequestDTO(BaseModel):
    """
    TermsAndConditionsRequestDTO
    """
    accept: StrictBool = Field(..., description="This flag specifies if the customer has accepted or rejected the Terms and Conditions.")
    name: StrictStr = Field(..., description="This is the name of the TnC for which the accept flag is being sent.")
    version_id: StrictStr = Field(..., alias="versionId", description="This is the version of the TnC for which the accept flag is being sent.")
    __properties = ["accept", "name", "versionId"]

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
    def from_json(cls, json_str: str) -> TermsAndConditionsRequestDTO:
        """Create an instance of TermsAndConditionsRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TermsAndConditionsRequestDTO:
        """Create an instance of TermsAndConditionsRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TermsAndConditionsRequestDTO.parse_obj(obj)

        _obj = TermsAndConditionsRequestDTO.parse_obj({
            "accept": obj.get("accept"),
            "name": obj.get("name"),
            "version_id": obj.get("versionId")
        })
        return _obj


