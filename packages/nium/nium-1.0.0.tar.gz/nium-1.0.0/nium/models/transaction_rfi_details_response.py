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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, validator
from nium.models.wallet_rfi_attribute_response import WalletRfiAttributeResponse

class TransactionRfiDetailsResponse(BaseModel):
    """
    TransactionRfiDetailsResponse
    """
    description: Optional[StrictStr] = Field(None, description="This field contains the description of the RFI.")
    document_type: Optional[StrictStr] = Field(None, alias="documentType", description="This field contains the type of the document if applicable, for example, POI, POA, etc.")
    mandatory: Optional[StrictBool] = Field(None, description="This flag signifies if the RFI is mandatory or not.")
    remarks: Optional[StrictStr] = Field(None, description="This field contains the remarks provided while raising the RFI.")
    required_data: Optional[conlist(WalletRfiAttributeResponse)] = Field(None, alias="requiredData", description="This array contains the required data for the RFI.")
    rfi_hash_id: Optional[StrictStr] = Field(None, alias="rfiHashId", description="This field contains the unique RFI hash ID.")
    rfi_id: Optional[StrictStr] = Field(None, alias="rfiId", description="This field contains the unique identifier for group of RFI raised for the customer transaction.")
    rfi_status: Optional[StrictStr] = Field(None, alias="rfiStatus", description="This field contains Transaction RFI status.")
    transaction_entity_type: Optional[StrictStr] = Field(None, alias="transactionEntityType", description="This field contains the type of the transaction entity. The possible values are: DEBTOR CREDITOR")
    type: Optional[StrictStr] = Field(None, description="This field contains the type of RFI. It could be document or data.")
    __properties = ["description", "documentType", "mandatory", "remarks", "requiredData", "rfiHashId", "rfiId", "rfiStatus", "transactionEntityType", "type"]

    @validator('rfi_status')
    def rfi_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NONE', 'IN_PROGRESS', 'COMPLETED', 'ACTION_REQUIRED', 'ERROR', 'REJECT', 'EXPIRED', 'RFI_REQUESTED', 'RFI_RESPONDED', 'UNKNOWN', 'INITIATED', 'PENDING', 'CLEAR', 'CLOSED'):
            raise ValueError("must be one of enum values ('NONE', 'IN_PROGRESS', 'COMPLETED', 'ACTION_REQUIRED', 'ERROR', 'REJECT', 'EXPIRED', 'RFI_REQUESTED', 'RFI_RESPONDED', 'UNKNOWN', 'INITIATED', 'PENDING', 'CLEAR', 'CLOSED')")
        return value

    @validator('transaction_entity_type')
    def transaction_entity_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('DEBTOR', 'CREDITOR'):
            raise ValueError("must be one of enum values ('DEBTOR', 'CREDITOR')")
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
    def from_json(cls, json_str: str) -> TransactionRfiDetailsResponse:
        """Create an instance of TransactionRfiDetailsResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in required_data (list)
        _items = []
        if self.required_data:
            for _item in self.required_data:
                if _item:
                    _items.append(_item.to_dict())
            _dict['requiredData'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionRfiDetailsResponse:
        """Create an instance of TransactionRfiDetailsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionRfiDetailsResponse.parse_obj(obj)

        _obj = TransactionRfiDetailsResponse.parse_obj({
            "description": obj.get("description"),
            "document_type": obj.get("documentType"),
            "mandatory": obj.get("mandatory"),
            "remarks": obj.get("remarks"),
            "required_data": [WalletRfiAttributeResponse.from_dict(_item) for _item in obj.get("requiredData")] if obj.get("requiredData") is not None else None,
            "rfi_hash_id": obj.get("rfiHashId"),
            "rfi_id": obj.get("rfiId"),
            "rfi_status": obj.get("rfiStatus"),
            "transaction_entity_type": obj.get("transactionEntityType"),
            "type": obj.get("type")
        })
        return _obj


