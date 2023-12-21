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

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, StrictStr
from nium.models.gpi_response_dto import GPIResponseDTO

class RemittanceEventsResponseDTO2(BaseModel):
    """
    RemittanceEventsResponseDTO2
    """
    error_code: Optional[StrictStr] = Field(None, alias="errorCode", description="This field contains ISO error code.")
    error_description: Optional[StrictStr] = Field(None, alias="errorDescription", description="This field contains ISO reason description.")
    error_reason_code: Optional[StrictStr] = Field(None, alias="errorReasonCode", description="This field contains ISO reason code.")
    estimated_delivery_time: Optional[StrictStr] = Field(None, alias="estimatedDeliveryTime")
    gpi: Optional[GPIResponseDTO] = None
    last_updated_at: Optional[datetime] = Field(None, alias="lastUpdatedAt")
    partner_reference_number: Optional[StrictStr] = Field(None, alias="partnerReferenceNumber")
    payment_reference_number: Optional[StrictStr] = Field(None, alias="paymentReferenceNumber")
    status: Optional[StrictStr] = None
    status_details: Optional[StrictStr] = Field(None, alias="statusDetails")
    system_reference_number: Optional[StrictStr] = Field(None, alias="systemReferenceNumber")
    __properties = ["errorCode", "errorDescription", "errorReasonCode", "estimatedDeliveryTime", "gpi", "lastUpdatedAt", "partnerReferenceNumber", "paymentReferenceNumber", "status", "statusDetails", "systemReferenceNumber"]

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
    def from_json(cls, json_str: str) -> RemittanceEventsResponseDTO2:
        """Create an instance of RemittanceEventsResponseDTO2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of gpi
        if self.gpi:
            _dict['gpi'] = self.gpi.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RemittanceEventsResponseDTO2:
        """Create an instance of RemittanceEventsResponseDTO2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RemittanceEventsResponseDTO2.parse_obj(obj)

        _obj = RemittanceEventsResponseDTO2.parse_obj({
            "error_code": obj.get("errorCode"),
            "error_description": obj.get("errorDescription"),
            "error_reason_code": obj.get("errorReasonCode"),
            "estimated_delivery_time": obj.get("estimatedDeliveryTime"),
            "gpi": GPIResponseDTO.from_dict(obj.get("gpi")) if obj.get("gpi") is not None else None,
            "last_updated_at": obj.get("lastUpdatedAt"),
            "partner_reference_number": obj.get("partnerReferenceNumber"),
            "payment_reference_number": obj.get("paymentReferenceNumber"),
            "status": obj.get("status"),
            "status_details": obj.get("statusDetails"),
            "system_reference_number": obj.get("systemReferenceNumber")
        })
        return _obj


