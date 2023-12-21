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


from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, validator

class AdditionalFeesDTO(BaseModel):
    """
    AdditionalFeesDTO
    """
    fee_type: Optional[StrictStr] = Field(None, alias="feeType", description="This field accepts the fee type as FIXED (flat) or PERCENTAGE")
    fee_value: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="feeValue", description="This field accepts the client's fee value to be added on existing fee value")
    fx_markup: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="fxMarkup", description="This field accepts the client's additional fx markup rate to be added on existing fx markup")
    __properties = ["feeType", "feeValue", "fxMarkup"]

    @validator('fee_type')
    def fee_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('FIXED', 'PERCENTAGE'):
            raise ValueError("must be one of enum values ('FIXED', 'PERCENTAGE')")
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
    def from_json(cls, json_str: str) -> AdditionalFeesDTO:
        """Create an instance of AdditionalFeesDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AdditionalFeesDTO:
        """Create an instance of AdditionalFeesDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AdditionalFeesDTO.parse_obj(obj)

        _obj = AdditionalFeesDTO.parse_obj({
            "fee_type": obj.get("feeType"),
            "fee_value": obj.get("feeValue"),
            "fx_markup": obj.get("fxMarkup")
        })
        return _obj


