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
from nium.models.compliance_identification_doc_dto import ComplianceIdentificationDocDTO
from nium.models.customer_tax_detail_dto import CustomerTaxDetailDTO

class CustomerDataRequestDTO(BaseModel):
    """
    CustomerDataRequestDTO
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo", description="This is key/value pair object which accepts additional info. Expected keys are identificationType and identificationValue   identificationType  : This field accepts the name of the identification type, for example, Passport.  Note: This field is mandatory for certain clients with certain KYC modes pre-approved by NIUM's compliance or when the KYC mode is Screening. If you have plans to offer the Payout/Send feature then please ensure to reach out to your NIUM's representative to discuss on the requirement of this field.   identificationValue : This field accepts the identification value provided by the customer. Note: This field is mandatory for certain clients with certain KYC modes pre-approved by NIUM's compliance or when the KYC mode is Screening. If you have plans to offer the Payout/Send feature then please ensure to reach out to your NIUM's representative to discuss on the requirement of this field.  Example : { \"identificationType\": \"Passport\",  \"identificationValue\" : \"P123456A\" }")
    billing_address1: StrictStr = Field(..., alias="billingAddress1", description="This field accepts the line 1 of customer’s billing address. Maximum character limit: 40")
    billing_address2: Optional[StrictStr] = Field(None, alias="billingAddress2", description="This field accepts the line 2 of customer’s billing address. Maximum character limit: 40")
    billing_city: StrictStr = Field(..., alias="billingCity", description="This field accepts the city of customer’s billing address. Maximum character limit: 20")
    billing_country: StrictStr = Field(..., alias="billingCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of customer’s billing address.")
    billing_landmark: Optional[StrictStr] = Field(None, alias="billingLandmark", description="This field accepts the landmark for customer’s billing address. Maximum character limit: 40")
    billing_state: Optional[StrictStr] = Field(None, alias="billingState", description="This field accepts the state of customer’s billing address. Maximum character limit: 30")
    billing_zip_code: StrictStr = Field(..., alias="billingZipCode", description="This field accepts the zipcode of customer’s billing address. Maximum character limit: 10")
    birth_country: Optional[StrictStr] = Field(None, alias="birthCountry")
    correspondence_address1: Optional[StrictStr] = Field(None, alias="correspondenceAddress1", description="This field accepts the line 1 of customer's correspondence address. Maximum character limit: 40")
    correspondence_address2: Optional[StrictStr] = Field(None, alias="correspondenceAddress2", description="This field accepts the line 2 of customer's correspondence address. Maximum character limit: 40")
    correspondence_city: Optional[StrictStr] = Field(None, alias="correspondenceCity", description="This field accepts the city of customer's correspondence address. Maximum character limit: 20")
    correspondence_country: Optional[StrictStr] = Field(None, alias="correspondenceCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of customer's correspondence address.")
    correspondence_landmark: Optional[StrictStr] = Field(None, alias="correspondenceLandmark", description="This field accepts the landmark for customer's correspondence address. Maximum character limit: 40")
    correspondence_state: Optional[StrictStr] = Field(None, alias="correspondenceState", description="This field accepts the state of customer’s correspondence address. Maximum character limit: 30")
    correspondence_zip_code: Optional[StrictStr] = Field(None, alias="correspondenceZipCode", description="This field accepts the zipcode of customer's correspondence address. Maximum character limit: 10")
    country_code: StrictStr = Field(..., alias="countryCode", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country prefix code to the customer’s mobile number.")
    country_ip: Optional[StrictStr] = Field(None, alias="countryIP", description="The country IP for the device by the customer for initiating the request.")
    country_of_birth: Optional[StrictStr] = Field(None, alias="countryOfBirth", description="This field accepts the 2-letter [ISO country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s country of birth. Note:This field is mandatory for EU and UK.")
    customer_hash_id: StrictStr = Field(..., alias="customerHashId", description="This field accepts previously generated unique customer identifier of customer.")
    date_of_birth: StrictStr = Field(..., alias="dateOfBirth", description="This field accepts the date of birth of the customer in YYYY-MM-DD format. Minimum customer age should be 18 years. Please discuss with your NIUM account manager for any special use-cases.")
    delivery_address1: StrictStr = Field(..., alias="deliveryAddress1", description="This field accepts the line 1 of customer’s delivery address. Maximum character limit: 40")
    delivery_address2: Optional[StrictStr] = Field(None, alias="deliveryAddress2", description="This field accepts the line 2 of customer's delivery address. Maximum character limit: 40")
    delivery_city: StrictStr = Field(..., alias="deliveryCity", description="This field accepts the city of customer’s delivery address. Maximum character limit: 20")
    delivery_country: StrictStr = Field(..., alias="deliveryCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of customer’s billing address.")
    delivery_landmark: Optional[StrictStr] = Field(None, alias="deliveryLandmark", description="This field accepts the landmark for customer's delivery address. Maximum character limit: 40")
    delivery_state: Optional[StrictStr] = Field(None, alias="deliveryState", description="This field accepts the state of customer's delivery address. Maximum character limit: 30")
    delivery_zip_code: StrictStr = Field(..., alias="deliveryZipCode", description="This field accepts the zipcode of customer's delivery address. Maximum character limit: 10")
    device_info: Optional[StrictStr] = Field(None, alias="deviceInfo", description="The OS of the device used by the customer for initiating the request.")
    email: StrictStr = Field(..., description="This field accepts the unique email address of the customer.  Maximum character limit: 60")
    enable_doc_upload: Optional[StrictBool] = Field(None, alias="enableDocUpload")
    estimated_monthly_funding: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFunding", description="This field accepts the estimated monthly funding amount expected in the wallet. This field is required when estimatedMonthlyFundingCurrency field is provided in the request. Note:This field is mandatory for EU and UK.")
    estimated_monthly_funding_currency: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFundingCurrency", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) in which estimated monthly funding is expected in the wallet, for example, SGD. Note:This field is mandatory for EU and UK.")
    expected_countries_to_send_receive_from: Optional[conlist(StrictStr)] = Field(None, alias="expectedCountriesToSendReceiveFrom", description="This is an array of 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) to allow the client to capture the expected countries to send/receive international payments from. This field is required when internationalPaymentsSupported field is true, for example, [“FR”, “DE”]. Note:This field is mandatory for EU and UK.")
    first_name: StrictStr = Field(..., alias="firstName", description="This field accepts the first name of the customer.  Maximum character limit: 40")
    gender: Optional[StrictStr] = Field(None, description="This field accepts the gender of the customer.")
    identification_doc: Optional[conlist(ComplianceIdentificationDocDTO)] = Field(None, alias="identificationDoc")
    intended_use_of_account: Optional[StrictStr] = Field(None, alias="intendedUseOfAccount", description="This field accepts customer’s intended use of account. Note:This field is mandatory for EU and UK.")
    international_payments_supported: Optional[StrictBool] = Field(None, alias="internationalPaymentsSupported", description="This field indicates if the customer will be doing International send/receive payments. The default value will be false. Note:This field is mandatory for EU and UK.")
    ip_address: Optional[StrictStr] = Field(None, alias="ipAddress", description="The IP address of the device used by the customer for initiating the request.")
    kyc: Optional[StrictBool] = None
    last_name: StrictStr = Field(..., alias="lastName", description="This field accepts the last name of the customer. Maximum character limit: 40")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field accepts the middle name of the customer.  Maximum character limit: 40")
    mobile: StrictStr = Field(..., description="This field accepts the mobile number of the customer without the country prefix code. Maximum character limit: 20")
    nationality: StrictStr = Field(..., description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s citizenship.")
    native_language_name: Optional[StrictStr] = Field(None, alias="nativeLanguageName", description="This field contains the customer's name in native language.  Maximum character limit: 40")
    occupation: Optional[StrictStr] = Field(None, description="This field accepts the customer’s occupation. Refer to [Enum values](https://docs.nium.com/apis/docs/unified-add-customer-api) for the description.   Note: This field is mandatory for CA.")
    pep: StrictBool = Field(..., description="This field will ensure either a customer is a Politically Exposed Person (PEP) or not. Note:This field is mandatory for EU and UK.")
    preferred_name: Optional[StrictStr] = Field(None, alias="preferredName", description="This field accepts the common name or preferred name of the customer. It is also acceptable to pass the first name in this field. Maximum character limit: 20")
    segment: Optional[StrictStr] = Field(None, description="This is the fee segment associated with a client. Maximum character limit: 64")
    session_id: Optional[StrictStr] = Field(None, alias="sessionId", description="The session Id for the session of the customer for initiating the request.")
    tax_details: conlist(CustomerTaxDetailDTO) = Field(..., alias="taxDetails", description="This is an array of tax details provided for compliance onboarding for EU customers. Note:This field is mandatory for EU and UK.")
    upgrade_request: Optional[StrictBool] = Field(None, alias="upgradeRequest")
    __properties = ["additionalInfo", "billingAddress1", "billingAddress2", "billingCity", "billingCountry", "billingLandmark", "billingState", "billingZipCode", "birthCountry", "correspondenceAddress1", "correspondenceAddress2", "correspondenceCity", "correspondenceCountry", "correspondenceLandmark", "correspondenceState", "correspondenceZipCode", "countryCode", "countryIP", "countryOfBirth", "customerHashId", "dateOfBirth", "deliveryAddress1", "deliveryAddress2", "deliveryCity", "deliveryCountry", "deliveryLandmark", "deliveryState", "deliveryZipCode", "deviceInfo", "email", "enableDocUpload", "estimatedMonthlyFunding", "estimatedMonthlyFundingCurrency", "expectedCountriesToSendReceiveFrom", "firstName", "gender", "identificationDoc", "intendedUseOfAccount", "internationalPaymentsSupported", "ipAddress", "kyc", "lastName", "middleName", "mobile", "nationality", "nativeLanguageName", "occupation", "pep", "preferredName", "segment", "sessionId", "taxDetails", "upgradeRequest"]

    @validator('estimated_monthly_funding')
    def estimated_monthly_funding_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('<1000', '1000-5000', '5001-10000', '10001-20000', '>20000'):
            raise ValueError("must be one of enum values ('<1000', '1000-5000', '5001-10000', '10001-20000', '>20000')")
        return value

    @validator('gender')
    def gender_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Male', 'Female', 'Others'):
            raise ValueError("must be one of enum values ('Male', 'Female', 'Others')")
        return value

    @validator('intended_use_of_account')
    def intended_use_of_account_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Receiving from/Transfers to accounts I own', 'Receiving from/Transfers to friends or family', 'Property goods or services payments', 'Education-related payment', 'Investments', 'Receive or send donations', 'Saving', 'Day-to-day spending', 'Receiving a salary'):
            raise ValueError("must be one of enum values ('Receiving from/Transfers to accounts I own', 'Receiving from/Transfers to friends or family', 'Property goods or services payments', 'Education-related payment', 'Investments', 'Receive or send donations', 'Saving', 'Day-to-day spending', 'Receiving a salary')")
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
    def from_json(cls, json_str: str) -> CustomerDataRequestDTO:
        """Create an instance of CustomerDataRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in identification_doc (list)
        _items = []
        if self.identification_doc:
            for _item in self.identification_doc:
                if _item:
                    _items.append(_item.to_dict())
            _dict['identificationDoc'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tax_details (list)
        _items = []
        if self.tax_details:
            for _item in self.tax_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taxDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerDataRequestDTO:
        """Create an instance of CustomerDataRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerDataRequestDTO.parse_obj(obj)

        _obj = CustomerDataRequestDTO.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "billing_address1": obj.get("billingAddress1"),
            "billing_address2": obj.get("billingAddress2"),
            "billing_city": obj.get("billingCity"),
            "billing_country": obj.get("billingCountry"),
            "billing_landmark": obj.get("billingLandmark"),
            "billing_state": obj.get("billingState"),
            "billing_zip_code": obj.get("billingZipCode"),
            "birth_country": obj.get("birthCountry"),
            "correspondence_address1": obj.get("correspondenceAddress1"),
            "correspondence_address2": obj.get("correspondenceAddress2"),
            "correspondence_city": obj.get("correspondenceCity"),
            "correspondence_country": obj.get("correspondenceCountry"),
            "correspondence_landmark": obj.get("correspondenceLandmark"),
            "correspondence_state": obj.get("correspondenceState"),
            "correspondence_zip_code": obj.get("correspondenceZipCode"),
            "country_code": obj.get("countryCode"),
            "country_ip": obj.get("countryIP"),
            "country_of_birth": obj.get("countryOfBirth"),
            "customer_hash_id": obj.get("customerHashId"),
            "date_of_birth": obj.get("dateOfBirth"),
            "delivery_address1": obj.get("deliveryAddress1"),
            "delivery_address2": obj.get("deliveryAddress2"),
            "delivery_city": obj.get("deliveryCity"),
            "delivery_country": obj.get("deliveryCountry"),
            "delivery_landmark": obj.get("deliveryLandmark"),
            "delivery_state": obj.get("deliveryState"),
            "delivery_zip_code": obj.get("deliveryZipCode"),
            "device_info": obj.get("deviceInfo"),
            "email": obj.get("email"),
            "enable_doc_upload": obj.get("enableDocUpload"),
            "estimated_monthly_funding": obj.get("estimatedMonthlyFunding"),
            "estimated_monthly_funding_currency": obj.get("estimatedMonthlyFundingCurrency"),
            "expected_countries_to_send_receive_from": obj.get("expectedCountriesToSendReceiveFrom"),
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "identification_doc": [ComplianceIdentificationDocDTO.from_dict(_item) for _item in obj.get("identificationDoc")] if obj.get("identificationDoc") is not None else None,
            "intended_use_of_account": obj.get("intendedUseOfAccount"),
            "international_payments_supported": obj.get("internationalPaymentsSupported"),
            "ip_address": obj.get("ipAddress"),
            "kyc": obj.get("kyc"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "mobile": obj.get("mobile"),
            "nationality": obj.get("nationality"),
            "native_language_name": obj.get("nativeLanguageName"),
            "occupation": obj.get("occupation"),
            "pep": obj.get("pep"),
            "preferred_name": obj.get("preferredName"),
            "segment": obj.get("segment"),
            "session_id": obj.get("sessionId"),
            "tax_details": [CustomerTaxDetailDTO.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None,
            "upgrade_request": obj.get("upgradeRequest")
        })
        return _obj


