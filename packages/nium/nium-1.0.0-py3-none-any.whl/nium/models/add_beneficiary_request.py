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
from nium.models.beneficiary_detail_request import BeneficiaryDetailRequest
from nium.models.payout_request import PayoutRequest

class AddBeneficiaryRequest(BaseModel):
    """
    AddBeneficiaryRequest
    """
    authentication_code: Optional[StrictStr] = Field(None, alias="authenticationCode", description="This field accepts the authentication code generated as part of SCA (Strong Customer Authentication). Note: Authentication code must be passed if regulatory region of the program is UK or EU. Otherwise, please do not use this field and do not pass any value.")
    beneficiary_detail: BeneficiaryDetailRequest = Field(..., alias="beneficiaryDetail")
    payout_detail: PayoutRequest = Field(..., alias="payoutDetail")
    __properties = ["authenticationCode", "beneficiaryDetail", "payoutDetail"]

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
    def from_json(cls, json_str: str) -> AddBeneficiaryRequest:
        """Create an instance of AddBeneficiaryRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of beneficiary_detail
        if self.beneficiary_detail:
            _dict['beneficiaryDetail'] = self.beneficiary_detail.to_dict()
        # override the default output from pydantic by calling `to_dict()` of payout_detail
        if self.payout_detail:
            _dict['payoutDetail'] = self.payout_detail.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddBeneficiaryRequest:
        """Create an instance of AddBeneficiaryRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddBeneficiaryRequest.parse_obj(obj)

        _obj = AddBeneficiaryRequest.parse_obj({
            "authentication_code": obj.get("authenticationCode"),
            "beneficiary_detail": BeneficiaryDetailRequest.from_dict(obj.get("beneficiaryDetail")) if obj.get("beneficiaryDetail") is not None else None,
            "payout_detail": PayoutRequest.from_dict(obj.get("payoutDetail")) if obj.get("payoutDetail") is not None else None
        })
        return _obj


