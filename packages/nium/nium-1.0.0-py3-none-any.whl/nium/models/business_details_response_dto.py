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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.association_details import AssociationDetails
from nium.models.corporate_address_dto import CorporateAddressDTO
from nium.models.corporate_document_details_dto import CorporateDocumentDetailsDTO
from nium.models.partnership_details import PartnershipDetails
from nium.models.regulatory_details import RegulatoryDetails
from nium.models.tax_details import TaxDetails

class BusinessDetailsResponseDTO(BaseModel):
    """
    BusinessDetailsResponseDTO
    """
    association_detail: Optional[AssociationDetails] = Field(None, alias="associationDetail")
    business_address: Optional[CorporateAddressDTO] = Field(None, alias="businessAddress")
    business_extract_covered_stakeholder: Optional[StrictStr] = Field(None, alias="businessExtractCoveredStakeholder", description="This field contains business extract covered stakeholder which specifies if the business extract document given covers the stakeholder details. The value for this field can be either Yes or No.")
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field contains the business name of the entity.")
    business_registration_number: Optional[StrictStr] = Field(None, alias="businessRegistrationNumber", description="This field contains the business registration number of the entity.")
    business_registration_type: Optional[StrictStr] = Field(None, alias="businessRegistrationType", description="This field contains the business registration number type.")
    business_type: Optional[StrictStr] = Field(None, alias="businessType", description="This field contains the legal entity type of the business.")
    case_id: Optional[StrictStr] = Field(None, alias="caseId", description="This field contains the case ID of the corporate customer.")
    client_id: Optional[StrictStr] = Field(None, alias="clientId", description="This field contains the client ID of the corporate customer.")
    compliance_region: Optional[StrictStr] = Field(None, alias="complianceRegion", description="This field contains the compliance region of the customer.")
    description: Optional[StrictStr] = Field(None, description="This field contains the  description of the business details")
    document_details: Optional[conlist(CorporateDocumentDetailsDTO)] = Field(None, alias="documentDetails", description="This is an array which contains the document details.")
    former_name: Optional[StrictStr] = Field(None, alias="formerName", description="This field contains the former name.")
    legislation_name: Optional[StrictStr] = Field(None, alias="legislationName", description="This field contains the name of the legislation under which the corporate entity being onboarded was formed.")
    legislation_type: Optional[StrictStr] = Field(None, alias="legislationType", description="This field contains the type of the legislation under which the corporate entity being onboarded was formed. The possible values are:  Established under Commonwealth legislation Established under State Territory legislation Other")
    listed_exchange: Optional[StrictStr] = Field(None, alias="listedExchange", description="This field contains the exchange where the company got listed.")
    partnership_details: Optional[PartnershipDetails] = Field(None, alias="partnershipDetails")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field contains the  reference id of the entity")
    registered_address: Optional[CorporateAddressDTO] = Field(None, alias="registeredAddress")
    registered_country: Optional[StrictStr] = Field(None, alias="registeredCountry", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) where business is registered.")
    registered_date: Optional[StrictStr] = Field(None, alias="registeredDate", description="This field contains the business registration date.")
    regulatory_details: Optional[RegulatoryDetails] = Field(None, alias="regulatoryDetails")
    settlor_name: Optional[StrictStr] = Field(None, alias="settlorName")
    stock_symbol: Optional[StrictStr] = Field(None, alias="stockSymbol")
    tax_details: Optional[conlist(TaxDetails)] = Field(None, alias="taxDetails", description="This array contains tax details provided during compliance onboarding for EU customers. Otherwise, it contains null.")
    trade_name: Optional[StrictStr] = Field(None, alias="tradeName", description="This field contains the trading name which is also known as Doing Business As(DBA)(In case the entity is doing business with a different name than the registered business name).")
    trustee_name: Optional[StrictStr] = Field(None, alias="trusteeName")
    website: Optional[StrictStr] = Field(None, description="This field contains the website of the company.")
    __properties = ["associationDetail", "businessAddress", "businessExtractCoveredStakeholder", "businessName", "businessRegistrationNumber", "businessRegistrationType", "businessType", "caseId", "clientId", "complianceRegion", "description", "documentDetails", "formerName", "legislationName", "legislationType", "listedExchange", "partnershipDetails", "referenceId", "registeredAddress", "registeredCountry", "registeredDate", "regulatoryDetails", "settlorName", "stockSymbol", "taxDetails", "tradeName", "trusteeName", "website"]

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
    def from_json(cls, json_str: str) -> BusinessDetailsResponseDTO:
        """Create an instance of BusinessDetailsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of association_detail
        if self.association_detail:
            _dict['associationDetail'] = self.association_detail.to_dict()
        # override the default output from pydantic by calling `to_dict()` of business_address
        if self.business_address:
            _dict['businessAddress'] = self.business_address.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in document_details (list)
        _items = []
        if self.document_details:
            for _item in self.document_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['documentDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of partnership_details
        if self.partnership_details:
            _dict['partnershipDetails'] = self.partnership_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of registered_address
        if self.registered_address:
            _dict['registeredAddress'] = self.registered_address.to_dict()
        # override the default output from pydantic by calling `to_dict()` of regulatory_details
        if self.regulatory_details:
            _dict['regulatoryDetails'] = self.regulatory_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in tax_details (list)
        _items = []
        if self.tax_details:
            for _item in self.tax_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taxDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BusinessDetailsResponseDTO:
        """Create an instance of BusinessDetailsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BusinessDetailsResponseDTO.parse_obj(obj)

        _obj = BusinessDetailsResponseDTO.parse_obj({
            "association_detail": AssociationDetails.from_dict(obj.get("associationDetail")) if obj.get("associationDetail") is not None else None,
            "business_address": CorporateAddressDTO.from_dict(obj.get("businessAddress")) if obj.get("businessAddress") is not None else None,
            "business_extract_covered_stakeholder": obj.get("businessExtractCoveredStakeholder"),
            "business_name": obj.get("businessName"),
            "business_registration_number": obj.get("businessRegistrationNumber"),
            "business_registration_type": obj.get("businessRegistrationType"),
            "business_type": obj.get("businessType"),
            "case_id": obj.get("caseId"),
            "client_id": obj.get("clientId"),
            "compliance_region": obj.get("complianceRegion"),
            "description": obj.get("description"),
            "document_details": [CorporateDocumentDetailsDTO.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None,
            "former_name": obj.get("formerName"),
            "legislation_name": obj.get("legislationName"),
            "legislation_type": obj.get("legislationType"),
            "listed_exchange": obj.get("listedExchange"),
            "partnership_details": PartnershipDetails.from_dict(obj.get("partnershipDetails")) if obj.get("partnershipDetails") is not None else None,
            "reference_id": obj.get("referenceId"),
            "registered_address": CorporateAddressDTO.from_dict(obj.get("registeredAddress")) if obj.get("registeredAddress") is not None else None,
            "registered_country": obj.get("registeredCountry"),
            "registered_date": obj.get("registeredDate"),
            "regulatory_details": RegulatoryDetails.from_dict(obj.get("regulatoryDetails")) if obj.get("regulatoryDetails") is not None else None,
            "settlor_name": obj.get("settlorName"),
            "stock_symbol": obj.get("stockSymbol"),
            "tax_details": [TaxDetails.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None,
            "trade_name": obj.get("tradeName"),
            "trustee_name": obj.get("trusteeName"),
            "website": obj.get("website")
        })
        return _obj


