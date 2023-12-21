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

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, conlist, validator
from nium.models.business_details_response_dto import BusinessDetailsResponseDTO
from nium.models.business_partner_details_response_dto import BusinessPartnerDetailsResponseDTO
from nium.models.customer_rfi_details_response import CustomerRfiDetailsResponse
from nium.models.customer_tax_detail_dto import CustomerTaxDetailDTO
from nium.models.payment_id_dto import PaymentIdDTO
from nium.models.professional_details import ProfessionalDetails
from nium.models.risk_assessment_info_response_dto import RiskAssessmentInfoResponseDTO
from nium.models.stakeholder_details_response_dto import StakeholderDetailsResponseDTO

class CustomerDetailResponse(BaseModel):
    """
    CustomerDetailResponse
    """
    tags: Optional[Dict[str, StrictStr]] = Field(None, description="This object contains the user defined key-value pairs provided by the client.")
    billing_address1: Optional[StrictStr] = Field(None, alias="billingAddress1", description="This field contains the line 1 of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address, which is used for KYC.")
    billing_address2: Optional[StrictStr] = Field(None, alias="billingAddress2", description="This field contains the line 2 of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_city: Optional[StrictStr] = Field(None, alias="billingCity", description="This field contains the city of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address.")
    billing_country: Optional[StrictStr] = Field(None, alias="billingCountry", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_landmark: Optional[StrictStr] = Field(None, alias="billingLandmark", description="This field contains the landmark for customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_state: Optional[StrictStr] = Field(None, alias="billingState", description="This field contains the state of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address, if provided during customer onboarding. Otherwise, it contains null.")
    billing_zip_code: Optional[StrictStr] = Field(None, alias="billingZipCode", description="This field contains the zip code of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] billing address.")
    block_comment: Optional[StrictStr] = Field(None, alias="blockComment", description="This field contains the comment entered while blocking the customer, if applicable. Otherwise, it contains null.")
    block_reason: Optional[StrictStr] = Field(None, alias="blockReason", description="This field contains the reason for blocking the customer, if applicable. Otherwise, it contains null.")
    block_updated_by: Optional[StrictStr] = Field(None, alias="blockUpdatedBy", description="This field contains the details of the entity updating a customer block/unblock, if applicable. Otherwise, it contains null. The possible values are CLIENT or NIUM.")
    business_details: Optional[BusinessDetailsResponseDTO] = Field(None, alias="businessDetails")
    business_partner: Optional[conlist(BusinessPartnerDetailsResponseDTO)] = Field(None, alias="businessPartner")
    compliance_level: Optional[StrictStr] = Field(None, alias="complianceLevel", description="This field contains the compliance level for the customer. The possible values for customer type INDIVIDUAL are: SCREENING_KYC, SCREENING, SCREENING_KYB. The possible values for customer type CORPORATE is SCREENING_KYB.")
    compliance_remarks: Optional[StrictStr] = Field(None, alias="complianceRemarks", description="This field contains the compliance remarks from Compliance officer, if applicable.")
    compliance_status: Optional[StrictStr] = Field(None, alias="complianceStatus", description="This field contains the overall compliance status of the customer.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field contains the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for identifying the country prefix to the customer’s mobile number.")
    country_of_birth: Optional[StrictStr] = Field(None, alias="countryOfBirth", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s country of birth.")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the timestamp of customer creation in the format YYY-MM-DD hh:mm:ss, for example, 2021-07-29 06:11:43.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique customer identifier generated at the time of customer creation.")
    customer_id: Optional[StrictInt] = Field(None, alias="customerId", description="This field contains an internal NIUM customer identifier. This field shall be deprecated in future.")
    customer_type: Optional[StrictStr] = Field(None, alias="customerType", description="This field contains the customer type which is either <B>INDIVIDUAL</B> or <B>CORPORATE</B> and this depends on customer onboarding flows.")
    date_of_birth: Optional[StrictStr] = Field(None, alias="dateOfBirth", description="This field contains the date of birth of the customer [INDIVIDUAL] or applicant [CORPORATE] in YYYY-MM-DD format.")
    delivery_address1: Optional[StrictStr] = Field(None, alias="deliveryAddress1", description="This field contains the line 1 of customer [INDIVIDUAL] or applicant [CORPORATE] delivery address. It is used for card delivery.")
    delivery_address2: Optional[StrictStr] = Field(None, alias="deliveryAddress2", description="This field contains the line 2 of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] delivery address, if provided during customer onboarding. It is used for card delivery. Otherwise, it contains null.")
    delivery_city: Optional[StrictStr] = Field(None, alias="deliveryCity", description="This field contains the city of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] delivery address.")
    delivery_country: Optional[StrictStr] = Field(None, alias="deliveryCountry", description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] delivery address, if provided during customer onboarding. Otherwise, it contains null.")
    delivery_landmark: Optional[StrictStr] = Field(None, alias="deliveryLandmark", description="This field contains the landmark for customer’s [INDIVIDUAL] or applicant’s [CORPORATE] delivery address, if provided during customer onboarding. Otherwise, it contains null.")
    delivery_state: Optional[StrictStr] = Field(None, alias="deliveryState", description="This field contains the state of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] delivery address, if provided during customer onboarding. Otherwise, it contains null.")
    delivery_zip_code: Optional[StrictStr] = Field(None, alias="deliveryZipCode", description="This field contains the zip code of customer’s [INDIVIDUAL] or applicant’s [CORPORATE] delivery address.")
    designation: Optional[StrictStr] = Field(None, description="This field contains the designation of an employee, if provided during customer onboarding. Otherwise, it contains null.")
    email: Optional[StrictStr] = Field(None, description="This field contains the unique email address of the customer.")
    employee_id: Optional[StrictStr] = Field(None, alias="employeeId", description="This field contains the employee ID of an employee, if provided during customer onboarding. Otherwise, it contains null.")
    estimated_monthly_funding: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFunding", description="This field contains the estimated monthly funding amount expected in the wallet. This field is required when estimatedMonthlyFundingCurrency field is provided in the request.")
    estimated_monthly_funding_currency: Optional[StrictStr] = Field(None, alias="estimatedMonthlyFundingCurrency", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) in which estimated monthly funding is expected in the wallet, for example, SGD.")
    expected_countries_to_send_receive_from: Optional[conlist(StrictStr)] = Field(None, alias="expectedCountriesToSendReceiveFrom", description="This is an array of 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) to allow the client to capture the expected countries to send/receive international payments from. This field is required when internationalPaymentsSupported field is true, for example, [“FR”, “DE”].")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field contains the first name of the customer [INDIVIDUAL] or applicant [CORPORATE].")
    gender: Optional[StrictStr] = Field(None, description="This field contains the gender of the customer [INDIVIDUAL] or applicant [CORPORATE], if provided during customer onboarding. The possible values are - Male, Female, or Others. Otherwise, it contains null.")
    identification_data: Optional[conlist(Dict[str, StrictStr])] = Field(None, alias="identificationData", description="This array contains objects consisting of type and value of each uploaded document.")
    identification_types: Optional[conlist(StrictStr)] = Field(None, alias="identificationTypes", description="This array contains the list of identification used during KYC. Otherwise, it contains null.")
    intended_use_of_account: Optional[StrictStr] = Field(None, alias="intendedUseOfAccount", description="This flag contains the customer’s intended use of account.")
    international_payments_supported: Optional[StrictBool] = Field(None, alias="internationalPaymentsSupported", description="This field indicates if the customer will be doing International send/receive payments. The default value will be false.")
    kyc_mode: Optional[StrictStr] = Field(None, alias="kycMode", description="This field contains the kyc mode  The possible values for customer type INDIVIDUAL are: E_KYC, MANUAL_KYC, SCREENING, EVERIFY_KYC, or NONE.  The possible values for customer type CORPORATE are: KYB or NONE.")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field contains the last name of the customer [INDIVIDUAL] or applicant [CORPORATE].")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field contains the middle name of the customer [INDIVIDUAL] or applicant [CORPORATE], if provided. Otherwise, it contains null.")
    mobile: Optional[StrictStr] = Field(None, description="This field contains the mobile number of the customer without the country code.")
    nationality: Optional[StrictStr] = Field(None, description="This field contains the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer [INDIVIDUAL] or applicant [CORPORATE] citizenship.")
    native_language_name: Optional[StrictStr] = Field(None, alias="nativeLanguageName", description="This field contains the name of the customer in native language, if provided during customer onboarding. Otherwise, it contains null")
    payment_ids: Optional[conlist(PaymentIdDTO)] = Field(None, alias="paymentIds", description="This field contains the unique payment Ids assigned to the customer.")
    pep: Optional[StrictBool] = Field(None, description="This flag indicates if a customer is a Politically Exposed Person (PEP) or not.")
    preferred_name: Optional[StrictStr] = Field(None, alias="preferredName", description="This field contains the preferred name of the customer[INDIVIDUAL] or business name [CORPORATE].")
    professional_details: Optional[conlist(ProfessionalDetails)] = Field(None, alias="professionalDetails", description="This array contains the applicant's professional details information")
    reference_id: Optional[StrictStr] = Field(None, alias="referenceId", description="This field contains the  applicant's reference id")
    regulatory_region: Optional[StrictStr] = Field(None, alias="regulatoryRegion", description="This field contains the regulatory region of the customer.")
    remarks: Optional[StrictStr] = Field(None, description="This field contains any system-generated compliance comments, if applicable.")
    rfi_details: Optional[conlist(CustomerRfiDetailsResponse)] = Field(None, alias="rfiDetails", description="This array contains the details of RFI, if raised. Otherwise, it contains null.")
    risk_assessment_info: Optional[RiskAssessmentInfoResponseDTO] = Field(None, alias="riskAssessmentInfo")
    segment: Optional[StrictStr] = Field(None, description="This field contains the fee segment applicable to the customer. Otherwise, it contains null.")
    stakeholder_details: Optional[conlist(StakeholderDetailsResponseDTO)] = Field(None, alias="stakeholderDetails", description="This is an array object may contain the stakeholder details in certain client onboarding flows. It is null for individual customer onboarding flows.")
    status: Optional[StrictStr] = Field(None, description="This field contains the overall KYC status of the customer")
    tax_details: Optional[conlist(CustomerTaxDetailDTO)] = Field(None, alias="taxDetails", description="This array contains tax details provided during compliance onboarding for EU customers. Otherwise, it contains null.")
    terms_and_condition_acceptance_flag: Optional[StrictBool] = Field(None, alias="termsAndConditionAcceptanceFlag", description="This flag denotes that the customer has accepted the Terms and Conditions.")
    terms_and_condition_name: Optional[StrictStr] = Field(None, alias="termsAndConditionName", description="This name that the customer has accepted the Terms and Conditions.")
    terms_and_condition_version_id: Optional[StrictStr] = Field(None, alias="termsAndConditionVersionId", description="This version that the customer has accepted the Terms and Conditions.")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="This field contains the timestamp of last customer updation in the format YYY-MM-DD hh:mm:ss, for example, 2021-07-29 06:11:43.")
    verification_consent: Optional[StrictBool] = Field(None, alias="verificationConsent", description="This flag contain the customer consent to proceed in case e-Document verification flow is initiated.")
    wallet_hash_id: Optional[StrictStr] = Field(None, alias="walletHashId", description="This field contains the unique wallet identifier generated simultaneously with customer creation.")
    __properties = ["tags", "billingAddress1", "billingAddress2", "billingCity", "billingCountry", "billingLandmark", "billingState", "billingZipCode", "blockComment", "blockReason", "blockUpdatedBy", "businessDetails", "businessPartner", "complianceLevel", "complianceRemarks", "complianceStatus", "countryCode", "countryOfBirth", "createdAt", "customerHashId", "customerId", "customerType", "dateOfBirth", "deliveryAddress1", "deliveryAddress2", "deliveryCity", "deliveryCountry", "deliveryLandmark", "deliveryState", "deliveryZipCode", "designation", "email", "employeeId", "estimatedMonthlyFunding", "estimatedMonthlyFundingCurrency", "expectedCountriesToSendReceiveFrom", "firstName", "gender", "identificationData", "identificationTypes", "intendedUseOfAccount", "internationalPaymentsSupported", "kycMode", "lastName", "middleName", "mobile", "nationality", "nativeLanguageName", "paymentIds", "pep", "preferredName", "professionalDetails", "referenceId", "regulatoryRegion", "remarks", "rfiDetails", "riskAssessmentInfo", "segment", "stakeholderDetails", "status", "taxDetails", "termsAndConditionAcceptanceFlag", "termsAndConditionName", "termsAndConditionVersionId", "updatedAt", "verificationConsent", "walletHashId"]

    @validator('block_reason')
    def block_reason_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('CUSTOMER_REQUEST', 'CLIENT_REQUEST', 'DECEASED', 'ACCOUNT_CLOSURE', 'SUSPICIOUS_ACTIVITY', 'FRAUDULENT_ACTIVITY', 'POTENTIAL_SANCTION', 'SANCTIONED_CUSTOMER'):
            raise ValueError("must be one of enum values ('CUSTOMER_REQUEST', 'CLIENT_REQUEST', 'DECEASED', 'ACCOUNT_CLOSURE', 'SUSPICIOUS_ACTIVITY', 'FRAUDULENT_ACTIVITY', 'POTENTIAL_SANCTION', 'SANCTIONED_CUSTOMER')")
        return value

    @validator('block_updated_by')
    def block_updated_by_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NIUM', 'CLIENT'):
            raise ValueError("must be one of enum values ('NIUM', 'CLIENT')")
        return value

    @validator('compliance_status')
    def compliance_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INITIATED', 'IN_PROGRESS', 'ACTION_REQUIRED', 'RFI_REQUESTED', 'COMPLETED', 'REJECT', 'ERROR', 'EXPIRED', 'CLOSED'):
            raise ValueError("must be one of enum values ('INITIATED', 'IN_PROGRESS', 'ACTION_REQUIRED', 'RFI_REQUESTED', 'COMPLETED', 'REJECT', 'ERROR', 'EXPIRED', 'CLOSED')")
        return value

    @validator('customer_type')
    def customer_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INDIVIDUAL', 'CORPORATE'):
            raise ValueError("must be one of enum values ('INDIVIDUAL', 'CORPORATE')")
        return value

    @validator('estimated_monthly_funding')
    def estimated_monthly_funding_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('<1000', '1000-5000', '5001-10000', '10001-20000', '>20000'):
            raise ValueError("must be one of enum values ('<1000', '1000-5000', '5001-10000', '10001-20000', '>20000')")
        return value

    @validator('regulatory_region')
    def regulatory_region_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('SG', 'EU', 'AU', 'HK', 'UK'):
            raise ValueError("must be one of enum values ('SG', 'EU', 'AU', 'HK', 'UK')")
        return value

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Pending', 'Clear', 'Failed', 'Suspended', 'Blocked'):
            raise ValueError("must be one of enum values ('Pending', 'Clear', 'Failed', 'Suspended', 'Blocked')")
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
    def from_json(cls, json_str: str) -> CustomerDetailResponse:
        """Create an instance of CustomerDetailResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of business_details
        if self.business_details:
            _dict['businessDetails'] = self.business_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in business_partner (list)
        _items = []
        if self.business_partner:
            for _item in self.business_partner:
                if _item:
                    _items.append(_item.to_dict())
            _dict['businessPartner'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in payment_ids (list)
        _items = []
        if self.payment_ids:
            for _item in self.payment_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['paymentIds'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in professional_details (list)
        _items = []
        if self.professional_details:
            for _item in self.professional_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['professionalDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in rfi_details (list)
        _items = []
        if self.rfi_details:
            for _item in self.rfi_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rfiDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of risk_assessment_info
        if self.risk_assessment_info:
            _dict['riskAssessmentInfo'] = self.risk_assessment_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in stakeholder_details (list)
        _items = []
        if self.stakeholder_details:
            for _item in self.stakeholder_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['stakeholderDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tax_details (list)
        _items = []
        if self.tax_details:
            for _item in self.tax_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['taxDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerDetailResponse:
        """Create an instance of CustomerDetailResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerDetailResponse.parse_obj(obj)

        _obj = CustomerDetailResponse.parse_obj({
            "tags": obj.get("tags"),
            "billing_address1": obj.get("billingAddress1"),
            "billing_address2": obj.get("billingAddress2"),
            "billing_city": obj.get("billingCity"),
            "billing_country": obj.get("billingCountry"),
            "billing_landmark": obj.get("billingLandmark"),
            "billing_state": obj.get("billingState"),
            "billing_zip_code": obj.get("billingZipCode"),
            "block_comment": obj.get("blockComment"),
            "block_reason": obj.get("blockReason"),
            "block_updated_by": obj.get("blockUpdatedBy"),
            "business_details": BusinessDetailsResponseDTO.from_dict(obj.get("businessDetails")) if obj.get("businessDetails") is not None else None,
            "business_partner": [BusinessPartnerDetailsResponseDTO.from_dict(_item) for _item in obj.get("businessPartner")] if obj.get("businessPartner") is not None else None,
            "compliance_level": obj.get("complianceLevel"),
            "compliance_remarks": obj.get("complianceRemarks"),
            "compliance_status": obj.get("complianceStatus"),
            "country_code": obj.get("countryCode"),
            "country_of_birth": obj.get("countryOfBirth"),
            "created_at": obj.get("createdAt"),
            "customer_hash_id": obj.get("customerHashId"),
            "customer_id": obj.get("customerId"),
            "customer_type": obj.get("customerType"),
            "date_of_birth": obj.get("dateOfBirth"),
            "delivery_address1": obj.get("deliveryAddress1"),
            "delivery_address2": obj.get("deliveryAddress2"),
            "delivery_city": obj.get("deliveryCity"),
            "delivery_country": obj.get("deliveryCountry"),
            "delivery_landmark": obj.get("deliveryLandmark"),
            "delivery_state": obj.get("deliveryState"),
            "delivery_zip_code": obj.get("deliveryZipCode"),
            "designation": obj.get("designation"),
            "email": obj.get("email"),
            "employee_id": obj.get("employeeId"),
            "estimated_monthly_funding": obj.get("estimatedMonthlyFunding"),
            "estimated_monthly_funding_currency": obj.get("estimatedMonthlyFundingCurrency"),
            "expected_countries_to_send_receive_from": obj.get("expectedCountriesToSendReceiveFrom"),
            "first_name": obj.get("firstName"),
            "gender": obj.get("gender"),
            "identification_data": obj.get("identificationData"),
            "identification_types": obj.get("identificationTypes"),
            "intended_use_of_account": obj.get("intendedUseOfAccount"),
            "international_payments_supported": obj.get("internationalPaymentsSupported"),
            "kyc_mode": obj.get("kycMode"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "mobile": obj.get("mobile"),
            "nationality": obj.get("nationality"),
            "native_language_name": obj.get("nativeLanguageName"),
            "payment_ids": [PaymentIdDTO.from_dict(_item) for _item in obj.get("paymentIds")] if obj.get("paymentIds") is not None else None,
            "pep": obj.get("pep"),
            "preferred_name": obj.get("preferredName"),
            "professional_details": [ProfessionalDetails.from_dict(_item) for _item in obj.get("professionalDetails")] if obj.get("professionalDetails") is not None else None,
            "reference_id": obj.get("referenceId"),
            "regulatory_region": obj.get("regulatoryRegion"),
            "remarks": obj.get("remarks"),
            "rfi_details": [CustomerRfiDetailsResponse.from_dict(_item) for _item in obj.get("rfiDetails")] if obj.get("rfiDetails") is not None else None,
            "risk_assessment_info": RiskAssessmentInfoResponseDTO.from_dict(obj.get("riskAssessmentInfo")) if obj.get("riskAssessmentInfo") is not None else None,
            "segment": obj.get("segment"),
            "stakeholder_details": [StakeholderDetailsResponseDTO.from_dict(_item) for _item in obj.get("stakeholderDetails")] if obj.get("stakeholderDetails") is not None else None,
            "status": obj.get("status"),
            "tax_details": [CustomerTaxDetailDTO.from_dict(_item) for _item in obj.get("taxDetails")] if obj.get("taxDetails") is not None else None,
            "terms_and_condition_acceptance_flag": obj.get("termsAndConditionAcceptanceFlag"),
            "terms_and_condition_name": obj.get("termsAndConditionName"),
            "terms_and_condition_version_id": obj.get("termsAndConditionVersionId"),
            "updated_at": obj.get("updatedAt"),
            "verification_consent": obj.get("verificationConsent"),
            "wallet_hash_id": obj.get("walletHashId")
        })
        return _obj


