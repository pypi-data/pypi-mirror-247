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
from nium.models.product_document import ProductDocument

class ProductDocumentDetail(BaseModel):
    """
    ProductDocumentDetail
    """
    document: Optional[conlist(ProductDocument)] = Field(None, description="This array accepts the document to be uploaded.  AU: Optional EU: Optional UK: Optional SG: Optional")
    document_color: Optional[StrictStr] = Field(None, alias="documentColor", description="This field accepts the color for Medicare card.  AU: Optional EU: Optional UK: Optional SG: Optional")
    document_expiry_date: Optional[StrictStr] = Field(None, alias="documentExpiryDate", description="This field accepts the date of the document expiry This field is required only if the documents are being uploaded  AU: Optional EU: Conditional UK: Optional SG: Optional")
    document_holder_name: Optional[StrictStr] = Field(None, alias="documentHolderName", description="This field accepts the name of the document holder for the uploaded document.  AU: Optional EU: Required UK: Optional SG: Optional")
    document_issuance_country: Optional[StrictStr] = Field(None, alias="documentIssuanceCountry", description="This field accepts the name of the document issuing country.  AU: Optional EU: Conditional UK: Optional SG: Optional")
    document_issuance_state: Optional[StrictStr] = Field(None, alias="documentIssuanceState")
    document_issued_date: Optional[StrictStr] = Field(None, alias="documentIssuedDate", description="This field accepts the date of the document issuance. This field should be sent when available on the document.  AU: Optional EU: Optional UK: Optional SG: Optional")
    document_issuing_authority: Optional[StrictStr] = Field(None, alias="documentIssuingAuthority", description="This field accepts the name of the issuing authority of the document.  AU: Optional EU: Optional UK: Optional SG: Optional")
    document_number: Optional[StrictStr] = Field(None, alias="documentNumber", description="This field accepts the document number for the uploaded document. This field is required only if the documents are being uploaded  AU: Optional EU: Required UK: Optional SG: Optional")
    document_reference_number: Optional[StrictStr] = Field(None, alias="documentReferenceNumber", description="This field accepts the document reference number for the uploaded document.  AU: Conditional EU: Optional UK: Optional SG: Optional")
    document_type: Optional[StrictStr] = Field(None, alias="documentType", description="This field accepts the type of the document. The acceptable types of the documents are:  Business Registration Document Trust Deed Partnership Deed Association Deed Register of Directors Register of Shareholders  AU: Optional EU: Required UK: Optional SG: Optional")
    __properties = ["document", "documentColor", "documentExpiryDate", "documentHolderName", "documentIssuanceCountry", "documentIssuanceState", "documentIssuedDate", "documentIssuingAuthority", "documentNumber", "documentReferenceNumber", "documentType"]

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
    def from_json(cls, json_str: str) -> ProductDocumentDetail:
        """Create an instance of ProductDocumentDetail from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in document (list)
        _items = []
        if self.document:
            for _item in self.document:
                if _item:
                    _items.append(_item.to_dict())
            _dict['document'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductDocumentDetail:
        """Create an instance of ProductDocumentDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductDocumentDetail.parse_obj(obj)

        _obj = ProductDocumentDetail.parse_obj({
            "document": [ProductDocument.from_dict(_item) for _item in obj.get("document")] if obj.get("document") is not None else None,
            "document_color": obj.get("documentColor"),
            "document_expiry_date": obj.get("documentExpiryDate"),
            "document_holder_name": obj.get("documentHolderName"),
            "document_issuance_country": obj.get("documentIssuanceCountry"),
            "document_issuance_state": obj.get("documentIssuanceState"),
            "document_issued_date": obj.get("documentIssuedDate"),
            "document_issuing_authority": obj.get("documentIssuingAuthority"),
            "document_number": obj.get("documentNumber"),
            "document_reference_number": obj.get("documentReferenceNumber"),
            "document_type": obj.get("documentType")
        })
        return _obj


