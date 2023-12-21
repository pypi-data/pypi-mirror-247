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
from pydantic import BaseModel, Field, StrictBool, StrictStr
from nium.models.file import File
from nium.models.url import URL

class Resource(BaseModel):
    """
    Resource
    """
    description: Optional[StrictStr] = None
    file: Optional[File] = None
    filename: Optional[StrictStr] = None
    input_stream: Optional[Dict[str, Any]] = Field(None, alias="inputStream")
    open: Optional[StrictBool] = None
    readable: Optional[StrictBool] = None
    uri: Optional[str] = None
    url: Optional[URL] = None
    __properties = ["description", "file", "filename", "inputStream", "open", "readable", "uri", "url"]

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
    def from_json(cls, json_str: str) -> Resource:
        """Create an instance of Resource from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of file
        if self.file:
            _dict['file'] = self.file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of url
        if self.url:
            _dict['url'] = self.url.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Resource:
        """Create an instance of Resource from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Resource.parse_obj(obj)

        _obj = Resource.parse_obj({
            "description": obj.get("description"),
            "file": File.from_dict(obj.get("file")) if obj.get("file") is not None else None,
            "filename": obj.get("filename"),
            "input_stream": obj.get("inputStream"),
            "open": obj.get("open"),
            "readable": obj.get("readable"),
            "uri": obj.get("uri"),
            "url": URL.from_dict(obj.get("url")) if obj.get("url") is not None else None
        })
        return _obj


