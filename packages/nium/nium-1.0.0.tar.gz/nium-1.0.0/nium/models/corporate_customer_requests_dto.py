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
from nium.models.business_details import BusinessDetails
from nium.models.product_customer_tag_dto import ProductCustomerTagDTO
from nium.models.risk_assessment_info import RiskAssessmentInfo

class CorporateCustomerRequestsDTO(BaseModel):
    """
    CorporateCustomerRequestsDTO
    """
    tags: Optional[conlist(ProductCustomerTagDTO)] = Field(None, description="This object contains the user defined key-value pairs provided by the client. The maximum number of tags allowed is 15.  AU: Optional EU: Optional UK: Optional SG: Optional")
    authentication_code: Optional[StrictStr] = Field(None, alias="authenticationCode", description="This field accepts the authentication code generated as part of SCA (Strong Customer Authentication). Note: : Authentication code must be passed if regulatory region of the program is UK or EU. Otherwise, please do not use this field and do not pass any value.")
    business_details: Optional[BusinessDetails] = Field(None, alias="businessDetails")
    client_id: Optional[StrictStr] = Field(None, alias="clientId", description="This field accepts the NIUM client Id of the customer. This field should be provided only while performing the re-initiate KYB process.  AU: Optional EU: Optional UK: Optional SG: Optional")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field accepts the unique customer identifier generated at the time of customer creation. It is received in the response of the previously executed Onboard Customer API. This field should be provided only while performing the re-initiate KYB process.  AU: Optional EU: Optional UK: Optional SG: Optional")
    region: Optional[StrictStr] = Field(None, description="This field accepts the region code for which onboarding has been triggered. The acceptable value are: AU EU UK SG  AU: Required EU: Required UK: Required SG: Required")
    risk_assessment_info: Optional[RiskAssessmentInfo] = Field(None, alias="riskAssessmentInfo")
    __properties = ["tags", "authenticationCode", "businessDetails", "clientId", "customerHashId", "region", "riskAssessmentInfo"]

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
    def from_json(cls, json_str: str) -> CorporateCustomerRequestsDTO:
        """Create an instance of CorporateCustomerRequestsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item in self.tags:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tags'] = _items
        # override the default output from pydantic by calling `to_dict()` of business_details
        if self.business_details:
            _dict['businessDetails'] = self.business_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of risk_assessment_info
        if self.risk_assessment_info:
            _dict['riskAssessmentInfo'] = self.risk_assessment_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateCustomerRequestsDTO:
        """Create an instance of CorporateCustomerRequestsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateCustomerRequestsDTO.parse_obj(obj)

        _obj = CorporateCustomerRequestsDTO.parse_obj({
            "tags": [ProductCustomerTagDTO.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "authentication_code": obj.get("authenticationCode"),
            "business_details": BusinessDetails.from_dict(obj.get("businessDetails")) if obj.get("businessDetails") is not None else None,
            "client_id": obj.get("clientId"),
            "customer_hash_id": obj.get("customerHashId"),
            "region": obj.get("region"),
            "risk_assessment_info": RiskAssessmentInfo.from_dict(obj.get("riskAssessmentInfo")) if obj.get("riskAssessmentInfo") is not None else None
        })
        return _obj


