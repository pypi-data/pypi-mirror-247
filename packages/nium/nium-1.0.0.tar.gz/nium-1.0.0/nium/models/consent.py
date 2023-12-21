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
from nium.models.access import Access
from nium.models.sca_status import ScaStatus

class Consent(BaseModel):
    """
    Consent
    """
    access: Optional[Access] = None
    consent_status: Optional[StrictStr] = Field(None, alias="consentStatus", description="Authentication status of the consent.")
    frequency_per_day: Optional[StrictInt] = Field(None, alias="frequencyPerDay", description="This field indicates the requested maximum frequency for an access per day.")
    last_action_date: Optional[StrictStr] = Field(None, alias="lastActionDate", description="This date is containing the date of the last action on the consent object either through the XS2A interface or the PSU/ASPSP interface having an impact on the status.")
    recurring_indicator: Optional[StrictBool] = Field(None, alias="recurringIndicator", description="If the consent is for recurring access to the account data then the recurringIndicator value will be true or if the consent is for one access to the account data then the recurringIndicator value will be false.")
    sca_status: Optional[ScaStatus] = Field(None, alias="scaStatus")
    valid_until: Optional[StrictStr] = Field(None, alias="validUntil", description="This valid date for the requested consent. The content is the local ASPSP date in ISODate and the format is 2017-10-30.")
    __properties = ["access", "consentStatus", "frequencyPerDay", "lastActionDate", "recurringIndicator", "scaStatus", "validUntil"]

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
    def from_json(cls, json_str: str) -> Consent:
        """Create an instance of Consent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of access
        if self.access:
            _dict['access'] = self.access.to_dict()
        # override the default output from pydantic by calling `to_dict()` of sca_status
        if self.sca_status:
            _dict['scaStatus'] = self.sca_status.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Consent:
        """Create an instance of Consent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Consent.parse_obj(obj)

        _obj = Consent.parse_obj({
            "access": Access.from_dict(obj.get("access")) if obj.get("access") is not None else None,
            "consent_status": obj.get("consentStatus"),
            "frequency_per_day": obj.get("frequencyPerDay"),
            "last_action_date": obj.get("lastActionDate"),
            "recurring_indicator": obj.get("recurringIndicator"),
            "sca_status": ScaStatus.from_dict(obj.get("scaStatus")) if obj.get("scaStatus") is not None else None,
            "valid_until": obj.get("validUntil")
        })
        return _obj


