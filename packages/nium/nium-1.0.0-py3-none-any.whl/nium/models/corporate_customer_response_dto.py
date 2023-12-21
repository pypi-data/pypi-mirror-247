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
from nium.models.business_details_response_v2_dto import BusinessDetailsResponseV2DTO
from nium.models.risk_assessment_info_v2 import RiskAssessmentInfoV2

class CorporateCustomerResponseDTO(BaseModel):
    """
    CorporateCustomerResponseDTO
    """
    business_details: Optional[BusinessDetailsResponseV2DTO] = Field(None, alias="businessDetails")
    case_id: Optional[StrictStr] = Field(None, alias="caseId")
    client_id: Optional[StrictStr] = Field(None, alias="clientId", description="This field accepts the NIUM client Id of the customer. This field should be provided only while performing the re-initiate KYB process.  AU: Optional EU: Optional UK: Optional SG: Optional")
    compliance_region: Optional[StrictStr] = Field(None, alias="complianceRegion", description="This field accepts the region code for which onboarding has been triggered. The acceptable value are: AU EU UK SG  AU: Required EU: Required UK: Required SG: Required")
    risk_assessment_info: Optional[RiskAssessmentInfoV2] = Field(None, alias="riskAssessmentInfo")
    __properties = ["businessDetails", "caseId", "clientId", "complianceRegion", "riskAssessmentInfo"]

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
    def from_json(cls, json_str: str) -> CorporateCustomerResponseDTO:
        """Create an instance of CorporateCustomerResponseDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> CorporateCustomerResponseDTO:
        """Create an instance of CorporateCustomerResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateCustomerResponseDTO.parse_obj(obj)

        _obj = CorporateCustomerResponseDTO.parse_obj({
            "business_details": BusinessDetailsResponseV2DTO.from_dict(obj.get("businessDetails")) if obj.get("businessDetails") is not None else None,
            "case_id": obj.get("caseId"),
            "client_id": obj.get("clientId"),
            "compliance_region": obj.get("complianceRegion"),
            "risk_assessment_info": RiskAssessmentInfoV2.from_dict(obj.get("riskAssessmentInfo")) if obj.get("riskAssessmentInfo") is not None else None
        })
        return _obj


