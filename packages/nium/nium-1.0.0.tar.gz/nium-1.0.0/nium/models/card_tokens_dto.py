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

class CardTokensDTO(BaseModel):
    """
    This array contains the token details.  # noqa: E501
    """
    provider_type: Optional[StrictStr] = Field(None, alias="providerType", description="This field contains the wallet provider.It can contain two values - googlePay applePay")
    token_reference_number: Optional[StrictStr] = Field(None, alias="tokenReferenceNumber", description="This field contains the reference number for the token provided against the provisioning request.")
    token_number: Optional[StrictStr] = Field(None, alias="tokenNumber", description="This field contains the token value created for the provisioned card.")
    token_requester_id: Optional[StrictStr] = Field(None, alias="tokenRequesterId", description="This field contains the identifier for the provisioning service.")
    device_id: Optional[StrictStr] = Field(None, alias="deviceId", description="This field contains the unique ID of the device on which the card is provisioned.")
    device_type: Optional[StrictStr] = Field(None, alias="deviceType", description="This field contains the device type in numeric format used for provisioning.")
    status: Optional[StrictStr] = Field(None, description="This field contains the token status.")
    created_at: Optional[StrictStr] = Field(None, alias="createdAt", description="This field contains the date and time of token creation in the format - YYYY-MM-DD HH:mm:ss.")
    updated_at: Optional[StrictStr] = Field(None, alias="updatedAt", description="This field contains the date and time of token update in the format - YYYY-MM-DD HH:mm:ss.")
    __properties = ["providerType", "tokenReferenceNumber", "tokenNumber", "tokenRequesterId", "deviceId", "deviceType", "status", "createdAt", "updatedAt"]

    @validator('provider_type')
    def provider_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('googlePay,applePay,samsungPay,unknown'):
            raise ValueError("must be one of enum values ('googlePay,applePay,samsungPay,unknown')")
        return value

    @validator('token_requester_id')
    def token_requester_id_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('googlePay,applePay'):
            raise ValueError("must be one of enum values ('googlePay,applePay')")
        return value

    @validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('ACTIVE,SUSPENDED,DEACTIVATED,UNKNOWN'):
            raise ValueError("must be one of enum values ('ACTIVE,SUSPENDED,DEACTIVATED,UNKNOWN')")
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
    def from_json(cls, json_str: str) -> CardTokensDTO:
        """Create an instance of CardTokensDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CardTokensDTO:
        """Create an instance of CardTokensDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CardTokensDTO.parse_obj(obj)

        _obj = CardTokensDTO.parse_obj({
            "provider_type": obj.get("providerType"),
            "token_reference_number": obj.get("tokenReferenceNumber"),
            "token_number": obj.get("tokenNumber"),
            "token_requester_id": obj.get("tokenRequesterId"),
            "device_id": obj.get("deviceId"),
            "device_type": obj.get("deviceType"),
            "status": obj.get("status"),
            "created_at": obj.get("createdAt"),
            "updated_at": obj.get("updatedAt")
        })
        return _obj


