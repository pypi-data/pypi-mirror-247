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
from nium.models.corporate_address import CorporateAddress
from nium.models.corporate_contact_details import CorporateContactDetails
from nium.models.corporate_document_detail import CorporateDocumentDetail
from nium.models.corporate_professional_details import CorporateProfessionalDetails

class CorporateStakeholderDetails(BaseModel):
    """
    CorporateStakeholderDetails
    """
    address: Optional[CorporateAddress] = None
    contact_details: Optional[CorporateContactDetails] = Field(None, alias="contactDetails")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field accepts the date of birth of the stakeholder in yyyy-MM-dd format.  AU: Optional EU: Required UK: Required SG: Required")
    document_details: Optional[conlist(CorporateDocumentDetail)] = Field(None, alias="documentDetails", description="This array accepts the document details for the stakeholder. This field is required only if the documents are being uploaded.  AU: Optional EU: Conditional UK: Optional SG: Optional")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field contains the first name of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field contains the last name of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field contains the middle name of the stakeholder.  AU: Optional EU: Optional UK: Optional SG: Optional")
    nationality: Optional[StrictStr] = Field(None, description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the nationality of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    professional_details: Optional[conlist(CorporateProfessionalDetails)] = Field(None, alias="professionalDetails", description="This array accepts the professional details of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    __properties = ["address", "contactDetails", "dateOfBirth", "documentDetails", "firstName", "lastName", "middleName", "nationality", "professionalDetails"]

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
    def from_json(cls, json_str: str) -> CorporateStakeholderDetails:
        """Create an instance of CorporateStakeholderDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of address
        if self.address:
            _dict['address'] = self.address.to_dict()
        # override the default output from pydantic by calling `to_dict()` of contact_details
        if self.contact_details:
            _dict['contactDetails'] = self.contact_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in document_details (list)
        _items = []
        if self.document_details:
            for _item in self.document_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['documentDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in professional_details (list)
        _items = []
        if self.professional_details:
            for _item in self.professional_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['professionalDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateStakeholderDetails:
        """Create an instance of CorporateStakeholderDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateStakeholderDetails.parse_obj(obj)

        _obj = CorporateStakeholderDetails.parse_obj({
            "address": CorporateAddress.from_dict(obj.get("address")) if obj.get("address") is not None else None,
            "contact_details": CorporateContactDetails.from_dict(obj.get("contactDetails")) if obj.get("contactDetails") is not None else None,
            "date_of_birth": obj.get("dateOfBirth"),
            "document_details": [CorporateDocumentDetail.from_dict(_item) for _item in obj.get("documentDetails")] if obj.get("documentDetails") is not None else None,
            "first_name": obj.get("firstName"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "nationality": obj.get("nationality"),
            "professional_details": [CorporateProfessionalDetails.from_dict(_item) for _item in obj.get("professionalDetails")] if obj.get("professionalDetails") is not None else None
        })
        return _obj


