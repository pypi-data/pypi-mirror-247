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

class P2PTransferDTO(BaseModel):
    """
    P2PTransferDTO
    """
    amount: Union[StrictFloat, StrictInt] = Field(..., description="The amount to be transferred.")
    authentication_code: Optional[StrictStr] = Field(None, alias="authenticationCode", description="This field accepts the authentication code generated as part of SCA (Strong Customer Authentication). Note: Authentication code is expected if regulatory region is UK or EU.")
    country_ip: Optional[StrictStr] = Field(None, alias="countryIP")
    currency_code: StrictStr = Field(..., alias="currencyCode", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the amount.")
    customer_comments: Optional[StrictStr] = Field(None, alias="customerComments", description="This field accepts customer comments for the P2P transfer. Maximum character limit is 512")
    destination_wallet_hash_id: StrictStr = Field(..., alias="destinationWalletHashId", description="The wallet hash Id under the same client which will receive the funds.")
    device_info: Optional[StrictStr] = Field(None, alias="deviceInfo")
    exemption_code: Optional[StrictStr] = Field(None, alias="exemptionCode", description="This field accepts the reason code for the exemption provided as part of SCA (Strong Customer Authentication), which can be one of the following values: 01 - Trusted Beneficiary 02 - Low Value Transaction 03 - Recurring Transactions 04 - Payment to Self  Note: Exemption code is expected if regulatory region is UK or EU")
    ip_address: Optional[StrictStr] = Field(None, alias="ipAddress")
    session_id: Optional[StrictStr] = Field(None, alias="sessionId")
    __properties = ["amount", "authenticationCode", "countryIP", "currencyCode", "customerComments", "destinationWalletHashId", "deviceInfo", "exemptionCode", "ipAddress", "sessionId"]

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
    def from_json(cls, json_str: str) -> P2PTransferDTO:
        """Create an instance of P2PTransferDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> P2PTransferDTO:
        """Create an instance of P2PTransferDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return P2PTransferDTO.parse_obj(obj)

        _obj = P2PTransferDTO.parse_obj({
            "amount": obj.get("amount"),
            "authentication_code": obj.get("authenticationCode"),
            "country_ip": obj.get("countryIP"),
            "currency_code": obj.get("currencyCode"),
            "customer_comments": obj.get("customerComments"),
            "destination_wallet_hash_id": obj.get("destinationWalletHashId"),
            "device_info": obj.get("deviceInfo"),
            "exemption_code": obj.get("exemptionCode"),
            "ip_address": obj.get("ipAddress"),
            "session_id": obj.get("sessionId")
        })
        return _obj


