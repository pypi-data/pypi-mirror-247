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
from pydantic import BaseModel, conlist
from nium.models.customer_details_response_v2_dto import CustomerDetailsResponseV2DTO
from nium.models.pagination import Pagination

class PaginatedResponseDTOCustomerDetailsResponseV2DTO(BaseModel):
    """
    PaginatedResponseDTOCustomerDetailsResponseV2DTO
    """
    content: Optional[conlist(CustomerDetailsResponseV2DTO)] = None
    pagination: Optional[Pagination] = None
    __properties = ["content", "pagination"]

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
    def from_json(cls, json_str: str) -> PaginatedResponseDTOCustomerDetailsResponseV2DTO:
        """Create an instance of PaginatedResponseDTOCustomerDetailsResponseV2DTO from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of pagination
        if self.pagination:
            _dict['pagination'] = self.pagination.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PaginatedResponseDTOCustomerDetailsResponseV2DTO:
        """Create an instance of PaginatedResponseDTOCustomerDetailsResponseV2DTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaginatedResponseDTOCustomerDetailsResponseV2DTO.parse_obj(obj)

        _obj = PaginatedResponseDTOCustomerDetailsResponseV2DTO.parse_obj({
            "content": [CustomerDetailsResponseV2DTO.from_dict(_item) for _item in obj.get("content")] if obj.get("content") is not None else None,
            "pagination": Pagination.from_dict(obj.get("pagination")) if obj.get("pagination") is not None else None
        })
        return _obj


