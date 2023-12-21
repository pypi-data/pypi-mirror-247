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
from nium.models.business_details2 import BusinessDetails2
from nium.models.risk_assessment_info import RiskAssessmentInfo

class ProductRfiResponseRequest(BaseModel):
    """
    ProductRfiResponseRequest
    """
    business_info: Optional[BusinessDetails2] = Field(None, alias="businessInfo")
    rfi_template_id: Optional[StrictStr] = Field(None, alias="rfiTemplateId", description="This field accepts the RFI template ID as received in [Fetch Corporate Customer RFI Details](https://docs.nium.com/baas/fetch-corporate-customer-rfi-details) API.")
    risk_assessment_info: Optional[RiskAssessmentInfo] = Field(None, alias="riskAssessmentInfo")
    __properties = ["businessInfo", "rfiTemplateId", "riskAssessmentInfo"]

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
    def from_json(cls, json_str: str) -> ProductRfiResponseRequest:
        """Create an instance of ProductRfiResponseRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of business_info
        if self.business_info:
            _dict['businessInfo'] = self.business_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of risk_assessment_info
        if self.risk_assessment_info:
            _dict['riskAssessmentInfo'] = self.risk_assessment_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductRfiResponseRequest:
        """Create an instance of ProductRfiResponseRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductRfiResponseRequest.parse_obj(obj)

        _obj = ProductRfiResponseRequest.parse_obj({
            "business_info": BusinessDetails2.from_dict(obj.get("businessInfo")) if obj.get("businessInfo") is not None else None,
            "rfi_template_id": obj.get("rfiTemplateId"),
            "risk_assessment_info": RiskAssessmentInfo.from_dict(obj.get("riskAssessmentInfo")) if obj.get("riskAssessmentInfo") is not None else None
        })
        return _obj


