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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, validator

class CustomerApiError(BaseModel):
    """
    CustomerApiError
    """
    errors: Optional[conlist(StrictStr)] = Field(None, description="List of errors occurred.")
    message: Optional[StrictStr] = Field(None, description="Error message descriptor.")
    status: Optional[StrictStr] = Field(None, description="HttpStatus of the request : BAD_REQUEST, INTERNAL_SERVER_ERROR.")
    __properties = ["errors", "message", "status"]

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('200 OK', '400 BAD_REQUEST', '403 FORBIDDEN', '404 NOT_FOUND', '500 INTERNAL_SERVER_ERROR', '502 BAD_GATEWAY', '503 SERVICE_UNAVAILABLE'):
            raise ValueError("must be one of enum values ('200 OK', '400 BAD_REQUEST', '403 FORBIDDEN', '404 NOT_FOUND', '500 INTERNAL_SERVER_ERROR', '502 BAD_GATEWAY', '503 SERVICE_UNAVAILABLE')")
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
    def from_json(cls, json_str: str) -> CustomerApiError:
        """Create an instance of CustomerApiError from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerApiError:
        """Create an instance of CustomerApiError from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerApiError.parse_obj(obj)

        _obj = CustomerApiError.parse_obj({
            "errors": obj.get("errors"),
            "message": obj.get("message"),
            "status": obj.get("status")
        })
        return _obj


