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
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist
from nium.models.customer_tax_detail_dto import CustomerTaxDetailDTO

class EVerifyCustomerRegistrationRequestDTO(BaseModel):
    """
    EVerifyCustomerRegistrationRequestDTO
    """
    billing_address1: StrictStr = Field(..., alias="billingAddress1", description="This field accepts the line 1 of customer’s billing address. Maximum character limit: 40")
    billing_address2: Optional[StrictStr] = Field(None, alias="billingAddress2", description="This field accepts the line 2 of customer’s billing address. Maximum character limit: 40")
    billing_city: StrictStr = Field(..., alias="billingCity", description="This field accepts the city of customer’s billing address. Maximum character limit: 20")
    billing_country: StrictStr = Field(..., alias="billingCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of customer’s billing address.")
    billing_state: Optional[StrictStr] = Field(None, alias="billingState", description="This field accepts the state of customer’s billing address. Maximum character limit: 30")
    billing_zip_code: StrictStr = Field(..., alias="billingZipCode", description="This field accepts the zipcode of customer’s billing address. Maximum character limit: 10")
    country_code: StrictStr = Field(..., alias="countryCode", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country prefix code to the customer’s mobile number.")
    country_ip: Optional[StrictStr] = Field(None, alias="countryIP", description="This field accepts the country IP for the device by the customer for initiating the request.")
    country_of_birth: Optional[StrictStr] = Field(None, alias="countryOfBirth", description="This field accepts the 2-letter [ISO country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s country of birth. Note: This field is mandatory for EU and UK.")
    customer_hash_id: StrictStr = Field(..., alias="customerHashId", description="This field accepts previously generated unique customer identifier of customer.")
    date_of_birth: StrictStr = Field(..., alias="dateOfBirth", description="This field accepts the date of birth of the customer in YYYY-MM-DD format. Minimum customer age should be 18 years. Please discuss with your NIUM account manager for any special use-cases.")
    device_info: Optional[StrictStr] = Field(None, alias="deviceInfo", description="This field accepts the OS of the device used by the customer for initiating the request.")
    email: StrictStr = Field(..., description="This field accepts the unique email address of the customer. Maximum character limit: 60")
    estimated_monthly_funding: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFunding", description="This field accepts the estimated monthly funding amount expected in the wallet. This field is required when estimatedMonthlyFundingCurrency field is provided in the request. The possible values are: • <1000 • 1000-5000 • 5001-10000 • 10001-20000 • >20000 Note: This field is mandatory for EU and UK.")
    estimated_monthly_funding_currency: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFundingCurrency", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) in which estimated monthly funding is expected in the wallet, for example, SGD. Note: This field is mandatory for EU and UK.")
    expected_countries_to_send_receive_from: Optional[conlist(StrictStr)] = Field(None, alias="expectedCountriesToSendReceiveFrom", description="This is an array of 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) to allow the client to capture the expected countries to send/receive international payments from. This field is required when internationalPaymentsSupported field is true, for example, [“FR”, “DE”]. Note: This field is mandatory for EU and UK.")
    first_name: StrictStr = Field(..., alias="firstName", description="This field accepts the first name of the customer. Maximum character limit: 40")
    gender: Optional[StrictStr] = Field(None, description="This field accepts the gender of the customer. This field can accept only one of the following values: • Male • Female • Others")
    intended_use_of_account: Optional[StrictStr] = Field(None, alias="intendedUseOfAccount", description="This field accepts the customer’s intended use of account. The possible values are: • Receiving from/Transfers to accounts I own • Receiving from/Transfers to friends or family • Property, goods or services payments • Education-related payment • Investments • Receive or send donations • Saving • Day-to-day spending • Receiving a salary Note: This field is mandatory for EU and UK.")
    international_payments_supported: Optional[StrictBool] = Field(None, alias="internationalPaymentsSupported", description="This field specifies if the customer will be doing International send/receive payments. The default value will be false. Note: This field is mandatory for EU and UK.")
    ip_address: Optional[StrictStr] = Field(None, alias="ipAddress", description="This field accepts the IP address of the device used by the customer for initiating the request.")
    last_name: StrictStr = Field(..., alias="lastName", description="This field accepts the last name of the customer. Maximum character limit: 40")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field accepts the middle name of the customer. Maximum character limit: 40")
    mobile: StrictStr = Field(..., description="This field accepts the mobile number of the customer without the country prefix code. Maximum character limit: 20")
    nationality: StrictStr = Field(..., description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s citizenship.")
    native_language_name: Optional[StrictStr] = Field(None, alias="nativeLanguageName", description="This field accepts the customer's name in native language. Maximum character limit: 40")
    pep: Optional[StrictBool] = Field(None, description="This field specifies if the customer is a Politically Exposed Person (PEP) or not. Note: This field is mandatory for EU and UK.")
    preferred_name: Optional[StrictStr] = Field(None, alias="preferredName", description="This field accepts the common name or preferred name of the customer. It is also acceptable to pass the first name in this field. Maximum character limit: 20")
    segment: Optional[StrictStr] = Field(None, description="This field accepts the fee segment associated with a client. Maximum character limit: 64")
    session_id: Optional[StrictStr] = Field(None, alias="sessionId", description="This field accepts the session ID for the session of the customer for initiating the request.")
    tax_details: Optional[conlist(CustomerTaxDetailDTO)] = Field(None, alias="taxDetails", description="This is an array of tax details provided for compliance onboarding for EU customers. Note: This field is mandatory for EU and UK.")
    upgrade_request: Optional[StrictBool] = Field(None, alias="upgradeRequest")
    verification_consent: StrictBool = Field(..., alias="verificationConsent", description="This field specifies if the electronic verification consent to process customer data for compliance or not.")
    __properties = ["billingAddress1", "billingAddress2", "billingCity", "billingCountry", "billingState", "billingZipCode", "countryCode", "countryIP", "countryOfBirth", "customerHashId", "dateOfBirth", "deviceInfo", "email", "estimatedMonthlyFunding", "estimatedMonthlyFundingCurrency", "expectedCountriesToSendReceiveFrom", "firstName", "gender", "intendedUseOfAccount", "internationalPaymentsSupported", "ipAddress", "lastName", "middleName", "mobile", "nationality", "nativeLanguageName", "pep", "preferredName", "segment", "sessionId", "taxDetails", "upgradeRequest", "verificationConsent"]

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
    def from_json(cls, json_str: str) -> EVerifyCustomerRegistrationRequestDTO:
        """Create an instance of EVerifyCustomerRegistrationRequestDTO from a JSON string"""
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
    def from_dict(cls, obj: dict) -> EVerifyCustomerRegistrationRequestDTO:
        """Create an instance of EVerifyCustomerRegistrationRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return EVerifyCustomerRegistrationRequestDTO.parse_obj(obj)

        _obj = EVerifyCustomerRegistrationRequestDTO.parse_obj({
            "billing_address1": obj.get("billingAddress1"),
            "billing_address2": obj.get("billingAddress2"),
            "billing_city": obj.get("billingCity"),
            "billing_country": obj.get("billingCountry"),
            "billing_state": obj.get("billingState"),
            "billing_zip_code": obj.get("billingZipCode"),
            "country_code": obj.get("countryCode"),
            "country_ip": obj.get("countryIP"),
            "country_of_birth": obj.get("countryOfBirth"),
            "customer_hash_id": obj.get("customerHashId"),
            "date_of_birth": obj.get("dateOfBirth"),
            "device_info": obj.get("deviceInfo"),
            "email": obj.get("email"),
            "estimated_monthly_funding": obj.get("estimatedMonthlyFunding"),
            "estimated_monthly_funding_currency": obj.get("estimatedMonthlyFundingCurrency"),
            "expected_countries_to_send_receive_from": obj.get("expectedCountriesToSendReceiveFrom"),
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "intended_use_of_account": obj.get("intendedUseOfAccount"),
            "international_payments_supported": obj.get("internationalPaymentsSupported"),
            "ip_address": obj.get("ipAddress"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "mobile": obj.get("mobile"),
            "nationality": obj.get("nationality"),
            "native_language_name": obj.get("nativeLanguageName"),
            "pep": obj.get("pep"),
            "preferred_name": obj.get("preferredName"),
            "segment": obj.get("segment"),
            "session_id": obj.get("sessionId"),
            "tax_details": [CustomerTaxDetailDTO.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None,
            "upgrade_request": obj.get("upgradeRequest"),
            "verification_consent": obj.get("verificationConsent")
        })
        return _obj


