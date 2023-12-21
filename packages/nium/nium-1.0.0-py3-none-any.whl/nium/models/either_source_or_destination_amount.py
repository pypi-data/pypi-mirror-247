# coding: utf-8

"""
    NIUM Platform

    NIUM Platform

    Contact: experience@nium.com
    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
from inspect import getfullargspec
import json
import pprint
import re  # noqa: F401

from typing import Any, List, Optional
from pydantic import BaseModel, Field, StrictStr, ValidationError, validator
from nium.models.with_destination_amount1 import WithDestinationAmount1
from nium.models.with_source_amount1 import WithSourceAmount1
from typing import Union, Any, List, TYPE_CHECKING
from pydantic import StrictStr, Field

EITHERSOURCEORDESTINATIONAMOUNT_ONE_OF_SCHEMAS = ["WithDestinationAmount1", "WithSourceAmount1"]

class EitherSourceOrDestinationAmount(BaseModel):
    """
    EitherSourceOrDestinationAmount
    """
    # data type: WithSourceAmount1
    oneof_schema_1_validator: Optional[WithSourceAmount1] = None
    # data type: WithDestinationAmount1
    oneof_schema_2_validator: Optional[WithDestinationAmount1] = None
    if TYPE_CHECKING:
        actual_instance: Union[WithDestinationAmount1, WithSourceAmount1]
    else:
        actual_instance: Any
    one_of_schemas: List[str] = Field(EITHERSOURCEORDESTINATIONAMOUNT_ONE_OF_SCHEMAS, const=True)

    class Config:
        validate_assignment = True

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = EitherSourceOrDestinationAmount.construct()
        error_messages = []
        match = 0
        # validate data type: WithSourceAmount1
        if not isinstance(v, WithSourceAmount1):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WithSourceAmount1`")
        else:
            match += 1
        # validate data type: WithDestinationAmount1
        if not isinstance(v, WithDestinationAmount1):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WithDestinationAmount1`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in EitherSourceOrDestinationAmount with oneOf schemas: WithDestinationAmount1, WithSourceAmount1. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in EitherSourceOrDestinationAmount with oneOf schemas: WithDestinationAmount1, WithSourceAmount1. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: dict) -> EitherSourceOrDestinationAmount:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> EitherSourceOrDestinationAmount:
        """Returns the object represented by the json string"""
        instance = EitherSourceOrDestinationAmount.construct()
        error_messages = []
        match = 0

        # deserialize data into WithSourceAmount1
        try:
            instance.actual_instance = WithSourceAmount1.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into WithDestinationAmount1
        try:
            instance.actual_instance = WithDestinationAmount1.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into EitherSourceOrDestinationAmount with oneOf schemas: WithDestinationAmount1, WithSourceAmount1. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into EitherSourceOrDestinationAmount with oneOf schemas: WithDestinationAmount1, WithSourceAmount1. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        to_json = getattr(self.actual_instance, "to_json", None)
        if callable(to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> dict:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        to_dict = getattr(self.actual_instance, "to_dict", None)
        if callable(to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.dict())


