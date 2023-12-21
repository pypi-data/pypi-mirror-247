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

class Beneficiary(BaseModel):
    """
    Beneficiary
    """
    id: StrictStr = Field(..., description="This is an unique beneficiary ID which depends upon the destination currency and payout method. The beneficiary Id and payout ID can be found out using [Beneficiary List](https://docs.nium.com/baas/beneficiary-list) API.")
    __properties = ["id"]

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
    def from_json(cls, json_str: str) -> Beneficiary:
        """Create an instance of Beneficiary from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Beneficiary:
        """Create an instance of Beneficiary from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Beneficiary.parse_obj(obj)

        _obj = Beneficiary.parse_obj({
            "id": obj.get("id")
        })
        return _obj


