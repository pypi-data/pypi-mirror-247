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

class CorporateDocumentDetailsDTO(BaseModel):
    """
    CorporateDocumentDetailsDTO
    """
    document_issuance_country: Optional[StrictStr] = Field(None, alias="documentIssuanceCountry", description="This field contains the identification issuance Country value of each uploaded document, which was provided during document upload.")
    identification_type: Optional[StrictStr] = Field(None, alias="identificationType", description="This field contains the identification document type. The possible identification document type are: AU: Passport, Driver Licence, Medicare Number  UK & EU: National ID & Passport")
    identification_value: Optional[StrictStr] = Field(None, alias="identificationValue", description="This field contains the identification document value of each uploaded document, which was provided during document upload.")
    __properties = ["documentIssuanceCountry", "identificationType", "identificationValue"]

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
    def from_json(cls, json_str: str) -> CorporateDocumentDetailsDTO:
        """Create an instance of CorporateDocumentDetailsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateDocumentDetailsDTO:
        """Create an instance of CorporateDocumentDetailsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateDocumentDetailsDTO.parse_obj(obj)

        _obj = CorporateDocumentDetailsDTO.parse_obj({
            "document_issuance_country": obj.get("documentIssuanceCountry"),
            "identification_type": obj.get("identificationType"),
            "identification_value": obj.get("identificationValue")
        })
        return _obj


