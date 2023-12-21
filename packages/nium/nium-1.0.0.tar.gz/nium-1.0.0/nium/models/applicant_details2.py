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


from typing import Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, validator
from nium.models.contact_details import ContactDetails
from nium.models.product_address import ProductAddress
from nium.models.product_document_detail import ProductDocumentDetail
from nium.models.product_professional_details import ProductProfessionalDetails
from nium.models.product_tax_details import ProductTaxDetails

class ApplicantDetails2(BaseModel):
    """
    ApplicantDetails2
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo")
    address: Optional[ProductAddress] = None
    birth_country: Optional[StrictStr] = Field(None, alias="birthCountry")
    contact_details: Optional[ContactDetails] = Field(None, alias="contactDetails")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth")
    document_details: Optional[ProductDocumentDetail] = Field(None, alias="documentDetails")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field accepts the first name of the applicant.")
    gender: Optional[StrictStr] = Field(None, description="This field accepts the gender of the applicant.")
    is_resident: Optional[StrictStr] = Field(None, alias="isResident")
    kyc_mode: Optional[StrictStr] = Field(None, alias="kycMode", description="This field accepts the registered business name of the business partner.")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field accepts the last name of the applicant.")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field accepts the middle name of the applicant.")
    nationality: Optional[StrictStr] = Field(None, description="This field accepts the [2-letter ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the nationality of the applicant.")
    occupation: Optional[StrictStr] = Field(None, description="This field accepts the customer's occupation. Refer to [Enum values](https://docs.nium.com/apis/docs/unified-add-customer-api) for the description.   Note: This field is mandatory for CA.")
    professional_details: Optional[conlist(ProductProfessionalDetails)] = Field(None, alias="professionalDetails", description="This array accepts the professional details of the applicant.")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field accepts the reference ID of the applicant for which the RFI is raised.")
    tax_details: Optional[conlist(ProductTaxDetails)] = Field(None, alias="taxDetails")
    __properties = ["additionalInfo", "address", "birthCountry", "contactDetails", "dateOfBirth", "documentDetails", "firstName", "gender", "isResident", "kycMode", "lastName", "middleName", "nationality", "occupation", "professionalDetails", "referenceId", "taxDetails"]

    @validator('occupation')
    def occupation_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('OC0001', 'OC1001', 'OC1002', 'OC1003', 'OC1110', 'OC1120', 'OC1201', 'OC1210', 'OC1211', 'OC1220', 'OC1310', 'OC1311', 'OC1320', 'OC1410', 'OC1411', 'OC1420', 'OC1430', 'OC1440', 'OC2001', 'OC2110', 'OC2111', 'OC2112', 'OC2120', 'OC2121', 'OC2122', 'OC2123', 'OC2130', 'OC2131', 'OC2132', 'OC2133', 'OC2139', 'OC2210', 'OC2211', 'OC2221', 'OC2222', 'OC2223', 'OC2230', 'OC2231', 'OC3001', 'OC3110', 'OC3111', 'OC3112', 'OC3120', 'OC3130', 'OC3210', 'OC3211', 'OC3212', 'OC3220', 'OC3310', 'OC4001', 'OC4002', 'OC4003', 'OC4004', 'OC4110', 'OC4120', 'OC4121', 'OC4122', 'OC4130', 'OC4131', 'OC4132', 'OC4140', 'OC4210', 'OC4220', 'OC4310', 'OC4320', 'OC4410', 'OC4420', 'OC4510', 'OC5001', 'OC5110', 'OC5111', 'OC5112', 'OC5210', 'OC5211', 'OC5212', 'OC5310', 'OC5311', 'OC5312', 'OC5320', 'OC5410', 'OC5510', 'OC6001', 'OC6002', 'OC6003', 'OC6004', 'OC6201', 'OC6202', 'OC6210', 'OC6220', 'OC6310', 'OC6320', 'OC6321', 'OC6322', 'OC6410', 'OC6420', 'OC6430', 'OC6431', 'OC6432', 'OC6440', 'OC6441', 'OC6510', 'OC6520', 'OC6521', 'OC6522', 'OC6531', 'OC6532', 'OC7001', 'OC7002', 'OC7201', 'OC7202', 'OC7210', 'OC7220', 'OC7230', 'OC7231', 'OC7232', 'OC7240', 'OC7241', 'OC7242', 'OC7250', 'OC7260', 'OC7299', 'OC7310', 'OC7311', 'OC7320', 'OC7330', 'OC7331', 'OC7340', 'OC7410', 'OC7420', 'OC7510', 'OC7511', 'OC7520', 'OC7521', 'OC8001', 'OC8002', 'OC8201', 'OC8202', 'OC8203', 'OC8310', 'OC8311', 'OC8312', 'OC8410', 'OC8411', 'OC8412', 'OC8510', 'OC8511', 'OC8512', 'OC9001', 'OC9201', 'OC9202', 'OC9210', 'OC9310', 'OC9320', 'OC9410', 'OC9411', 'OC9412', 'OC9413', 'OC9414', 'OC9415', 'OC9420', 'OC9421', 'OC9510'):
            raise ValueError("must be one of enum values ('OC0001', 'OC1001', 'OC1002', 'OC1003', 'OC1110', 'OC1120', 'OC1201', 'OC1210', 'OC1211', 'OC1220', 'OC1310', 'OC1311', 'OC1320', 'OC1410', 'OC1411', 'OC1420', 'OC1430', 'OC1440', 'OC2001', 'OC2110', 'OC2111', 'OC2112', 'OC2120', 'OC2121', 'OC2122', 'OC2123', 'OC2130', 'OC2131', 'OC2132', 'OC2133', 'OC2139', 'OC2210', 'OC2211', 'OC2221', 'OC2222', 'OC2223', 'OC2230', 'OC2231', 'OC3001', 'OC3110', 'OC3111', 'OC3112', 'OC3120', 'OC3130', 'OC3210', 'OC3211', 'OC3212', 'OC3220', 'OC3310', 'OC4001', 'OC4002', 'OC4003', 'OC4004', 'OC4110', 'OC4120', 'OC4121', 'OC4122', 'OC4130', 'OC4131', 'OC4132', 'OC4140', 'OC4210', 'OC4220', 'OC4310', 'OC4320', 'OC4410', 'OC4420', 'OC4510', 'OC5001', 'OC5110', 'OC5111', 'OC5112', 'OC5210', 'OC5211', 'OC5212', 'OC5310', 'OC5311', 'OC5312', 'OC5320', 'OC5410', 'OC5510', 'OC6001', 'OC6002', 'OC6003', 'OC6004', 'OC6201', 'OC6202', 'OC6210', 'OC6220', 'OC6310', 'OC6320', 'OC6321', 'OC6322', 'OC6410', 'OC6420', 'OC6430', 'OC6431', 'OC6432', 'OC6440', 'OC6441', 'OC6510', 'OC6520', 'OC6521', 'OC6522', 'OC6531', 'OC6532', 'OC7001', 'OC7002', 'OC7201', 'OC7202', 'OC7210', 'OC7220', 'OC7230', 'OC7231', 'OC7232', 'OC7240', 'OC7241', 'OC7242', 'OC7250', 'OC7260', 'OC7299', 'OC7310', 'OC7311', 'OC7320', 'OC7330', 'OC7331', 'OC7340', 'OC7410', 'OC7420', 'OC7510', 'OC7511', 'OC7520', 'OC7521', 'OC8001', 'OC8002', 'OC8201', 'OC8202', 'OC8203', 'OC8310', 'OC8311', 'OC8312', 'OC8410', 'OC8411', 'OC8412', 'OC8510', 'OC8511', 'OC8512', 'OC9001', 'OC9201', 'OC9202', 'OC9210', 'OC9310', 'OC9320', 'OC9410', 'OC9411', 'OC9412', 'OC9413', 'OC9414', 'OC9415', 'OC9420', 'OC9421', 'OC9510')")
        return value

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
    def from_json(cls, json_str: str) -> ApplicantDetails2:
        """Create an instance of ApplicantDetails2 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of document_details
        if self.document_details:
            _dict['documentDetails'] = self.document_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in professional_details (list)
        _items = []
        if self.professional_details:
            for _item in self.professional_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['professionalDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tax_details (list)
        _items = []
        if self.tax_details:
            for _item in self.tax_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taxDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ApplicantDetails2:
        """Create an instance of ApplicantDetails2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ApplicantDetails2.parse_obj(obj)

        _obj = ApplicantDetails2.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "address": ProductAddress.from_dict(obj.get("address")) if obj.get("address") is not None else None,
            "birth_country": obj.get("birthCountry"),
            "contact_details": ContactDetails.from_dict(obj.get("contactDetails")) if obj.get("contactDetails") is not None else None,
            "date_of_birth": obj.get("dateOfBirth"),
            "document_details": ProductDocumentDetail.from_dict(obj.get("documentDetails")) if obj.get("documentDetails") is not None else None,
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "is_resident": obj.get("isResident"),
            "kyc_mode": obj.get("kycMode"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "nationality": obj.get("nationality"),
            "occupation": obj.get("occupation"),
            "professional_details": [ProductProfessionalDetails.from_dict(_item) for _item in obj.get("professionalDetails")] if obj.get("professionalDetails") is not None else None,
            "reference_id": obj.get("referenceId"),
            "tax_details": [ProductTaxDetails.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None
        })
        return _obj


