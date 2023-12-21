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
from nium.models.business_partner import BusinessPartner
from nium.models.stakeholder_details import StakeholderDetails

class Stakeholders(BaseModel):
    """
    Stakeholders
    """
    business_partner: Optional[BusinessPartner] = Field(None, alias="businessPartner")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field accepts the unique reference ID for the Individual or Business Stakeholder provided by client.  AU: Optional EU: Optional UK: Optional SG: Optional")
    stakeholder_details: Optional[StakeholderDetails] = Field(None, alias="stakeholderDetails")
    __properties = ["businessPartner", "referenceId", "stakeholderDetails"]

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
    def from_json(cls, json_str: str) -> Stakeholders:
        """Create an instance of Stakeholders from a JSON string"""
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
    def from_dict(cls, obj: dict) -> Stakeholders:
        """Create an instance of Stakeholders from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Stakeholders.parse_obj(obj)

        _obj = Stakeholders.parse_obj({
            "business_partner": BusinessPartner.from_dict(obj.get("businessPartner")) if obj.get("businessPartner") is not None else None,
            "reference_id": obj.get("referenceId"),
            "stakeholder_details": StakeholderDetails.from_dict(obj.get("stakeholderDetails")) if obj.get("stakeholderDetails") is not None else None
        })
        return _obj


