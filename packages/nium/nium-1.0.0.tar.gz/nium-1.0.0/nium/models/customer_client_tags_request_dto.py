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
from nium.models.customer_client_tag_request_dto import CustomerClientTagRequestDTO

class CustomerClientTagsRequestDTO(BaseModel):
    """
    CustomerClientTagsRequestDTO
    """
    tags: conlist(CustomerClientTagRequestDTO) = Field(..., description="This object accepts the user defined key-value pairs. The maximum number of tags allowed is 15.")
    __properties = ["tags"]

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
    def from_json(cls, json_str: str) -> CustomerClientTagsRequestDTO:
        """Create an instance of CustomerClientTagsRequestDTO from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerClientTagsRequestDTO:
        """Create an instance of CustomerClientTagsRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerClientTagsRequestDTO.parse_obj(obj)

        _obj = CustomerClientTagsRequestDTO.parse_obj({
            "tags": [CustomerClientTagRequestDTO.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None
        })
        return _obj


