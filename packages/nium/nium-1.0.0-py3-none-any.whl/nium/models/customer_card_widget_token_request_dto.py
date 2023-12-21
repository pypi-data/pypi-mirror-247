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
from nium.models.css_attribute_dto import CSSAttributeDTO

class CustomerCardWidgetTokenRequestDTO(BaseModel):
    """
    CustomerCardWidgetTokenRequestDTO
    """
    card_type: StrictStr = Field(..., alias="cardType")
    client_domain: Optional[StrictStr] = Field(None, alias="clientDomain", description="This field contains the domain name where the widget needs to be embedded")
    css_attributes: Optional[CSSAttributeDTO] = Field(None, alias="cssAttributes")
    destination_country: Optional[StrictStr] = Field(None, alias="destinationCountry", description="This field contains the 2-letter [ISO-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of the destination country.")
    __properties = ["cardType", "clientDomain", "cssAttributes", "destinationCountry"]

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
    def from_json(cls, json_str: str) -> CustomerCardWidgetTokenRequestDTO:
        """Create an instance of CustomerCardWidgetTokenRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of css_attributes
        if self.css_attributes:
            _dict['cssAttributes'] = self.css_attributes.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerCardWidgetTokenRequestDTO:
        """Create an instance of CustomerCardWidgetTokenRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerCardWidgetTokenRequestDTO.parse_obj(obj)

        _obj = CustomerCardWidgetTokenRequestDTO.parse_obj({
            "card_type": obj.get("cardType"),
            "client_domain": obj.get("clientDomain"),
            "css_attributes": CSSAttributeDTO.from_dict(obj.get("cssAttributes")) if obj.get("cssAttributes") is not None else None,
            "destination_country": obj.get("destinationCountry")
        })
        return _obj


