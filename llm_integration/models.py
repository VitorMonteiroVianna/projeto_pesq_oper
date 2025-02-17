from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LLMRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_text = models.TextField()
    response_text = models.TextField()
    input_tokens = models.IntegerField()
    output_tokens = models.IntegerField()
    total_tokens = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.total_tokens = self.input_tokens + self.output_tokens
        super().save(*args, **kwargs)

    def __str__(self):
        return f"LLM Request {self.id} - User: {self.user if self.user else 'Internal'}"
