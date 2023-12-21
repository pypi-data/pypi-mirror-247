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
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, validator
from nium.models.tax_details_response_dto import TaxDetailsResponseDTO

class IndividualCustomerResponseDTO(BaseModel):
    """
    IndividualCustomerResponseDTO
    """
    billing_address1: Optional[StrictStr] = Field(None, alias="billingAddress1")
    billing_address2: Optional[StrictStr] = Field(None, alias="billingAddress2", description="This field contains the line 2 of individual customer’s billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_city: Optional[StrictStr] = Field(None, alias="billingCity", description="This field contains the city of individual customer’s billing address.")
    billing_country: Optional[StrictStr] = Field(None, alias="billingCountry", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_landmark: Optional[StrictStr] = Field(None, alias="billingLandmark", description="This field contains the landmark for individual customer’s billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_state: Optional[StrictStr] = Field(None, alias="billingState", description="This field contains the state of individual customer’s billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_zip_code: Optional[StrictStr] = Field(None, alias="billingZipCode", description="This field contains the zip code of individual customer’s  billing address.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field contains the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for identifying the country prefix to the customer’s mobile number.")
    country_of_birth: Optional[StrictStr] = Field(None, alias="countryOfBirth", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s country of birth.")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field contains the date of birth of the customer [INDIVIDUAL] or applicant [CORPORATE] in YYYY-MM-DD format.")
    designation: Optional[StrictStr] = Field(None, description="This field contains the designation of an employee, if provided during customer onboarding. Otherwise, it contains null.")
    email: Optional[StrictStr] = Field(None, description="This field contains the unique email address of the customer.")
    employee_id: Optional[StrictStr] = Field(None, alias="employeeId", description="This field contains the employee ID of an employee, if provided during customer onboarding. Otherwise, it contains null.")
    estimated_monthly_funding: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFunding", description="This field contains the estimated monthly funding amount expected in the wallet. This field is required when estimatedMonthlyFundingCurrency field is provided in the request.")
    estimated_monthly_funding_currency: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFundingCurrency", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) in which estimated monthly funding is expected in the wallet, for example, SGD.")
    expected_countries_to_send_receive_from: Optional[conlist(StrictStr)] = Field(None, alias="expectedCountriesToSendReceiveFrom", description="This is an array of 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) to allow the client to capture the expected countries to send/receive international payments from. This field is required when internationalPaymentsSupported field is true, for example, [“FR”, “DE”].")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field contains the first name of the individual customer.")
    gender: Optional[StrictStr] = Field(None, description="This field contains the gender of the individual customer, if provided during customer onboarding. The possible values are - Male, Female, or Others. Otherwise, it contains null.")
    identification_data: Optional[conlist(Dict[str, StrictStr])] = Field(None, alias="identificationData", description="This array contains objects consisting of type and value of each uploaded document.")
    international_payments_supported: Optional[StrictBool] = Field(None, alias="internationalPaymentsSupported", description="This field indicates if the customer will be doing International send/receive payments. The default value will be false.")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field contains the last name of the individual customer.")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field contains the middle name of the individual customer, if provided. Otherwise, it contains null.")
    mobile: Optional[StrictStr] = Field(None, description="This field contains the mobile number of the customer without the country code.")
    nationality: Optional[StrictStr] = Field(None, description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer [INDIVIDUAL] or applicant [CORPORATE] citizenship.")
    native_language_name: Optional[StrictStr] = Field(None, alias="nativeLanguageName", description="This field contains the name of the customer in native language, if provided during customer onboarding. Otherwise, it contains null")
    occupation: Optional[StrictStr] = Field(None, description="This field accepts the customer’s occupation. Refer to [Enum values](https://docs.nium.com/apis/docs/unified-add-customer-api) for the description.   Note: This field is mandatory for CA.")
    parent_customer_hash_id: Optional[StrictStr] = Field(None, alias="parentCustomerHashId", description="This field is to identify with which Corporate customer does that Individual customer is tagged to")
    pep: Optional[StrictBool] = Field(None, description="This flag indicates if a customer is a Politically Exposed Person (PEP) or not.")
    preferred_name: Optional[StrictStr] = Field(None, alias="preferredName", description="This field contains the preferred name of the individual customer")
    tax_details: Optional[conlist(TaxDetailsResponseDTO)] = Field(None, alias="taxDetails", description="This array contains tax details provided during compliance onboarding for EU customers. Otherwise, it contains null.")
    __properties = ["billingAddress1", "billingAddress2", "billingCity", "billingCountry", "billingLandmark", "billingState", "billingZipCode", "countryCode", "countryOfBirth", "dateOfBirth", "designation", "email", "employeeId", "estimatedMonthlyFunding", "estimatedMonthlyFundingCurrency", "expectedCountriesToSendReceiveFrom", "firstName", "gender", "identificationData", "internationalPaymentsSupported", "lastName", "middleName", "mobile", "nationality", "nativeLanguageName", "occupation", "parentCustomerHashId", "pep", "preferredName", "taxDetails"]

    @validator('estimated_monthly_funding')
    def estimated_monthly_funding_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('<1000', '1000-5000', '5001-10000', '10001-20000', '>20000'):
            raise ValueError("must be one of enum values ('<1000', '1000-5000', '5001-10000', '10001-20000', '>20000')")
        return value

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
    def from_json(cls, json_str: str) -> IndividualCustomerResponseDTO:
        """Create an instance of IndividualCustomerResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in tax_details (list)
        _items = []
        if self.tax_details:
            for _item in self.tax_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taxDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IndividualCustomerResponseDTO:
        """Create an instance of IndividualCustomerResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IndividualCustomerResponseDTO.parse_obj(obj)

        _obj = IndividualCustomerResponseDTO.parse_obj({
            "billing_address1": obj.get("billingAddress1"),
            "billing_address2": obj.get("billingAddress2"),
            "billing_city": obj.get("billingCity"),
            "billing_country": obj.get("billingCountry"),
            "billing_landmark": obj.get("billingLandmark"),
            "billing_state": obj.get("billingState"),
            "billing_zip_code": obj.get("billingZipCode"),
            "country_code": obj.get("countryCode"),
            "country_of_birth": obj.get("countryOfBirth"),
            "date_of_birth": obj.get("dateOfBirth"),
            "designation": obj.get("designation"),
            "email": obj.get("email"),
            "employee_id": obj.get("employeeId"),
            "estimated_monthly_funding": obj.get("estimatedMonthlyFunding"),
            "estimated_monthly_funding_currency": obj.get("estimatedMonthlyFundingCurrency"),
            "expected_countries_to_send_receive_from": obj.get("expectedCountriesToSendReceiveFrom"),
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "identification_data": obj.get("identificationData"),
            "international_payments_supported": obj.get("internationalPaymentsSupported"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "mobile": obj.get("mobile"),
            "nationality": obj.get("nationality"),
            "native_language_name": obj.get("nativeLanguageName"),
            "occupation": obj.get("occupation"),
            "parent_customer_hash_id": obj.get("parentCustomerHashId"),
            "pep": obj.get("pep"),
            "preferred_name": obj.get("preferredName"),
            "tax_details": [TaxDetailsResponseDTO.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None
        })
        return _obj


