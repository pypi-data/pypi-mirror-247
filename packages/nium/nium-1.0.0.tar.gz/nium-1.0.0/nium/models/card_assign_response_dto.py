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
from pydantic import BaseModel, Field, StrictStr, validator

class CardAssignResponseDTO(BaseModel):
    """
    CardAssignResponseDTO
    """
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashId", description="Unique card identifier generated while new/add-on card issuance.")
    card_activation_status: Optional[StrictStr] = Field(None, alias="cardActivationStatus", description="This field contains the card activation status. The values are VIRTUAL_ACTIVE and INACTIVE. In case of Assign Card flow, expected status is INACTIVE.")
    masked_card_number: Optional[StrictStr] = Field(None, alias="maskedCardNumber", description="This field contains the 16-digit masked card number in format 1234-56xx-xxxx-3456.")
    __properties = ["cardHashId", "cardActivationStatus", "maskedCardNumber"]

    @validator('card_activation_status')
    def card_activation_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('VIRTUAL_ACTIVE,INACTIVE'):
            raise ValueError("must be one of enum values ('VIRTUAL_ACTIVE,INACTIVE')")
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
    def from_json(cls, json_str: str) -> CardAssignResponseDTO:
        """Create an instance of CardAssignResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CardAssignResponseDTO:
        """Create an instance of CardAssignResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CardAssignResponseDTO.parse_obj(obj)

        _obj = CardAssignResponseDTO.parse_obj({
            "card_hash_id": obj.get("cardHashId"),
            "card_activation_status": obj.get("cardActivationStatus"),
            "masked_card_number": obj.get("maskedCardNumber")
        })
        return _obj


