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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist

class ProductCorporateCustomerResponseDTO(BaseModel):
    """
    ProductCorporateCustomerResponseDTO
    """
    case_id: Optional[StrictStr] = Field(None, alias="caseId", description="This field contains the compliance case Id of the customer.")
    client_id: Optional[StrictStr] = Field(None, alias="clientId", description="This field contains the NIUM client Id of the customer.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique customer identifier generated at the time of customer creation.")
    errors: Optional[conlist(Dict[str, Any])] = Field(None, description="This field contains the list of error code and description from compliance service.")
    redirect_url: Optional[StrictStr] = Field(None, alias="redirectUrl", description="This field contains the redirect URL of the compliance authority.")
    remarks: Optional[StrictStr] = Field(None, description="This field contains the remarks auto-generated during the compliance process.")
    status: Optional[StrictStr] = Field(None, description="This field contains the compliance status. As a response of this API, the only possible value of status is IN_PROGRESS.")
    wallet_hash_id: Optional[StrictStr] = Field(None, alias="walletHashId", description="This field contains the unique wallet identifier generated simultaneously with customer creation.")
    __properties = ["caseId", "clientId", "customerHashId", "errors", "redirectUrl", "remarks", "status", "walletHashId"]

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
    def from_json(cls, json_str: str) -> ProductCorporateCustomerResponseDTO:
        """Create an instance of ProductCorporateCustomerResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductCorporateCustomerResponseDTO:
        """Create an instance of ProductCorporateCustomerResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductCorporateCustomerResponseDTO.parse_obj(obj)

        _obj = ProductCorporateCustomerResponseDTO.parse_obj({
            "case_id": obj.get("caseId"),
            "client_id": obj.get("clientId"),
            "customer_hash_id": obj.get("customerHashId"),
            "errors": obj.get("errors"),
            "redirect_url": obj.get("redirectUrl"),
            "remarks": obj.get("remarks"),
            "status": obj.get("status"),
            "wallet_hash_id": obj.get("walletHashId")
        })
        return _obj


