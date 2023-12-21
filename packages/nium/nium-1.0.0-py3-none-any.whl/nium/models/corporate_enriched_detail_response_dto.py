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
from pydantic import BaseModel, Field
from nium.models.corporate_business_details import CorporateBusinessDetails
from nium.models.corporate_risk_assessment_info import CorporateRiskAssessmentInfo

class CorporateEnrichedDetailResponseDTO(BaseModel):
    """
    CorporateEnrichedDetailResponseDTO
    """
    business_details: Optional[CorporateBusinessDetails] = Field(None, alias="businessDetails")
    risk_assessment_info: Optional[CorporateRiskAssessmentInfo] = Field(None, alias="riskAssessmentInfo")
    __properties = ["businessDetails", "riskAssessmentInfo"]

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
    def from_json(cls, json_str: str) -> CorporateEnrichedDetailResponseDTO:
        """Create an instance of CorporateEnrichedDetailResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of business_details
        if self.business_details:
            _dict['businessDetails'] = self.business_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of risk_assessment_info
        if self.risk_assessment_info:
            _dict['riskAssessmentInfo'] = self.risk_assessment_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateEnrichedDetailResponseDTO:
        """Create an instance of CorporateEnrichedDetailResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateEnrichedDetailResponseDTO.parse_obj(obj)

        _obj = CorporateEnrichedDetailResponseDTO.parse_obj({
            "business_details": CorporateBusinessDetails.from_dict(obj.get("businessDetails")) if obj.get("businessDetails") is not None else None,
            "risk_assessment_info": CorporateRiskAssessmentInfo.from_dict(obj.get("riskAssessmentInfo")) if obj.get("riskAssessmentInfo") is not None else None
        })
        return _obj


