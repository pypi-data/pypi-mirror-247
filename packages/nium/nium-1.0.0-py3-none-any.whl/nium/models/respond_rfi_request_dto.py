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
from nium.models.product_rfi_response_request import ProductRfiResponseRequest

class RespondRfiRequestDTO(BaseModel):
    """
    RespondRfiRequestDTO
    """
    case_id: Optional[StrictStr] = Field(None, alias="caseId", description="This field accepts the compliance case Id of the customer.")
    client_id: Optional[StrictStr] = Field(None, alias="clientId", description="This field accepts the NIUM client Id of the customer.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique customer identifier generated at the time of customer creation.")
    region: Optional[StrictStr] = None
    rfi_response_request: Optional[conlist(ProductRfiResponseRequest)] = Field(None, alias="rfiResponseRequest", description="This is an array which accepts the requests for information, depending upon documents required to raise RFI.")
    __properties = ["caseId", "clientId", "customerHashId", "region", "rfiResponseRequest"]

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
    def from_json(cls, json_str: str) -> RespondRfiRequestDTO:
        """Create an instance of RespondRfiRequestDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> RespondRfiRequestDTO:
        """Create an instance of RespondRfiRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RespondRfiRequestDTO.parse_obj(obj)

        _obj = RespondRfiRequestDTO.parse_obj({
            "case_id": obj.get("caseId"),
            "client_id": obj.get("clientId"),
            "customer_hash_id": obj.get("customerHashId"),
            "region": obj.get("region"),
            "rfi_response_request": [ProductRfiResponseRequest.from_dict(_item) for _item in obj.get("rfiResponseRequest")] if obj.get("rfiResponseRequest") is not None else None
        })
        return _obj


