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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.payment_id_dto import PaymentIdDTO

class CustomerDetailResponseDTO(BaseModel):
    """
    CustomerDetailResponseDTO
    """
    compliance_status: Optional[StrictStr] = Field(None, alias="complianceStatus")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique client identifier generated and shared before API handshake")
    kyc_status: Optional[StrictStr] = Field(None, alias="kycStatus")
    payment_ids: Optional[conlist(PaymentIdDTO)] = Field(None, alias="paymentIds", description="This is an array which contains the paymentIds assigned to the customer")
    redirect_url: Optional[StrictStr] = Field(None, alias="redirectUrl")
    wallet_hash_id: Optional[StrictStr] = Field(None, alias="walletHashId", description="This field contains the unique wallet identifier generated simultaneously with customer creation.")
    __properties = ["complianceStatus", "customerHashId", "kycStatus", "paymentIds", "redirectUrl", "walletHashId"]

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
    def from_json(cls, json_str: str) -> CustomerDetailResponseDTO:
        """Create an instance of CustomerDetailResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in payment_ids (list)
        _items = []
        if self.payment_ids:
            for _item in self.payment_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['paymentIds'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerDetailResponseDTO:
        """Create an instance of CustomerDetailResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerDetailResponseDTO.parse_obj(obj)

        _obj = CustomerDetailResponseDTO.parse_obj({
            "compliance_status": obj.get("complianceStatus"),
            "customer_hash_id": obj.get("customerHashId"),
            "kyc_status": obj.get("kycStatus"),
            "payment_ids": [PaymentIdDTO.from_dict(_item) for _item in obj.get("paymentIds")] if obj.get("paymentIds") is not None else None,
            "redirect_url": obj.get("redirectUrl"),
            "wallet_hash_id": obj.get("walletHashId")
        })
        return _obj


