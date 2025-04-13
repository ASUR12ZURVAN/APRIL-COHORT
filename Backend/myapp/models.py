from django.db import models


class Ticket_issue(models.Model):
    ticket_text = models.TextField()
    response_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.response_text}"
