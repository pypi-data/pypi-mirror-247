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


from typing import List
from pydantic import BaseModel, Field, conlist
from nium.models.wallet_rfi_response_request import WalletRfiResponseRequest

class PayoutUploadRfiDocumentRequestDTO(BaseModel):
    """
    PayoutUploadRfiDocumentRequestDTO
    """
    rfi_response_request: conlist(WalletRfiResponseRequest) = Field(..., alias="rfiResponseRequest", description="This array contains the objects for each RFI being responded to. This facilitates responding to multiple RFIs in one-go for the same transaction. Refer the example for more details.")
    __properties = ["rfiResponseRequest"]

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
    def from_json(cls, json_str: str) -> PayoutUploadRfiDocumentRequestDTO:
        """Create an instance of PayoutUploadRfiDocumentRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in rfi_response_request (list)
        _items = []
        if self.rfi_response_request:
            for _item in self.rfi_response_request:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rfiResponseRequest'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PayoutUploadRfiDocumentRequestDTO:
        """Create an instance of PayoutUploadRfiDocumentRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PayoutUploadRfiDocumentRequestDTO.parse_obj(obj)

        _obj = PayoutUploadRfiDocumentRequestDTO.parse_obj({
            "rfi_response_request": [WalletRfiResponseRequest.from_dict(_item) for _item in obj.get("rfiResponseRequest")] if obj.get("rfiResponseRequest") is not None else None
        })
        return _obj


