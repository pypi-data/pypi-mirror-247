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
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist, validator
from nium.models.card_tokens_dto import CardTokensDTO

class CardResponseDTO(BaseModel):
    """
    CardResponseDTO
    """
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashId", description="This field contains the unique card identifier generated while new/add-on card issuance.")
    card_type: Optional[StrictStr] = Field(None, alias="cardType", description="This field contains the card type to be issued. The acceptable values are: GPR_PHY: This value is used to issue a physical card. GPR_VIR: This value is used to issue a virtual card. GPR_VIR_UP2PHY: This value is used to issue a virtual upgrade to physical card.")
    card_status: Optional[StrictStr] = Field(None, alias="cardStatus", description="This field contains the activation status of the card.")
    masked_card_number: Optional[StrictStr] = Field(None, alias="maskedCardNumber", description="This field contains the 16-digit masked card number in format 1234-56xx-xxxx-3456.")
    proxy_number: Optional[StrictStr] = Field(None, alias="proxyNumber", description="This field contains the reference number for the card.")
    logo_id: Optional[StrictStr] = Field(None, alias="logoId", description="This field contains the pre-defined logo for card issuance.")
    plastic_id: Optional[StrictStr] = Field(None, alias="plasticId", description="This field contains the pre-defined plastic Id which is used to determine card design.")
    region_code: Optional[StrictStr] = Field(None, alias="regionCode", description="This field contains the 2-letter [region code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the card.")
    block_reason: Optional[StrictStr] = Field(None, alias="blockReason", description="This field contains the reason for card block.")
    replaced_on: Optional[StrictStr] = Field(None, alias="replacedOn", description="This field contains the timestamp when the card was replaced, otherwise null.")
    issuance_mode: Optional[StrictStr] = Field(None, alias="issuanceMode", description="This field contains the mode of delivery of a card.")
    issuance_type: Optional[StrictStr] = Field(None, alias="issuanceType", description="This field contains the type of the card issued.The values can be primaryCard, additionalCard, or replaceCard.")
    embossing_line1: Optional[StrictStr] = Field(None, alias="embossingLine1", description="This field contains the printed name on line 1.")
    embossing_line2: Optional[StrictStr] = Field(None, alias="embossingLine2", description="This field contains the printed name on line 2.")
    first_name: Optional[StrictStr] = Field(None, alias="firstName", description="This field contains the first name of the card holder.")
    middle_name: Optional[StrictStr] = Field(None, alias="middleName", description="This field contains the middle name of the card holder.")
    last_name: Optional[StrictStr] = Field(None, alias="lastName", description="This field contains the last name of the card holder.")
    email: Optional[StrictStr] = Field(None, description="This field contains the email ID of the card holder.")
    country_code: Optional[StrictStr] = Field(None, alias="countryCode", description="This field contains the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for identifying the country prefix to a mobile number.")
    mobile: Optional[StrictStr] = Field(None, description="This field contains the mobile number of the card holder.")
    demog_overridden: Optional[StrictBool] = Field(None, alias="demogOverridden", description="This field is required in case of ADD_ON cards. If sent as false, the card shall be issued in the name of the customer(primary card holder). If sent as true, the card shall be issued in the name of the add-on card holder whose full details need to be provided.")
    created_at: Optional[StrictStr] = Field(None, alias="createdAt", description="This field contains the date and time of card creation")
    updated_at: Optional[StrictStr] = Field(None, alias="updatedAt", description="This field contains the date and time of card updation")
    tokens: Optional[conlist(CardTokensDTO)] = Field(None, description="This array contains the token details.")
    __properties = ["cardHashId", "cardType", "cardStatus", "maskedCardNumber", "proxyNumber", "logoId", "plasticId", "regionCode", "blockReason", "replacedOn", "issuanceMode", "issuanceType", "embossingLine1", "embossingLine2", "firstName", "middleName", "lastName", "email", "countryCode", "mobile", "demogOverridden", "createdAt", "updatedAt", "tokens"]

    @validator('card_status')
    def card_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INACTIVE,ACTIVE,VIRTUAL_ACTIVE,TEMP_BLOCK,P_BLOCK'):
            raise ValueError("must be one of enum values ('INACTIVE,ACTIVE,VIRTUAL_ACTIVE,TEMP_BLOCK,P_BLOCK')")
        return value

    @validator('block_reason')
    def block_reason_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('fraud,cardLost,cardStolen,damaged'):
            raise ValueError("must be one of enum values ('fraud,cardLost,cardStolen,damaged')")
        return value

    @validator('issuance_mode')
    def issuance_mode_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('NORMAL_DELIVERY_LOCAL,EXPRESS_DELIVERY_LOCAL,INTERNATIONAL_DELIVERY'):
            raise ValueError("must be one of enum values ('NORMAL_DELIVERY_LOCAL,EXPRESS_DELIVERY_LOCAL,INTERNATIONAL_DELIVERY')")
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
    def from_json(cls, json_str: str) -> CardResponseDTO:
        """Create an instance of CardResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in tokens (list)
        _items = []
        if self.tokens:
            for _item in self.tokens:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tokens'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CardResponseDTO:
        """Create an instance of CardResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CardResponseDTO.parse_obj(obj)

        _obj = CardResponseDTO.parse_obj({
            "card_hash_id": obj.get("cardHashId"),
            "card_type": obj.get("cardType"),
            "card_status": obj.get("cardStatus"),
            "masked_card_number": obj.get("maskedCardNumber"),
            "proxy_number": obj.get("proxyNumber"),
            "logo_id": obj.get("logoId"),
            "plastic_id": obj.get("plasticId"),
            "region_code": obj.get("regionCode"),
            "block_reason": obj.get("blockReason"),
            "replaced_on": obj.get("replacedOn"),
            "issuance_mode": obj.get("issuanceMode"),
            "issuance_type": obj.get("issuanceType"),
            "embossing_line1": obj.get("embossingLine1"),
            "embossing_line2": obj.get("embossingLine2"),
            "first_name": obj.get("firstName"),
            "middle_name": obj.get("middleName"),
            "last_name": obj.get("lastName"),
            "email": obj.get("email"),
            "country_code": obj.get("countryCode"),
            "mobile": obj.get("mobile"),
            "demog_overridden": obj.get("demogOverridden"),
            "created_at": obj.get("createdAt"),
            "updated_at": obj.get("updatedAt"),
            "tokens": [CardTokensDTO.from_dict(_item) for _item in obj.get("tokens")] if obj.get("tokens") is not None else None
        })
        return _obj


