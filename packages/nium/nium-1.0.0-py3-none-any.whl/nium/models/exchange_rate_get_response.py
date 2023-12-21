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

from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, StrictFloat, StrictInt

class ExchangeRateGetResponse(BaseModel):
    """
    ExchangeRateGetResponse
    """
    average: Optional[Union[StrictFloat, StrictInt]] = None
    min: Optional[Union[StrictFloat, StrictInt]] = None
    max: Optional[Union[StrictFloat, StrictInt]] = None
    time: Optional[datetime] = None
    __properties = ["average", "min", "max", "time"]

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
    def from_json(cls, json_str: str) -> ExchangeRateGetResponse:
        """Create an instance of ExchangeRateGetResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExchangeRateGetResponse:
        """Create an instance of ExchangeRateGetResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExchangeRateGetResponse.parse_obj(obj)

        _obj = ExchangeRateGetResponse.parse_obj({
            "average": obj.get("average"),
            "min": obj.get("min"),
            "max": obj.get("max"),
            "time": obj.get("time")
        })
        return _obj


