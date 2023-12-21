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


from typing import Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.corporate_addresses import CorporateAddresses
from nium.models.corporate_legal_details import CorporateLegalDetails
from nium.models.corporate_stakeholders import CorporateStakeholders

class CorporateBusinessDetails(BaseModel):
    """
    CorporateBusinessDetails
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo", description="This object accepts additional information about the business.  AU: Optional EU: Optional UK: Optional SG: Optional")
    addresses: Optional[CorporateAddresses] = None
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field contains the name of a business.  AU: Required EU: Required UK: Required SG: Required")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber", description="This field accepts the business registration number of the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    legal_details: Optional[CorporateLegalDetails] = Field(None, alias="legalDetails")
    stakeholders: Optional[conlist(CorporateStakeholders)] = Field(None, description="This array accepts the stakeholder details for the new corporate entity to be onboarded. This field is required in case the region is AU and entity type [refer businessDetails.businessType] is one of the following: Sole Trader Unregulated Trust Partnerships Government Body Association  AU: Required EU: Required UK: Required SG: Required")
    website: Optional[StrictStr] = Field(None, description="This field accepts the business website link of the new corporate entity to be onboarded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    __properties = ["additionalInfo", "addresses", "businessName", "businessRegistrationNumber", "legalDetails", "stakeholders", "website"]

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
    def from_json(cls, json_str: str) -> CorporateBusinessDetails:
        """Create an instance of CorporateBusinessDetails from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in stakeholders (list)
        _items = []
        if self.stakeholders:
            for _item in self.stakeholders:
                if _item:
                    _items.append(_item.to_dict())
            _dict['stakeholders'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateBusinessDetails:
        """Create an instance of CorporateBusinessDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateBusinessDetails.parse_obj(obj)

        _obj = CorporateBusinessDetails.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "addresses": CorporateAddresses.from_dict(obj.get("addresses")) if obj.get("addresses") is not None else None,
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "legal_details": CorporateLegalDetails.from_dict(obj.get("legalDetails")) if obj.get("legalDetails") is not None else None,
            "stakeholders": [CorporateStakeholders.from_dict(_item) for _item in obj.get("stakeholders")] if obj.get("stakeholders") is not None else None,
            "website": obj.get("website")
        })
        return _obj


