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
from pydantic import BaseModel, Field, StrictStr, validator

class CardInfo(BaseModel):
    """
    Card details  # noqa: E501
    """
    card_product_id: Optional[StrictStr] = Field(None, alias="cardProductId", description="Pre-defined product Id, defined at NIUM and communicated to client for card issuance.")
    plastic_id: Optional[StrictStr] = Field(None, alias="plasticId", description="This field contains the pre-defined plastic Id which is used to determine card design.")
    region_code: Optional[StrictStr] = Field(None, alias="regionCode", description="This field contains the 2-letter [region code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the card.")
    masked_card_number: Optional[StrictStr] = Field(None, alias="maskedCardNumber", description="This field contains the 16-digit masked card number in format 1234-56xx-xxxx-3456.")
    proxy_number: Optional[StrictStr] = Field(None, alias="proxyNumber", description="This field contains the reference number for the card.")
    card_type: Optional[StrictStr] = Field(None, alias="cardType", description="This field contains the issued card type.")
    issuance_type: Optional[StrictStr] = Field(None, alias="issuanceType", description="This field contains the type of the card issued.")
    card_status: Optional[StrictStr] = Field(None, alias="cardStatus", description="This field contains the activation status of the card.")
    child_customer_hash_id: Optional[StrictStr] = Field(None, alias="childCustomerHashId", description="Child customer hash Id")
    __properties = ["cardProductId", "plasticId", "regionCode", "maskedCardNumber", "proxyNumber", "cardType", "issuanceType", "cardStatus", "childCustomerHashId"]

    @validator('card_status')
    def card_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('INACTIVE,ACTIVE,VIRTUAL_ACTIVE,TEMP_BLOCK,P_BLOCK'):
            raise ValueError("must be one of enum values ('INACTIVE,ACTIVE,VIRTUAL_ACTIVE,TEMP_BLOCK,P_BLOCK')")
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
    def from_json(cls, json_str: str) -> CardInfo:
        """Create an instance of CardInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CardInfo:
        """Create an instance of CardInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CardInfo.parse_obj(obj)

        _obj = CardInfo.parse_obj({
            "card_product_id": obj.get("cardProductId"),
            "plastic_id": obj.get("plasticId"),
            "region_code": obj.get("regionCode"),
            "masked_card_number": obj.get("maskedCardNumber"),
            "proxy_number": obj.get("proxyNumber"),
            "card_type": obj.get("cardType"),
            "issuance_type": obj.get("issuanceType"),
            "card_status": obj.get("cardStatus"),
            "child_customer_hash_id": obj.get("childCustomerHashId")
        })
        return _obj


