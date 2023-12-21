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

class RiskAssessmentInfo(BaseModel):
    """
    RiskAssessmentInfo
    """
    annual_turnover: Optional[StrictStr] = Field(None, alias="annualTurnover", description="This field accepts the annual turnover for the corporate entity to be onboarded. Please refer to the [Glossary of Annual Turnover](https://docs.nium.com/baas/onboard-corporate-customer#glossary-of-annual-turnover): for the applicable values  AU: Required EU: Required UK: Required SG: Required")
    country_of_operation: Optional[conlist(StrictStr)] = Field(None, alias="countryOfOperation", description="This array accepts the list of countries where business operations exist apart from the registered country for the corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    industry_sector: Optional[StrictStr] = Field(None, alias="industrySector", description="This field accepts the industry sector for the corporate entity to be onboarded. Please refer to the [Glossary of Industry Sector](https://docs.nium.com/baas/onboard-corporate-customer#glossary-of-industry-sector): for the applicable values.  AU: Required EU: Required UK: Required SG: Required")
    intended_use_of_account: Optional[StrictStr] = Field(None, alias="intendedUseOfAccount")
    ofac_licence_present: Optional[StrictStr] = Field(None, alias="ofacLicencePresent", description="This field accepts Yes or No to ensure if the OFAC licence is present or not for the new corporate entity to be onboarded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    restricted_countries: Optional[conlist(StrictStr)] = Field(None, alias="restrictedCountries", description="This array accepts the restricted country names.  AU: Optional EU: Optional UK: Optional SG: Optional")
    risk_score: Optional[StrictStr] = Field(None, alias="riskScore", description="This field accepts the risk score assigned to the corporate. Note: This field will be used for capturing risk score assigned by clients to the corporate entity being onboarded. These fields will only be applicable for clients who have been pre-approved to manage the KYB process on their own and hence will be used for sending the risk score that was assigned to the corporate entity as part of the KYB process at client’s end.  AU: Optional EU: Optional UK: Optional SG: Optional")
    risk_severity: Optional[StrictStr] = Field(None, alias="riskSeverity", description="This field accepts the risk severity assigned to the corporate. The possible value are: HIGH MEDIUM LOW RESTRICTED Note: This field will be used for capturing risk severity assigned by clients to the corporate entity being onboarded. These fields will only be applicable for clients who have been pre-approved to manage the KYB process on their own and hence will be used for sending the risk severity that was assigned to the corporate entity as part of the KYB process at client’s end.  AU: Optional EU: Optional UK: Optional SG: Optional")
    total_employees: Optional[StrictStr] = Field(None, alias="totalEmployees", description="This field accepts the total number of employees for the corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    transaction_countries: Optional[conlist(StrictStr)] = Field(None, alias="transactionCountries")
    travel_restricted_country: Optional[StrictStr] = Field(None, alias="travelRestrictedCountry", description="This field accepts Yes or No to ensure if the country is travel restricted country or not for the new corporate entity to be onboarded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    __properties = ["annualTurnover", "countryOfOperation", "industrySector", "intendedUseOfAccount", "ofacLicencePresent", "restrictedCountries", "riskScore", "riskSeverity", "totalEmployees", "transactionCountries", "travelRestrictedCountry"]

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
    def from_json(cls, json_str: str) -> RiskAssessmentInfo:
        """Create an instance of RiskAssessmentInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RiskAssessmentInfo:
        """Create an instance of RiskAssessmentInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RiskAssessmentInfo.parse_obj(obj)

        _obj = RiskAssessmentInfo.parse_obj({
            "annual_turnover": obj.get("annualTurnover"),
            "country_of_operation": obj.get("countryOfOperation"),
            "industry_sector": obj.get("industrySector"),
            "intended_use_of_account": obj.get("intendedUseOfAccount"),
            "ofac_licence_present": obj.get("ofacLicencePresent"),
            "restricted_countries": obj.get("restrictedCountries"),
            "risk_score": obj.get("riskScore"),
            "risk_severity": obj.get("riskSeverity"),
            "total_employees": obj.get("totalEmployees"),
            "transaction_countries": obj.get("transactionCountries"),
            "travel_restricted_country": obj.get("travelRestrictedCountry")
        })
        return _obj


