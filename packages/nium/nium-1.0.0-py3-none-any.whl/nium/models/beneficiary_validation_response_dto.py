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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class BeneficiaryValidationResponseDTO(BaseModel):
    """
    BeneficiaryValidationResponseDTO
    """
    beneficiary_bank_code: Optional[StrictStr] = Field(None, alias="beneficiaryBankCode", description="This field contains beneficiary bank code if the payout method is proxy and proxy type is VPA.")
    beneficiary_name: Optional[StrictStr] = Field(None, alias="beneficiaryName", description="This field contains beneficiary name if the payout method is proxy.")
    status: Optional[StrictStr] = Field(None, description="This field contains the status only when the proxy type is VPA. The possible values are: VE: Virtual Address Available F: Failed VN: Virtual Address not Available")
    valid: Optional[StrictBool] = Field(None, description="This field will return true if the provided details are valid otherwise false.")
    __properties = ["beneficiaryBankCode", "beneficiaryName", "status", "valid"]

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
    def from_json(cls, json_str: str) -> BeneficiaryValidationResponseDTO:
        """Create an instance of BeneficiaryValidationResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BeneficiaryValidationResponseDTO:
        """Create an instance of BeneficiaryValidationResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BeneficiaryValidationResponseDTO.parse_obj(obj)

        _obj = BeneficiaryValidationResponseDTO.parse_obj({
            "beneficiary_bank_code": obj.get("beneficiaryBankCode"),
            "beneficiary_name": obj.get("beneficiaryName"),
            "status": obj.get("status"),
            "valid": obj.get("valid")
        })
        return _obj


