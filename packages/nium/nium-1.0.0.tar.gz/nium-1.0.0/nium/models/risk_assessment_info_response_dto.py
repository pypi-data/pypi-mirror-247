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
from pydantic import BaseModel, Field, StrictStr, conlist

class RiskAssessmentInfoResponseDTO(BaseModel):
    """
    RiskAssessmentInfoResponseDTO
    """
    annual_turnover: Optional[StrictStr] = Field(None, alias="annualTurnover", description="This field contains the annual turnover of the business.")
    industry_sector: Optional[StrictStr] = Field(None, alias="industrySector", description="This field contains the industry sector of the business.")
    intended_use_of_account: Optional[StrictStr] = Field(None, alias="intendedUseOfAccount")
    total_employees: Optional[StrictStr] = Field(None, alias="totalEmployees", description="This field contains the total number of employee for the business.")
    transaction_countries: Optional[conlist(StrictStr)] = Field(None, alias="transactionCountries", description="This field contains the list of countries where the customer is expected to send/receive/spend from his account")
    __properties = ["annualTurnover", "industrySector", "intendedUseOfAccount", "totalEmployees", "transactionCountries"]

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
    def from_json(cls, json_str: str) -> RiskAssessmentInfoResponseDTO:
        """Create an instance of RiskAssessmentInfoResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RiskAssessmentInfoResponseDTO:
        """Create an instance of RiskAssessmentInfoResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RiskAssessmentInfoResponseDTO.parse_obj(obj)

        _obj = RiskAssessmentInfoResponseDTO.parse_obj({
            "annual_turnover": obj.get("annualTurnover"),
            "industry_sector": obj.get("industrySector"),
            "intended_use_of_account": obj.get("intendedUseOfAccount"),
            "total_employees": obj.get("totalEmployees"),
            "transaction_countries": obj.get("transactionCountries")
        })
        return _obj


