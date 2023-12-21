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
from nium.models.card_acceptor_address import CardAcceptorAddress
from nium.models.transaction_amount import TransactionAmount

class Transaction(BaseModel):
    """
    Transaction
    """
    bban: Optional[StrictStr] = Field(None, description="Basic Bank Account Number (BBAN) Identifier.")
    booking_date: Optional[datetime] = Field(None, alias="bookingDate")
    card_acceptor_address: Optional[CardAcceptorAddress] = Field(None, alias="cardAcceptorAddress")
    card_acceptor_id: Optional[StrictStr] = Field(None, alias="cardAcceptorId")
    card_transaction_id: Optional[StrictStr] = Field(None, alias="cardTransactionId")
    currency: Optional[StrictStr] = Field(None, description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    iban: Optional[StrictStr] = Field(None, description="International Bank Account Number (IBAN) of an account, for example: \"FR7612345987650123456789014.")
    masked_pan: Optional[StrictStr] = Field(None, alias="maskedPAN")
    masked_pan: Optional[StrictStr] = Field(None, alias="maskedPan", description="Primary Account Number (PAN) of a card in a masked form. This is used for card account in responses, for example \"1234\". The maximum length: 35")
    msisdn: Optional[StrictStr] = Field(None, description="An alias to access a payment account via a registered mobile phone number. The maximum length: 35")
    original_amount: Optional[TransactionAmount] = Field(None, alias="originalAmount")
    pan: Optional[StrictStr] = Field(None, description="Primary Account Number (PAN) of a card, can be tokenized by the ASPSP due to PCI DSS requirements. This is used for card account in responses. The maximum length: 35")
    transaction_amount: Optional[TransactionAmount] = Field(None, alias="transactionAmount")
    transaction_date: Optional[datetime] = Field(None, alias="transactionDate")
    __properties = ["bban", "bookingDate", "cardAcceptorAddress", "cardAcceptorId", "cardTransactionId", "currency", "iban", "maskedPAN", "maskedPan", "msisdn", "originalAmount", "pan", "transactionAmount", "transactionDate"]

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
    def from_json(cls, json_str: str) -> Transaction:
        """Create an instance of Transaction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of card_acceptor_address
        if self.card_acceptor_address:
            _dict['cardAcceptorAddress'] = self.card_acceptor_address.to_dict()
        # override the default output from pydantic by calling `to_dict()` of original_amount
        if self.original_amount:
            _dict['originalAmount'] = self.original_amount.to_dict()
        # override the default output from pydantic by calling `to_dict()` of transaction_amount
        if self.transaction_amount:
            _dict['transactionAmount'] = self.transaction_amount.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Transaction:
        """Create an instance of Transaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Transaction.parse_obj(obj)

        _obj = Transaction.parse_obj({
            "bban": obj.get("bban"),
            "booking_date": obj.get("bookingDate"),
            "card_acceptor_address": CardAcceptorAddress.from_dict(obj.get("cardAcceptorAddress")) if obj.get("cardAcceptorAddress") is not None else None,
            "card_acceptor_id": obj.get("cardAcceptorId"),
            "card_transaction_id": obj.get("cardTransactionId"),
            "currency": obj.get("currency"),
            "iban": obj.get("iban"),
            "masked_pan": obj.get("maskedPAN"),
            "masked_pan": obj.get("maskedPan"),
            "msisdn": obj.get("msisdn"),
            "original_amount": TransactionAmount.from_dict(obj.get("originalAmount")) if obj.get("originalAmount") is not None else None,
            "pan": obj.get("pan"),
            "transaction_amount": TransactionAmount.from_dict(obj.get("transactionAmount")) if obj.get("transactionAmount") is not None else None,
            "transaction_date": obj.get("transactionDate")
        })
        return _obj


