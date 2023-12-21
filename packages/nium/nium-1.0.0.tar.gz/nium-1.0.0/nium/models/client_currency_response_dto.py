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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

class ClientCurrencyResponseDTO(BaseModel):
    """
    ClientCurrencyResponseDTO
    """
    authorization_order: Optional[StrictInt] = Field(None, alias="authorizationOrder", description="This is the authorization order based on priority for available currencies. The order starts from 0 as a highest priority.")
    currency_code: Optional[StrictStr] = Field(None, alias="currencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    decimal_unit: Optional[StrictInt] = Field(None, alias="decimalUnit", description="This field contains the decimal unit which will be used for rounding off, for example 0")
    fx_sell_allowed: Optional[StrictBool] = Field(None, alias="fxSellAllowed", description="This field indicates if forex sell is allowed or not for the currency.")
    remittance_allowed: Optional[StrictBool] = Field(None, alias="remittanceAllowed", description="This field specifies if the remittance is allowed with the respective currency or not.")
    __properties = ["authorizationOrder", "currencyCode", "decimalUnit", "fxSellAllowed", "remittanceAllowed"]

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
    def from_json(cls, json_str: str) -> ClientCurrencyResponseDTO:
        """Create an instance of ClientCurrencyResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ClientCurrencyResponseDTO:
        """Create an instance of ClientCurrencyResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ClientCurrencyResponseDTO.parse_obj(obj)

        _obj = ClientCurrencyResponseDTO.parse_obj({
            "authorization_order": obj.get("authorizationOrder"),
            "currency_code": obj.get("currencyCode"),
            "decimal_unit": obj.get("decimalUnit"),
            "fx_sell_allowed": obj.get("fxSellAllowed"),
            "remittance_allowed": obj.get("remittanceAllowed")
        })
        return _obj


