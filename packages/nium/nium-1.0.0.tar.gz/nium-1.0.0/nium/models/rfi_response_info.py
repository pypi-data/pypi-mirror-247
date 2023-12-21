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


from typing import Dict, Optional
from pydantic import BaseModel, Field, StrictStr
from nium.models.address_dto import AddressDTO
from nium.models.identification_doc_dto import IdentificationDocDTO

class RfiResponseInfo(BaseModel):
    """
    RfiResponseInfo
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo", description="This object accepts RFI raised for additional information fields.")
    address: Optional[AddressDTO] = None
    bank_account_number: Optional[StrictStr] = Field(None, alias="bankAccountNumber", description="This field accepts the bank account number.")
    bank_name: Optional[StrictStr] = Field(None, alias="bankName", description="This field accepts the bank name.")
    company_name: Optional[StrictStr] = Field(None, alias="companyName", description="This field accepts the company name of the customer.")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field accepts the date of birth of the customer. The format is yyyy-mm-dd.")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field accepts the first name of the customer. Maximum character limit: 50.")
    identification_doc: Optional[IdentificationDocDTO] = Field(None, alias="identificationDoc")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field accepts the last name of the customer. Maximum character limit: 50.")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field accepts the middle name of the customer. Maximum character limit: 50.")
    nationality: Optional[StrictStr] = Field(None, description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s citizenship.")
    __properties = ["additionalInfo", "address", "bankAccountNumber", "bankName", "companyName", "dateOfBirth", "firstName", "identificationDoc", "lastName", "middleName", "nationality"]

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
    def from_json(cls, json_str: str) -> RfiResponseInfo:
        """Create an instance of RfiResponseInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of address
        if self.address:
            _dict['address'] = self.address.to_dict()
        # override the default output from pydantic by calling `to_dict()` of identification_doc
        if self.identification_doc:
            _dict['identificationDoc'] = self.identification_doc.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RfiResponseInfo:
        """Create an instance of RfiResponseInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RfiResponseInfo.parse_obj(obj)

        _obj = RfiResponseInfo.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "address": AddressDTO.from_dict(obj.get("address")) if obj.get("address") is not None else None,
            "bank_account_number": obj.get("bankAccountNumber"),
            "bank_name": obj.get("bankName"),
            "company_name": obj.get("companyName"),
            "date_of_birth": obj.get("dateOfBirth"),
            "first_name": obj.get("firstName"),
            "identification_doc": IdentificationDocDTO.from_dict(obj.get("identificationDoc")) if obj.get("identificationDoc") is not None else None,
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "nationality": obj.get("nationality")
        })
        return _obj


