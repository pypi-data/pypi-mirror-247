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

class AddCardV2ResponseDTO(BaseModel):
    """
    AddCardV2ResponseDTO
    """
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashId", description="Unique card identifier generated while new/add-on card issuance.")
    card_activation_status: Optional[StrictStr] = Field(None, alias="cardActivationStatus", description="Card activation status values are VIRTUAL_ACTIVE and INACTIVE")
    __properties = ["cardHashId", "cardActivationStatus"]

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
    def from_json(cls, json_str: str) -> AddCardV2ResponseDTO:
        """Create an instance of AddCardV2ResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddCardV2ResponseDTO:
        """Create an instance of AddCardV2ResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddCardV2ResponseDTO.parse_obj(obj)

        _obj = AddCardV2ResponseDTO.parse_obj({
            "card_hash_id": obj.get("cardHashId"),
            "card_activation_status": obj.get("cardActivationStatus")
        })
        return _obj


