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
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, conlist, validator
from nium.models.transaction_rfi_details_response import TransactionRfiDetailsResponse

class TransactionResponseDTO(BaseModel):
    """
    TransactionResponseDTO
    """
    tags: Optional[Dict[str, StrictStr]] = Field(None, description="This object contains the user defined key-value pairs provided by the client.")
    acquirer_country_code: Optional[StrictStr] = Field(None, alias="acquirerCountryCode", description="This field contains the country code of the acquirer.")
    acquiring_institution_code: Optional[StrictStr] = Field(None, alias="acquiringInstitutionCode", description="This field contains the acquiring institution code that identifies the financial institution acting as the acquirer of the transaction.")
    auth_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="authAmount", description="This field contains an authorization amount of the transaction.")
    auth_code: Optional[StrictStr] = Field(None, alias="authCode", description="This field contains the authorization code.")
    auth_currency_code: Optional[StrictStr] = Field(None, alias="authCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) of the auth currency, the currency in which amount is deducted from wallet.")
    billing_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="billingAmount", description="This field contains the equivalent transaction amount in base currency.")
    billing_conversion_rate: Optional[StrictStr] = Field(None, alias="billingConversionRate", description="This field contains the conversion rate of transaction currency to billing currency which is present for all card transactions.")
    billing_currency_code: Optional[StrictStr] = Field(None, alias="billingCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the billing currency or base currency")
    billing_replacement_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="billingReplacementAmount", description="The corrected amount of a transaction in a partial reversal. This is defined by ISO-8583 as a fixed length field with four subfields, but only the first subfield is used. A 12 position field for the corrected, billing amount of a customer's transaction, in the billing currency. The field is right justified, with lead zero fill.")
    business_transaction: Optional[StrictBool] = Field(None, alias="businessTransaction", description="This flag is used to mark or unmark a transaction as a business transaction.")
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashID", description="This field contains the unique card identifier generated while new/add-on card issuance.")
    card_transaction_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="cardTransactionAmount", description="This field contains the amount of a card transaction.")
    child_customer_hash_id: Optional[StrictStr] = Field(None, alias="childCustomerHashId", description="This field contains the unique child customer identifier generated while new child customer created.")
    client_hash_id: Optional[StrictStr] = Field(None, alias="clientHashId", description="Unique client identifier generated and shared before API handshake.")
    comments: Optional[StrictStr] = Field(None, description="This field contains the auto-generated comments with details on the transactions such as reason for transaction decline.")
    compliance_status: Optional[StrictStr] = Field(None, alias="complianceStatus", description="This field contains the compliance status of the transaction.The possible values are: NULL IN_PROGRESS ACTION_REQUIRED RFI_REQUESTED RFI_RESPONDED COMPLETED ERROR REJECT EXPIRED")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="This field contains the date and time of transaction when created in UTC.")
    current_with_holding_balance: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="currentWithHoldingBalance", description="This field will be deprecated in the future.")
    customer_hash_id: Optional[StrictStr] = Field(None, alias="customerHashId", description="This field contains the unique customer identifier generated while new customer created.")
    date_of_transaction: Optional[datetime] = Field(None, alias="dateOfTransaction", description="This field contains the date on which the transaction occurred in yyyy-MM-dd format.")
    debit: Optional[StrictBool] = Field(None, description="This field contains the flag signifies if the transaction is a debit transaction.")
    effective_auth_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="effectiveAuthAmount", description="This field contains an effective authorization amount which includes fees, markup, etc.")
    labels: Optional[Dict[str, StrictStr]] = Field(None, description="This object will contain different key-value pairs depending upon the type of transaction. Essentially, this object will contain different labels based on the type of transaction. The list will change over time depending on different use-cases. Please refer to the [Glossary of Labels:](https://docs.nium.com/baas/get-transactions#glossary-of-labels) complete list.")
    local_date: Optional[StrictStr] = Field(None, alias="localDate", description="This field contains the local date of the transaction.")
    local_time: Optional[StrictStr] = Field(None, alias="localTime", description="This field contains the local time of the transaction.")
    masked_card_number: Optional[StrictStr] = Field(None, alias="maskedCardNumber", description="This field contains the 16-digit masked card number in format 1234-56xx-xxxx-3456.")
    mcc: Optional[StrictStr] = Field(None, description="This field contains the four-digit Merchant Category Code.")
    merchant_category: Optional[StrictStr] = Field(None, alias="merchantCategory", description="This field contains the merchant category such as Airlines, Hotels, Shopping, etc.")
    merchant_city: Optional[StrictStr] = Field(None, alias="merchantCity", description="This field contains the city name of the merchant.")
    merchant_country: Optional[StrictStr] = Field(None, alias="merchantCountry", description="This field contains the country of the merchant.")
    merchant_id: Optional[StrictStr] = Field(None, alias="merchantID", description="This field contains the unique merchant identifier.")
    merchant_latitude: Optional[StrictStr] = Field(None, alias="merchantLatitude", description="This field contains the latitude of the merchant captured during geo-tagging.")
    merchant_longitude: Optional[StrictStr] = Field(None, alias="merchantLongitude", description="This field contains the longitude of the merchant captured during geo-tagging.")
    merchant_name: Optional[StrictStr] = Field(None, alias="merchantName", description="This field contains the name of the merchant.")
    merchant_name_location: Optional[StrictStr] = Field(None, alias="merchantNameLocation", description="This field contains the full merchant name and location data as received from network.")
    merchant_tagged_name: Optional[StrictStr] = Field(None, alias="merchantTaggedName", description="This field contains the tagged name of the merchant.")
    merchant_zoom_index: Optional[StrictStr] = Field(None, alias="merchantZoomIndex", description="This field contains the merchant map zoom index.")
    original_authorization_code: Optional[StrictStr] = Field(None, alias="originalAuthorizationCode", description="This field contains the authorization code of the original transaction in case of reversal.")
    partner_reference_number: Optional[StrictStr] = Field(None, alias="partnerReferenceNumber", description="This field contains the provided by an RHA client in response to an authorization.")
    payment_instrument_hash_id: Optional[StrictStr] = Field(None, alias="paymentInstrumentHashId", description="This field contains the unique payment instrument identifier generated for the linked card.")
    pos_condition_code: Optional[StrictStr] = Field(None, alias="posConditionCode", description="This field contains the pos condition code that describes the condition under which the transaction takes place at the point of service. 00 - Normal transaction 01 - Cardholder not present 03 - Merchant suspicious 08 - Mail/telephone order 51 - Account Verification Message(AVM) 55 - ICC Capable Branch ATM 59 - Electronic Commerce 90 - Recurring Payment")
    pos_entry_capability_code: Optional[StrictStr] = Field(None, alias="posEntryCapabilityCode", description="This field provides information about the terminal used at the point of service.Type of terminal field values include:0 - Unspecified 2 - Unattended terminal(customer-operated) 4 - Electronic cash register 7 - Telephone device 8 - MCAS device 9 - Mobile acceptance solution(mPOS) Capability of terminal field values include: 0 - Unspecified 1 - Terminal not used 2 - Magnetic stripe read capability 3 - Bar code read capability 4 - OCR read capability 5 - Integrated circuit card read capability 9 - Terminal does not read card data ")
    pos_entry_mode: Optional[StrictStr] = Field(None, alias="posEntryMode", description="This field contains the pos entry code that identifies the actual method used to capture the account number and expiration date, and the PIN capture capability of the terminal.This is a fixed‑length field with three subfields, as follows: 1. Positions 1‑2 - PAN and Date Entry Mode: This is a two‑digit code that identifies the actual method used at the point of service to enter the cardholder account number and card expiry date. 00 - Unknown 01 - Keyed transaction 02 - Magnetic stripe read 05 - Chip was read at the terminal 07 - Contactless 90 - Magnetic stripe read and transmitted unaltered 91 - Contactless - Magnetic stripe data (MSD) transmitted 2. Position 3 - PIN Entry Capability: This is a one‑digit code that identifies the capability of the authorization terminal, if one was used, to capture PINs. This coding does not necessarily mean that a PIN was entered or is included in this message: 0 - Unknown 1 - Terminal can accept PINs 2 - Terminal cannot accept PINs 3 - mPOS terminal can accept software-based PINs (Mastercard only) 3. Position 4 - Unused(filler): This is one digit of filler, which must be zero. ")
    previous_balance: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="previousBalance", description="This field contains the previous balance in the wallet.")
    processing_code: Optional[StrictStr] = Field(None, alias="processingCode", description="This field contains the processing code is a 6 character Visa field. Refer to the [link](https://en.wikipedia.org/wiki/ISO_8583#Processing_code) for more details on the processing code.")
    receipt_file_name: Optional[StrictStr] = Field(None, alias="receiptFileName", description="This field contains the name of the receipt file.")
    receipt_type: Optional[StrictStr] = Field(None, alias="receiptType", description="This field contains the receipt type.Expected values are as follows:  image/png image/jpg image/jpeg application/pdf")
    retrieval_reference_number: Optional[StrictStr] = Field(None, alias="retrievalReferenceNumber", description="This field contains the 12 digit number that is used with other data elements as a key to identify and track all messages related to a given customer transaction.")
    rfi_details: Optional[conlist(TransactionRfiDetailsResponse)] = Field(None, alias="rfiDetails", description="This field is an array that holds RFI details.")
    rha_transaction_id: Optional[StrictStr] = Field(None, alias="rhaTransactionId", description="This field contains the transaction Id for an RHA client.")
    settlement_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="settlementAmount", description="This field contains the settlement amount of a transaction. This amount is valid only for a settled transaction.")
    settlement_auth_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="settlementAuthAmount", description="This field contains the settlement auth amount of a transaction. This amount is valid only for a settled transaction.")
    settlement_billing_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="settlementBillingAmount")
    settlement_currency: Optional[StrictStr] = Field(None, alias="settlementCurrency")
    settlement_date: Optional[StrictStr] = Field(None, alias="settlementDate", description="This field contains the settlement date in case of a Settled transaction. Otherwise, it is null.")
    settlement_status: Optional[StrictStr] = Field(None, alias="settlementStatus", description="This field contains the settlement status.This field can take the following values: Unsettled Settled  Released Disputed DisputeClosed Waived")
    settlement_transaction_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="settlementTransactionAmount")
    status: Optional[StrictStr] = Field(None, description="This field contains the status. This field can take the following values: Pending: Transaction authorization is awaiting success or failure. Approved: Transaction is successfully authorized. Rejected: Transaction is rejected due to NIUM risk and compliance policies. Declined: Transaction is declined. Reversal: Transaction is reversed. Blocked: Transaction is blocked")
    system_trace_audit_number: Optional[StrictStr] = Field(None, alias="systemTraceAuditNumber", description="This field contains the system trace audit number assigned to uniquely identify a transaction.")
    terminal_id: Optional[StrictStr] = Field(None, alias="terminalID", description="This field contains the unique terminal ID.")
    transaction_currency_code: Optional[StrictStr] = Field(None, alias="transactionCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the transaction currency.")
    transaction_replacement_amount: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="transactionReplacementAmount", description="The corrected amount of a transaction in a partial reversal. This is defined by ISO-8583 as a fixed length field with four subfields, but only the first subfield is used. A 12 position field for the corrected, actual amount of a customer's transaction, in the transaction currency. The field is right justified, with lead zero fill.")
    transaction_type: Optional[StrictStr] = Field(None, alias="transactionType", description="This field contains the transaction can be one of the complete list of transactions mentioned in [Glossary of Transaction Types](https://docs.nium.com/baas/get-transactions#glossary-of-transaction-types).")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="This field contains the date and time when the transaction was last updated in UTC.")
    wallet_hash_id: Optional[StrictStr] = Field(None, alias="walletHashId", description="This field contains the unique wallet identifier generated while new wallet created.")
    __properties = ["tags", "acquirerCountryCode", "acquiringInstitutionCode", "authAmount", "authCode", "authCurrencyCode", "billingAmount", "billingConversionRate", "billingCurrencyCode", "billingReplacementAmount", "businessTransaction", "cardHashID", "cardTransactionAmount", "childCustomerHashId", "clientHashId", "comments", "complianceStatus", "createdAt", "currentWithHoldingBalance", "customerHashId", "dateOfTransaction", "debit", "effectiveAuthAmount", "labels", "localDate", "localTime", "maskedCardNumber", "mcc", "merchantCategory", "merchantCity", "merchantCountry", "merchantID", "merchantLatitude", "merchantLongitude", "merchantName", "merchantNameLocation", "merchantTaggedName", "merchantZoomIndex", "originalAuthorizationCode", "partnerReferenceNumber", "paymentInstrumentHashId", "posConditionCode", "posEntryCapabilityCode", "posEntryMode", "previousBalance", "processingCode", "receiptFileName", "receiptType", "retrievalReferenceNumber", "rfiDetails", "rhaTransactionId", "settlementAmount", "settlementAuthAmount", "settlementBillingAmount", "settlementCurrency", "settlementDate", "settlementStatus", "settlementTransactionAmount", "status", "systemTraceAuditNumber", "terminalID", "transactionCurrencyCode", "transactionReplacementAmount", "transactionType", "updatedAt", "walletHashId"]

    @validator('compliance_status')
    def compliance_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NONE', 'IN_PROGRESS', 'COMPLETED', 'ACTION_REQUIRED', 'ERROR', 'REJECT', 'EXPIRED', 'RFI_REQUESTED', 'RFI_RESPONDED', 'UNKNOWN', 'INITIATED', 'PENDING', 'CLEAR', 'CLOSED'):
            raise ValueError("must be one of enum values ('NONE', 'IN_PROGRESS', 'COMPLETED', 'ACTION_REQUIRED', 'ERROR', 'REJECT', 'EXPIRED', 'RFI_REQUESTED', 'RFI_RESPONDED', 'UNKNOWN', 'INITIATED', 'PENDING', 'CLEAR', 'CLOSED')")
        return value

    @validator('settlement_status')
    def settlement_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('APPROVED', 'DECLINED', 'BLOCKED', 'SETTLED', 'UNSETTLED', 'REVERSAL', 'RELEASED', 'PENDING', 'WAIVED', 'DISPUTED', 'DISPUTE_CLOSED', 'IN_PROGRESS', 'REJECTED', 'RETURNED', 'AWAITING_FUNDS', 'EXPIRED', 'CANCELLED', 'SCHEDULED', 'NA'):
            raise ValueError("must be one of enum values ('APPROVED', 'DECLINED', 'BLOCKED', 'SETTLED', 'UNSETTLED', 'REVERSAL', 'RELEASED', 'PENDING', 'WAIVED', 'DISPUTED', 'DISPUTE_CLOSED', 'IN_PROGRESS', 'REJECTED', 'RETURNED', 'AWAITING_FUNDS', 'EXPIRED', 'CANCELLED', 'SCHEDULED', 'NA')")
        return value

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('APPROVED', 'DECLINED', 'BLOCKED', 'SETTLED', 'UNSETTLED', 'REVERSAL', 'RELEASED', 'PENDING', 'WAIVED', 'DISPUTED', 'DISPUTE_CLOSED', 'IN_PROGRESS', 'REJECTED', 'RETURNED', 'AWAITING_FUNDS', 'EXPIRED', 'CANCELLED', 'SCHEDULED', 'NA'):
            raise ValueError("must be one of enum values ('APPROVED', 'DECLINED', 'BLOCKED', 'SETTLED', 'UNSETTLED', 'REVERSAL', 'RELEASED', 'PENDING', 'WAIVED', 'DISPUTED', 'DISPUTE_CLOSED', 'IN_PROGRESS', 'REJECTED', 'RETURNED', 'AWAITING_FUNDS', 'EXPIRED', 'CANCELLED', 'SCHEDULED', 'NA')")
        return value

    @validator('transaction_type')
    def transaction_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Debit', 'Reversal', 'Original_Credit', 'Original_Credit_Reversal', 'Balance_Inquiry', 'Partial_Reversal', 'Reversal_Advice', 'Decline_Advice', 'Incremental_Auth_Reversal', 'Auto_Sweep', 'Auto_Sweep_Payout', 'Auto_Sweep_Payout_Reversal', 'Settlement_Debit', 'Settlement_Credit', 'Settlement_Reversal', 'Settlement_Direct_Reversal', 'Settlement_Direct_Debit', 'Fee_Debit', 'Fee_Reversal', 'Fee_Waiver', 'Client_Prefund', 'Client_Refund', 'Wallet_Refund', 'Wallet_Credit_Mode_Card', 'Wallet_Credit_Mode_Prefund', 'Wallet_Credit_Mode_Prefund_Cross_Currency', 'Wallet_Credit_Mode_Offline', 'Wallet_Credit_Mode_Offline_Cross_Currency', 'Wallet_Credit_Mode_Offline_ThirdParty', 'Wallet_Credit_Mode_Direct_Debit', 'Wallet_Credit_Mode_Direct_Debit_Reversal', 'Customer_Wallet_Credit_Fund_Transfer', 'Customer_Wallet_Debit_Fund_Transfer', 'Wallet_Fund_Transfer', 'Client_Fund_Transfer', 'Wallet_Hold', 'Wallet_Unhold', 'Remittance_Debit', 'Remittance_Debit_External', 'Remittance_Reversal', 'Remittance_Client_Auto_Sweep', 'Remittance_Client_Auto_Sweep_Reversal', 'Remittance_Debit_Prescreening', 'Remittance_Debit_External_Prescreening', 'Remittance_Bene_Microdeposit', 'Remittance_Bene_Microdeposit_Reversal', 'Regulatory_Auto_Sweep', 'Regulatory_Block', 'Regulatory_Block_Release', 'Regulatory_Debit', 'Regulatory_Debit_Reversal', 'Transfer_Local', 'Transfer_Local_Reversal', 'Cashback_Credit', 'Cashback_Credit_Client', 'Chargeback_Credit', 'Customer_Wallet_Debit_Intra_Region', 'Customer_Wallet_Credit_Intra_Region', 'Customer_Wallet_Debit_Cross_Region', 'Customer_Wallet_Credit_Cross_Region', 'Direct_Debit_Payout', 'Direct_Debit_Payout_Reversal', 'Invoicing_Debit', 'NA'):
            raise ValueError("must be one of enum values ('Debit', 'Reversal', 'Original_Credit', 'Original_Credit_Reversal', 'Balance_Inquiry', 'Partial_Reversal', 'Reversal_Advice', 'Decline_Advice', 'Incremental_Auth_Reversal', 'Auto_Sweep', 'Auto_Sweep_Payout', 'Auto_Sweep_Payout_Reversal', 'Settlement_Debit', 'Settlement_Credit', 'Settlement_Reversal', 'Settlement_Direct_Reversal', 'Settlement_Direct_Debit', 'Fee_Debit', 'Fee_Reversal', 'Fee_Waiver', 'Client_Prefund', 'Client_Refund', 'Wallet_Refund', 'Wallet_Credit_Mode_Card', 'Wallet_Credit_Mode_Prefund', 'Wallet_Credit_Mode_Prefund_Cross_Currency', 'Wallet_Credit_Mode_Offline', 'Wallet_Credit_Mode_Offline_Cross_Currency', 'Wallet_Credit_Mode_Offline_ThirdParty', 'Wallet_Credit_Mode_Direct_Debit', 'Wallet_Credit_Mode_Direct_Debit_Reversal', 'Customer_Wallet_Credit_Fund_Transfer', 'Customer_Wallet_Debit_Fund_Transfer', 'Wallet_Fund_Transfer', 'Client_Fund_Transfer', 'Wallet_Hold', 'Wallet_Unhold', 'Remittance_Debit', 'Remittance_Debit_External', 'Remittance_Reversal', 'Remittance_Client_Auto_Sweep', 'Remittance_Client_Auto_Sweep_Reversal', 'Remittance_Debit_Prescreening', 'Remittance_Debit_External_Prescreening', 'Remittance_Bene_Microdeposit', 'Remittance_Bene_Microdeposit_Reversal', 'Regulatory_Auto_Sweep', 'Regulatory_Block', 'Regulatory_Block_Release', 'Regulatory_Debit', 'Regulatory_Debit_Reversal', 'Transfer_Local', 'Transfer_Local_Reversal', 'Cashback_Credit', 'Cashback_Credit_Client', 'Chargeback_Credit', 'Customer_Wallet_Debit_Intra_Region', 'Customer_Wallet_Credit_Intra_Region', 'Customer_Wallet_Debit_Cross_Region', 'Customer_Wallet_Credit_Cross_Region', 'Direct_Debit_Payout', 'Direct_Debit_Payout_Reversal', 'Invoicing_Debit', 'NA')")
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
    def from_json(cls, json_str: str) -> TransactionResponseDTO:
        """Create an instance of TransactionResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in rfi_details (list)
        _items = []
        if self.rfi_details:
            for _item in self.rfi_details:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rfiDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionResponseDTO:
        """Create an instance of TransactionResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionResponseDTO.parse_obj(obj)

        _obj = TransactionResponseDTO.parse_obj({
            "tags": obj.get("tags"),
            "acquirer_country_code": obj.get("acquirerCountryCode"),
            "acquiring_institution_code": obj.get("acquiringInstitutionCode"),
            "auth_amount": obj.get("authAmount"),
            "auth_code": obj.get("authCode"),
            "auth_currency_code": obj.get("authCurrencyCode"),
            "billing_amount": obj.get("billingAmount"),
            "billing_conversion_rate": obj.get("billingConversionRate"),
            "billing_currency_code": obj.get("billingCurrencyCode"),
            "billing_replacement_amount": obj.get("billingReplacementAmount"),
            "business_transaction": obj.get("businessTransaction"),
            "card_hash_id": obj.get("cardHashID"),
            "card_transaction_amount": obj.get("cardTransactionAmount"),
            "child_customer_hash_id": obj.get("childCustomerHashId"),
            "client_hash_id": obj.get("clientHashId"),
            "comments": obj.get("comments"),
            "compliance_status": obj.get("complianceStatus"),
            "created_at": obj.get("createdAt"),
            "current_with_holding_balance": obj.get("currentWithHoldingBalance"),
            "customer_hash_id": obj.get("customerHashId"),
            "date_of_transaction": obj.get("dateOfTransaction"),
            "debit": obj.get("debit"),
            "effective_auth_amount": obj.get("effectiveAuthAmount"),
            "labels": obj.get("labels"),
            "local_date": obj.get("localDate"),
            "local_time": obj.get("localTime"),
            "masked_card_number": obj.get("maskedCardNumber"),
            "mcc": obj.get("mcc"),
            "merchant_category": obj.get("merchantCategory"),
            "merchant_city": obj.get("merchantCity"),
            "merchant_country": obj.get("merchantCountry"),
            "merchant_id": obj.get("merchantID"),
            "merchant_latitude": obj.get("merchantLatitude"),
            "merchant_longitude": obj.get("merchantLongitude"),
            "merchant_name": obj.get("merchantName"),
            "merchant_name_location": obj.get("merchantNameLocation"),
            "merchant_tagged_name": obj.get("merchantTaggedName"),
            "merchant_zoom_index": obj.get("merchantZoomIndex"),
            "original_authorization_code": obj.get("originalAuthorizationCode"),
            "partner_reference_number": obj.get("partnerReferenceNumber"),
            "payment_instrument_hash_id": obj.get("paymentInstrumentHashId"),
            "pos_condition_code": obj.get("posConditionCode"),
            "pos_entry_capability_code": obj.get("posEntryCapabilityCode"),
            "pos_entry_mode": obj.get("posEntryMode"),
            "previous_balance": obj.get("previousBalance"),
            "processing_code": obj.get("processingCode"),
            "receipt_file_name": obj.get("receiptFileName"),
            "receipt_type": obj.get("receiptType"),
            "retrieval_reference_number": obj.get("retrievalReferenceNumber"),
            "rfi_details": [TransactionRfiDetailsResponse.from_dict(_item) for _item in obj.get("rfiDetails")] if obj.get("rfiDetails") is not None else None,
            "rha_transaction_id": obj.get("rhaTransactionId"),
            "settlement_amount": obj.get("settlementAmount"),
            "settlement_auth_amount": obj.get("settlementAuthAmount"),
            "settlement_billing_amount": obj.get("settlementBillingAmount"),
            "settlement_currency": obj.get("settlementCurrency"),
            "settlement_date": obj.get("settlementDate"),
            "settlement_status": obj.get("settlementStatus"),
            "settlement_transaction_amount": obj.get("settlementTransactionAmount"),
            "status": obj.get("status"),
            "system_trace_audit_number": obj.get("systemTraceAuditNumber"),
            "terminal_id": obj.get("terminalID"),
            "transaction_currency_code": obj.get("transactionCurrencyCode"),
            "transaction_replacement_amount": obj.get("transactionReplacementAmount"),
            "transaction_type": obj.get("transactionType"),
            "updated_at": obj.get("updatedAt"),
            "wallet_hash_id": obj.get("walletHashId")
        })
        return _obj


