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
from pydantic import BaseModel, Field, StrictStr, validator

class RemitterRequestDTO(BaseModel):
    """
    RemitterRequestDTO
    """
    account_type: Optional[StrictStr] = Field(None, alias="accountType", description="This field accepts the Remitter's account type as INDIVIDUAL or CORPORATE")
    address: Optional[StrictStr] = Field(None, description="This field accepts address for Remitter's place of residence.")
    bank_account_number: Optional[StrictStr] = Field(None, alias="bankAccountNumber", description="This field accepts the account number of the Remitter.")
    city: Optional[StrictStr] = Field(None, description="This field accepts the city for Remitter's place of residence.")
    contact_number: Optional[StrictStr] = Field(None, alias="contactNumber", description="This field accepts the Remitter's contact number.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field accepts the country of residence for the remitter.")
    dob: Optional[StrictStr] = Field(None, description="This field accepts Remitter's birth date.")
    identification_number: Optional[StrictStr] = Field(None, alias="identificationNumber", description="ID number of the selected identificationType.")
    identification_type: Optional[StrictStr] = Field(None, alias="identificationType", description="This field accepts the ID document type of the remitter e.g. Passport, National_ID etc..")
    industry_type: Optional[StrictStr] = Field(None, alias="industryType", description="This field accepts industry type associated with the remitter.")
    name: Optional[StrictStr] = Field(None, description="This field accepts the name of the remitter.")
    nationality: Optional[StrictStr] = Field(None, description="This field accepts Remitter's nationality.")
    originating_fi_name: Optional[StrictStr] = Field(None, alias="originatingFIName", description="This field accepts the name of the financial institution where the request was initiated. This is typically applicable for requests that did not originate at the financial institution who is a direct Nium customer.")
    place_of_birth: Optional[StrictStr] = Field(None, alias="placeOfBirth", description="This field accepts Remitter's place of birth.")
    postcode: Optional[StrictStr] = Field(None, description="This field accepts the postcode  for Remitter's place of residence.")
    state: Optional[StrictStr] = Field(None, description="This field accepts the state  for Remitter's place of residence.")
    __properties = ["accountType", "address", "bankAccountNumber", "city", "contactNumber", "countryCode", "dob", "identificationNumber", "identificationType", "industryType", "name", "nationality", "originatingFIName", "placeOfBirth", "postcode", "state"]

    @validator('account_type')
    def account_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INDIVIDUAL', 'CORPORATE'):
            raise ValueError("must be one of enum values ('INDIVIDUAL', 'CORPORATE')")
        return value

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
    def from_json(cls, json_str: str) -> RemitterRequestDTO:
        """Create an instance of RemitterRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RemitterRequestDTO:
        """Create an instance of RemitterRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RemitterRequestDTO.parse_obj(obj)

        _obj = RemitterRequestDTO.parse_obj({
            "account_type": obj.get("accountType"),
            "address": obj.get("address"),
            "bank_account_number": obj.get("bankAccountNumber"),
            "city": obj.get("city"),
            "contact_number": obj.get("contactNumber"),
            "country_code": obj.get("countryCode"),
            "dob": obj.get("dob"),
            "identification_number": obj.get("identificationNumber"),
            "identification_type": obj.get("identificationType"),
            "industry_type": obj.get("industryType"),
            "name": obj.get("name"),
            "nationality": obj.get("nationality"),
            "originating_fi_name": obj.get("originatingFIName"),
            "place_of_birth": obj.get("placeOfBirth"),
            "postcode": obj.get("postcode"),
            "state": obj.get("state")
        })
        return _obj


