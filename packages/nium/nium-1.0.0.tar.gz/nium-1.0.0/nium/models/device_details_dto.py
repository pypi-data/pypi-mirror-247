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

class DeviceDetailsDTO(BaseModel):
    """
    DeviceDetailsDTO
    """
    country_ip: Optional[StrictStr] = Field(None, alias="countryIP", description="This field accepts the country IP for the device by the customer for initiating the request.")
    device_info: Optional[StrictStr] = Field(None, alias="deviceInfo", description="This field accepts the device information used by the customer for initiating the request.")
    ip_address: Optional[StrictStr] = Field(None, alias="ipAddress", description="This field accepts the IP address of the device used by the customer for initiating the request.")
    session_id: Optional[StrictStr] = Field(None, alias="sessionId", description="This field accepts the session Id for the session of the customer for initiating the request.")
    __properties = ["countryIP", "deviceInfo", "ipAddress", "sessionId"]

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
    def from_json(cls, json_str: str) -> DeviceDetailsDTO:
        """Create an instance of DeviceDetailsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DeviceDetailsDTO:
        """Create an instance of DeviceDetailsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DeviceDetailsDTO.parse_obj(obj)

        _obj = DeviceDetailsDTO.parse_obj({
            "country_ip": obj.get("countryIP"),
            "device_info": obj.get("deviceInfo"),
            "ip_address": obj.get("ipAddress"),
            "session_id": obj.get("sessionId")
        })
        return _obj


