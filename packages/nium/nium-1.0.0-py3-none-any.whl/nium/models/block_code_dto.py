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
from pydantic import BaseModel, Field, StrictStr, constr, validator

class BlockCodeDTO(BaseModel):
    """
    BlockCodeDTO
    """
    reason: Optional[StrictStr] = Field(None, description="This field accepts the reason for card block. It is required only in case of a permanent block [blockAction = permanentBlock]. Otherwise, it is not necessary.The possible values are: fraud cardLost cardStolen damaged")
    block_action: StrictStr = Field(..., alias="blockAction", description="The field accepts the block action to be applied on the card.The possible values are: permanentBlock temporaryBlock unblock")
    remarks: Optional[constr(strict=True, max_length=255, min_length=0)] = None
    comments: Optional[StrictStr] = None
    __properties = ["reason", "blockAction", "remarks", "comments"]

    @validator('reason')
    def reason_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('fraud, cardLost, cardStolen,damaged'):
            raise ValueError("must be one of enum values ('fraud, cardLost, cardStolen,damaged')")
        return value

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
    def from_json(cls, json_str: str) -> BlockCodeDTO:
        """Create an instance of BlockCodeDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BlockCodeDTO:
        """Create an instance of BlockCodeDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BlockCodeDTO.parse_obj(obj)

        _obj = BlockCodeDTO.parse_obj({
            "reason": obj.get("reason"),
            "block_action": obj.get("blockAction"),
            "remarks": obj.get("remarks"),
            "comments": obj.get("comments")
        })
        return _obj


