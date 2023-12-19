from datetime import datetime
from marshmallow import fields as marshmallow_fields
from s4.platform.entity.entity import Entity, EntitySchema
from s4.platform.entity.field_value import FieldValue, FieldValueSchema
from s4.platform.internal.base_schema import BaseSchema
from typing import Optional


class Task(object):
    def __init__(self, *, iri: str, claim_iri: Optional[str] = None, fields: dict[str, FieldValue],
                 used_entity_iris: list[str], invalidated_entity_iris: list[str],
                 generated_entities: list[Entity], activity_id: Optional[str] = None, 
                 activity_name: Optional[str] = None,process_definition_iri: Optional[str] = None,
                 execution_details_blob: Optional[str] = None, external_task_output: Optional[str] = None,
                 started_at_time: datetime, ended_at_time: datetime, last_changed_at_time: Optional[datetime] = None,
                 was_committed_by: str, was_last_changed_by: Optional[str] = None,
                 was_reverted_by: Optional[str] = None):
        self.iri = iri
        self.claim_iri = claim_iri
        self.was_reverted_by = was_reverted_by
        self.was_last_changed_by = was_last_changed_by
        self.was_committed_by = was_committed_by
        self.last_changed_at_time = last_changed_at_time
        self.ended_at_time = ended_at_time
        self.started_at_time = started_at_time
        self.external_task_output = external_task_output
        self.execution_details_blob = execution_details_blob
        self.process_definition_iri = process_definition_iri
        self.activity_name = activity_name
        self.activity_id = activity_id
        self.fields = fields
        self.used_entity_iris = used_entity_iris
        self.invalidated_entity_iris = invalidated_entity_iris
        self.generated_entities = generated_entities


class TaskSchema(BaseSchema):
    def __init__(self, **kwargs):
        super().__init__(Task, **kwargs)

    iri = marshmallow_fields.Str(load_only=True)
    claim_iri = marshmallow_fields.Str(load_only=True)
    fields = marshmallow_fields.Dict(keys=marshmallow_fields.Str,
                                     values=marshmallow_fields.Nested(FieldValueSchema),
                                     load_only=True)
    used_entity_iris = marshmallow_fields.List(marshmallow_fields.Str, load_only=True)
    invalidated_entity_iris = marshmallow_fields.List(marshmallow_fields.Str, load_only=True)
    generated_entities = marshmallow_fields.List(marshmallow_fields.Nested(EntitySchema))
    was_reverted_by = marshmallow_fields.Str(load_only=True)
    was_last_changed_by = marshmallow_fields.Str(load_only=True)
    was_committed_by = marshmallow_fields.Str(load_only=True)
    last_changed_at_time = marshmallow_fields.DateTime(load_only=True)
    ended_at_time = marshmallow_fields.DateTime(load_only=True)
    started_at_time = marshmallow_fields.DateTime(load_only=True)
    external_task_output = marshmallow_fields.Str(load_only=True)
    execution_details_blob = marshmallow_fields.Str(load_only=True)
    process_definition_iri = marshmallow_fields.Str(load_only=True)
    activity_name = marshmallow_fields.Str(load_only=True)
    activity_id = marshmallow_fields.Str(load_only=True)
