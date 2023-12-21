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

class LocalIsoResponse(BaseModel):
    """
    LocalIsoResponse
    """
    additional_amount: Optional[StrictStr] = Field(None, alias="additionalAmount", description="This field contains balance inquiry amount")
    authorization_code: Optional[StrictStr] = Field(None, alias="authorizationCode", description="This field contains the authorization code")
    date_of_transaction: Optional[StrictStr] = Field(None, alias="dateOfTransaction", description="This field contains the date of transaction")
    response_code: Optional[StrictStr] = Field(None, alias="responseCode", description="This field contains the response code value")
    rrn: Optional[StrictStr] = Field(None, description="This field contains the rrn")
    stan: Optional[StrictStr] = Field(None, description="This field contains the stan")
    status: Optional[StrictStr] = Field(None, description="This field contains the status")
    __properties = ["additionalAmount", "authorizationCode", "dateOfTransaction", "responseCode", "rrn", "stan", "status"]

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
    def from_json(cls, json_str: str) -> LocalIsoResponse:
        """Create an instance of LocalIsoResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LocalIsoResponse:
        """Create an instance of LocalIsoResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LocalIsoResponse.parse_obj(obj)

        _obj = LocalIsoResponse.parse_obj({
            "additional_amount": obj.get("additionalAmount"),
            "authorization_code": obj.get("authorizationCode"),
            "date_of_transaction": obj.get("dateOfTransaction"),
            "response_code": obj.get("responseCode"),
            "rrn": obj.get("rrn"),
            "stan": obj.get("stan"),
            "status": obj.get("status")
        })
        return _obj


