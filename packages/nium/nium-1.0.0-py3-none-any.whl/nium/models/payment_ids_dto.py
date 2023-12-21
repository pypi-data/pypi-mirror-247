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

class PaymentIdsDTO(BaseModel):
    """
    PaymentIdsDTO
    """
    account_name: Optional[StrictStr] = Field(None, alias="accountName", description="This field contains the name of the account.")
    account_type: Optional[StrictStr] = Field(None, alias="accountType", description="This field contains the type of an account.")
    bank_address: Optional[StrictStr] = Field(None, alias="bankAddress", description="This field contains the full address of the bank.")
    bank_name: Optional[StrictStr] = Field(None, alias="bankName", description="This field contains the bank name.The possible values are:")
    bank_name_full: Optional[StrictStr] = Field(None, alias="bankNameFull", description="This field contains the full name of the bank.")
    currency_code: Optional[StrictStr] = Field(None, alias="currencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    routing_code_type1: Optional[StrictStr] = Field(None, alias="routingCodeType1", description="This field contains the routing code type 1.")
    routing_code_type2: Optional[StrictStr] = Field(None, alias="routingCodeType2", description="This field contains the routing code type 2.")
    routing_code_value1: Optional[StrictStr] = Field(None, alias="routingCodeValue1", description="This field contains the routing code type 1 value.")
    routing_code_value2: Optional[StrictStr] = Field(None, alias="routingCodeValue2", description="This field contains the routing code type 2 value.")
    unique_payer_id: Optional[StrictStr] = Field(None, alias="uniquePayerId", description="This is a unique email Id provided to the customer in addition to uniquePaymentId for supported regions and configuration, or else it will be null, for example, abc12_ca@nium.com.")
    unique_payment_id: Optional[StrictStr] = Field(None, alias="uniquePaymentId", description="This field is the virtual account number per currency provided to customers for supported regions and configuration, for example, IBAN in EU, virtual account number from Moonova in AU, or else, it will be null.")
    __properties = ["accountName", "accountType", "bankAddress", "bankName", "bankNameFull", "currencyCode", "routingCodeType1", "routingCodeType2", "routingCodeValue1", "routingCodeValue2", "uniquePayerId", "uniquePaymentId"]

    @validator('account_type')
    def account_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('LOCAL', 'GLOBAL', 'LOCAL+GLOBAL'):
            raise ValueError("must be one of enum values ('LOCAL', 'GLOBAL', 'LOCAL+GLOBAL')")
        return value

    @validator('bank_name')
    def bank_name_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('BOL_LT', 'MONOOVA_AU', 'DBS_HK', 'DBS_SG', 'JPM_AU', 'JPM_SG', 'CB_GB', 'CFSB_US'):
            raise ValueError("must be one of enum values ('BOL_LT', 'MONOOVA_AU', 'DBS_HK', 'DBS_SG', 'JPM_AU', 'JPM_SG', 'CB_GB', 'CFSB_US')")
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
    def from_json(cls, json_str: str) -> PaymentIdsDTO:
        """Create an instance of PaymentIdsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PaymentIdsDTO:
        """Create an instance of PaymentIdsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaymentIdsDTO.parse_obj(obj)

        _obj = PaymentIdsDTO.parse_obj({
            "account_name": obj.get("accountName"),
            "account_type": obj.get("accountType"),
            "bank_address": obj.get("bankAddress"),
            "bank_name": obj.get("bankName"),
            "bank_name_full": obj.get("bankNameFull"),
            "currency_code": obj.get("currencyCode"),
            "routing_code_type1": obj.get("routingCodeType1"),
            "routing_code_type2": obj.get("routingCodeType2"),
            "routing_code_value1": obj.get("routingCodeValue1"),
            "routing_code_value2": obj.get("routingCodeValue2"),
            "unique_payer_id": obj.get("uniquePayerId"),
            "unique_payment_id": obj.get("uniquePaymentId")
        })
        return _obj


