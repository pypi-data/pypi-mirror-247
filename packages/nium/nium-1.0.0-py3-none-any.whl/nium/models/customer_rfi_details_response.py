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
from nium.models.rfi_attribute_response import RfiAttributeResponse

class CustomerRfiDetailsResponse(BaseModel):
    """
    CustomerRfiDetailsResponse
    """
    description: Optional[StrictStr] = Field(None, description="This field contains the RFI description or field for which RFI is raised. The example values are passport, gender, etc.")
    document_type: Optional[StrictStr] = Field(None, alias="documentType", description="This field contains the type of document requested as part of RFI. The possible values are POI, POA, or NA.")
    mandatory: Optional[StrictBool] = Field(None, description="This flag determines the mandatory nature of the RFI.")
    remarks: Optional[StrictStr] = Field(None, description="This field contains the compliance officer’s remarks while raising the RFI.")
    required_data: Optional[conlist(RfiAttributeResponse)] = Field(None, alias="requiredData", description="This array contains objects with details of each mandatory RFI field that is required by NIUM team. It is mandatory to respond to an RFI with all the required fields. While responding to an RFI, you may refer these details. Example, Passport has many fields and an RFI may be raised for passport number. Referring this array, you may determine which field/value is needed and if it is an RFI for data or document.")
    rfi_hash_id: Optional[StrictStr] = Field(None, alias="rfiHashId", description="This field contains the unique identifier for each RFI raised for the customer.")
    rfi_id: Optional[StrictStr] = Field(None, alias="rfiId", description="This field contains the unique identifier for group of RFI raised for the customer.")
    rfi_status: Optional[StrictStr] = Field(None, alias="rfiStatus", description="This field contains status of the RFI. The possible values are:  RFI_REQUESTED   RFI_RESPONDED")
    rfi_type: Optional[StrictStr] = Field(None, alias="rfiType", description="This field contains type of the RFI.possible values are:  INTERNAL   EXTERNAL")
    type: Optional[StrictStr] = Field(None, description="This field contains the type of RFI. The possible values are data or document.")
    __properties = ["description", "documentType", "mandatory", "remarks", "requiredData", "rfiHashId", "rfiId", "rfiStatus", "rfiType", "type"]

    @validator('rfi_type')
    def rfi_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INTERNAL', 'EXTERNAL'):
            raise ValueError("must be one of enum values ('INTERNAL', 'EXTERNAL')")
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
    def from_json(cls, json_str: str) -> CustomerRfiDetailsResponse:
        """Create an instance of CustomerRfiDetailsResponse from a JSON string"""
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
    def from_dict(cls, obj: dict) -> CustomerRfiDetailsResponse:
        """Create an instance of CustomerRfiDetailsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerRfiDetailsResponse.parse_obj(obj)

        _obj = CustomerRfiDetailsResponse.parse_obj({
            "description": obj.get("description"),
            "document_type": obj.get("documentType"),
            "mandatory": obj.get("mandatory"),
            "remarks": obj.get("remarks"),
            "required_data": [RfiAttributeResponse.from_dict(_item) for _item in obj.get("requiredData")] if obj.get("requiredData") is not None else None,
            "rfi_hash_id": obj.get("rfiHashId"),
            "rfi_id": obj.get("rfiId"),
            "rfi_status": obj.get("rfiStatus"),
            "rfi_type": obj.get("rfiType"),
            "type": obj.get("type")
        })
        return _obj


