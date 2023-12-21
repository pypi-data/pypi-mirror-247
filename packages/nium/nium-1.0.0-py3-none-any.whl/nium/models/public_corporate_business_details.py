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
from nium.models.corporate_addresses import CorporateAddresses

class PublicCorporateBusinessDetails(BaseModel):
    """
    PublicCorporateBusinessDetails
    """
    addresses: Optional[CorporateAddresses] = None
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field contains the name of a business.  AU: Required EU: Required UK: Required SG: Required")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber", description="This field accepts the business registration number of the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    business_type: Optional[StrictStr] = Field(None, alias="businessType", description="This field accepts the legal entity type of the business. The supported entity types are: Sole Trader  Private Limited Company Public Company Partnership Limited Liability Partnership Firm Government Body Associations Trust Regulated Trust Unregulated Trust  AU: Required EU: Required UK: Required SG: Required")
    search_reference_id: Optional[StrictStr] = Field(None, alias="searchReferenceId")
    website: Optional[StrictStr] = Field(None, description="This field accepts the business website link of the new corporate entity to be onboarded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    __properties = ["addresses", "businessName", "businessRegistrationNumber", "businessType", "searchReferenceId", "website"]

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
    def from_json(cls, json_str: str) -> PublicCorporateBusinessDetails:
        """Create an instance of PublicCorporateBusinessDetails from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PublicCorporateBusinessDetails:
        """Create an instance of PublicCorporateBusinessDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PublicCorporateBusinessDetails.parse_obj(obj)

        _obj = PublicCorporateBusinessDetails.parse_obj({
            "addresses": CorporateAddresses.from_dict(obj.get("addresses")) if obj.get("addresses") is not None else None,
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "business_type": obj.get("businessType"),
            "search_reference_id": obj.get("searchReferenceId"),
            "website": obj.get("website")
        })
        return _obj


