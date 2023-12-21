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


from typing import Dict, Optional
from pydantic import BaseModel, Field, StrictStr, constr, validator
from nium.models.address import Address

class AddCardRequestV2(BaseModel):
    """
    AddCardRequestV2
    """
    card_product_id: StrictStr = Field(..., alias="cardProductId", description="Pre-defined product Id, defined at NIUM and communicated to client for card issuance.")
    card_type: StrictStr = Field(..., alias="cardType", description="This field accepts the card type to be issued. The acceptable values are:\\n\" + \"PHY: This value is used to issue a physical card\\n\" + \"VIR: This value is used to issue a virtual card\\n\" + \"VIRUP2PHY: This value is used to issue a virtual upgrade to physical card")
    card_expiry: StrictStr = Field(..., alias="cardExpiry", description="Expiry date to be set for virtual and virtual physical cards. For physical cards do not send this field. This field is in MMYY format. For virtual cards, the last acceptable date is the year-end of the 5th year from now. Card will be valid till the last day of the month and year of expiry.")
    name_on_card: Optional[constr(strict=True, max_length=26, min_length=1)] = Field(None, alias="nameOnCard", description="This field can be used to print the customer name. The value sent in this field will be printed on the card.If this field is left empty, line 1 will not be printed on the card. This field accepts alphanumeric characters along with space(s) The maximum character limit is 26.")
    additional_line: Optional[constr(strict=True, max_length=26, min_length=1)] = Field(None, alias="additionalLine", description="This field can be used to send the company name or employeeID. Anything sent in this field will be printed on the card.  This field accepts alphanumeric characters along with space(s). The maximum character limit is 26.")
    delivery: Optional[Address] = None
    email: Optional[StrictStr] = Field(None, description="Email of the card holder.")
    country_code: Optional[constr(strict=True)] = Field(None, alias="countryCode", description="Country code of recipient's phone number accepted in [2-letter ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf).")
    mobile: Optional[StrictStr] = Field(None, description="Mobile field is where the recipient's mobile phone number.")
    issuance_mode: Optional[StrictStr] = Field(None, alias="issuanceMode", description="This field is only required for physical cards(PHY) mode of delivery of a card. Possible values are: normal_delivery_local express_delivery_local international_deliveryinternational_delivery_track international_delivery_track_sign")
    plastic_id: constr(strict=True, max_length=10, min_length=0) = Field(..., alias="plasticId", description="Pre-defined plastic Id defined at NIUM and communicated to client. It is used to determine the card design")
    child_customer_hash_id: Optional[StrictStr] = Field(None, alias="childCustomerHashId", description="This field contains the child customerHashId")
    additional_info: Optional[Dict[str, StrictStr]] = Field(None, alias="additionalInfo", description="This field accepts additional information in form of map with key value pairs as string.")
    __properties = ["cardProductId", "cardType", "cardExpiry", "nameOnCard", "additionalLine", "delivery", "email", "countryCode", "mobile", "issuanceMode", "plasticId", "childCustomerHashId", "additionalInfo"]

    @validator('country_code')
    def country_code_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"[A-Z]{2}", value):
            raise ValueError(r"must validate the regular expression /[A-Z]{2}/")
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
    def from_json(cls, json_str: str) -> AddCardRequestV2:
        """Create an instance of AddCardRequestV2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of delivery
        if self.delivery:
            _dict['delivery'] = self.delivery.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddCardRequestV2:
        """Create an instance of AddCardRequestV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddCardRequestV2.parse_obj(obj)

        _obj = AddCardRequestV2.parse_obj({
            "card_product_id": obj.get("cardProductId"),
            "card_type": obj.get("cardType"),
            "card_expiry": obj.get("cardExpiry"),
            "name_on_card": obj.get("nameOnCard"),
            "additional_line": obj.get("additionalLine"),
            "delivery": Address.from_dict(obj.get("delivery")) if obj.get("delivery") is not None else None,
            "email": obj.get("email"),
            "country_code": obj.get("countryCode"),
            "mobile": obj.get("mobile"),
            "issuance_mode": obj.get("issuanceMode"),
            "plastic_id": obj.get("plasticId"),
            "child_customer_hash_id": obj.get("childCustomerHashId"),
            "additional_info": obj.get("additionalInfo")
        })
        return _obj


