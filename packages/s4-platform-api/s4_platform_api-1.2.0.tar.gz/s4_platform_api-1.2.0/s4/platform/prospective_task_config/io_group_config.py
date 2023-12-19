from marshmallow import fields

from typing import Dict, List
from s4.platform.internal.base_schema import BaseSchema
from s4.platform.prospective_task_config.group_config import (
    GroupConfig,
    GroupConfigSchema,
)


class IoGroupConfig(object):
    def __init__(
        self, *, inputs: Dict[str, GroupConfig], outputs: Dict[str, GroupConfig], manual: bool = False
    ):
        self.inputs = inputs
        for key, inputConfig in self.inputs.items():
            if inputConfig.invalidate is None:
                inputConfig.invalidate = True
        self.outputs = outputs
        for key, outputConfig in self.outputs.items():
            if outputConfig.invalidate is None:
                outputConfig.invalidate = False
        self.manual = manual


class IoGroupConfigSchema(BaseSchema):
    def __init__(self, **kwargs):
        super().__init__(IoGroupConfig, **kwargs)

    inputs = fields.Dict(
        keys=fields.Str, values=fields.Nested(GroupConfigSchema), required=True
    )
    outputs = fields.Dict(
        keys=fields.Str, values=fields.Nested(GroupConfigSchema), required=True
    )
    manual = fields.Bool(allow_none=True)
