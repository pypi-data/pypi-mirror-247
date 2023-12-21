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
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, validator

class Payout(BaseModel):
    """
    Payout
    """
    audit_id: Optional[StrictInt] = Field(None, description="The audit Id must be taken from [Exchange Rate Lock and Hold](https://docs.nium.com/baas/exchange-rate-lock-and-hold) API.")
    destination_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="This field accepts the destination amount for remittance. Either the source or the destination amount is mandatory.  Allowed decimal limit is 2.")
    pre_screening: Optional[StrictBool] = Field(None, alias="preScreening", description="This field indicates if compliance checks to be done at the time of payout creation. This field is applicable for Scheduled Payout or Post Funded Payout only.")
    scheduled_payout_date: Optional[StrictStr] = Field(None, alias="scheduledPayoutDate", description="This field accepts scheduled payout date in yyyy-MM-dd format")
    service_time: Optional[StrictStr] = Field(None, alias="serviceTime", description="This field should denote the date of providing of service/export in yyyy-MM-dd format")
    source_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="This field accepts the source amount for remittance. Either the source or the destination amount is mandatory.  Allowed decimal limit is 2.")
    source_currency: Optional[StrictStr] = Field(None, description="This field accepts the source currency for remittance.")
    swift_fee_type: Optional[StrictStr] = Field(None, alias="swiftFeeType", description="This field accepts the swift fee type and defines who will bear the SWIFT charges for the given transaction. Clients can send any of the below values basis which, they will be charged for the SWIFT transaction. In case this field is absent SHA will be applied by default.  BEN - SWIFT charges borne by the beneficiary SHA - SWIFT charges shared by the customer and beneficiary OUR - SWIFT charges borne by the customer  Note: Clients should make sure that fee template is configured for each of the swift fee type. To know if the template is configured, clients should call [Fee Details](https://docs.nium.com/baas/get-fee-details) API")
    trade_order_id: Optional[StrictStr] = Field(None, alias="tradeOrderID", description="This field should denote the invoice number relevant to the transaction")
    __properties = ["audit_id", "destination_amount", "preScreening", "scheduledPayoutDate", "serviceTime", "source_amount", "source_currency", "swiftFeeType", "tradeOrderID"]

    @validator('swift_fee_type')
    def swift_fee_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('BEN', 'OUR', 'SHA'):
            raise ValueError("must be one of enum values ('BEN', 'OUR', 'SHA')")
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
    def from_json(cls, json_str: str) -> Payout:
        """Create an instance of Payout from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Payout:
        """Create an instance of Payout from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Payout.parse_obj(obj)

        _obj = Payout.parse_obj({
            "audit_id": obj.get("audit_id"),
            "destination_amount": obj.get("destination_amount"),
            "pre_screening": obj.get("preScreening"),
            "scheduled_payout_date": obj.get("scheduledPayoutDate"),
            "service_time": obj.get("serviceTime"),
            "source_amount": obj.get("source_amount"),
            "source_currency": obj.get("source_currency"),
            "swift_fee_type": obj.get("swiftFeeType"),
            "trade_order_id": obj.get("tradeOrderID")
        })
        return _obj


