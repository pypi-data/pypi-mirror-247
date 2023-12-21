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



from pydantic import BaseModel, Field, constr

class AssignCardDTO(BaseModel):
    """
    AssignCardDTO
    """
    account_number: constr(strict=True, max_length=19, min_length=16) = Field(..., alias="accountNumber", description="This field accepts the 19-digit account number (also known as card proxy number) printed on the non-personalized physical card. Alternately, the leading zeros may also be ignored in which case only the last 16-digits are required. For example, account number can be entered as 0007560010000160875, 007560010000160875, 07560010000160875 or 7560010000160875")
    card_number_last4_digits: constr(strict=True, max_length=4, min_length=4) = Field(..., alias="cardNumberLast4Digits", description="This field accepts the last 4 digit of the card number")
    __properties = ["accountNumber", "cardNumberLast4Digits"]

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
    def from_json(cls, json_str: str) -> AssignCardDTO:
        """Create an instance of AssignCardDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AssignCardDTO:
        """Create an instance of AssignCardDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AssignCardDTO.parse_obj(obj)

        _obj = AssignCardDTO.parse_obj({
            "account_number": obj.get("accountNumber"),
            "card_number_last4_digits": obj.get("cardNumberLast4Digits")
        })
        return _obj


