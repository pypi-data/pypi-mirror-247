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



from pydantic import BaseModel, Field, StrictStr, validator

class TransactionsReceiptDTO(BaseModel):
    """
    TransactionsReceiptDTO
    """
    document: StrictStr = Field(..., description="This field contains the receipt as uploaded in Base64 encoded format.")
    receipt_file_name: StrictStr = Field(..., alias="receiptFileName", description="This field contains the name of the file as uploaded.")
    receipt_type: StrictStr = Field(..., alias="receiptType", description="This field contains the file type of the uploaded receipt.")
    __properties = ["document", "receiptFileName", "receiptType"]

    @validator('receipt_type')
    def receipt_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('image/png', 'image/jpg', 'image/jpeg', 'application/pdf'):
            raise ValueError("must be one of enum values ('image/png', 'image/jpg', 'image/jpeg', 'application/pdf')")
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
    def from_json(cls, json_str: str) -> TransactionsReceiptDTO:
        """Create an instance of TransactionsReceiptDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionsReceiptDTO:
        """Create an instance of TransactionsReceiptDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionsReceiptDTO.parse_obj(obj)

        _obj = TransactionsReceiptDTO.parse_obj({
            "document": obj.get("document"),
            "receipt_file_name": obj.get("receiptFileName"),
            "receipt_type": obj.get("receiptType")
        })
        return _obj


