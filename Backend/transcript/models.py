from django.db import models

# Create your models here.
# transcript/models.py


class CallTranscript(models.Model):
    raw_text = models.TextField()
    customer_parts = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from .services import extract_customer_responses
        self.customer_parts = extract_customer_responses(self.raw_text)
        super().save(*args, **kwargs)