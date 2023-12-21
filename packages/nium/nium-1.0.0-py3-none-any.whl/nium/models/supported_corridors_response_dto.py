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

class SupportedCorridorsResponseDTO(BaseModel):
    """
    SupportedCorridorsResponseDTO
    """
    beneficiary_account_type: Optional[StrictStr] = Field(None, alias="beneficiaryAccountType")
    customer_type: Optional[StrictStr] = Field(None, alias="customerType")
    destination_country: Optional[StrictStr] = Field(None, alias="destinationCountry")
    destination_currency: Optional[StrictStr] = Field(None, alias="destinationCurrency")
    payout_method: Optional[StrictStr] = Field(None, alias="payoutMethod")
    routing_code_type: Optional[StrictStr] = Field(None, alias="routingCodeType")
    __properties = ["beneficiaryAccountType", "customerType", "destinationCountry", "destinationCurrency", "payoutMethod", "routingCodeType"]

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
    def from_json(cls, json_str: str) -> SupportedCorridorsResponseDTO:
        """Create an instance of SupportedCorridorsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SupportedCorridorsResponseDTO:
        """Create an instance of SupportedCorridorsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SupportedCorridorsResponseDTO.parse_obj(obj)

        _obj = SupportedCorridorsResponseDTO.parse_obj({
            "beneficiary_account_type": obj.get("beneficiaryAccountType"),
            "customer_type": obj.get("customerType"),
            "destination_country": obj.get("destinationCountry"),
            "destination_currency": obj.get("destinationCurrency"),
            "payout_method": obj.get("payoutMethod"),
            "routing_code_type": obj.get("routingCodeType")
        })
        return _obj


