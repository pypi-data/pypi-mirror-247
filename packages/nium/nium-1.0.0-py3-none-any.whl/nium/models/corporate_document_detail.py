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

class CorporateDocumentDetail(BaseModel):
    """
    CorporateDocumentDetail
    """
    document_number: Optional[StrictStr] = Field(None, alias="documentNumber", description="This field accepts the document number for the uploaded document. This field is required only if the documents are being uploaded  AU: Optional EU: Required UK: Optional SG: Optional")
    document_type: Optional[StrictStr] = Field(None, alias="documentType", description="This field accepts the type of the document. The acceptable types of the documents are:  Business Registration Document Trust Deed Partnership Deed Association Deed Register of Directors Register of Shareholders  AU: Optional EU: Required UK: Optional SG: Optional")
    __properties = ["documentNumber", "documentType"]

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
    def from_json(cls, json_str: str) -> CorporateDocumentDetail:
        """Create an instance of CorporateDocumentDetail from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateDocumentDetail:
        """Create an instance of CorporateDocumentDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateDocumentDetail.parse_obj(obj)

        _obj = CorporateDocumentDetail.parse_obj({
            "document_number": obj.get("documentNumber"),
            "document_type": obj.get("documentType")
        })
        return _obj


