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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class AddBeneficiaryRequestDTO(BaseModel):
    """
    AddBeneficiaryRequestDTO
    """
    authentication_code: Optional[StrictStr] = Field(None, alias="authenticationCode", description="This fields accepts the authenticationCode generated as part of SCA(Strong Customer Authentication). Note: Authentication code must be passed if regulatory region of the program is UK or EU and License Entity NIUM. For other region, this field is non-mandatory.")
    auto_sweep_payout_account: Optional[StrictBool] = Field(None, alias="autoSweepPayoutAccount")
    beneficiary_account_number: Optional[StrictStr] = Field(None, alias="beneficiaryAccountNumber", description="This field accepts an account number.")
    beneficiary_account_type: StrictStr = Field(..., alias="beneficiaryAccountType", description="This field accepts the bank account type of the beneficiary. The account type can be either Individual or Corporate.")
    beneficiary_address: Optional[StrictStr] = Field(None, alias="beneficiaryAddress", description="This field accepts an address of the beneficiary.")
    beneficiary_alias: Optional[StrictStr] = Field(None, alias="beneficiaryAlias", description="This field accepts the alias of beneficiary.")
    beneficiary_bank_account_type: Optional[StrictStr] = Field(None, alias="beneficiaryBankAccountType", description="This field accepts the type of account. This field is conditional in case of WALLET payout and the possible values are: Current Saving Maestra Checking")
    beneficiary_bank_code: Optional[StrictStr] = Field(None, alias="beneficiaryBankCode", description="This field accepts the beneficiary bank code.")
    beneficiary_bank_name: Optional[StrictStr] = Field(None, alias="beneficiaryBankName", description="This field accepts the beneficiary bank name.")
    beneficiary_card_expiry_date: Optional[StrictStr] = Field(None, alias="beneficiaryCardExpiryDate", description="This field accepts expiry date of card.")
    beneficiary_card_issuer_name: Optional[StrictStr] = Field(None, alias="beneficiaryCardIssuerName", description="This field accepts issuer name of the card.")
    beneficiary_city: Optional[StrictStr] = Field(None, alias="beneficiaryCity", description="This field accepts the city of the beneficiary.")
    beneficiary_contact_country_code: Optional[StrictStr] = Field(None, alias="beneficiaryContactCountryCode", description="This field accepts the mobile number country code of the beneficiary.")
    beneficiary_contact_name: Optional[StrictStr] = Field(None, alias="beneficiaryContactName")
    beneficiary_contact_number: Optional[StrictStr] = Field(None, alias="beneficiaryContactNumber", description="This field accepts the mobile number of the beneficiary.")
    beneficiary_country_code: StrictStr = Field(..., alias="beneficiaryCountryCode", description="This field accepts the [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of the beneficiary.")
    beneficiary_dob: Optional[StrictStr] = Field(None, alias="beneficiaryDob")
    beneficiary_email: Optional[StrictStr] = Field(None, alias="beneficiaryEmail", description="This field accepts an email of the beneficiary.")
    beneficiary_entity_type: Optional[StrictStr] = Field(None, alias="beneficiaryEntityType")
    beneficiary_establishment_date: Optional[StrictStr] = Field(None, alias="beneficiaryEstablishmentDate")
    beneficiary_identification_type: Optional[StrictStr] = Field(None, alias="beneficiaryIdentificationType", description="This field accepts the type of identification document name for a beneficiary.")
    beneficiary_identification_value: Optional[StrictStr] = Field(None, alias="beneficiaryIdentificationValue", description="This field accepts an identification document number for the beneficiary.")
    beneficiary_name: StrictStr = Field(..., alias="beneficiaryName", description="This field accepts the name of the beneficiary.")
    beneficiary_postcode: Optional[StrictStr] = Field(None, alias="beneficiaryPostcode", description="This field accepts the postal code of the beneficiary.")
    beneficiary_state: Optional[StrictStr] = Field(None, alias="beneficiaryState", description="This field accepts the state of the beneficiary.")
    default_auto_sweep_payout_account: Optional[StrictBool] = Field(None, alias="defaultAutoSweepPayoutAccount")
    destination_country: Optional[StrictStr] = Field(None, alias="destinationCountry", description="This field contains the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of the destination country.")
    destination_currency: StrictStr = Field(..., alias="destinationCurrency", description="This field accepts the 3-letter [ISO-4217 destination currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    encrypted_beneficiary_card_token: Optional[StrictStr] = Field(None, alias="encryptedBeneficiaryCardToken", description="This field accepts the system generated token number to identify the card stored at NIUM's platform. Note: This field is mandatory if the client is non-PCI DSS compliant.")
    payout_method: StrictStr = Field(..., alias="payoutMethod", description="This field accepts the payout method for the remittance payout. This field can accept one of the following values: LOCAL SWIFT WALLET CARD PROXY FEDWIRE")
    proxy_type: Optional[StrictStr] = Field(None, alias="proxyType", description="This field indicates the proxy type sent in the payment request. For SGD-PayNow: The proxy type can be MOBILE, UEN , NRIC, or VPA  For INR-UPI: The proxy type should be VPA For BRL-PIX: The proxy type can be MOBILE, ID, EMAIL, or RANDOM_KEY  For AUD-PayID: The proxy type can be MOBILE, EMAIL, ABN, or ORGANISATION_ID (only domestic payouts are allowed) For MYR-DuitNow: The proxy type can be NRIC, PASSPORT, CORPORATE_REGISTRATION_NUMBER, MOBILE, or ARMY_ID Note: This field is mandatory when the payoutMethod type is PROXY ")
    proxy_value: Optional[StrictStr] = Field(None, alias="proxyValue", description="This field indicates the proxy value such as VPA, UEN, or mobile number etc. Note: This field is mandatory when the payoutMethod type is PROXY The mobile number should include country code.")
    remitter_beneficiary_relationship: Optional[StrictStr] = Field(None, alias="remitterBeneficiaryRelationship", description="This field accepts the relationship of the beneficiary with the remitter.")
    routing_code_type1: Optional[StrictStr] = Field(None, alias="routingCodeType1", description="This field accepts the routing code type 1, for example, SWIFT for all countries, IFSC for India, SORT CODE for UK, ACH CODE for USA, BRANCH CODE for Brazil and Bangladesh, BSB CODE for Australia, BANK CODE for HongKong.")
    routing_code_type2: Optional[StrictStr] = Field(None, alias="routingCodeType2", description="This field accepts the routing code type 2, for example, SWIFT for all countries, IFSC for India, SORT CODE for UK, ACH CODE for USA, BRANCH CODE for Brazil and Bangladesh, BSB CODE for Australia, BANK CODE for HongKong.")
    routing_code_value1: Optional[StrictStr] = Field(None, alias="routingCodeValue1", description="This field accepts the routing code value 1, for example, ADCBINBB or ADCBINBB123 for SWIFT, SBIN0000058 for IFSC, 100000 for SORT CODE, 111000025 for ACH CODE, 012515 for BSB CODE, 151 for BANK CODE.")
    routing_code_value2: Optional[StrictStr] = Field(None, alias="routingCodeValue2", description="This field accepts the routing code value 2, for example, ADCBINBB or ADCBINBB123 for SWIFT, SBIN0000058 for IFSC, 100000 for SORT CODE, 111000025 for ACH CODE, 012515 for BSB CODE, 151 for BANK CODE.")
    __properties = ["authenticationCode", "autoSweepPayoutAccount", "beneficiaryAccountNumber", "beneficiaryAccountType", "beneficiaryAddress", "beneficiaryAlias", "beneficiaryBankAccountType", "beneficiaryBankCode", "beneficiaryBankName", "beneficiaryCardExpiryDate", "beneficiaryCardIssuerName", "beneficiaryCity", "beneficiaryContactCountryCode", "beneficiaryContactName", "beneficiaryContactNumber", "beneficiaryCountryCode", "beneficiaryDob", "beneficiaryEmail", "beneficiaryEntityType", "beneficiaryEstablishmentDate", "beneficiaryIdentificationType", "beneficiaryIdentificationValue", "beneficiaryName", "beneficiaryPostcode", "beneficiaryState", "defaultAutoSweepPayoutAccount", "destinationCountry", "destinationCurrency", "encryptedBeneficiaryCardToken", "payoutMethod", "proxyType", "proxyValue", "remitterBeneficiaryRelationship", "routingCodeType1", "routingCodeType2", "routingCodeValue1", "routingCodeValue2"]

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
    def from_json(cls, json_str: str) -> AddBeneficiaryRequestDTO:
        """Create an instance of AddBeneficiaryRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddBeneficiaryRequestDTO:
        """Create an instance of AddBeneficiaryRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddBeneficiaryRequestDTO.parse_obj(obj)

        _obj = AddBeneficiaryRequestDTO.parse_obj({
            "authentication_code": obj.get("authenticationCode"),
            "auto_sweep_payout_account": obj.get("autoSweepPayoutAccount"),
            "beneficiary_account_number": obj.get("beneficiaryAccountNumber"),
            "beneficiary_account_type": obj.get("beneficiaryAccountType"),
            "beneficiary_address": obj.get("beneficiaryAddress"),
            "beneficiary_alias": obj.get("beneficiaryAlias"),
            "beneficiary_bank_account_type": obj.get("beneficiaryBankAccountType"),
            "beneficiary_bank_code": obj.get("beneficiaryBankCode"),
            "beneficiary_bank_name": obj.get("beneficiaryBankName"),
            "beneficiary_card_expiry_date": obj.get("beneficiaryCardExpiryDate"),
            "beneficiary_card_issuer_name": obj.get("beneficiaryCardIssuerName"),
            "beneficiary_city": obj.get("beneficiaryCity"),
            "beneficiary_contact_country_code": obj.get("beneficiaryContactCountryCode"),
            "beneficiary_contact_name": obj.get("beneficiaryContactName"),
            "beneficiary_contact_number": obj.get("beneficiaryContactNumber"),
            "beneficiary_country_code": obj.get("beneficiaryCountryCode"),
            "beneficiary_dob": obj.get("beneficiaryDob"),
            "beneficiary_email": obj.get("beneficiaryEmail"),
            "beneficiary_entity_type": obj.get("beneficiaryEntityType"),
            "beneficiary_establishment_date": obj.get("beneficiaryEstablishmentDate"),
            "beneficiary_identification_type": obj.get("beneficiaryIdentificationType"),
            "beneficiary_identification_value": obj.get("beneficiaryIdentificationValue"),
            "beneficiary_name": obj.get("beneficiaryName"),
            "beneficiary_postcode": obj.get("beneficiaryPostcode"),
            "beneficiary_state": obj.get("beneficiaryState"),
            "default_auto_sweep_payout_account": obj.get("defaultAutoSweepPayoutAccount"),
            "destination_country": obj.get("destinationCountry"),
            "destination_currency": obj.get("destinationCurrency"),
            "encrypted_beneficiary_card_token": obj.get("encryptedBeneficiaryCardToken"),
            "payout_method": obj.get("payoutMethod"),
            "proxy_type": obj.get("proxyType"),
            "proxy_value": obj.get("proxyValue"),
            "remitter_beneficiary_relationship": obj.get("remitterBeneficiaryRelationship"),
            "routing_code_type1": obj.get("routingCodeType1"),
            "routing_code_type2": obj.get("routingCodeType2"),
            "routing_code_value1": obj.get("routingCodeValue1"),
            "routing_code_value2": obj.get("routingCodeValue2")
        })
        return _obj


