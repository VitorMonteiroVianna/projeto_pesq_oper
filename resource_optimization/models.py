import uuid
from django.db import models
from django.contrib.auth import get_user_model
from llm_integration.models import LLMRequest

User = get_user_model()

class OptimizationProcess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='optimizations')
    input_data = models.TextField()
    result_data = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pendente'), ('completed', 'Concluído'), ('failed', 'Falhou')], 
        default='pending'
    )
    llm_request = models.OneToOneField(LLMRequest, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    credit_cost = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['-created_at']

    def charge_credits(self):
        if self.user.credit_balance.withdraw(self.credit_cost):
            return True
        return False

    def __str__(self):
        return f"Optimization {self.id} - {self.user} ({self.status})"

class ResultAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    optimization_process = models.ForeignKey(OptimizationProcess, on_delete=models.CASCADE, related_name='optimizations', null=True)
    analysis_text = models.TextField(null=True, blank=True)
    ai_used = models.BooleanField(default=False)
    llm_request = models.OneToOneField(LLMRequest, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Analysis for Optimization {self.optimization_process.id}"
