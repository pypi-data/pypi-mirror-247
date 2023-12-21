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

class AddCustomerResponseDTO(BaseModel):
    """
    AddCustomerResponseDTO
    """
    compliance_status: Optional[StrictStr] = Field(None, alias="complianceStatus", description="This field contains the compliance status of the customer. Possible values are: • INITIATED • IN_PROGRESS • ACTION_REQUIRED • RFI_REQUESTED • COMPLETED • REJECT • ERROR • EXPIRED • CLOSED")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="Unique customer identifier generated on customer creation")
    kyc_status: Optional[StrictStr] = Field(None, alias="kycStatus", description="This field contains the kyc status and this shall be available only in applicable cases. Please call [Customer Details](https://docs.nium.com/baas/get--customer-details) to fetch accurate kyc status.")
    payment_ids: Optional[conlist(PaymentIdDTO)] = Field(None, alias="paymentIds", description="This is an array which contains the paymentIds assigned to the customer.")
    redirect_url: Optional[StrictStr] = Field(None, alias="redirectUrl", description="This field contains the redirect URL where the customer should be redirected for verification.")
    wallet_hash_id: Optional[StrictStr] = Field(None, alias="walletHashId", description="Unique wallet identifier generated simultaneously with customer creation.")
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
    def from_json(cls, json_str: str) -> AddCustomerResponseDTO:
        """Create an instance of AddCustomerResponseDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> AddCustomerResponseDTO:
        """Create an instance of AddCustomerResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddCustomerResponseDTO.parse_obj(obj)

        _obj = AddCustomerResponseDTO.parse_obj({
            "compliance_status": obj.get("complianceStatus"),
            "customer_hash_id": obj.get("customerHashId"),
            "kyc_status": obj.get("kycStatus"),
            "payment_ids": [PaymentIdDTO.from_dict(_item) for _item in obj.get("paymentIds")] if obj.get("paymentIds") is not None else None,
            "redirect_url": obj.get("redirectUrl"),
            "wallet_hash_id": obj.get("walletHashId")
        })
        return _obj


