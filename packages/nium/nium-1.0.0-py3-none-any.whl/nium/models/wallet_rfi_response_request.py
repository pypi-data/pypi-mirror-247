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



from pydantic import BaseModel, Field, StrictStr
from nium.models.rfi_response_info import RfiResponseInfo

class WalletRfiResponseRequest(BaseModel):
    """
    WalletRfiResponseRequest
    """
    rfi_hash_id: StrictStr = Field(..., alias="rfiHashId", description="This field accepts the unique RFI hash ID.")
    rfi_response_info: RfiResponseInfo = Field(..., alias="rfiResponseInfo")
    __properties = ["rfiHashId", "rfiResponseInfo"]

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
    def from_json(cls, json_str: str) -> WalletRfiResponseRequest:
        """Create an instance of WalletRfiResponseRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of rfi_response_info
        if self.rfi_response_info:
            _dict['rfiResponseInfo'] = self.rfi_response_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletRfiResponseRequest:
        """Create an instance of WalletRfiResponseRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletRfiResponseRequest.parse_obj(obj)

        _obj = WalletRfiResponseRequest.parse_obj({
            "rfi_hash_id": obj.get("rfiHashId"),
            "rfi_response_info": RfiResponseInfo.from_dict(obj.get("rfiResponseInfo")) if obj.get("rfiResponseInfo") is not None else None
        })
        return _obj


