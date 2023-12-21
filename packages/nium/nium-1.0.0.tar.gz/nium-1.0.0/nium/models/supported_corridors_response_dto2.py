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
from pydantic import BaseModel, Field, StrictStr, conlist

class SupportedCorridorsResponseDTO2(BaseModel):
    """
    SupportedCorridorsResponseDTO2
    """
    account_verification: Optional[StrictStr] = Field(None, alias="accountVerification", description="This field provides whether account verification is supported or not.")
    additional_info: Optional[StrictStr] = Field(None, alias="additionalInfo", description="This field provides additional information with respect to the corridor.")
    beneficiary_account_type: Optional[StrictStr] = Field(None, alias="beneficiaryAccountType", description="This field provides the beneficiary account type.")
    beneficiary_statement_narrative: Optional[StrictStr] = Field(None, alias="beneficiaryStatementNarrative", description="This field provides information that will be visible on the beneficiary statement for payout transaction.")
    channels: Optional[StrictStr] = Field(None, description="This field provides information on channel supported. ")
    client_type: Optional[StrictStr] = Field(None, alias="clientType", description="This field provides type of Client e.g. FI, NonFI")
    customer_country: Optional[conlist(StrictStr)] = Field(None, alias="customerCountry", description="List of countries accepted as remitter country.")
    customer_type: Optional[StrictStr] = Field(None, alias="customerType", description="This field provides the type of customer.")
    cutoff_delivery_notes: Optional[StrictStr] = Field(None, alias="cutoffDeliveryNotes", description="This field provides information on Cut-off times and delivery.")
    delivery_tat: Optional[StrictStr] = Field(None, alias="deliveryTAT", description="This field provides information on delivery times such as Realtime, T0 – same day , T1 – next day etc.")
    destination_country: Optional[StrictStr] = Field(None, alias="destinationCountry", description="This field provides the 2-letter ISO-2 destination country code.")
    destination_currency: Optional[StrictStr] = Field(None, alias="destinationCurrency", description="This field provides destination Currency.")
    fx_source: Optional[StrictStr] = Field(None, alias="fxSource", description="This field provides information on the FX source.")
    limit_currency: Optional[StrictStr] = Field(None, alias="limitCurrency", description="This field provides currency for the minimum and maximum limits.")
    mandatory_data_requirement: Optional[conlist(StrictStr)] = Field(None, alias="mandatoryDataRequirement", description="This field provides information on mandatory information required for payout request.")
    maximum_amount: Optional[StrictStr] = Field(None, alias="maximumAmount", description="This field provides information for maximum amount for the corridor, currency and payment method")
    minimum_amount: Optional[StrictStr] = Field(None, alias="minimumAmount", description="This field provides information for minimum amount for the corridor, currency and payment method.")
    network_participant: Optional[StrictStr] = Field(None, alias="networkParticipant", description="This field provides type of network participant.")
    payout_method: Optional[StrictStr] = Field(None, alias="payoutMethod", description="This field accepts the different modes of payout. ")
    proof_of_payment: Optional[StrictStr] = Field(None, alias="proofOfPayment", description="This field provides information on proof of payment.")
    routing_code_type: Optional[StrictStr] = Field(None, alias="routingCodeType", description="This field provides the routing code type for the currency. For example SWIFT, ACH CODE etc.  The possible values are:  • SWIFT for all cases where SWIFT is applicable  • IFSC (relevant for India)  • ACH CODE (relevant for USA)  • BSB CODE (relevant for Australia)  • SORT CODE (relevant for the UK)  • LOCATION ID (relevant for Nepal)  • BANK CODE (relevant for few countries including Canada, Hong Kong, Sri Lanka, South Korea, Pakistan, Brazil, and some more)  • TRANSIT NUMBER (relevant for Canada)  • BRANCH CODE (relevant for Sri Lanka, Vietnam, Brazil, Uruguay, Kenya and some more)")
    supporting_documents: Optional[conlist(StrictStr)] = Field(None, alias="supportingDocuments", description="This field provides information on any supporting documents required for payout for e.g. Invoice etc")
    wallets: Optional[conlist(StrictStr)] = Field(None, description="This field provides information on wallets partners.")
    __properties = ["accountVerification", "additionalInfo", "beneficiaryAccountType", "beneficiaryStatementNarrative", "channels", "clientType", "customerCountry", "customerType", "cutoffDeliveryNotes", "deliveryTAT", "destinationCountry", "destinationCurrency", "fxSource", "limitCurrency", "mandatoryDataRequirement", "maximumAmount", "minimumAmount", "networkParticipant", "payoutMethod", "proofOfPayment", "routingCodeType", "supportingDocuments", "wallets"]

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
    def from_json(cls, json_str: str) -> SupportedCorridorsResponseDTO2:
        """Create an instance of SupportedCorridorsResponseDTO2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SupportedCorridorsResponseDTO2:
        """Create an instance of SupportedCorridorsResponseDTO2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SupportedCorridorsResponseDTO2.parse_obj(obj)

        _obj = SupportedCorridorsResponseDTO2.parse_obj({
            "account_verification": obj.get("accountVerification"),
            "additional_info": obj.get("additionalInfo"),
            "beneficiary_account_type": obj.get("beneficiaryAccountType"),
            "beneficiary_statement_narrative": obj.get("beneficiaryStatementNarrative"),
            "channels": obj.get("channels"),
            "client_type": obj.get("clientType"),
            "customer_country": obj.get("customerCountry"),
            "customer_type": obj.get("customerType"),
            "cutoff_delivery_notes": obj.get("cutoffDeliveryNotes"),
            "delivery_tat": obj.get("deliveryTAT"),
            "destination_country": obj.get("destinationCountry"),
            "destination_currency": obj.get("destinationCurrency"),
            "fx_source": obj.get("fxSource"),
            "limit_currency": obj.get("limitCurrency"),
            "mandatory_data_requirement": obj.get("mandatoryDataRequirement"),
            "maximum_amount": obj.get("maximumAmount"),
            "minimum_amount": obj.get("minimumAmount"),
            "network_participant": obj.get("networkParticipant"),
            "payout_method": obj.get("payoutMethod"),
            "proof_of_payment": obj.get("proofOfPayment"),
            "routing_code_type": obj.get("routingCodeType"),
            "supporting_documents": obj.get("supportingDocuments"),
            "wallets": obj.get("wallets")
        })
        return _obj


