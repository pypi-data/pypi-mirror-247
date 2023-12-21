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

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, ValidationError, validator
from nium.models.with_destination_amount import WithDestinationAmount
from nium.models.with_source_amount import WithSourceAmount
from typing import Union, Any, List, TYPE_CHECKING
from pydantic import StrictStr, Field

EITHERSOURCEORDESTINATIONAMOUNTORNOAMOUNT_ONE_OF_SCHEMAS = ["WithDestinationAmount", "WithSourceAmount", "object"]

class EitherSourceOrDestinationAmountOrNoAmount(BaseModel):
    """
    EitherSourceOrDestinationAmountOrNoAmount
    """
    # data type: object
    oneof_schema_1_validator: Optional[Dict[str, Any]] = None
    # data type: WithSourceAmount
    oneof_schema_2_validator: Optional[WithSourceAmount] = None
    # data type: WithDestinationAmount
    oneof_schema_3_validator: Optional[WithDestinationAmount] = None
    if TYPE_CHECKING:
        actual_instance: Union[WithDestinationAmount, WithSourceAmount, object]
    else:
        actual_instance: Any
    one_of_schemas: List[str] = Field(EITHERSOURCEORDESTINATIONAMOUNTORNOAMOUNT_ONE_OF_SCHEMAS, const=True)

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
        instance = EitherSourceOrDestinationAmountOrNoAmount.construct()
        error_messages = []
        match = 0
        # validate data type: object
        try:
            instance.oneof_schema_1_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: WithSourceAmount
        if not isinstance(v, WithSourceAmount):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WithSourceAmount`")
        else:
            match += 1
        # validate data type: WithDestinationAmount
        if not isinstance(v, WithDestinationAmount):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WithDestinationAmount`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in EitherSourceOrDestinationAmountOrNoAmount with oneOf schemas: WithDestinationAmount, WithSourceAmount, object. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in EitherSourceOrDestinationAmountOrNoAmount with oneOf schemas: WithDestinationAmount, WithSourceAmount, object. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: dict) -> EitherSourceOrDestinationAmountOrNoAmount:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> EitherSourceOrDestinationAmountOrNoAmount:
        """Returns the object represented by the json string"""
        instance = EitherSourceOrDestinationAmountOrNoAmount.construct()
        error_messages = []
        match = 0

        # deserialize data into object
        try:
            # validation
            instance.oneof_schema_1_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_1_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into WithSourceAmount
        try:
            instance.actual_instance = WithSourceAmount.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into WithDestinationAmount
        try:
            instance.actual_instance = WithDestinationAmount.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into EitherSourceOrDestinationAmountOrNoAmount with oneOf schemas: WithDestinationAmount, WithSourceAmount, object. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into EitherSourceOrDestinationAmountOrNoAmount with oneOf schemas: WithDestinationAmount, WithSourceAmount, object. Details: " + ", ".join(error_messages))
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


