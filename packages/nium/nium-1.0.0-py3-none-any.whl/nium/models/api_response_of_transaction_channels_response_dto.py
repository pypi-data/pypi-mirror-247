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
from pydantic import BaseModel, Field, StrictStr, validator
from nium.models.transaction_channels_response_dto import TransactionChannelsResponseDTO

class ApiResponseOfTransactionChannelsResponseDTO(BaseModel):
    """
    ApiResponseOfTransactionChannelsResponseDTO
    """
    body: Optional[TransactionChannelsResponseDTO] = None
    code: Optional[StrictStr] = Field(None, description="This field will return the HTTP status code with its interpretation.")
    message: Optional[StrictStr] = Field(None, description="This field will return the response message.")
    status: Optional[StrictStr] = Field(None, description="This field signifies if the request was successful or has an error.")
    __properties = ["body", "code", "message", "status"]

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
    def from_json(cls, json_str: str) -> ApiResponseOfTransactionChannelsResponseDTO:
        """Create an instance of ApiResponseOfTransactionChannelsResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of body
        if self.body:
            _dict['body'] = self.body.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ApiResponseOfTransactionChannelsResponseDTO:
        """Create an instance of ApiResponseOfTransactionChannelsResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ApiResponseOfTransactionChannelsResponseDTO.parse_obj(obj)

        _obj = ApiResponseOfTransactionChannelsResponseDTO.parse_obj({
            "body": TransactionChannelsResponseDTO.from_dict(obj.get("body")) if obj.get("body") is not None else None,
            "code": obj.get("code"),
            "message": obj.get("message"),
            "status": obj.get("status")
        })
        return _obj


