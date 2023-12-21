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


from typing import Optional
from pydantic import BaseModel, Field, StrictStr

class BlockAndReplaceStatus(BaseModel):
    """
    Card block/replace status  # noqa: E501
    """
    block_reason: Optional[StrictStr] = Field(None, alias="blockReason", description="This field contains the card block reason.")
    replaced_on: Optional[StrictStr] = Field(None, alias="replacedOn", description="This field contains the card replacement date")
    __properties = ["blockReason", "replacedOn"]

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
    def from_json(cls, json_str: str) -> BlockAndReplaceStatus:
        """Create an instance of BlockAndReplaceStatus from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BlockAndReplaceStatus:
        """Create an instance of BlockAndReplaceStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BlockAndReplaceStatus.parse_obj(obj)

        _obj = BlockAndReplaceStatus.parse_obj({
            "block_reason": obj.get("blockReason"),
            "replaced_on": obj.get("replacedOn")
        })
        return _obj


