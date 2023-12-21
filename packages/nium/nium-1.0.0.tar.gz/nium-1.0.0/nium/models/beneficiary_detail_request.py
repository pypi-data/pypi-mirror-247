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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class BeneficiaryDetailRequest(BaseModel):
    """
    BeneficiaryDetailRequest
    """
    account_type: StrictStr = Field(..., description="This field accepts the bank account type of the beneficiary. The account_type can be either Individual or Company.")
    address: Optional[StrictStr] = Field(None, description="This field accepts an address of the beneficiary.")
    autosweep_payout_account: Optional[StrictBool] = Field(None, description="This field accepts the boolean value for the autosweepPayoutAccount.")
    beneficiary_contact_name: Optional[StrictStr] = Field(None, description="This field accepts the contact name of the beneficiary.")
    beneficiary_dob: Optional[StrictStr] = Field(None, description="This field accepts the date of birth of the beneficiary in the format YYYY-MM-DD, for example, 2023-07-08")
    beneficiary_entity_type: Optional[StrictStr] = Field(None, description="This field accepts the entity type of the beneficiary.")
    beneficiary_establishment_date: Optional[StrictStr] = Field(None, description="This field accepts the date of establishment of the beneficiary in the format YYYY-MM-DD, for example, 2023-07-08")
    city: Optional[StrictStr] = Field(None, description="This field accepts the city of the beneficiary. Maximum character limit: 50.")
    contact_country_code: Optional[StrictStr] = Field(None, description="This field accepts the ISO-2 country code for the mobile number of beneficiary.")
    contact_number: Optional[StrictStr] = Field(None, description="This field accepts the mobile number of the beneficiary.")
    country_code: StrictStr = Field(..., description="This field accepts the [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the mobile number of beneficiary.")
    default_autosweep_payout_account: Optional[StrictBool] = Field(None, description="This field accepts the boolean value for the defaultAutosweepPayoutAccount.")
    email: Optional[StrictStr] = Field(None, description="This field accepts an email of the beneficiary.")
    name: StrictStr = Field(..., description="This field accepts the name of the beneficiary.The beneficiary_group_name is required.Name can contain alphabets, numbers, and special characters that is (. , () ' / -). Maximum character limit: 150.")
    postcode: Optional[StrictStr] = Field(None, description="This field accepts the postal code of the beneficiary.")
    relationship: Optional[StrictStr] = Field(None, description="This field accepts the relationship of the beneficiary with the remitter.")
    state: Optional[StrictStr] = Field(None, description="This field accepts the state of the beneficiary.Maximum character limit: 50.")
    __properties = ["account_type", "address", "autosweep_payout_account", "beneficiary_contact_name", "beneficiary_dob", "beneficiary_entity_type", "beneficiary_establishment_date", "city", "contact_country_code", "contact_number", "country_code", "default_autosweep_payout_account", "email", "name", "postcode", "relationship", "state"]

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
    def from_json(cls, json_str: str) -> BeneficiaryDetailRequest:
        """Create an instance of BeneficiaryDetailRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BeneficiaryDetailRequest:
        """Create an instance of BeneficiaryDetailRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BeneficiaryDetailRequest.parse_obj(obj)

        _obj = BeneficiaryDetailRequest.parse_obj({
            "account_type": obj.get("account_type"),
            "address": obj.get("address"),
            "autosweep_payout_account": obj.get("autosweep_payout_account"),
            "beneficiary_contact_name": obj.get("beneficiary_contact_name"),
            "beneficiary_dob": obj.get("beneficiary_dob"),
            "beneficiary_entity_type": obj.get("beneficiary_entity_type"),
            "beneficiary_establishment_date": obj.get("beneficiary_establishment_date"),
            "city": obj.get("city"),
            "contact_country_code": obj.get("contact_country_code"),
            "contact_number": obj.get("contact_number"),
            "country_code": obj.get("country_code"),
            "default_autosweep_payout_account": obj.get("default_autosweep_payout_account"),
            "email": obj.get("email"),
            "name": obj.get("name"),
            "postcode": obj.get("postcode"),
            "relationship": obj.get("relationship"),
            "state": obj.get("state")
        })
        return _obj


