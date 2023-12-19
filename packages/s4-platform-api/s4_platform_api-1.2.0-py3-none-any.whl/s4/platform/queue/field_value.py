from typing import Optional

from marshmallow import fields
from s4.platform.internal.base_schema import BaseSchema
from s4.platform.internal.fields_mixin import BaseFieldValue


class FieldValue(BaseFieldValue):
    def __init__(self, *, value: Optional[str], data_type: str):
        self.value = value
        self.data_type = data_type


class FieldValueSchema(BaseSchema):
    def __init__(self, **kwargs):
        super().__init__(FieldValue, **kwargs)

    value = fields.Str(required=True)
    data_type = fields.Str(required=True)
