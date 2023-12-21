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

class CorporateRiskAssessmentInfo(BaseModel):
    """
    CorporateRiskAssessmentInfo
    """
    annual_turnover: Optional[StrictStr] = Field(None, alias="annualTurnover", description="This field accepts the annual turnover for the corporate entity to be onboarded. Please refer to the [Glossary of Annual Turnover](https://docs.nium.com/baas/onboard-corporate-customer#glossary-of-annual-turnover): for the applicable values  AU: Required EU: Required UK: Required SG: Required")
    total_employees: Optional[StrictStr] = Field(None, alias="totalEmployees", description="This field accepts the total number of employees for the corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    __properties = ["annualTurnover", "totalEmployees"]

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
    def from_json(cls, json_str: str) -> CorporateRiskAssessmentInfo:
        """Create an instance of CorporateRiskAssessmentInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateRiskAssessmentInfo:
        """Create an instance of CorporateRiskAssessmentInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateRiskAssessmentInfo.parse_obj(obj)

        _obj = CorporateRiskAssessmentInfo.parse_obj({
            "annual_turnover": obj.get("annualTurnover"),
            "total_employees": obj.get("totalEmployees")
        })
        return _obj


