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

class PinUpdateRequestDTO(BaseModel):
    """
    PinUpdateRequestDTO
    """
    pin_block: StrictStr = Field(..., alias="pinBlock", description="This field accepts the base64 encoded pin block.")
    __properties = ["pinBlock"]

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
    def from_json(cls, json_str: str) -> PinUpdateRequestDTO:
        """Create an instance of PinUpdateRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PinUpdateRequestDTO:
        """Create an instance of PinUpdateRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PinUpdateRequestDTO.parse_obj(obj)

        _obj = PinUpdateRequestDTO.parse_obj({
            "pin_block": obj.get("pinBlock")
        })
        return _obj


