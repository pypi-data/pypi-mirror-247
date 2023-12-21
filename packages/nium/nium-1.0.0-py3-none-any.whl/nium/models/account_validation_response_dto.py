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
from nium.models.beneficiary_details_dto import BeneficiaryDetailsDTO

class AccountValidationResponseDTO(BaseModel):
    """
    AccountValidationResponseDTO
    """
    account_validation_id: Optional[StrictStr] = Field(None, alias="accountValidationId", description="This field contains the unique identifier.")
    beneficiary: Optional[BeneficiaryDetailsDTO] = None
    status: Optional[StrictStr] = Field(None, description="This will provide the status of the CoP call. This can be one of confirmation_in_progress, verified, not_verified or not_supported.")
    __properties = ["accountValidationId", "beneficiary", "status"]

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
    def from_json(cls, json_str: str) -> AccountValidationResponseDTO:
        """Create an instance of AccountValidationResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of beneficiary
        if self.beneficiary:
            _dict['beneficiary'] = self.beneficiary.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AccountValidationResponseDTO:
        """Create an instance of AccountValidationResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AccountValidationResponseDTO.parse_obj(obj)

        _obj = AccountValidationResponseDTO.parse_obj({
            "account_validation_id": obj.get("accountValidationId"),
            "beneficiary": BeneficiaryDetailsDTO.from_dict(obj.get("beneficiary")) if obj.get("beneficiary") is not None else None,
            "status": obj.get("status")
        })
        return _obj


