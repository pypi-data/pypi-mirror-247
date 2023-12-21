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

class BusinessPartnerDetailsResponseDTO(BaseModel):
    """
    BusinessPartnerDetailsResponseDTO
    """
    address_line1: Optional[StrictStr] = Field(None, alias="addressLine1", description="This field contains the address line 1 of the registered address.")
    address_line2: Optional[StrictStr] = Field(None, alias="addressLine2", description="This field contains the address line 2 of the registered address.")
    business_entity_type: Optional[StrictStr] = Field(None, alias="businessEntityType", description="This field contains the entity type of the business partner. The possible values are: Director Ultimate Beneficial Owner Shareholder Authorized Signatory Authorized Representative Protector Partner Trustee Settlor Members Executor")
    business_name: Optional[StrictStr] = Field(None, alias="businessName", description="This field contains the registered business name of the business partner.")
    business_type: Optional[StrictStr] = Field(None, alias="businessType", description="This field contains the legal entity type of the business. The supported entity types are: Sole Trader Private Limited Company Public Company Partnership Limited Liability Partnership Firm Government Body Associations Trust Regulated Trust Unregulated Trust Unincorporated Partnership")
    city: Optional[StrictStr] = Field(None, description="This field contains the city name of the registered address.")
    country: Optional[StrictStr] = Field(None, description="This field contains the country name of the registered address.")
    postcode: Optional[StrictStr] = Field(None, description="This field contains the postcode of the registered address.")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field contains the unique reference ID.")
    registered_country: Optional[StrictStr] = Field(None, alias="registeredCountry", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf).")
    registered_date: Optional[StrictStr] = Field(None, alias="registeredDate", description="This field contains the business registration date.")
    registration_number: Optional[StrictStr] = Field(None, alias="registrationNumber", description="This field contains the registered business registration number of the business partner.")
    share_percentage: Optional[StrictStr] = Field(None, alias="sharePercentage", description="This field contains the share percentage that the business partner or the stakeholder holds in the company.")
    state: Optional[StrictStr] = Field(None, description="This field contains the state name of the registered address.")
    __properties = ["addressLine1", "addressLine2", "businessEntityType", "businessName", "businessType", "city", "country", "postcode", "referenceId", "registeredCountry", "registeredDate", "registrationNumber", "sharePercentage", "state"]

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
    def from_json(cls, json_str: str) -> BusinessPartnerDetailsResponseDTO:
        """Create an instance of BusinessPartnerDetailsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BusinessPartnerDetailsResponseDTO:
        """Create an instance of BusinessPartnerDetailsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BusinessPartnerDetailsResponseDTO.parse_obj(obj)

        _obj = BusinessPartnerDetailsResponseDTO.parse_obj({
            "address_line1": obj.get("addressLine1"),
            "address_line2": obj.get("addressLine2"),
            "business_entity_type": obj.get("businessEntityType"),
            "business_name": obj.get("businessName"),
            "business_type": obj.get("businessType"),
            "city": obj.get("city"),
            "country": obj.get("country"),
            "postcode": obj.get("postcode"),
            "reference_id": obj.get("referenceId"),
            "registered_country": obj.get("registeredCountry"),
            "registered_date": obj.get("registeredDate"),
            "registration_number": obj.get("registrationNumber"),
            "share_percentage": obj.get("sharePercentage"),
            "state": obj.get("state")
        })
        return _obj


