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
from nium.models.identification_document_dto import IdentificationDocumentDTO

class ComplianceIdentificationDocDTO(BaseModel):
    """
    ComplianceIdentificationDocDTO
    """
    identification_doc_color: Optional[StrictStr] = Field(None, alias="identificationDocColor", description="This field accepts the color of the medicare card which may be one of three values - G, B, Y. It is mandatory for medicare card.")
    identification_doc_expiry: Optional[StrictStr] = Field(None, alias="identificationDocExpiry", description="This field accepts the identification document expiry date. The valid values are: dateOfExpiry for passport dateOfExpiry for government letter ")
    identification_doc_holder_name: Optional[StrictStr] = Field(None, alias="identificationDocHolderName", description="This field accepts the name of the document holder exactly according to the proof of identity document uploaded.")
    identification_doc_issuance_country: Optional[StrictStr] = Field(None, alias="identificationDocIssuanceCountry", description="This field accepts the country of the issuance for the document being uploaded.")
    identification_doc_reference_number: Optional[StrictStr] = Field(None, alias="identificationDocReferenceNumber", description="This field is mandatory for medicare card and accepts the document reference number for the following documents: Government Letter Bank Statement Utility Bill Employer Letter Medicare Card")
    identification_document: Optional[conlist(IdentificationDocumentDTO)] = Field(None, alias="identificationDocument", description="It is an array of actual Base-64 documents as required. The maximum allowed size of this payload is 10MB. A separate object is needed for each document image.")
    identification_issuing_authority: Optional[StrictStr] = Field(None, alias="identificationIssuingAuthority", description="This field accepts the authorized issuer of the document for example, the name of the government agency issuing the document.")
    identification_issuing_date: Optional[StrictStr] = Field(None, alias="identificationIssuingDate", description="This field accepts the identification issuing date. The valid values are: dateOfIssue for FIN dateOfIssue for passport dateOfIssue for GovernmentLetter statementGeneratedOn for BankStatement billGeneratedOn for utilityBill")
    identification_type: StrictStr = Field(..., alias="identificationType", description="This field accepts the identificationType for the document being uploaded for KYC.  Note: For EU, the acceptable values for identificationType are Passport, National ID.")
    identification_value: Optional[StrictStr] = Field(None, alias="identificationValue", description="This field accepts the identification value.)")
    __properties = ["identificationDocColor", "identificationDocExpiry", "identificationDocHolderName", "identificationDocIssuanceCountry", "identificationDocReferenceNumber", "identificationDocument", "identificationIssuingAuthority", "identificationIssuingDate", "identificationType", "identificationValue"]

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
    def from_json(cls, json_str: str) -> ComplianceIdentificationDocDTO:
        """Create an instance of ComplianceIdentificationDocDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in identification_document (list)
        _items = []
        if self.identification_document:
            for _item in self.identification_document:
                if _item:
                    _items.append(_item.to_dict())
            _dict['identificationDocument'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ComplianceIdentificationDocDTO:
        """Create an instance of ComplianceIdentificationDocDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ComplianceIdentificationDocDTO.parse_obj(obj)

        _obj = ComplianceIdentificationDocDTO.parse_obj({
            "identification_doc_color": obj.get("identificationDocColor"),
            "identification_doc_expiry": obj.get("identificationDocExpiry"),
            "identification_doc_holder_name": obj.get("identificationDocHolderName"),
            "identification_doc_issuance_country": obj.get("identificationDocIssuanceCountry"),
            "identification_doc_reference_number": obj.get("identificationDocReferenceNumber"),
            "identification_document": [IdentificationDocumentDTO.from_dict(_item) for _item in obj.get("identificationDocument")] if obj.get("identificationDocument") is not None else None,
            "identification_issuing_authority": obj.get("identificationIssuingAuthority"),
            "identification_issuing_date": obj.get("identificationIssuingDate"),
            "identification_type": obj.get("identificationType"),
            "identification_value": obj.get("identificationValue")
        })
        return _obj


