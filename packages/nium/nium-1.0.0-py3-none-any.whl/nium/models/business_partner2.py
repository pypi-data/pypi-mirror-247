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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.addresses import Addresses
from nium.models.legal_details import LegalDetails
from nium.models.product_document_detail import ProductDocumentDetail
from nium.models.product_regulatory_details import ProductRegulatoryDetails

class BusinessPartner2(BaseModel):
    """
    BusinessPartner2
    """
    addresses: Optional[Addresses] = None
    business_entity_type: Optional[StrictStr] = Field(None, alias="businessEntityType")
    business_in_other_countries: Optional[conlist(Dict[str, Any])] = Field(None, alias="businessInOtherCountries")
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field accepts the registered business name of the business partner.")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber", description="This field accepts the registered business registration number of the business partner.")
    business_type: Optional[StrictStr] = Field(None, alias="businessType")
    description: Optional[StrictStr] = None
    document_details: Optional[ProductDocumentDetail] = Field(None, alias="documentDetails")
    legal_details: Optional[LegalDetails] = Field(None, alias="legalDetails")
    purpose_code: Optional[StrictStr] = Field(None, alias="purposeCode")
    regulatory_details: Optional[ProductRegulatoryDetails] = Field(None, alias="regulatoryDetails")
    share_percentage: Optional[StrictStr] = Field(None, alias="sharePercentage", description="This field accepts the percentage of shares held by stakeholder.")
    ticker: Optional[StrictStr] = None
    trade_name: Optional[StrictStr] = Field(None, alias="tradeName")
    trustee_name: Optional[StrictStr] = Field(None, alias="trusteeName")
    website: Optional[StrictStr] = None
    __properties = ["addresses", "businessEntityType", "businessInOtherCountries", "businessName", "businessRegistrationNumber", "businessType", "description", "documentDetails", "legalDetails", "purposeCode", "regulatoryDetails", "sharePercentage", "ticker", "tradeName", "trusteeName", "website"]

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
    def from_json(cls, json_str: str) -> BusinessPartner2:
        """Create an instance of BusinessPartner2 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of document_details
        if self.document_details:
            _dict['documentDetails'] = self.document_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of legal_details
        if self.legal_details:
            _dict['legalDetails'] = self.legal_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of regulatory_details
        if self.regulatory_details:
            _dict['regulatoryDetails'] = self.regulatory_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BusinessPartner2:
        """Create an instance of BusinessPartner2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BusinessPartner2.parse_obj(obj)

        _obj = BusinessPartner2.parse_obj({
            "addresses": Addresses.from_dict(obj.get("addresses")) if obj.get("addresses") is not None else None,
            "business_entity_type": obj.get("businessEntityType"),
            "business_in_other_countries": obj.get("businessInOtherCountries"),
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "business_type": obj.get("businessType"),
            "description": obj.get("description"),
            "document_details": ProductDocumentDetail.from_dict(obj.get("documentDetails")) if obj.get("documentDetails") is not None else None,
            "legal_details": LegalDetails.from_dict(obj.get("legalDetails")) if obj.get("legalDetails") is not None else None,
            "purpose_code": obj.get("purposeCode"),
            "regulatory_details": ProductRegulatoryDetails.from_dict(obj.get("regulatoryDetails")) if obj.get("regulatoryDetails") is not None else None,
            "share_percentage": obj.get("sharePercentage"),
            "ticker": obj.get("ticker"),
            "trade_name": obj.get("tradeName"),
            "trustee_name": obj.get("trusteeName"),
            "website": obj.get("website")
        })
        return _obj


