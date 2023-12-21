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


from typing import List, Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, conlist, validator
from nium.models.auto_sweep_bank_details import AutoSweepBankDetails
from nium.models.client_currency_response_dto import ClientCurrencyResponseDTO
from nium.models.payment_ids_dto import PaymentIdsDTO
from nium.models.remitter_account_white_list import RemitterAccountWhiteList

class ClientDetailResponseDTO2(BaseModel):
    """
    ClientDetailResponseDTO2
    """
    account_validation: Optional[StrictBool] = Field(None, alias="accountValidation", description="This is applicable to RHA clients. This field will ensure whether the account-validation transactions are forwarded to client or not")
    allow_inter_client_wallet_transfer: Optional[StrictBool] = Field(None, alias="allowInterClientWalletTransfer", description="This field indicates whether inter client wallet transfer is allowed or not.")
    allow_third_party_funding: Optional[StrictBool] = Field(None, alias="allowThirdPartyFunding", description="This field specifies if third party funding is allowed or not.")
    apple_pay_support: Optional[StrictBool] = Field(None, alias="applePaySupport", description="This field contains the flag for apple pay support.")
    auto_sweep_bank_details: Optional[AutoSweepBankDetails] = Field(None, alias="autoSweepBankDetails")
    billing_address_as_corporate: Optional[StrictBool] = Field(None, alias="billingAddressAsCorporate", description="This field indicates whether individual customer at child level should have same billing address as business address of corporate's at parent level.")
    card_txn_narrative: Optional[StrictStr] = Field(None, alias="cardTxnNarrative", description="This field specifies the default transaction narrative.")
    card_txn_product_code: Optional[StrictStr] = Field(None, alias="cardTxnProductCode", description="This field specifies the internal card transaction product code.")
    card_txn_redirect_url: Optional[StrictStr] = Field(None, alias="cardTxnRedirectUrl", description="This field contains the card transaction redirected URL.")
    child_must_have_parent: Optional[StrictBool] = Field(None, alias="childMustHaveParent", description="This field indicates whether individual customer at child level must have corporate customer at parent level.")
    client_hash_id: Optional[StrictStr] = Field(None, alias="clientHashId", description="This field contains the unique client identifier generated and shared before API handshake.")
    client_id_number: Optional[StrictStr] = Field(None, alias="clientIdNumber", description="This field shall be deprecated in future.")
    compliance_callback_url: Optional[StrictStr] = Field(None, alias="complianceCallbackUrl", description="This field specifies the compliance callback URL.")
    compliance_status_callback_url: Optional[StrictStr] = Field(None, alias="complianceStatusCallbackUrl", description="This field contains the redirection URL for compliance callback.")
    confirmation_of_payee: Optional[StrictBool] = Field(None, alias="confirmationOfPayee", description="This field indicates whether Confirmation of Payee is allowed or not.")
    contact_no: Optional[StrictStr] = Field(None, alias="contactNo", description="This field contains the client's contact number.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field contains the 3-letter ISO-4217 currency code.")
    currencies: Optional[conlist(ClientCurrencyResponseDTO)] = Field(None, description="This is an array objects which holds currency details.")
    currency_authorization_type: Optional[StrictStr] = Field(None, alias="currencyAuthorizationType", description="This field denotes the authorization type of a client. The valid values are as shown below and you may further refer to the detailed [Explanation of currencyAuthorizationType](https://docs.nium.com/baas/get-client-details#explanation-of-currencyauthorizationtype):")
    custom_fee_enabled: Optional[StrictBool] = Field(None, alias="customFeeEnabled", description="This field contains the client preference to levy custom fee.")
    customer_auth_url: Optional[StrictStr] = Field(None, alias="customerAuthUrl", description="This field contains the customer authorization URL.")
    deduplication_flag: Optional[StrictBool] = Field(None, alias="deduplicationFlag", description="This field contains the mobile/email uniqueness flag.")
    ekyc_redirect_url: Optional[StrictStr] = Field(None, alias="ekycRedirectUrl")
    email: Optional[StrictStr] = Field(None, description="This field contains the client's email Id.")
    funding_instrument_type: Optional[StrictStr] = Field(None, alias="fundingInstrumentType", description="This field is used to define whether the customer is allowed to fund their wallet or not. If yes that is not RESTRICTED, then either using DEBIT CARD or both DEBIT and CREDIT cards.")
    google_pay_support: Optional[StrictBool] = Field(None, alias="googlePaySupport", description="This field contains the flag for google pay support.")
    license_entity: Optional[StrictStr] = Field(None, alias="licenseEntity", description="This field contains the license ownership for a client.The possible values are:")
    logo_url: Optional[StrictStr] = Field(None, alias="logoUrl", description="This field contains the client's logo URL.")
    markup: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="This field contains the cross currency transaction markup value.")
    minimum_customer_age: Optional[StrictInt] = Field(None, alias="minimumCustomerAge", description="This field contains the minimum customer age which should be 18 years. Please discuss with your NIUM account manager for any special use-cases.")
    name: Optional[StrictStr] = Field(None, description="This field contains the name of a client.")
    notification_webhook: Optional[StrictStr] = Field(None, alias="notificationWebhook", description="This field contains the Webhook notification redirection URL.")
    payment_ids: Optional[conlist(PaymentIdsDTO)] = Field(None, alias="paymentIds", description="This is an array object which holds the client payment Id response details.")
    post_funded_payout: Optional[StrictBool] = Field(None, alias="postFundedPayout", description="This field contains the Post Funded Payout of the client.")
    prefund_name: Optional[StrictStr] = Field(None, alias="prefundName", description="This field contains the name defined for ICC transactions")
    regulatory_region: Optional[StrictStr] = Field(None, alias="regulatoryRegion", description="This field contains the regulatory region of the client.")
    samsung_pay_support: Optional[StrictBool] = Field(None, alias="samsungPaySupport", description="This field contains the flag for samsung pay support.")
    whitelisted_remitter_accounts: Optional[conlist(RemitterAccountWhiteList)] = Field(None, alias="whitelistedRemitterAccounts", description="This is an array object which holds the remitter accounts which are whitelisted for the client.")
    __properties = ["accountValidation", "allowInterClientWalletTransfer", "allowThirdPartyFunding", "applePaySupport", "autoSweepBankDetails", "billingAddressAsCorporate", "cardTxnNarrative", "cardTxnProductCode", "cardTxnRedirectUrl", "childMustHaveParent", "clientHashId", "clientIdNumber", "complianceCallbackUrl", "complianceStatusCallbackUrl", "confirmationOfPayee", "contactNo", "countryCode", "currencies", "currencyAuthorizationType", "customFeeEnabled", "customerAuthUrl", "deduplicationFlag", "ekycRedirectUrl", "email", "fundingInstrumentType", "googlePaySupport", "licenseEntity", "logoUrl", "markup", "minimumCustomerAge", "name", "notificationWebhook", "paymentIds", "postFundedPayout", "prefundName", "regulatoryRegion", "samsungPaySupport", "whitelistedRemitterAccounts"]

    @validator('currency_authorization_type')
    def currency_authorization_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('SINGLE', 'DUAL', 'MULTI', 'AUTO_SWEEP'):
            raise ValueError("must be one of enum values ('SINGLE', 'DUAL', 'MULTI', 'AUTO_SWEEP')")
        return value

    @validator('funding_instrument_type')
    def funding_instrument_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('RESTRICTED', 'ONLY_DEBIT', 'CREDIT_AND_DEBIT'):
            raise ValueError("must be one of enum values ('RESTRICTED', 'ONLY_DEBIT', 'CREDIT_AND_DEBIT')")
        return value

    @validator('license_entity')
    def license_entity_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NIUM', 'THIRD_PARTY'):
            raise ValueError("must be one of enum values ('NIUM', 'THIRD_PARTY')")
        return value

    @validator('regulatory_region')
    def regulatory_region_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('SG', 'EU', 'AU', 'HK', 'UK', 'US', 'CA'):
            raise ValueError("must be one of enum values ('SG', 'EU', 'AU', 'HK', 'UK', 'US', 'CA')")
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
    def from_json(cls, json_str: str) -> ClientDetailResponseDTO2:
        """Create an instance of ClientDetailResponseDTO2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of auto_sweep_bank_details
        if self.auto_sweep_bank_details:
            _dict['autoSweepBankDetails'] = self.auto_sweep_bank_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in currencies (list)
        _items = []
        if self.currencies:
            for _item in self.currencies:
                if _item:
                    _items.append(_item.to_dict())
            _dict['currencies'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in payment_ids (list)
        _items = []
        if self.payment_ids:
            for _item in self.payment_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['paymentIds'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in whitelisted_remitter_accounts (list)
        _items = []
        if self.whitelisted_remitter_accounts:
            for _item in self.whitelisted_remitter_accounts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['whitelistedRemitterAccounts'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ClientDetailResponseDTO2:
        """Create an instance of ClientDetailResponseDTO2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ClientDetailResponseDTO2.parse_obj(obj)

        _obj = ClientDetailResponseDTO2.parse_obj({
            "account_validation": obj.get("accountValidation"),
            "allow_inter_client_wallet_transfer": obj.get("allowInterClientWalletTransfer"),
            "allow_third_party_funding": obj.get("allowThirdPartyFunding"),
            "apple_pay_support": obj.get("applePaySupport"),
            "auto_sweep_bank_details": AutoSweepBankDetails.from_dict(obj.get("autoSweepBankDetails")) if obj.get("autoSweepBankDetails") is not None else None,
            "billing_address_as_corporate": obj.get("billingAddressAsCorporate"),
            "card_txn_narrative": obj.get("cardTxnNarrative"),
            "card_txn_product_code": obj.get("cardTxnProductCode"),
            "card_txn_redirect_url": obj.get("cardTxnRedirectUrl"),
            "child_must_have_parent": obj.get("childMustHaveParent"),
            "client_hash_id": obj.get("clientHashId"),
            "client_id_number": obj.get("clientIdNumber"),
            "compliance_callback_url": obj.get("complianceCallbackUrl"),
            "compliance_status_callback_url": obj.get("complianceStatusCallbackUrl"),
            "confirmation_of_payee": obj.get("confirmationOfPayee"),
            "contact_no": obj.get("contactNo"),
            "country_code": obj.get("countryCode"),
            "currencies": [ClientCurrencyResponseDTO.from_dict(_item) for _item in obj.get("currencies")] if obj.get("currencies") is not None else None,
            "currency_authorization_type": obj.get("currencyAuthorizationType"),
            "custom_fee_enabled": obj.get("customFeeEnabled"),
            "customer_auth_url": obj.get("customerAuthUrl"),
            "deduplication_flag": obj.get("deduplicationFlag"),
            "ekyc_redirect_url": obj.get("ekycRedirectUrl"),
            "email": obj.get("email"),
            "funding_instrument_type": obj.get("fundingInstrumentType"),
            "google_pay_support": obj.get("googlePaySupport"),
            "license_entity": obj.get("licenseEntity"),
            "logo_url": obj.get("logoUrl"),
            "markup": obj.get("markup"),
            "minimum_customer_age": obj.get("minimumCustomerAge"),
            "name": obj.get("name"),
            "notification_webhook": obj.get("notificationWebhook"),
            "payment_ids": [PaymentIdsDTO.from_dict(_item) for _item in obj.get("paymentIds")] if obj.get("paymentIds") is not None else None,
            "post_funded_payout": obj.get("postFundedPayout"),
            "prefund_name": obj.get("prefundName"),
            "regulatory_region": obj.get("regulatoryRegion"),
            "samsung_pay_support": obj.get("samsungPaySupport"),
            "whitelisted_remitter_accounts": [RemitterAccountWhiteList.from_dict(_item) for _item in obj.get("whitelistedRemitterAccounts")] if obj.get("whitelistedRemitterAccounts") is not None else None
        })
        return _obj


