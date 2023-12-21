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

class Labels(BaseModel):
    """
    Labels
    """
    acquirer_exemption_reason: Optional[StrictStr] = Field(None, alias="acquirerExemptionReason")
    acs_outcome: Optional[StrictStr] = Field(None, alias="acsOutcome")
    ecommerce_indicator: Optional[StrictStr] = Field(None, alias="ecommerceIndicator")
    multi_clearing_sequence_ind: Optional[StrictStr] = Field(None, alias="multiClearingSequenceInd")
    recurring_transaction_indicator: Optional[StrictStr] = Field(None, alias="recurringTransactionIndicator")
    sca_indicator: Optional[StrictStr] = Field(None, alias="scaIndicator")
    sca_reason_indicator: Optional[StrictStr] = Field(None, alias="scaReasonIndicator")
    __properties = ["acquirerExemptionReason", "acsOutcome", "ecommerceIndicator", "multiClearingSequenceInd", "recurringTransactionIndicator", "scaIndicator", "scaReasonIndicator"]

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
    def from_json(cls, json_str: str) -> Labels:
        """Create an instance of Labels from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Labels:
        """Create an instance of Labels from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Labels.parse_obj(obj)

        _obj = Labels.parse_obj({
            "acquirer_exemption_reason": obj.get("acquirerExemptionReason"),
            "acs_outcome": obj.get("acsOutcome"),
            "ecommerce_indicator": obj.get("ecommerceIndicator"),
            "multi_clearing_sequence_ind": obj.get("multiClearingSequenceInd"),
            "recurring_transaction_indicator": obj.get("recurringTransactionIndicator"),
            "sca_indicator": obj.get("scaIndicator"),
            "sca_reason_indicator": obj.get("scaReasonIndicator")
        })
        return _obj


