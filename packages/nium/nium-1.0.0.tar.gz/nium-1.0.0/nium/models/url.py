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


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr

class URL(BaseModel):
    """
    URL
    """
    host: Optional[StrictStr] = None
    authority: Optional[StrictStr] = None
    content: Optional[Dict[str, Any]] = None
    default_port: Optional[StrictInt] = Field(None, alias="defaultPort")
    file: Optional[StrictStr] = None
    path: Optional[StrictStr] = None
    port: Optional[StrictInt] = None
    protocol: Optional[StrictStr] = None
    query: Optional[StrictStr] = None
    ref: Optional[StrictStr] = None
    user_info: Optional[StrictStr] = Field(None, alias="userInfo")
    __properties = ["host", "authority", "content", "defaultPort", "file", "path", "port", "protocol", "query", "ref", "userInfo"]

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
    def from_json(cls, json_str: str) -> URL:
        """Create an instance of URL from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> URL:
        """Create an instance of URL from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return URL.parse_obj(obj)

        _obj = URL.parse_obj({
            "host": obj.get("host"),
            "authority": obj.get("authority"),
            "content": obj.get("content"),
            "default_port": obj.get("defaultPort"),
            "file": obj.get("file"),
            "path": obj.get("path"),
            "port": obj.get("port"),
            "protocol": obj.get("protocol"),
            "query": obj.get("query"),
            "ref": obj.get("ref"),
            "user_info": obj.get("userInfo")
        })
        return _obj


