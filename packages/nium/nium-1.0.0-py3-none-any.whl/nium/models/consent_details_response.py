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
from nium.models.consent import Consent
from nium.models.payment import Payment

class ConsentDetailsResponse(BaseModel):
    """
    ConsentDetailsResponse
    """
    consent: Optional[Consent] = None
    id: Optional[StrictStr] = Field(None, description="Id of the consent to retrieve.")
    payment: Optional[Payment] = None
    __properties = ["consent", "id", "payment"]

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
    def from_json(cls, json_str: str) -> ConsentDetailsResponse:
        """Create an instance of ConsentDetailsResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of consent
        if self.consent:
            _dict['consent'] = self.consent.to_dict()
        # override the default output from pydantic by calling `to_dict()` of payment
        if self.payment:
            _dict['payment'] = self.payment.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ConsentDetailsResponse:
        """Create an instance of ConsentDetailsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ConsentDetailsResponse.parse_obj(obj)

        _obj = ConsentDetailsResponse.parse_obj({
            "consent": Consent.from_dict(obj.get("consent")) if obj.get("consent") is not None else None,
            "id": obj.get("id"),
            "payment": Payment.from_dict(obj.get("payment")) if obj.get("payment") is not None else None
        })
        return _obj


