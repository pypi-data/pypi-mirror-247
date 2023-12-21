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

class ProductAssociationDetails(BaseModel):
    """
    ProductAssociationDetails
    """
    association_chair_person: Optional[StrictStr] = Field(None, alias="associationChairPerson", description="This field accepts the full name of the association chair, secretary, treasurer.  AU: Optional EU: NA UK: NA SG: Optional")
    association_name: Optional[StrictStr] = Field(None, alias="associationName", description="This field accepts the full name of the association.  AU: Optional EU: NA UK: NA SG: Optional")
    association_number: Optional[StrictStr] = Field(None, alias="associationNumber", description="This field accepts an association number as issued by the applicable state/territory.  AU: Optional EU: NA UK: NA SG: Optional")
    __properties = ["associationChairPerson", "associationName", "associationNumber"]

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
    def from_json(cls, json_str: str) -> ProductAssociationDetails:
        """Create an instance of ProductAssociationDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductAssociationDetails:
        """Create an instance of ProductAssociationDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductAssociationDetails.parse_obj(obj)

        _obj = ProductAssociationDetails.parse_obj({
            "association_chair_person": obj.get("associationChairPerson"),
            "association_name": obj.get("associationName"),
            "association_number": obj.get("associationNumber")
        })
        return _obj


