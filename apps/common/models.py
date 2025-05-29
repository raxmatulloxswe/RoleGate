from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Created date',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Updated date',
    )

    class Meta:
        abstract = True
