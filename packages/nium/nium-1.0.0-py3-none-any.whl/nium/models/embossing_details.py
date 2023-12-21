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

class EmbossingDetails(BaseModel):
    """
    Embossing details  # noqa: E501
    """
    name_on_card: Optional[StrictStr] = Field(None, alias="nameOnCard", description="This field contains the printed name on card.")
    additional_line: Optional[StrictStr] = Field(None, alias="additionalLine", description="This field contains the printed additional line on card.")
    issuance_mode: Optional[StrictStr] = Field(None, alias="issuanceMode", description="This field contains the mode of delivery of a card.")
    created_on: Optional[StrictStr] = Field(None, alias="createdOn", description="This field contains the card created date")
    processed_on: Optional[StrictStr] = Field(None, alias="processedOn", description="This field contains the card processed date")
    printed_on: Optional[StrictStr] = Field(None, alias="printedOn", description="This field contains the card printed date")
    dispatched_on: Optional[StrictStr] = Field(None, alias="dispatchedOn", description="This field contains the card dispatched date")
    dispatch_awb: Optional[StrictStr] = Field(None, alias="dispatchAWB", description="This field contains the card dispatched airway bill")
    __properties = ["nameOnCard", "additionalLine", "issuanceMode", "createdOn", "processedOn", "printedOn", "dispatchedOn", "dispatchAWB"]

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
    def from_json(cls, json_str: str) -> EmbossingDetails:
        """Create an instance of EmbossingDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> EmbossingDetails:
        """Create an instance of EmbossingDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return EmbossingDetails.parse_obj(obj)

        _obj = EmbossingDetails.parse_obj({
            "name_on_card": obj.get("nameOnCard"),
            "additional_line": obj.get("additionalLine"),
            "issuance_mode": obj.get("issuanceMode"),
            "created_on": obj.get("createdOn"),
            "processed_on": obj.get("processedOn"),
            "printed_on": obj.get("printedOn"),
            "dispatched_on": obj.get("dispatchedOn"),
            "dispatch_awb": obj.get("dispatchAWB")
        })
        return _obj


