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

class ProductDocument(BaseModel):
    """
    ProductDocument
    """
    document: Optional[StrictStr] = Field(None, description="This field accepts the Base64 encoded document to be uploaded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    file_name: Optional[StrictStr] = Field(None, alias="fileName", description="This field accepts the file name of the document to be uploaded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    file_type: Optional[StrictStr] = Field(None, alias="fileType", description="This field accepts the file type of the document to be uploaded. The valid values are: jpg jpeg png pdf image/jpg image/jpeg image/png application/pdf  AU: Optional EU: Optional UK: Optional SG: Optional")
    __properties = ["document", "fileName", "fileType"]

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
    def from_json(cls, json_str: str) -> ProductDocument:
        """Create an instance of ProductDocument from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductDocument:
        """Create an instance of ProductDocument from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductDocument.parse_obj(obj)

        _obj = ProductDocument.parse_obj({
            "document": obj.get("document"),
            "file_name": obj.get("fileName"),
            "file_type": obj.get("fileType")
        })
        return _obj


