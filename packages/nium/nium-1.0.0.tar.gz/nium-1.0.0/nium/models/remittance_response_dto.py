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

class RemittanceResponseDTO(BaseModel):
    """
    RemittanceResponseDTO
    """
    estimated_delivery_time: Optional[StrictStr] = Field(None, alias="estimatedDeliveryTime", description="This field is estimated delivery time of transaction.")
    message: Optional[StrictStr] = Field(None, description="This field will return a success message if the money transferred successfully.")
    payment_id: Optional[StrictStr] = Field(None, description="This field contains the unique payment ID.")
    system_reference_number: Optional[StrictStr] = Field(None, description="This is a unique system reference number assigned to the transaction.")
    __properties = ["estimatedDeliveryTime", "message", "payment_id", "system_reference_number"]

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
    def from_json(cls, json_str: str) -> RemittanceResponseDTO:
        """Create an instance of RemittanceResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RemittanceResponseDTO:
        """Create an instance of RemittanceResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RemittanceResponseDTO.parse_obj(obj)

        _obj = RemittanceResponseDTO.parse_obj({
            "estimated_delivery_time": obj.get("estimatedDeliveryTime"),
            "message": obj.get("message"),
            "payment_id": obj.get("payment_id"),
            "system_reference_number": obj.get("system_reference_number")
        })
        return _obj


