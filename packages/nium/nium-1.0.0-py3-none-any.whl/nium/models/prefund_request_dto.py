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


from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr

class PrefundRequestDTO(BaseModel):
    """
    PrefundRequestDTO
    """
    amount: Union[StrictFloat, StrictInt] = Field(..., description="This field accepts the amount transferred to account")
    bank_reference_number: Optional[StrictStr] = Field(None, alias="bankReferenceNumber", description="This field accepts the reference number provided by the bank during fund transfer")
    bene_account_number: Optional[StrictStr] = Field(None, alias="beneAccountNumber", description="This field accepts the virtual account number")
    client_account_number: Optional[StrictStr] = Field(None, alias="clientAccountNumber", description="This field accepts the client's bank account number for reference from which the client has transferred money.")
    comments: Optional[StrictStr] = Field(None, description="This field accepts the comments which need to be passed, if any.")
    currency_code: StrictStr = Field(..., alias="currencyCode", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    date_of_transfer: Optional[StrictStr] = Field(None, alias="dateOfTransfer", description="This field accepts the date of the client's prefund transfer to the NIUM bank account. This request can be raised for a transfer within 30 days.")
    nium_account_number: Optional[StrictStr] = Field(None, alias="niumAccountNumber", description="This field accepts the NIUM account number to which the client has transferred the money.")
    requester_id: Optional[StrictStr] = Field(None, alias="requesterId", description="This field accepts the client's unique requester ID.")
    __properties = ["amount", "bankReferenceNumber", "beneAccountNumber", "clientAccountNumber", "comments", "currencyCode", "dateOfTransfer", "niumAccountNumber", "requesterId"]

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
    def from_json(cls, json_str: str) -> PrefundRequestDTO:
        """Create an instance of PrefundRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PrefundRequestDTO:
        """Create an instance of PrefundRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PrefundRequestDTO.parse_obj(obj)

        _obj = PrefundRequestDTO.parse_obj({
            "amount": obj.get("amount"),
            "bank_reference_number": obj.get("bankReferenceNumber"),
            "bene_account_number": obj.get("beneAccountNumber"),
            "client_account_number": obj.get("clientAccountNumber"),
            "comments": obj.get("comments"),
            "currency_code": obj.get("currencyCode"),
            "date_of_transfer": obj.get("dateOfTransfer"),
            "nium_account_number": obj.get("niumAccountNumber"),
            "requester_id": obj.get("requesterId")
        })
        return _obj


