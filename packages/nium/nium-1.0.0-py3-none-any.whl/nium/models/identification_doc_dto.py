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

class IdentificationDocDTO(BaseModel):
    """
    IdentificationDocDTO
    """
    identification_doc_color: Optional[StrictStr] = Field(None, alias="identificationDocColor", description="This field accepts the color of the document being uploaded.")
    identification_doc_expiry: Optional[StrictStr] = Field(None, alias="identificationDocExpiry", description="This field accepts the expiry date of the document being uploaded.")
    identification_doc_holder_name: Optional[StrictStr] = Field(None, alias="identificationDocHolderName", description="This field accepts the name of the customer as per the document being uploaded.")
    identification_doc_issuance_country: Optional[StrictStr] = Field(None, alias="identificationDocIssuanceCountry", description="This field accepts the issuing country of the document being uploaded.")
    identification_doc_reference_number: Optional[StrictStr] = Field(None, alias="identificationDocReferenceNumber", description="This field accepts the reference number of the document being uploaded.")
    identification_document: Optional[conlist(IdentificationDocumentDTO)] = Field(None, alias="identificationDocument", description="It is an array of actual documents for the data provided in previous fields. We support a maximum of 4 files in the array, and the total max size should be less than 10 MB. A separate object is needed for each document image.")
    identification_issuing_authority: Optional[StrictStr] = Field(None, alias="identificationIssuingAuthority", description="This field accepts the authority issuing the document being uploaded.")
    identification_issuing_date: Optional[StrictStr] = Field(None, alias="identificationIssuingDate", description="This field accepts the date of issuance of the document being uploaded. The format should be yyyy-mm-dd. Example, 2010-10-10.")
    identification_type: Optional[StrictStr] = Field(None, alias="identificationType", description="This field accepts the type of document being uploaded.")
    identification_value: Optional[StrictStr] = Field(None, alias="identificationValue", description="This field accepts the unique document id being uploaded.")
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
    def from_json(cls, json_str: str) -> IdentificationDocDTO:
        """Create an instance of IdentificationDocDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> IdentificationDocDTO:
        """Create an instance of IdentificationDocDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IdentificationDocDTO.parse_obj(obj)

        _obj = IdentificationDocDTO.parse_obj({
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


