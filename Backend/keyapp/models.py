from django.db import models


class Transcript(models.Model):
    title = models.CharField(max_length=200)
    json_content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    keywords = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

# Create your models here.
