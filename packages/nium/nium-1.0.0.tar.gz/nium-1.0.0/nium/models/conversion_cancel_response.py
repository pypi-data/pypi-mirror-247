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


from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, constr
from nium.models.cancellation_reason import CancellationReason
from nium.models.conversion_status import ConversionStatus

class ConversionCancelResponse(BaseModel):
    """
    ConversionCancelResponse
    """
    id: Optional[StrictStr] = Field(None, description="Unique identifier of the conversion.")
    status: Optional[ConversionStatus] = None
    system_reference_number: Optional[StrictStr] = Field(None, alias="systemReferenceNumber", description="Unique identifier for wallet financial activities used in all Nium reports and dashboards. Refer to [doc](https://docs.nium.com/apis/reference/clienttransactions) for details.")
    cancellation_fee: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="cancellationFee", description="The fee charged when executing the cancellation.")
    cancellation_fee_currency_code: Optional[StrictStr] = Field(None, alias="cancellationFeeCurrencyCode", description="3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the cancellation fee.")
    cancellation_comment: Optional[constr(strict=True, max_length=512)] = Field(None, alias="cancellationComment", description="Free text comment for clients to record and track cancellation of the conversion.")
    cancellation_fee_system_reference_number: Optional[StrictStr] = Field(None, alias="cancellationFeeSystemReferenceNumber", description="Unique identifier for wallet financial activities used in all Nium reports and dashboards. Refer to [doc](https://docs.nium.com/apis/reference/clienttransactions) for details.")
    cancellation_reason: Optional[CancellationReason] = Field(None, alias="cancellationReason")
    __properties = ["id", "status", "systemReferenceNumber", "cancellationFee", "cancellationFeeCurrencyCode", "cancellationComment", "cancellationFeeSystemReferenceNumber", "cancellationReason"]

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
    def from_json(cls, json_str: str) -> ConversionCancelResponse:
        """Create an instance of ConversionCancelResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ConversionCancelResponse:
        """Create an instance of ConversionCancelResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ConversionCancelResponse.parse_obj(obj)

        _obj = ConversionCancelResponse.parse_obj({
            "id": obj.get("id"),
            "status": obj.get("status"),
            "system_reference_number": obj.get("systemReferenceNumber"),
            "cancellation_fee": obj.get("cancellationFee"),
            "cancellation_fee_currency_code": obj.get("cancellationFeeCurrencyCode"),
            "cancellation_comment": obj.get("cancellationComment"),
            "cancellation_fee_system_reference_number": obj.get("cancellationFeeSystemReferenceNumber"),
            "cancellation_reason": obj.get("cancellationReason")
        })
        return _obj


