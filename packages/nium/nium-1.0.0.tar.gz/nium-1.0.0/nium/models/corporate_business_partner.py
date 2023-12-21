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
from nium.models.business_partner_addresses import BusinessPartnerAddresses
from nium.models.corporate_business_partner_legal_details import CorporateBusinessPartnerLegalDetails

class CorporateBusinessPartner(BaseModel):
    """
    CorporateBusinessPartner
    """
    addresses: Optional[BusinessPartnerAddresses] = None
    business_entity_type: Optional[StrictStr] = Field(None, alias="businessEntityType", description="This field accepts the entity type of the business partner. The acceptable values are: Director Ultimate Beneficial Owner Shareholder Authorized Signatory Authorized Representative Protector Partner Trustee Settlor Members Executor  AU: Optional EU: Optional UK: Optional SG: Optional")
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field accepts the registered business name of the business partner. This is required when the stakeholder(s) is a business entity  AU: Optional EU: Conditional UK: Optional SG: Optional")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber", description="This field accepts the registered business registration number of the business partner. This is required when the stakeholder(s) is a business entity  AU: Optional EU: Conditional UK: Optional SG: Optional")
    legal_details: Optional[CorporateBusinessPartnerLegalDetails] = Field(None, alias="legalDetails")
    __properties = ["addresses", "businessEntityType", "businessName", "businessRegistrationNumber", "legalDetails"]

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
    def from_json(cls, json_str: str) -> CorporateBusinessPartner:
        """Create an instance of CorporateBusinessPartner from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of addresses
        if self.addresses:
            _dict['addresses'] = self.addresses.to_dict()
        # override the default output from pydantic by calling `to_dict()` of legal_details
        if self.legal_details:
            _dict['legalDetails'] = self.legal_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateBusinessPartner:
        """Create an instance of CorporateBusinessPartner from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateBusinessPartner.parse_obj(obj)

        _obj = CorporateBusinessPartner.parse_obj({
            "addresses": BusinessPartnerAddresses.from_dict(obj.get("addresses")) if obj.get("addresses") is not None else None,
            "business_entity_type": obj.get("businessEntityType"),
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "legal_details": CorporateBusinessPartnerLegalDetails.from_dict(obj.get("legalDetails")) if obj.get("legalDetails") is not None else None
        })
        return _obj


