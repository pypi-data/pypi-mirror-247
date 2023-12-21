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

class ApiError(BaseModel):
    """
    ApiError
    """
    status: Optional[StrictStr] = Field(None, description="HttpStatus of the request : BAD_REQUEST, INTERNAL_SERVER_ERROR")
    message: Optional[StrictStr] = Field(None, description="Error message descriptor")
    errors: Optional[conlist(StrictStr)] = Field(None, description="List of errors occurred")
    __properties = ["status", "message", "errors"]

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('100 CONTINUE', '101 SWITCHING_PROTOCOLS', '102 PROCESSING', '103 CHECKPOINT', '200 OK', '201 CREATED', '202 ACCEPTED', '203 NON_AUTHORITATIVE_INFORMATION', '204 NO_CONTENT', '205 RESET_CONTENT', '206 PARTIAL_CONTENT', '207 MULTI_STATUS', '208 ALREADY_REPORTED', '226 IM_USED', '300 MULTIPLE_CHOICES', '301 MOVED_PERMANENTLY', '302 FOUND', '302 MOVED_TEMPORARILY', '303 SEE_OTHER', '304 NOT_MODIFIED', '305 USE_PROXY', '307 TEMPORARY_REDIRECT', '308 PERMANENT_REDIRECT', '400 BAD_REQUEST', '401 UNAUTHORIZED', '402 PAYMENT_REQUIRED', '403 FORBIDDEN', '404 NOT_FOUND', '405 METHOD_NOT_ALLOWED', '406 NOT_ACCEPTABLE', '407 PROXY_AUTHENTICATION_REQUIRED', '408 REQUEST_TIMEOUT', '409 CONFLICT', '410 GONE', '411 LENGTH_REQUIRED', '412 PRECONDITION_FAILED', '413 PAYLOAD_TOO_LARGE', '413 REQUEST_ENTITY_TOO_LARGE', '414 URI_TOO_LONG', '414 REQUEST_URI_TOO_LONG', '415 UNSUPPORTED_MEDIA_TYPE', '416 REQUESTED_RANGE_NOT_SATISFIABLE', '417 EXPECTATION_FAILED', '418 I_AM_A_TEAPOT', '419 INSUFFICIENT_SPACE_ON_RESOURCE', '420 METHOD_FAILURE', '421 DESTINATION_LOCKED', '422 UNPROCESSABLE_ENTITY', '423 LOCKED', '424 FAILED_DEPENDENCY', '425 TOO_EARLY', '426 UPGRADE_REQUIRED', '428 PRECONDITION_REQUIRED', '429 TOO_MANY_REQUESTS', '431 REQUEST_HEADER_FIELDS_TOO_LARGE', '451 UNAVAILABLE_FOR_LEGAL_REASONS', '500 INTERNAL_SERVER_ERROR', '501 NOT_IMPLEMENTED', '502 BAD_GATEWAY', '503 SERVICE_UNAVAILABLE', '504 GATEWAY_TIMEOUT', '505 HTTP_VERSION_NOT_SUPPORTED', '506 VARIANT_ALSO_NEGOTIATES', '507 INSUFFICIENT_STORAGE', '508 LOOP_DETECTED', '509 BANDWIDTH_LIMIT_EXCEEDED', '510 NOT_EXTENDED', '511 NETWORK_AUTHENTICATION_REQUIRED'):
            raise ValueError("must be one of enum values ('100 CONTINUE', '101 SWITCHING_PROTOCOLS', '102 PROCESSING', '103 CHECKPOINT', '200 OK', '201 CREATED', '202 ACCEPTED', '203 NON_AUTHORITATIVE_INFORMATION', '204 NO_CONTENT', '205 RESET_CONTENT', '206 PARTIAL_CONTENT', '207 MULTI_STATUS', '208 ALREADY_REPORTED', '226 IM_USED', '300 MULTIPLE_CHOICES', '301 MOVED_PERMANENTLY', '302 FOUND', '302 MOVED_TEMPORARILY', '303 SEE_OTHER', '304 NOT_MODIFIED', '305 USE_PROXY', '307 TEMPORARY_REDIRECT', '308 PERMANENT_REDIRECT', '400 BAD_REQUEST', '401 UNAUTHORIZED', '402 PAYMENT_REQUIRED', '403 FORBIDDEN', '404 NOT_FOUND', '405 METHOD_NOT_ALLOWED', '406 NOT_ACCEPTABLE', '407 PROXY_AUTHENTICATION_REQUIRED', '408 REQUEST_TIMEOUT', '409 CONFLICT', '410 GONE', '411 LENGTH_REQUIRED', '412 PRECONDITION_FAILED', '413 PAYLOAD_TOO_LARGE', '413 REQUEST_ENTITY_TOO_LARGE', '414 URI_TOO_LONG', '414 REQUEST_URI_TOO_LONG', '415 UNSUPPORTED_MEDIA_TYPE', '416 REQUESTED_RANGE_NOT_SATISFIABLE', '417 EXPECTATION_FAILED', '418 I_AM_A_TEAPOT', '419 INSUFFICIENT_SPACE_ON_RESOURCE', '420 METHOD_FAILURE', '421 DESTINATION_LOCKED', '422 UNPROCESSABLE_ENTITY', '423 LOCKED', '424 FAILED_DEPENDENCY', '425 TOO_EARLY', '426 UPGRADE_REQUIRED', '428 PRECONDITION_REQUIRED', '429 TOO_MANY_REQUESTS', '431 REQUEST_HEADER_FIELDS_TOO_LARGE', '451 UNAVAILABLE_FOR_LEGAL_REASONS', '500 INTERNAL_SERVER_ERROR', '501 NOT_IMPLEMENTED', '502 BAD_GATEWAY', '503 SERVICE_UNAVAILABLE', '504 GATEWAY_TIMEOUT', '505 HTTP_VERSION_NOT_SUPPORTED', '506 VARIANT_ALSO_NEGOTIATES', '507 INSUFFICIENT_STORAGE', '508 LOOP_DETECTED', '509 BANDWIDTH_LIMIT_EXCEEDED', '510 NOT_EXTENDED', '511 NETWORK_AUTHENTICATION_REQUIRED')")
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
    def from_json(cls, json_str: str) -> ApiError:
        """Create an instance of ApiError from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ApiError:
        """Create an instance of ApiError from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ApiError.parse_obj(obj)

        _obj = ApiError.parse_obj({
            "status": obj.get("status"),
            "message": obj.get("message"),
            "errors": obj.get("errors")
        })
        return _obj


