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
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr
from nium.models.labels import Labels

class SettlementRequestDTO(BaseModel):
    """
    SettlementRequestDTO
    """
    authorization_code: Optional[StrictStr] = Field(None, alias="authorizationCode", description="This field contains the 6 digit authorization code")
    billing_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="billingAmount", description="This field contains the billing amount")
    billing_currency: Optional[StrictStr] = Field(None, alias="billingCurrency", description="This field contains the 3-letter ISO3 billing currency code")
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashId", description="This field contains the unique card identifier")
    card_number: Optional[StrictStr] = Field(None, alias="cardNumber", description="This field contains the complete 16 digit card number")
    client_hash_id: Optional[StrictStr] = Field(None, alias="clientHashId", description="This field contains the unique client identifier")
    client_id: Optional[StrictInt] = Field(None, alias="clientId", description="This field contains the unique client ID")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique customer identifier ")
    exchange_rate: Optional[StrictStr] = Field(None, alias="exchangeRate", description="This field contains the exchange rate from the source currency to the destination currency")
    labels: Optional[Labels] = None
    logo_id: Optional[StrictStr] = Field(None, alias="logoId", description="This field accepts the pre-defined logo Id")
    logo_identifier: Optional[StrictStr] = Field(None, alias="logoIdentifier", description="This field accepts the pre-defined logo Identifier")
    mask_card_number: Optional[StrictStr] = Field(None, alias="maskCardNumber", description="This field contains the 16-digit masked card number")
    merchant_category_code: Optional[StrictStr] = Field(None, alias="merchantCategoryCode", description="This field contains the 4-digit mcc code")
    merchant_country_code: Optional[StrictStr] = Field(None, alias="merchantCountryCode", description="This field contains the merchant country code")
    merchant_id: Optional[StrictStr] = Field(None, alias="merchantId", description="This field contains the unique merchant identifier")
    merchant_name_location: Optional[StrictStr] = Field(None, alias="merchantNameLocation", description="This field contains the full merchant name and location data")
    original_authorization_code: Optional[StrictStr] = Field(None, alias="originalAuthorizationCode", description="This field contains the authorization code of the original transaction")
    pos_entry_mode: Optional[StrictStr] = Field(None, alias="posEntryMode", description="This field contains the pos entry code that identifies the actual method used to capture the account number, expiration date, and the PIN")
    settlement_date: Optional[StrictStr] = Field(None, alias="settlementDate", description="This field contains the settlement date")
    settlement_id: Optional[StrictInt] = Field(None, alias="settlementId", description="This field contains the settlement id")
    sub_bin: Optional[StrictStr] = Field(None, alias="subBin", description="This field is optional & accepts the sub-bin")
    token_number: Optional[StrictStr] = Field(None, alias="tokenNumber", description="This field contains the token number")
    token_requester_id: Optional[StrictStr] = Field(None, alias="tokenRequesterId", description="This field contains the token requester id")
    transaction_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="transactionAmount", description="This field contains the transaction amount.")
    transaction_currency: Optional[StrictStr] = Field(None, alias="transactionCurrency", description="This field contains the 3-letter ISO3 transaction currency code.")
    transaction_type: Optional[StrictStr] = Field(None, alias="transactionType", description="This field contains the type of transaction, it can be C or D")
    visa_transaction_id: Optional[StrictStr] = Field(None, alias="visaTransactionId", description="This field contains the Unique ID provided for transaction by VISA")
    __properties = ["authorizationCode", "billingAmount", "billingCurrency", "cardHashId", "cardNumber", "clientHashId", "clientId", "customerHashId", "exchangeRate", "labels", "logoId", "logoIdentifier", "maskCardNumber", "merchantCategoryCode", "merchantCountryCode", "merchantId", "merchantNameLocation", "originalAuthorizationCode", "posEntryMode", "settlementDate", "settlementId", "subBin", "tokenNumber", "tokenRequesterId", "transactionAmount", "transactionCurrency", "transactionType", "visaTransactionId"]

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
    def from_json(cls, json_str: str) -> SettlementRequestDTO:
        """Create an instance of SettlementRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of labels
        if self.labels:
            _dict['labels'] = self.labels.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SettlementRequestDTO:
        """Create an instance of SettlementRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SettlementRequestDTO.parse_obj(obj)

        _obj = SettlementRequestDTO.parse_obj({
            "authorization_code": obj.get("authorizationCode"),
            "billing_amount": obj.get("billingAmount"),
            "billing_currency": obj.get("billingCurrency"),
            "card_hash_id": obj.get("cardHashId"),
            "card_number": obj.get("cardNumber"),
            "client_hash_id": obj.get("clientHashId"),
            "client_id": obj.get("clientId"),
            "customer_hash_id": obj.get("customerHashId"),
            "exchange_rate": obj.get("exchangeRate"),
            "labels": Labels.from_dict(obj.get("labels")) if obj.get("labels") is not None else None,
            "logo_id": obj.get("logoId"),
            "logo_identifier": obj.get("logoIdentifier"),
            "mask_card_number": obj.get("maskCardNumber"),
            "merchant_category_code": obj.get("merchantCategoryCode"),
            "merchant_country_code": obj.get("merchantCountryCode"),
            "merchant_id": obj.get("merchantId"),
            "merchant_name_location": obj.get("merchantNameLocation"),
            "original_authorization_code": obj.get("originalAuthorizationCode"),
            "pos_entry_mode": obj.get("posEntryMode"),
            "settlement_date": obj.get("settlementDate"),
            "settlement_id": obj.get("settlementId"),
            "sub_bin": obj.get("subBin"),
            "token_number": obj.get("tokenNumber"),
            "token_requester_id": obj.get("tokenRequesterId"),
            "transaction_amount": obj.get("transactionAmount"),
            "transaction_currency": obj.get("transactionCurrency"),
            "transaction_type": obj.get("transactionType"),
            "visa_transaction_id": obj.get("visaTransactionId")
        })
        return _obj


