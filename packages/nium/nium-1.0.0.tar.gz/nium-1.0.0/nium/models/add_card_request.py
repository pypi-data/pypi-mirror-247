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
from pydantic import BaseModel, Field, StrictBool, StrictStr, constr, validator

class AddCardRequest(BaseModel):
    """
    AddCardRequest
    """
    logo_identifier: StrictStr = Field(..., alias="logoIdentifier", description="Pre-defined logo Id in UUID format, defined at NIUM and communicated to client for card issuance.")
    plastic_id: constr(strict=True, max_length=10, min_length=0) = Field(..., alias="plasticId", description="Pre-defined plastic Id defined at NIUM and communicated to client. It is used to determine the card design")
    card_type: StrictStr = Field(..., alias="cardType", description="This field accepts the card type to be issued. The acceptable values are: GPR_PHY: This value is used to issue a physical card GPR_VIR: This value is used to issue a virtual card GPR_VIR_UP2PHY: This value is used to issue a virtual upgrade to physical card")
    card_issuance_action: StrictStr = Field(..., alias="cardIssuanceAction", description="This field determines if the card issued is primary or add-on. The possible values are: NEW(for a new card) ADD_ON(for add on card) Please note that a customer may have only one primary Physical(GPR_PHY) card, one primary Virtual(GPR_VIR) and only one primary virtual upgrade to physical card(GPR_VIR_UP2PHY). Any further cards can be issued as add-on cards.")
    card_fee_currency_code: constr(strict=True, max_length=3, min_length=3) = Field(..., alias="cardFeeCurrencyCode", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for one of the opted currencies in which the card issuance fee is to be charged")
    card_expiry: constr(strict=True, max_length=4, min_length=0) = Field(..., alias="cardExpiry", description="Expiry date to be set for virtual and virtual physical cards. For physical cards do not send this field. This field is in MMYY format. For virtual cards, the last acceptable date is the year-end of the 5th year from now. Card will be valid till the last day of the month and year of expiry.")
    embossing_line1: Optional[constr(strict=True, max_length=26, min_length=1)] = Field(None, alias="embossingLine1", description="This field can be used to print the customer name. The value sent in this field will be printed on the card.If this field is left empty, line 1 will not be printed on the card. This field accepts alphanumeric characters along with space(s) The maximum character limit is 26.")
    embossing_line2: Optional[constr(strict=True, max_length=26, min_length=1)] = Field(None, alias="embossingLine2", description="This field can be used to send the company name or employeeID. Anything sent in this field will be printed on the card.  This field accepts alphanumeric characters along with space(s). The maximum character limit is 26.")
    issuance_mode: Optional[StrictStr] = Field(None, alias="issuanceMode", description="This field is only required for physical cards(GPR_PHY) mode of delivery of a card. Possible values are: NORMAL_DELIVERY_LOCAL EXPRESS_DELIVERY_LOCAL INTERNATIONAL_DELIVERY")
    demog_overridden: Optional[StrictBool] = Field(None, alias="demogOverridden", description="This flag specifies if the demogOverriden is true or false The default value of demogOverridden is false. It should always be sent as false for issuing a primary card.")
    country_code: Optional[constr(strict=True, max_length=2, min_length=2)] = Field(None, alias="countryCode", description="This field accepts the [2-letter ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the add-on cardholder. This field is mandatory when demogOverridden is true.")
    mobile: Optional[constr(strict=True, max_length=20, min_length=6)] = Field(None, description="This field accepts the mobile number for the add-on cardholder. This field is mandatory when demogOverridden is true")
    email: Optional[constr(strict=True, max_length=60, min_length=4)] = Field(None, description="This field accepts the email ID for the add-on cardholder. This field is mandatory when demogOverridden is true")
    first_name: Optional[constr(strict=True, max_length=40, min_length=1)] = Field(None, alias="firstName", description="This field accepts the firstname for the add-on cardholder. This field is mandatory when demogOverridden is true")
    last_name: Optional[constr(strict=True, max_length=40, min_length=1)] = Field(None, alias="lastName", description="This field accepts the lastname for the add-on cardholder. This field is mandatory when demogOverridden is true")
    middle_name: Optional[constr(strict=True, max_length=40, min_length=1)] = Field(None, alias="middleName", description="The middle name of the customer")
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashId", description="This is the cardHashId of the primary(NEW) card which is already issued. It is mandatory to send this value when ADD_ON card is being issued. This field is not needed for NEW card")
    __properties = ["logoIdentifier", "plasticId", "cardType", "cardIssuanceAction", "cardFeeCurrencyCode", "cardExpiry", "embossingLine1", "embossingLine2", "issuanceMode", "demogOverridden", "countryCode", "mobile", "email", "firstName", "lastName", "middleName", "cardHashId"]

    @validator('card_type')
    def card_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('GPR_VIR', 'GPR_PHY', 'GPR_VIR_UP2PHY', 'VIR', 'PHY', 'VIRUP2PHY'):
            raise ValueError("must be one of enum values ('GPR_VIR', 'GPR_PHY', 'GPR_VIR_UP2PHY', 'VIR', 'PHY', 'VIRUP2PHY')")
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
    def from_json(cls, json_str: str) -> AddCardRequest:
        """Create an instance of AddCardRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddCardRequest:
        """Create an instance of AddCardRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddCardRequest.parse_obj(obj)

        _obj = AddCardRequest.parse_obj({
            "logo_identifier": obj.get("logoIdentifier"),
            "plastic_id": obj.get("plasticId"),
            "card_type": obj.get("cardType"),
            "card_issuance_action": obj.get("cardIssuanceAction"),
            "card_fee_currency_code": obj.get("cardFeeCurrencyCode"),
            "card_expiry": obj.get("cardExpiry"),
            "embossing_line1": obj.get("embossingLine1"),
            "embossing_line2": obj.get("embossingLine2"),
            "issuance_mode": obj.get("issuanceMode"),
            "demog_overridden": obj.get("demogOverridden"),
            "country_code": obj.get("countryCode"),
            "mobile": obj.get("mobile"),
            "email": obj.get("email"),
            "first_name": obj.get("firstName"),
            "last_name": obj.get("lastName"),
            "middle_name": obj.get("middleName"),
            "card_hash_id": obj.get("cardHashId")
        })
        return _obj


