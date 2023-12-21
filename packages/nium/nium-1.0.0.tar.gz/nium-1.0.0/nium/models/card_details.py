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
from nium.models.address import Address
from nium.models.block_and_replace_status import BlockAndReplaceStatus
from nium.models.card_info import CardInfo
from nium.models.card_tokens_dto import CardTokensDTO
from nium.models.demographics import Demographics
from nium.models.embossing_details import EmbossingDetails

class CardDetails(BaseModel):
    """
    CardDetails
    """
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashId", description="This field contains the unique card identifier generated while new/add-on card issuance.")
    details: Optional[CardInfo] = None
    embossing: Optional[EmbossingDetails] = None
    last_updated_on: Optional[StrictStr] = Field(None, alias="lastUpdatedOn", description="This field contains the last updated timestamp")
    block_and_replace_status: Optional[BlockAndReplaceStatus] = Field(None, alias="blockAndReplaceStatus")
    demographics: Optional[Demographics] = None
    delivered_to: Optional[Address] = Field(None, alias="deliveredTo")
    tokens: Optional[conlist(CardTokensDTO)] = Field(None, description="This array contains the token details.")
    __properties = ["cardHashId", "details", "embossing", "lastUpdatedOn", "blockAndReplaceStatus", "demographics", "deliveredTo", "tokens"]

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
    def from_json(cls, json_str: str) -> CardDetails:
        """Create an instance of CardDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of details
        if self.details:
            _dict['details'] = self.details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of embossing
        if self.embossing:
            _dict['embossing'] = self.embossing.to_dict()
        # override the default output from pydantic by calling `to_dict()` of block_and_replace_status
        if self.block_and_replace_status:
            _dict['blockAndReplaceStatus'] = self.block_and_replace_status.to_dict()
        # override the default output from pydantic by calling `to_dict()` of demographics
        if self.demographics:
            _dict['demographics'] = self.demographics.to_dict()
        # override the default output from pydantic by calling `to_dict()` of delivered_to
        if self.delivered_to:
            _dict['deliveredTo'] = self.delivered_to.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in tokens (list)
        _items = []
        if self.tokens:
            for _item in self.tokens:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tokens'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CardDetails:
        """Create an instance of CardDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CardDetails.parse_obj(obj)

        _obj = CardDetails.parse_obj({
            "card_hash_id": obj.get("cardHashId"),
            "details": CardInfo.from_dict(obj.get("details")) if obj.get("details") is not None else None,
            "embossing": EmbossingDetails.from_dict(obj.get("embossing")) if obj.get("embossing") is not None else None,
            "last_updated_on": obj.get("lastUpdatedOn"),
            "block_and_replace_status": BlockAndReplaceStatus.from_dict(obj.get("blockAndReplaceStatus")) if obj.get("blockAndReplaceStatus") is not None else None,
            "demographics": Demographics.from_dict(obj.get("demographics")) if obj.get("demographics") is not None else None,
            "delivered_to": Address.from_dict(obj.get("deliveredTo")) if obj.get("deliveredTo") is not None else None,
            "tokens": [CardTokensDTO.from_dict(_item) for _item in obj.get("tokens")] if obj.get("tokens") is not None else None
        })
        return _obj


