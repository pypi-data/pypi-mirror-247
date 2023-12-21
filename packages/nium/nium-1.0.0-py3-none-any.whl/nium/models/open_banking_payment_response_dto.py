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
from nium.models.account_reference import AccountReference
from nium.models.amount import Amount

class OpenBankingPaymentResponseDTO(BaseModel):
    """
    OpenBankingPaymentResponseDTO
    """
    comments: Optional[StrictStr] = Field(None, description="This field contains the system-generated comments for the transaction.")
    creditor_account: Optional[AccountReference] = Field(None, alias="creditorAccount")
    creditor_name: Optional[StrictStr] = Field(None, alias="creditorName", description="This field contains the name of the receiver for this flow.")
    debtor_account: Optional[AccountReference] = Field(None, alias="debtorAccount")
    instructed_amount: Optional[Amount] = Field(None, alias="instructedAmount")
    routing_code_value: Optional[StrictStr] = Field(None, alias="routingCodeValue", description="This field contains the BIC routing code for the transaction.")
    statement_narrative: Optional[StrictStr] = Field(None, alias="statementNarrative", description="This field contains the narrative for the transaction.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status of the transaction. The possible values are: INITIATED, PENDING, REJECTED, SENT_TO_BANK, PAID, RETURN")
    system_reference_number: Optional[StrictStr] = Field(None, alias="systemReferenceNumber", description="This field contains the unique, system generated reference number for the transaction.")
    __properties = ["comments", "creditorAccount", "creditorName", "debtorAccount", "instructedAmount", "routingCodeValue", "statementNarrative", "status", "systemReferenceNumber"]

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INITIATED', 'PENDING', 'REJECTED', 'SENT_TO_BANK', 'PAID', 'RETURN'):
            raise ValueError("must be one of enum values ('INITIATED', 'PENDING', 'REJECTED', 'SENT_TO_BANK', 'PAID', 'RETURN')")
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
    def from_json(cls, json_str: str) -> OpenBankingPaymentResponseDTO:
        """Create an instance of OpenBankingPaymentResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of creditor_account
        if self.creditor_account:
            _dict['creditorAccount'] = self.creditor_account.to_dict()
        # override the default output from pydantic by calling `to_dict()` of debtor_account
        if self.debtor_account:
            _dict['debtorAccount'] = self.debtor_account.to_dict()
        # override the default output from pydantic by calling `to_dict()` of instructed_amount
        if self.instructed_amount:
            _dict['instructedAmount'] = self.instructed_amount.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OpenBankingPaymentResponseDTO:
        """Create an instance of OpenBankingPaymentResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OpenBankingPaymentResponseDTO.parse_obj(obj)

        _obj = OpenBankingPaymentResponseDTO.parse_obj({
            "comments": obj.get("comments"),
            "creditor_account": AccountReference.from_dict(obj.get("creditorAccount")) if obj.get("creditorAccount") is not None else None,
            "creditor_name": obj.get("creditorName"),
            "debtor_account": AccountReference.from_dict(obj.get("debtorAccount")) if obj.get("debtorAccount") is not None else None,
            "instructed_amount": Amount.from_dict(obj.get("instructedAmount")) if obj.get("instructedAmount") is not None else None,
            "routing_code_value": obj.get("routingCodeValue"),
            "statement_narrative": obj.get("statementNarrative"),
            "status": obj.get("status"),
            "system_reference_number": obj.get("systemReferenceNumber")
        })
        return _obj


