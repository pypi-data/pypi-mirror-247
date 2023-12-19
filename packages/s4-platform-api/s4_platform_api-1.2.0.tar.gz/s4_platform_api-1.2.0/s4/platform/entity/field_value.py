from typing import Optional

from marshmallow import fields
from s4.platform.internal.base_schema import BaseSchema
from s4.platform.internal.fields_mixin import BaseFieldValue


class FieldValue(BaseFieldValue):
    def __init__(
        self,
        *,
        value: Optional[str],
        data_type: str,
        validation_errors: Optional[list[str]] = None
    ) -> None:
        self.value = value
        self.data_type = data_type
        # TODO: PF-1646
        #  There doesn't seem to be an obvious link for the validation_errors property
        self.validation_errors = validation_errors


class FieldValueSchema(BaseSchema):
    def __init__(self, **kwargs):
        super().__init__(FieldValue, **kwargs)

    value = fields.Str(allow_none=True)
    data_type = fields.Str(required=True)
    validation_errors = fields.List(fields.Str(), allow_none=True)
