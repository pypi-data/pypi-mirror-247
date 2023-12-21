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

class URI(BaseModel):
    """
    URI
    """
    host: Optional[StrictStr] = None
    absolute: Optional[StrictBool] = None
    authority: Optional[StrictStr] = None
    fragment: Optional[StrictStr] = None
    opaque: Optional[StrictBool] = None
    path: Optional[StrictStr] = None
    port: Optional[StrictInt] = None
    query: Optional[StrictStr] = None
    raw_authority: Optional[StrictStr] = Field(None, alias="rawAuthority")
    raw_fragment: Optional[StrictStr] = Field(None, alias="rawFragment")
    raw_path: Optional[StrictStr] = Field(None, alias="rawPath")
    raw_query: Optional[StrictStr] = Field(None, alias="rawQuery")
    raw_scheme_specific_part: Optional[StrictStr] = Field(None, alias="rawSchemeSpecificPart")
    raw_user_info: Optional[StrictStr] = Field(None, alias="rawUserInfo")
    scheme: Optional[StrictStr] = None
    scheme_specific_part: Optional[StrictStr] = Field(None, alias="schemeSpecificPart")
    user_info: Optional[StrictStr] = Field(None, alias="userInfo")
    __properties = ["host", "absolute", "authority", "fragment", "opaque", "path", "port", "query", "rawAuthority", "rawFragment", "rawPath", "rawQuery", "rawSchemeSpecificPart", "rawUserInfo", "scheme", "schemeSpecificPart", "userInfo"]

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
    def from_json(cls, json_str: str) -> URI:
        """Create an instance of URI from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> URI:
        """Create an instance of URI from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return URI.parse_obj(obj)

        _obj = URI.parse_obj({
            "host": obj.get("host"),
            "absolute": obj.get("absolute"),
            "authority": obj.get("authority"),
            "fragment": obj.get("fragment"),
            "opaque": obj.get("opaque"),
            "path": obj.get("path"),
            "port": obj.get("port"),
            "query": obj.get("query"),
            "raw_authority": obj.get("rawAuthority"),
            "raw_fragment": obj.get("rawFragment"),
            "raw_path": obj.get("rawPath"),
            "raw_query": obj.get("rawQuery"),
            "raw_scheme_specific_part": obj.get("rawSchemeSpecificPart"),
            "raw_user_info": obj.get("rawUserInfo"),
            "scheme": obj.get("scheme"),
            "scheme_specific_part": obj.get("schemeSpecificPart"),
            "user_info": obj.get("userInfo")
        })
        return _obj


