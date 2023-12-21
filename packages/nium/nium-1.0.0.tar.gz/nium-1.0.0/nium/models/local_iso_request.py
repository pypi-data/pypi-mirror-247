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
from pydantic import BaseModel, Field, StrictStr

class LocalIsoRequest(BaseModel):
    """
    LocalIsoRequest
    """
    acceptor_id42: Optional[StrictStr] = Field(None, alias="acceptorId42", description="This field contains the 15 character acceptor id")
    acceptor_name_location43: Optional[StrictStr] = Field(None, alias="acceptorNameLocation43", description="This field contains the acceptor name and location")
    acceptor_terminal_id41: Optional[StrictStr] = Field(None, alias="acceptorTerminalId41", description="This field contains the 8 character acceptor terminal id")
    ai_country_code19: Optional[StrictStr] = Field(None, alias="aiCountryCode19", description="This field contains the 3 character ai country code")
    ai_identity_code32: Optional[StrictStr] = Field(None, alias="aiIdentityCode32", description="This field contains the ai identity code")
    authorization_code38: Optional[StrictStr] = Field(None, alias="authorizationCode38", description="This field contains the 6 character authorization code")
    billing_amount6: Optional[StrictStr] = Field(None, alias="billingAmount6", description="This field contains the 12 character billing amount")
    billing_amount_fee30: Optional[StrictStr] = Field(None, alias="billingAmountFee30", description="This field contains the billing amount fee30")
    billing_amount_fee8: Optional[StrictStr] = Field(None, alias="billingAmountFee8", description="This field contains the billing amount fee8")
    billing_conversion_rate10: Optional[StrictStr] = Field(None, alias="billingConversionRate10", description="This field contains the billing conversion rate10")
    billing_currency_code51: Optional[StrictStr] = Field(None, alias="billingCurrencyCode51", description="This field contains the 3 character billing currency code")
    capture_date_yymm17: Optional[StrictStr] = Field(None, alias="captureDateYYMM17", description="This field contains the capture date")
    card_sequence_number23: Optional[StrictStr] = Field(None, alias="cardSequenceNumber23", description="This field contains the card sequence number")
    conversion_date_yymm16: Optional[StrictStr] = Field(None, alias="conversionDateYYMM16", description="This field contains the conversion date")
    expiry_date_yymm14: Optional[StrictStr] = Field(None, alias="expiryDateYYMM14", description="This field contains the expiry date")
    fi_country_code21: Optional[StrictStr] = Field(None, alias="fiCountryCode21", description="This field contains the 3 character fi country code")
    fi_identity_code33: Optional[StrictStr] = Field(None, alias="fiIdentityCode33", description="This field contains the fi identity code")
    local_date13: Optional[StrictStr] = Field(None, alias="localDate13", description="This field contains the local date13")
    local_time12: Optional[StrictStr] = Field(None, alias="localTime12", description="This field contains the local time12")
    merchant_type18: Optional[StrictStr] = Field(None, alias="merchantType18", description="This field contains the 4 character merchant type")
    message_type0: Optional[StrictStr] = Field(None, alias="messageType0", description="This field contains the 4 character message type")
    mid62: Optional[StrictStr] = Field(None, description="This field contains the mid62")
    misc_data58: Optional[StrictStr] = Field(None, alias="miscData58", description="This field contains the misc data")
    network_international_id24: Optional[StrictStr] = Field(None, alias="networkInternationalId24", description="This field contains the network international id")
    original_data_element90: Optional[StrictStr] = Field(None, alias="originalDataElement90", description="This field contains the original data element")
    pan2: Optional[StrictStr] = Field(None, description="This field contains the 16 character pan2")
    pos_condition_code25: Optional[StrictStr] = Field(None, alias="posConditionCode25", description="This field contains the 2 character pos condition code")
    pos_entry_capability_code60: Optional[StrictStr] = Field(None, alias="posEntryCapabilityCode60", description="This field contains the pos entry capability code")
    pos_entry_mode22: Optional[StrictStr] = Field(None, alias="posEntryMode22", description="This field contains the 4 character pos entry mode")
    pos_pin_capture_code26: Optional[StrictStr] = Field(None, alias="posPinCaptureCode26", description="This field contains the pos pin capture code")
    processing_code3: Optional[StrictStr] = Field(None, alias="processingCode3", description="This field contains the 6 character processing code")
    replacement_amount95: Optional[StrictStr] = Field(None, alias="replacementAmount95", description="This field contains the replacement amount")
    response_code39: Optional[StrictStr] = Field(None, alias="responseCode39", description="This field contains the 2 character response code")
    rrn: Optional[StrictStr] = Field(None, description="This field contains the rrn")
    settlement_amount5: Optional[StrictStr] = Field(None, alias="settlementAmount5", description="This field contains the settlement amount")
    settlement_amount_fee29: Optional[StrictStr] = Field(None, alias="settlementAmountFee29", description="This field contains the settlement amount fee")
    settlement_conversion_rate9: Optional[StrictStr] = Field(None, alias="settlementConversionRate9", description="This field contains the settlement conversion rate9")
    settlement_currency_code50: Optional[StrictStr] = Field(None, alias="settlementCurrencyCode50", description="This field contains the settlement currency code")
    settlement_date_yymm15: Optional[StrictStr] = Field(None, alias="settlementDateYYMM15", description="This field contains the settlement date")
    settlement_processing_amount_fee31: Optional[StrictStr] = Field(None, alias="settlementProcessingAmountFee31", description="This field contains the settlement processing amount fee")
    stan: Optional[StrictStr] = Field(None, description="This field contains the stan")
    trace_identifier115: Optional[StrictStr] = Field(None, alias="traceIdentifier115", description="This field contains the trace identifier")
    track2_data35: Optional[StrictStr] = Field(None, alias="track2Data35", description="This field contains the track 2 Data")
    transaction_amount4: Optional[StrictStr] = Field(None, alias="transactionAmount4", description="This field contains the 12 character transaction amount")
    transaction_amount_fee28: Optional[StrictStr] = Field(None, alias="transactionAmountFee28", description="This field contains the transaction amount fee")
    transaction_currency_code49: Optional[StrictStr] = Field(None, alias="transactionCurrencyCode49", description="This field contains the 3 character transaction currency code")
    __properties = ["acceptorId42", "acceptorNameLocation43", "acceptorTerminalId41", "aiCountryCode19", "aiIdentityCode32", "authorizationCode38", "billingAmount6", "billingAmountFee30", "billingAmountFee8", "billingConversionRate10", "billingCurrencyCode51", "captureDateYYMM17", "cardSequenceNumber23", "conversionDateYYMM16", "expiryDateYYMM14", "fiCountryCode21", "fiIdentityCode33", "localDate13", "localTime12", "merchantType18", "messageType0", "mid62", "miscData58", "networkInternationalId24", "originalDataElement90", "pan2", "posConditionCode25", "posEntryCapabilityCode60", "posEntryMode22", "posPinCaptureCode26", "processingCode3", "replacementAmount95", "responseCode39", "rrn", "settlementAmount5", "settlementAmountFee29", "settlementConversionRate9", "settlementCurrencyCode50", "settlementDateYYMM15", "settlementProcessingAmountFee31", "stan", "traceIdentifier115", "track2Data35", "transactionAmount4", "transactionAmountFee28", "transactionCurrencyCode49"]

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
    def from_json(cls, json_str: str) -> LocalIsoRequest:
        """Create an instance of LocalIsoRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LocalIsoRequest:
        """Create an instance of LocalIsoRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LocalIsoRequest.parse_obj(obj)

        _obj = LocalIsoRequest.parse_obj({
            "acceptor_id42": obj.get("acceptorId42"),
            "acceptor_name_location43": obj.get("acceptorNameLocation43"),
            "acceptor_terminal_id41": obj.get("acceptorTerminalId41"),
            "ai_country_code19": obj.get("aiCountryCode19"),
            "ai_identity_code32": obj.get("aiIdentityCode32"),
            "authorization_code38": obj.get("authorizationCode38"),
            "billing_amount6": obj.get("billingAmount6"),
            "billing_amount_fee30": obj.get("billingAmountFee30"),
            "billing_amount_fee8": obj.get("billingAmountFee8"),
            "billing_conversion_rate10": obj.get("billingConversionRate10"),
            "billing_currency_code51": obj.get("billingCurrencyCode51"),
            "capture_date_yymm17": obj.get("captureDateYYMM17"),
            "card_sequence_number23": obj.get("cardSequenceNumber23"),
            "conversion_date_yymm16": obj.get("conversionDateYYMM16"),
            "expiry_date_yymm14": obj.get("expiryDateYYMM14"),
            "fi_country_code21": obj.get("fiCountryCode21"),
            "fi_identity_code33": obj.get("fiIdentityCode33"),
            "local_date13": obj.get("localDate13"),
            "local_time12": obj.get("localTime12"),
            "merchant_type18": obj.get("merchantType18"),
            "message_type0": obj.get("messageType0"),
            "mid62": obj.get("mid62"),
            "misc_data58": obj.get("miscData58"),
            "network_international_id24": obj.get("networkInternationalId24"),
            "original_data_element90": obj.get("originalDataElement90"),
            "pan2": obj.get("pan2"),
            "pos_condition_code25": obj.get("posConditionCode25"),
            "pos_entry_capability_code60": obj.get("posEntryCapabilityCode60"),
            "pos_entry_mode22": obj.get("posEntryMode22"),
            "pos_pin_capture_code26": obj.get("posPinCaptureCode26"),
            "processing_code3": obj.get("processingCode3"),
            "replacement_amount95": obj.get("replacementAmount95"),
            "response_code39": obj.get("responseCode39"),
            "rrn": obj.get("rrn"),
            "settlement_amount5": obj.get("settlementAmount5"),
            "settlement_amount_fee29": obj.get("settlementAmountFee29"),
            "settlement_conversion_rate9": obj.get("settlementConversionRate9"),
            "settlement_currency_code50": obj.get("settlementCurrencyCode50"),
            "settlement_date_yymm15": obj.get("settlementDateYYMM15"),
            "settlement_processing_amount_fee31": obj.get("settlementProcessingAmountFee31"),
            "stan": obj.get("stan"),
            "trace_identifier115": obj.get("traceIdentifier115"),
            "track2_data35": obj.get("track2Data35"),
            "transaction_amount4": obj.get("transactionAmount4"),
            "transaction_amount_fee28": obj.get("transactionAmountFee28"),
            "transaction_currency_code49": obj.get("transactionCurrencyCode49")
        })
        return _obj


