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
from nium.models.address_v2 import AddressV2
from nium.models.business_partner_legal_details import BusinessPartnerLegalDetails

class BusinessPartnerV2(BaseModel):
    """
    BusinessPartnerV2
    """
    business_entity_type: Optional[StrictStr] = Field(None, alias="businessEntityType")
    business_name: Optional[StrictStr] = Field(None, alias="businessName")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber")
    business_type: Optional[StrictStr] = Field(None, alias="businessType")
    legal_details: Optional[BusinessPartnerLegalDetails] = Field(None, alias="legalDetails")
    registered_address: Optional[AddressV2] = Field(None, alias="registeredAddress")
    share_percentage: Optional[StrictStr] = Field(None, alias="sharePercentage")
    __properties = ["businessEntityType", "businessName", "businessRegistrationNumber", "businessType", "legalDetails", "registeredAddress", "sharePercentage"]

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
    def from_json(cls, json_str: str) -> BusinessPartnerV2:
        """Create an instance of BusinessPartnerV2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of legal_details
        if self.legal_details:
            _dict['legalDetails'] = self.legal_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of registered_address
        if self.registered_address:
            _dict['registeredAddress'] = self.registered_address.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BusinessPartnerV2:
        """Create an instance of BusinessPartnerV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BusinessPartnerV2.parse_obj(obj)

        _obj = BusinessPartnerV2.parse_obj({
            "business_entity_type": obj.get("businessEntityType"),
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "business_type": obj.get("businessType"),
            "legal_details": BusinessPartnerLegalDetails.from_dict(obj.get("legalDetails")) if obj.get("legalDetails") is not None else None,
            "registered_address": AddressV2.from_dict(obj.get("registeredAddress")) if obj.get("registeredAddress") is not None else None,
            "share_percentage": obj.get("sharePercentage")
        })
        return _obj


