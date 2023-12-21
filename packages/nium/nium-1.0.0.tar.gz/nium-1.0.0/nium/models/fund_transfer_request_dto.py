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


from typing import List, Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, conlist
from nium.models.client_custom_tag_dto import ClientCustomTagDTO
from nium.models.device_details_dto import DeviceDetailsDTO

class FundTransferRequestDTO(BaseModel):
    """
    FundTransferRequestDTO
    """
    tags: Optional[conlist(ClientCustomTagDTO)] = None
    authentication_code: Optional[StrictStr] = Field(None, alias="authenticationCode", description="This field accepts the authentication code generated as part of SCA (Strong Customer Authentication). Note: Authentication code is expected if regulatory region is UK or EU.")
    customer_comments: Optional[StrictStr] = Field(None, alias="customerComments", description="This field accepts customer comments for the P2P transfer. Maximum character limit is 512")
    destination_amount: Union[StrictFloat, StrictInt] = Field(..., alias="destinationAmount", description="The amount to be transferred.")
    destination_currency_code: StrictStr = Field(..., alias="destinationCurrencyCode", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the amount.")
    destination_wallet_hash_id: StrictStr = Field(..., alias="destinationWalletHashId", description="The wallet hash Id of NIUM’s customers who will receive the funds.")
    device_details: Optional[DeviceDetailsDTO] = Field(None, alias="deviceDetails")
    exemption_code: Optional[StrictStr] = Field(None, alias="exemptionCode", description="This field accepts the reason code for the exemption provided as part of SCA (Strong Customer Authentication), which can be one of the following values: 01 - Trusted Beneficiary 02 - Low Value Transaction 03 - Recurring Transactions 04 - Payment to Self  Note: Exemption code is expected if regulatory region is UK or EU")
    purpose_code: StrictStr = Field(..., alias="purposeCode", description="This field accepts the purpose code for the payment. Please refer to the [Glossary of Purpose Codes](https://docs.nium.com/apis/docs/purpose-of-transfer-codes): to identify the correct value to be provided.")
    source_amount: Union[StrictFloat, StrictInt] = Field(..., alias="sourceAmount", description="The amount to be transferred.")
    source_currency_code: StrictStr = Field(..., alias="sourceCurrencyCode", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the amount.")
    __properties = ["tags", "authenticationCode", "customerComments", "destinationAmount", "destinationCurrencyCode", "destinationWalletHashId", "deviceDetails", "exemptionCode", "purposeCode", "sourceAmount", "sourceCurrencyCode"]

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
    def from_json(cls, json_str: str) -> FundTransferRequestDTO:
        """Create an instance of FundTransferRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item in self.tags:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tags'] = _items
        # override the default output from pydantic by calling `to_dict()` of device_details
        if self.device_details:
            _dict['deviceDetails'] = self.device_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FundTransferRequestDTO:
        """Create an instance of FundTransferRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FundTransferRequestDTO.parse_obj(obj)

        _obj = FundTransferRequestDTO.parse_obj({
            "tags": [ClientCustomTagDTO.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "authentication_code": obj.get("authenticationCode"),
            "customer_comments": obj.get("customerComments"),
            "destination_amount": obj.get("destinationAmount"),
            "destination_currency_code": obj.get("destinationCurrencyCode"),
            "destination_wallet_hash_id": obj.get("destinationWalletHashId"),
            "device_details": DeviceDetailsDTO.from_dict(obj.get("deviceDetails")) if obj.get("deviceDetails") is not None else None,
            "exemption_code": obj.get("exemptionCode"),
            "purpose_code": obj.get("purposeCode"),
            "source_amount": obj.get("sourceAmount"),
            "source_currency_code": obj.get("sourceCurrencyCode")
        })
        return _obj


