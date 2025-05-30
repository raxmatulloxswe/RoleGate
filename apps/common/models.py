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


class AuditLog(BaseModel):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
    )
    action = models.CharField(
        max_length=99
    )
    data = models.JSONField(
        null=True, blank=True
    )
    token = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    ip_address = models.GenericIPAddressField(
        null=True, blank=True
    )
    user_agent = models.CharField(
        max_length=255,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.user} - {self.action}"


    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'