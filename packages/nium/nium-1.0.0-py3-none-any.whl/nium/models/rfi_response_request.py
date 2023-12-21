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
from nium.models.rfi_identification_doc import RfiIdentificationDoc

class RfiResponseRequest(BaseModel):
    """
    RfiResponseRequest
    """
    address_line1: Optional[StrictStr] = Field(None, alias="addressLine1", description="This field accepts the line1 of a customer's billing address. Maximum character limit: 40")
    address_line2: Optional[StrictStr] = Field(None, alias="addressLine2", description="This field accepts the line2 of a customer's billing address. Maximum character limit: 40")
    billing_country: Optional[StrictStr] = Field(None, alias="billingCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s billing country.")
    city: Optional[StrictStr] = Field(None, description="This field accepts the billing address city name. Maximum character limit: 30")
    country: Optional[StrictStr] = Field(None, description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of the customer’s billing address. It is important to pass this field if the card to be issued is to be used for GooglePay or ApplePay provisioning.")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field accepts the date of birth of a customer in YYYY-MM-DD format.")
    employment_status: Optional[StrictStr] = Field(None, alias="employmentStatus", description="This field accepts the customer's employment status. This field can accept alphanumeric characters. Maximum character limit: 30")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field accepts the first name of a customer. Maximum character limit: 40")
    gender: Optional[StrictStr] = Field(None, description="This field accepts the gender of the customer. The acceptable values are:  Male  Female  Others")
    identification_doc: Optional[RfiIdentificationDoc] = Field(None, alias="identificationDoc")
    industry_type: Optional[StrictStr] = Field(None, alias="industryType", description="This field accepts the customer's industry type. This field can accept alphanumeric characters. Maximum character limit: 30")
    intended_use_of_account: Optional[StrictStr] = Field(None, alias="intendedUseOfAccount", description="This field accepts the customer's intendedUse of account. This field can accept alphanumeric characters. Maximum character limit: 30")
    is_pep: Optional[StrictStr] = Field(None, alias="isPep", description="This field will ensure either a customer is a Politically Exposed Person (PEP) or not.")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field accepts the last name of a customer. Maximum character limit: 40")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field accepts the middle name of a customer. Maximum character limit: 40")
    nationality: Optional[StrictStr] = Field(None, description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s citizenship.")
    postcode: Optional[StrictStr] = Field(None, description="This field accepts the customer's billing ZIP code for the address. This field can accept alphanumeric characters, space, hyphen(-) and hash(#). Maximum character limit: 10")
    rfi_hash_id: StrictStr = Field(..., alias="rfiHashId", description="This field accepts the unique UUID rfiHashId received in Customer API.")
    source_of_funds: Optional[StrictStr] = Field(None, alias="sourceOfFunds", description="This field accepts the customer's source of funds. This field can accept alphanumeric characters. Maximum character limit: 30")
    state: Optional[StrictStr] = Field(None, description="This field accepts the customer's billing ZIP code for the address. This field can accept alphanumeric characters, space and hyphen(-). Maximum character limit: 30")
    __properties = ["addressLine1", "addressLine2", "billingCountry", "city", "country", "dateOfBirth", "employmentStatus", "firstName", "gender", "identificationDoc", "industryType", "intendedUseOfAccount", "isPep", "lastName", "middleName", "nationality", "postcode", "rfiHashId", "sourceOfFunds", "state"]

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
    def from_json(cls, json_str: str) -> RfiResponseRequest:
        """Create an instance of RfiResponseRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of identification_doc
        if self.identification_doc:
            _dict['identificationDoc'] = self.identification_doc.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RfiResponseRequest:
        """Create an instance of RfiResponseRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RfiResponseRequest.parse_obj(obj)

        _obj = RfiResponseRequest.parse_obj({
            "address_line1": obj.get("addressLine1"),
            "address_line2": obj.get("addressLine2"),
            "billing_country": obj.get("billingCountry"),
            "city": obj.get("city"),
            "country": obj.get("country"),
            "date_of_birth": obj.get("dateOfBirth"),
            "employment_status": obj.get("employmentStatus"),
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "identification_doc": RfiIdentificationDoc.from_dict(obj.get("identificationDoc")) if obj.get("identificationDoc") is not None else None,
            "industry_type": obj.get("industryType"),
            "intended_use_of_account": obj.get("intendedUseOfAccount"),
            "is_pep": obj.get("isPep"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "nationality": obj.get("nationality"),
            "postcode": obj.get("postcode"),
            "rfi_hash_id": obj.get("rfiHashId"),
            "source_of_funds": obj.get("sourceOfFunds"),
            "state": obj.get("state")
        })
        return _obj


