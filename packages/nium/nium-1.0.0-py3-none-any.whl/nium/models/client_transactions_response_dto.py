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
from pydantic import BaseModel, Field, StrictInt, conlist
from nium.models.transaction_response_dto import TransactionResponseDTO

class ClientTransactionsResponseDTO(BaseModel):
    """
    ClientTransactionsResponseDTO
    """
    content: Optional[conlist(TransactionResponseDTO)] = Field(None, description="This field contains an array that holds additional data.")
    total_elements: Optional[StrictInt] = Field(None, alias="totalElements", description="This field contains the number of elements in the response body.")
    total_pages: Optional[StrictInt] = Field(None, alias="totalPages", description="This field contains the number of pages in response body.")
    __properties = ["content", "totalElements", "totalPages"]

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
    def from_json(cls, json_str: str) -> ClientTransactionsResponseDTO:
        """Create an instance of ClientTransactionsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in content (list)
        _items = []
        if self.content:
            for _item in self.content:
                if _item:
                    _items.append(_item.to_dict())
            _dict['content'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ClientTransactionsResponseDTO:
        """Create an instance of ClientTransactionsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ClientTransactionsResponseDTO.parse_obj(obj)

        _obj = ClientTransactionsResponseDTO.parse_obj({
            "content": [TransactionResponseDTO.from_dict(_item) for _item in obj.get("content")] if obj.get("content") is not None else None,
            "total_elements": obj.get("totalElements"),
            "total_pages": obj.get("totalPages")
        })
        return _obj


