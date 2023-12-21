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


from typing import Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, validator
from nium.models.card_meta_data_response_dto import CardMetaDataResponseDTO

class BeneficiaryResponseDTO(BaseModel):
    """
    BeneficiaryResponseDTO
    """
    autosweep_payout_account: Optional[StrictBool] = Field(None, alias="autosweepPayoutAccount", description="This field accepts the boolean value for the autosweepPayoutAccount.")
    beneficiary_account_number: Optional[StrictStr] = Field(None, alias="beneficiaryAccountNumber", description="This field accepts an account number as a payout detail.")
    beneficiary_account_type: Optional[StrictStr] = Field(None, alias="beneficiaryAccountType", description="This field accepts the bank account type of the beneficiary. The account type can be either Individual or Company.")
    beneficiary_address: Optional[StrictStr] = Field(None, alias="beneficiaryAddress", description="This field accepts an address of the beneficiary.")
    beneficiary_bank_account_type: Optional[StrictStr] = Field(None, alias="beneficiaryBankAccountType", description="This field contains one of following four bank account types given at the time of beneficiary creation: • Current • Saving • Maestra • Checking")
    beneficiary_bank_code: Optional[StrictStr] = Field(None, alias="beneficiaryBankCode", description="This field accepts the bank code of the payout.")
    beneficiary_bank_name: Optional[StrictStr] = Field(None, alias="beneficiaryBankName", description="This field contains the beneficiary bank name.")
    beneficiary_card_expiry_date: Optional[StrictStr] = Field(None, alias="beneficiaryCardExpiryDate", description="This field contains the beneficiary’s card expiry date.")
    beneficiary_card_issuer_name: Optional[StrictStr] = Field(None, alias="beneficiaryCardIssuerName", description="This field contains the beneficiary’s card issuer name.")
    beneficiary_card_meta_data: Optional[CardMetaDataResponseDTO] = Field(None, alias="beneficiaryCardMetaData")
    beneficiary_card_number_mask: Optional[StrictStr] = Field(None, alias="beneficiaryCardNumberMask", description="This field contains the 16-digit masked card number of beneficiary in the format XXXX XXXX XXXX 8351.")
    beneficiary_card_token: Optional[StrictStr] = Field(None, alias="beneficiaryCardToken", description="This field contains the system generated token number to identify the card stored at NIUM's platform.")
    beneficiary_card_type: Optional[StrictStr] = Field(None, alias="beneficiaryCardType", description="This field contains the beneficiary card type, for example, VISA, geoswift.")
    beneficiary_city: Optional[StrictStr] = Field(None, alias="beneficiaryCity", description="This field accepts the city of the beneficiary.")
    beneficiary_contact_country_code: Optional[StrictStr] = Field(None, alias="beneficiaryContactCountryCode", description="This field accepts the mobile country code of the beneficiary.")
    beneficiary_contact_name: Optional[StrictStr] = Field(None, alias="beneficiaryContactName")
    beneficiary_contact_number: Optional[StrictStr] = Field(None, alias="beneficiaryContactNumber", description="This field accepts the mobile number of the beneficiary.")
    beneficiary_country_code: Optional[StrictStr] = Field(None, alias="beneficiaryCountryCode", description="This field accepts  the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the mobile number of beneficiary.")
    beneficiary_created_at: Optional[StrictStr] = Field(None, alias="beneficiaryCreatedAt", description="This field contains the date and time of beneficiary creation.")
    beneficiary_dob: Optional[StrictStr] = Field(None, alias="beneficiaryDob")
    beneficiary_email: Optional[StrictStr] = Field(None, alias="beneficiaryEmail", description="This field accepts an email of the beneficiary.")
    beneficiary_entity_type: Optional[StrictStr] = Field(None, alias="beneficiaryEntityType")
    beneficiary_establishment_date: Optional[StrictStr] = Field(None, alias="beneficiaryEstablishmentDate")
    beneficiary_hash_id: Optional[StrictStr] = Field(None, alias="beneficiaryHashId", description="This field contains the unique beneficiary hash ID.")
    beneficiary_identification_type: Optional[StrictStr] = Field(None, alias="beneficiaryIdentificationType", description="This field accepts the type of identification document name for a beneficiary.")
    beneficiary_identification_value: Optional[StrictStr] = Field(None, alias="beneficiaryIdentificationValue", description="This field accepts an identification document number for the beneficiary.")
    beneficiary_name: Optional[StrictStr] = Field(None, alias="beneficiaryName", description="This field accepts the name of the beneficiary.")
    beneficiary_postcode: Optional[StrictStr] = Field(None, alias="beneficiaryPostcode", description="This field accepts the postal code of the beneficiary.")
    beneficiary_state: Optional[StrictStr] = Field(None, alias="beneficiaryState", description="This field accepts the state of the beneficiary.")
    beneficiary_updated_at: Optional[StrictStr] = Field(None, alias="beneficiaryUpdatedAt", description="This field contains the date and time of beneficiary updation.")
    default_autosweep_payout_account: Optional[StrictBool] = Field(None, alias="defaultAutosweepPayoutAccount", description="This field accepts the boolean value for the defaultAutosweepPayoutAccount.")
    destination_country: Optional[StrictStr] = Field(None, alias="destinationCountry", description="This field accepts the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the payout bank.")
    destination_currency: Optional[StrictStr] = Field(None, alias="destinationCurrency", description="This field accepts the 3-letter [ISO-4217 destination currency code](https://www.iso.org/iso-4217-currency-codes.html) of the payout as per the destination country from supported corridors.")
    payout_created_at: Optional[StrictStr] = Field(None, alias="payoutCreatedAt", description="This field contains the date and time of payout creation.")
    payout_hash_id: Optional[StrictStr] = Field(None, alias="payoutHashId", description="This field contains the unique payout hash ID.")
    payout_method: Optional[StrictStr] = Field(None, alias="payoutMethod", description="This field accepts the payout method for the remittance payout.")
    payout_updated_at: Optional[StrictStr] = Field(None, alias="payoutUpdatedAt")
    proxy_type: Optional[StrictStr] = Field(None, alias="proxyType", description="This field contains the proxy type sent in the payment request. • For SGD-PayNow: The proxy type can be MOBILE, UEN, NRIC, or VPA. • For INR-UPI: The proxy type should be VPA. • For BRL-PIX: The proxy type can be MOBILE, ID, EMAIL, or RANDOM_KEY. • For AUD-PayID: The proxy type can be MOBILE, EMAIL, ABN, or ORGANISATION_ID( only domestic payouts are allowed). • For MYR-DuitNow: The proxy type can be NRIC, PASSPORT, CORPORATE_REGISTRATION_NUMBER, MOBILE, or ARMY_ID.")
    proxy_value: Optional[StrictStr] = Field(None, alias="proxyValue", description="This field contains the proxy value such as VPA, UEN, or mobile number etc.")
    remitter_beneficiary_relationship: Optional[StrictStr] = Field(None, alias="remitterBeneficiaryRelationship", description="This field accepts the relationship of the beneficiary with the remitter.")
    routing_code_type1: Optional[StrictStr] = Field(None, alias="routingCodeType1", description="This field accepts the routing code type 1, for example, SWIFT for all countries, IFSC for India, SORT CODE for UK, ACH CODE for USA, BRANCH CODE for Brazil and Bangladesh, BSB CODE for Australia, BANK CODE for HongKong.")
    routing_code_type2: Optional[StrictStr] = Field(None, alias="routingCodeType2", description="This field accepts the routing code type 2, for example, SWIFT for all countries, IFSC for India, SORT CODE for UK, ACH CODE for USA, BRANCH CODE for Brazil and Bangladesh, BSB CODE for Australia, BANK CODE for HongKong.")
    routing_code_value1: Optional[StrictStr] = Field(None, alias="routingCodeValue1", description="This field accepts the routing code value 1, for example, ADCBINBB or ADCBINBB123 for SWIFT, SBIN0000058 for IFSC, 100000 for SORT CODE, 111000025 for ACH CODE, 012515 for BSB CODE, 151 for BANK CODE.")
    routing_code_value2: Optional[StrictStr] = Field(None, alias="routingCodeValue2", description="This field accepts the routing code value 2, for example, ADCBINBB or ADCBINBB123 for SWIFT, SBIN0000058 for IFSC, 100000 for SORT CODE, 111000025 for ACH CODE, 012515 for BSB CODE, 151 for BANK CODE.")
    __properties = ["autosweepPayoutAccount", "beneficiaryAccountNumber", "beneficiaryAccountType", "beneficiaryAddress", "beneficiaryBankAccountType", "beneficiaryBankCode", "beneficiaryBankName", "beneficiaryCardExpiryDate", "beneficiaryCardIssuerName", "beneficiaryCardMetaData", "beneficiaryCardNumberMask", "beneficiaryCardToken", "beneficiaryCardType", "beneficiaryCity", "beneficiaryContactCountryCode", "beneficiaryContactName", "beneficiaryContactNumber", "beneficiaryCountryCode", "beneficiaryCreatedAt", "beneficiaryDob", "beneficiaryEmail", "beneficiaryEntityType", "beneficiaryEstablishmentDate", "beneficiaryHashId", "beneficiaryIdentificationType", "beneficiaryIdentificationValue", "beneficiaryName", "beneficiaryPostcode", "beneficiaryState", "beneficiaryUpdatedAt", "defaultAutosweepPayoutAccount", "destinationCountry", "destinationCurrency", "payoutCreatedAt", "payoutHashId", "payoutMethod", "payoutUpdatedAt", "proxyType", "proxyValue", "remitterBeneficiaryRelationship", "routingCodeType1", "routingCodeType2", "routingCodeValue1", "routingCodeValue2"]

    @validator('beneficiary_bank_account_type')
    def beneficiary_bank_account_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Current', 'Saving', 'Maestra', 'Checking'):
            raise ValueError("must be one of enum values ('Current', 'Saving', 'Maestra', 'Checking')")
        return value

    @validator('payout_method')
    def payout_method_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('LOCAL', 'SWIFT', 'WALLET', 'PROXY', 'CARD'):
            raise ValueError("must be one of enum values ('LOCAL', 'SWIFT', 'WALLET', 'PROXY', 'CARD')")
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
    def from_json(cls, json_str: str) -> BeneficiaryResponseDTO:
        """Create an instance of BeneficiaryResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of beneficiary_card_meta_data
        if self.beneficiary_card_meta_data:
            _dict['beneficiaryCardMetaData'] = self.beneficiary_card_meta_data.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BeneficiaryResponseDTO:
        """Create an instance of BeneficiaryResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BeneficiaryResponseDTO.parse_obj(obj)

        _obj = BeneficiaryResponseDTO.parse_obj({
            "autosweep_payout_account": obj.get("autosweepPayoutAccount"),
            "beneficiary_account_number": obj.get("beneficiaryAccountNumber"),
            "beneficiary_account_type": obj.get("beneficiaryAccountType"),
            "beneficiary_address": obj.get("beneficiaryAddress"),
            "beneficiary_bank_account_type": obj.get("beneficiaryBankAccountType"),
            "beneficiary_bank_code": obj.get("beneficiaryBankCode"),
            "beneficiary_bank_name": obj.get("beneficiaryBankName"),
            "beneficiary_card_expiry_date": obj.get("beneficiaryCardExpiryDate"),
            "beneficiary_card_issuer_name": obj.get("beneficiaryCardIssuerName"),
            "beneficiary_card_meta_data": CardMetaDataResponseDTO.from_dict(obj.get("beneficiaryCardMetaData")) if obj.get("beneficiaryCardMetaData") is not None else None,
            "beneficiary_card_number_mask": obj.get("beneficiaryCardNumberMask"),
            "beneficiary_card_token": obj.get("beneficiaryCardToken"),
            "beneficiary_card_type": obj.get("beneficiaryCardType"),
            "beneficiary_city": obj.get("beneficiaryCity"),
            "beneficiary_contact_country_code": obj.get("beneficiaryContactCountryCode"),
            "beneficiary_contact_name": obj.get("beneficiaryContactName"),
            "beneficiary_contact_number": obj.get("beneficiaryContactNumber"),
            "beneficiary_country_code": obj.get("beneficiaryCountryCode"),
            "beneficiary_created_at": obj.get("beneficiaryCreatedAt"),
            "beneficiary_dob": obj.get("beneficiaryDob"),
            "beneficiary_email": obj.get("beneficiaryEmail"),
            "beneficiary_entity_type": obj.get("beneficiaryEntityType"),
            "beneficiary_establishment_date": obj.get("beneficiaryEstablishmentDate"),
            "beneficiary_hash_id": obj.get("beneficiaryHashId"),
            "beneficiary_identification_type": obj.get("beneficiaryIdentificationType"),
            "beneficiary_identification_value": obj.get("beneficiaryIdentificationValue"),
            "beneficiary_name": obj.get("beneficiaryName"),
            "beneficiary_postcode": obj.get("beneficiaryPostcode"),
            "beneficiary_state": obj.get("beneficiaryState"),
            "beneficiary_updated_at": obj.get("beneficiaryUpdatedAt"),
            "default_autosweep_payout_account": obj.get("defaultAutosweepPayoutAccount"),
            "destination_country": obj.get("destinationCountry"),
            "destination_currency": obj.get("destinationCurrency"),
            "payout_created_at": obj.get("payoutCreatedAt"),
            "payout_hash_id": obj.get("payoutHashId"),
            "payout_method": obj.get("payoutMethod"),
            "payout_updated_at": obj.get("payoutUpdatedAt"),
            "proxy_type": obj.get("proxyType"),
            "proxy_value": obj.get("proxyValue"),
            "remitter_beneficiary_relationship": obj.get("remitterBeneficiaryRelationship"),
            "routing_code_type1": obj.get("routingCodeType1"),
            "routing_code_type2": obj.get("routingCodeType2"),
            "routing_code_value1": obj.get("routingCodeValue1"),
            "routing_code_value2": obj.get("routingCodeValue2")
        })
        return _obj


