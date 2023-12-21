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
from nium.models.corporate_business_partner import CorporateBusinessPartner
from nium.models.corporate_stakeholder_details import CorporateStakeholderDetails

class CorporateStakeholders(BaseModel):
    """
    CorporateStakeholders
    """
    business_partner: Optional[CorporateBusinessPartner] = Field(None, alias="businessPartner")
    entity_type: Optional[StrictStr] = Field(None, alias="entityType")
    stakeholder_details: Optional[CorporateStakeholderDetails] = Field(None, alias="stakeholderDetails")
    __properties = ["businessPartner", "entityType", "stakeholderDetails"]

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
    def from_json(cls, json_str: str) -> CorporateStakeholders:
        """Create an instance of CorporateStakeholders from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of business_partner
        if self.business_partner:
            _dict['businessPartner'] = self.business_partner.to_dict()
        # override the default output from pydantic by calling `to_dict()` of stakeholder_details
        if self.stakeholder_details:
            _dict['stakeholderDetails'] = self.stakeholder_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateStakeholders:
        """Create an instance of CorporateStakeholders from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateStakeholders.parse_obj(obj)

        _obj = CorporateStakeholders.parse_obj({
            "business_partner": CorporateBusinessPartner.from_dict(obj.get("businessPartner")) if obj.get("businessPartner") is not None else None,
            "entity_type": obj.get("entityType"),
            "stakeholder_details": CorporateStakeholderDetails.from_dict(obj.get("stakeholderDetails")) if obj.get("stakeholderDetails") is not None else None
        })
        return _obj


