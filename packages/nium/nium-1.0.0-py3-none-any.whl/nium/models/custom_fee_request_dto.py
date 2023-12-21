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

class CustomFeeRequestDTO(BaseModel):
    """
    CustomFeeRequestDTO
    """
    tags: Optional[conlist(ClientCustomTagDTO)] = Field(None, description="This is an array which accepts Client's custom tags & values. Maximum 15 key-value pairs can be sent in tags.")
    amount: Union[StrictFloat, StrictInt] = Field(..., description="This field accepts the amount to be debited from the Customer's wallet.")
    comments: Optional[StrictStr] = Field(None, description="This field accepts any comments for the custom fee to be levied. The maximum character limit is 255.")
    currency: StrictStr = Field(..., description="This field accepts the 3-letter ISO-4217 currency code for the currency of the fee to be charged (supported for any currencies enabled in the Customer's wallet)")
    fee_name: StrictStr = Field(..., alias="feeName", description="This field accepts the name of the fee. Number of characters supported: 3 to 50. Note: This field only accepts alphanumeric characters with -_.(hyphen, underscore, dot, and space)")
    __properties = ["tags", "amount", "comments", "currency", "feeName"]

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
    def from_json(cls, json_str: str) -> CustomFeeRequestDTO:
        """Create an instance of CustomFeeRequestDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> CustomFeeRequestDTO:
        """Create an instance of CustomFeeRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomFeeRequestDTO.parse_obj(obj)

        _obj = CustomFeeRequestDTO.parse_obj({
            "tags": [ClientCustomTagDTO.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "amount": obj.get("amount"),
            "comments": obj.get("comments"),
            "currency": obj.get("currency"),
            "fee_name": obj.get("feeName")
        })
        return _obj


