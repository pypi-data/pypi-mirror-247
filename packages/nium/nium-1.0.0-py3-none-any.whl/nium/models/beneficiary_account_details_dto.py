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

class BeneficiaryAccountDetailsDTO(BaseModel):
    """
    BeneficiaryAccountDetailsDTO
    """
    account_type: Optional[StrictStr] = Field(None, alias="accountType", description="This field accepts the bank account type of the beneficiary.")
    address: Optional[StrictStr] = Field(None, description="This field accepts an address of the beneficiary.")
    alias: Optional[StrictStr] = None
    city: Optional[StrictStr] = Field(None, description="This field accepts the city of the beneficiary.")
    contact_number: Optional[StrictStr] = Field(None, alias="contactNumber", description="This field accepts the mobile number of the beneficiary.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field accepts the [ISO-2 country code](https://docs.nium.com/apis/docs/currency-and-country-codes) for the mobile number of beneficiary.")
    email: Optional[StrictStr] = Field(None, description="This field accepts an email of the beneficiary.")
    name: Optional[StrictStr] = Field(None, description="This field accepts the name of a beneficiary.")
    postcode: Optional[StrictStr] = Field(None, description="This field accepts an postcode of the beneficiary.")
    remitter_beneficiary_relationship: Optional[StrictStr] = Field(None, alias="remitterBeneficiaryRelationship", description="This field accepts the relationship of the beneficiary with the remitter.")
    state: Optional[StrictStr] = Field(None, description="This field accepts the state of the beneficiary.")
    __properties = ["accountType", "address", "alias", "city", "contactNumber", "countryCode", "email", "name", "postcode", "remitterBeneficiaryRelationship", "state"]

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
    def from_json(cls, json_str: str) -> BeneficiaryAccountDetailsDTO:
        """Create an instance of BeneficiaryAccountDetailsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BeneficiaryAccountDetailsDTO:
        """Create an instance of BeneficiaryAccountDetailsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BeneficiaryAccountDetailsDTO.parse_obj(obj)

        _obj = BeneficiaryAccountDetailsDTO.parse_obj({
            "account_type": obj.get("accountType"),
            "address": obj.get("address"),
            "alias": obj.get("alias"),
            "city": obj.get("city"),
            "contact_number": obj.get("contactNumber"),
            "country_code": obj.get("countryCode"),
            "email": obj.get("email"),
            "name": obj.get("name"),
            "postcode": obj.get("postcode"),
            "remitter_beneficiary_relationship": obj.get("remitterBeneficiaryRelationship"),
            "state": obj.get("state")
        })
        return _obj


