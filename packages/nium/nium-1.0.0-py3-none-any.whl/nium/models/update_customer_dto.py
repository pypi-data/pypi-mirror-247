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


from typing import Dict, Optional
from pydantic import BaseModel, Field, StrictStr

class UpdateCustomerDTO(BaseModel):
    """
    UpdateCustomerDTO
    """
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo")
    authentication_code: Optional[StrictStr] = Field(None, alias="authenticationCode", description="This field accepts the authentication code generated as part of SCA (Strong Customer Authentication). Note: : Authentication code must be passed if regulatory region of the program is UK or EU. Otherwise, please do not use this field and do not pass any value.")
    billing_address1: Optional[StrictStr] = Field(None, alias="billingAddress1", description="Billing address line one of a customer.")
    billing_address2: Optional[StrictStr] = Field(None, alias="billingAddress2", description="Billing address line two of a customer.")
    billing_address_id: Optional[StrictStr] = Field(None, alias="billingAddressId")
    billing_city: Optional[StrictStr] = Field(None, alias="billingCity", description="Billing address city name.")
    billing_country: Optional[StrictStr] = Field(None, alias="billingCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of customer’s billing address. It is important to pass this field if the card to be issued is to be used for GooglePay or ApplePay provisioning.")
    billing_landmark: Optional[StrictStr] = Field(None, alias="billingLandmark", description="Billing landmark address field.")
    billing_state: Optional[StrictStr] = Field(None, alias="billingState", description="Billing address state name.")
    billing_zip_code: Optional[StrictStr] = Field(None, alias="billingZipCode", description="Billing address ZIP code.")
    block_type: Optional[StrictStr] = Field(None, alias="blockType")
    correspondence_address1: Optional[StrictStr] = Field(None, alias="correspondenceAddress1", description="Line one of the customer's correspondence address.")
    correspondence_address2: Optional[StrictStr] = Field(None, alias="correspondenceAddress2", description="Line two of the customer's correspondence address.")
    correspondence_address_id: Optional[StrictStr] = Field(None, alias="correspondenceAddressId")
    correspondence_city: Optional[StrictStr] = Field(None, alias="correspondenceCity", description="Correspondence address city name.")
    correspondence_country: Optional[StrictStr] = Field(None, alias="correspondenceCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of customer’s correspondence address.")
    correspondence_landmark: Optional[StrictStr] = Field(None, alias="correspondenceLandmark", description="Correspondence landmark address field.")
    correspondence_state: Optional[StrictStr] = Field(None, alias="correspondenceState", description="Correspondence address state name.")
    correspondence_zip_code: Optional[StrictStr] = Field(None, alias="correspondenceZipCode", description="Correspondence postal/ZIP code of a customer.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for identifying the country prefix to a mobile number.")
    country_ip: Optional[StrictStr] = Field(None, alias="countryIP", description="The country IP for the device by the customer for initiating the request.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="Unique customer identifier generated on customer creation.")
    delivery_address1: Optional[StrictStr] = Field(None, alias="deliveryAddress1", description="Line one of the address where the customer would like to receive a card.")
    delivery_address2: Optional[StrictStr] = Field(None, alias="deliveryAddress2", description="Line two of the customer's delivery address.")
    delivery_address_id: Optional[StrictStr] = Field(None, alias="deliveryAddressId")
    delivery_city: Optional[StrictStr] = Field(None, alias="deliveryCity", description="Customer's city name.")
    delivery_country: Optional[StrictStr] = Field(None, alias="deliveryCountry", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of customer's delivery address.")
    delivery_landmark: Optional[StrictStr] = Field(None, alias="deliveryLandmark", description="delivery landmark address field.")
    delivery_state: Optional[StrictStr] = Field(None, alias="deliveryState", description="Customer's state name.")
    delivery_zip_code: Optional[StrictStr] = Field(None, alias="deliveryZipCode", description="Customer's ZIP code.")
    device_info: Optional[StrictStr] = Field(None, alias="deviceInfo", description="The OS of the device used by the customer for initiating the request.")
    email: Optional[StrictStr] = Field(None, description="Customer's email address")
    employee_id: Optional[StrictStr] = Field(None, alias="employeeId", description="This field accepts the employee Id for the customer, in case of a corporate program.")
    ip_address: Optional[StrictStr] = Field(None, alias="ipAddress", description="The IP address of the device used by the customer for initiating the request.")
    mobile: Optional[StrictStr] = Field(None, description="Mobile number to be updated.")
    native_language_name: Optional[StrictStr] = Field(None, alias="nativeLanguageName", description="This field contains the customer's name in native language. Maximum character limit: 40")
    segment: Optional[StrictStr] = Field(None, description="This is the fee segment associated with a client. Maximum character limit: 64")
    session_id: Optional[StrictStr] = Field(None, alias="sessionId", description="The session Id for the session of the customer for initiating the request.")
    __properties = ["additionalInfo", "authenticationCode", "billingAddress1", "billingAddress2", "billingAddressId", "billingCity", "billingCountry", "billingLandmark", "billingState", "billingZipCode", "blockType", "correspondenceAddress1", "correspondenceAddress2", "correspondenceAddressId", "correspondenceCity", "correspondenceCountry", "correspondenceLandmark", "correspondenceState", "correspondenceZipCode", "countryCode", "countryIP", "customerHashId", "deliveryAddress1", "deliveryAddress2", "deliveryAddressId", "deliveryCity", "deliveryCountry", "deliveryLandmark", "deliveryState", "deliveryZipCode", "deviceInfo", "email", "employeeId", "ipAddress", "mobile", "nativeLanguageName", "segment", "sessionId"]

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
    def from_json(cls, json_str: str) -> UpdateCustomerDTO:
        """Create an instance of UpdateCustomerDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateCustomerDTO:
        """Create an instance of UpdateCustomerDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateCustomerDTO.parse_obj(obj)

        _obj = UpdateCustomerDTO.parse_obj({
            "additional_info": obj.get("additionalInfo"),
            "authentication_code": obj.get("authenticationCode"),
            "billing_address1": obj.get("billingAddress1"),
            "billing_address2": obj.get("billingAddress2"),
            "billing_address_id": obj.get("billingAddressId"),
            "billing_city": obj.get("billingCity"),
            "billing_country": obj.get("billingCountry"),
            "billing_landmark": obj.get("billingLandmark"),
            "billing_state": obj.get("billingState"),
            "billing_zip_code": obj.get("billingZipCode"),
            "block_type": obj.get("blockType"),
            "correspondence_address1": obj.get("correspondenceAddress1"),
            "correspondence_address2": obj.get("correspondenceAddress2"),
            "correspondence_address_id": obj.get("correspondenceAddressId"),
            "correspondence_city": obj.get("correspondenceCity"),
            "correspondence_country": obj.get("correspondenceCountry"),
            "correspondence_landmark": obj.get("correspondenceLandmark"),
            "correspondence_state": obj.get("correspondenceState"),
            "correspondence_zip_code": obj.get("correspondenceZipCode"),
            "country_code": obj.get("countryCode"),
            "country_ip": obj.get("countryIP"),
            "customer_hash_id": obj.get("customerHashId"),
            "delivery_address1": obj.get("deliveryAddress1"),
            "delivery_address2": obj.get("deliveryAddress2"),
            "delivery_address_id": obj.get("deliveryAddressId"),
            "delivery_city": obj.get("deliveryCity"),
            "delivery_country": obj.get("deliveryCountry"),
            "delivery_landmark": obj.get("deliveryLandmark"),
            "delivery_state": obj.get("deliveryState"),
            "delivery_zip_code": obj.get("deliveryZipCode"),
            "device_info": obj.get("deviceInfo"),
            "email": obj.get("email"),
            "employee_id": obj.get("employeeId"),
            "ip_address": obj.get("ipAddress"),
            "mobile": obj.get("mobile"),
            "native_language_name": obj.get("nativeLanguageName"),
            "segment": obj.get("segment"),
            "session_id": obj.get("sessionId")
        })
        return _obj


