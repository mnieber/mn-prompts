import uuid

from django.db import models

from blogs_be.common.fields import AutoCreatedAtField, AutoLastModifiedAtField


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = AutoCreatedAtField()
    modified_at = AutoLastModifiedAtField()
