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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

class File(BaseModel):
    """
    File
    """
    absolute: Optional[StrictBool] = None
    absolute_file: Optional[File] = Field(None, alias="absoluteFile")
    absolute_path: Optional[StrictStr] = Field(None, alias="absolutePath")
    canonical_file: Optional[File] = Field(None, alias="canonicalFile")
    canonical_path: Optional[StrictStr] = Field(None, alias="canonicalPath")
    directory: Optional[StrictBool] = None
    file: Optional[StrictBool] = None
    free_space: Optional[StrictInt] = Field(None, alias="freeSpace")
    hidden: Optional[StrictBool] = None
    name: Optional[StrictStr] = None
    parent: Optional[StrictStr] = None
    parent_file: Optional[File] = Field(None, alias="parentFile")
    path: Optional[StrictStr] = None
    total_space: Optional[StrictInt] = Field(None, alias="totalSpace")
    usable_space: Optional[StrictInt] = Field(None, alias="usableSpace")
    __properties = ["absolute", "absoluteFile", "absolutePath", "canonicalFile", "canonicalPath", "directory", "file", "freeSpace", "hidden", "name", "parent", "parentFile", "path", "totalSpace", "usableSpace"]

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
    def from_json(cls, json_str: str) -> File:
        """Create an instance of File from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of absolute_file
        if self.absolute_file:
            _dict['absoluteFile'] = self.absolute_file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of canonical_file
        if self.canonical_file:
            _dict['canonicalFile'] = self.canonical_file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of parent_file
        if self.parent_file:
            _dict['parentFile'] = self.parent_file.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> File:
        """Create an instance of File from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return File.parse_obj(obj)

        _obj = File.parse_obj({
            "absolute": obj.get("absolute"),
            "absolute_file": File.from_dict(obj.get("absoluteFile")) if obj.get("absoluteFile") is not None else None,
            "absolute_path": obj.get("absolutePath"),
            "canonical_file": File.from_dict(obj.get("canonicalFile")) if obj.get("canonicalFile") is not None else None,
            "canonical_path": obj.get("canonicalPath"),
            "directory": obj.get("directory"),
            "file": obj.get("file"),
            "free_space": obj.get("freeSpace"),
            "hidden": obj.get("hidden"),
            "name": obj.get("name"),
            "parent": obj.get("parent"),
            "parent_file": File.from_dict(obj.get("parentFile")) if obj.get("parentFile") is not None else None,
            "path": obj.get("path"),
            "total_space": obj.get("totalSpace"),
            "usable_space": obj.get("usableSpace")
        })
        return _obj

File.update_forward_refs()

