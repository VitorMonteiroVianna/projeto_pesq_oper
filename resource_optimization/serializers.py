from rest_framework import serializers
from .models import OptimizationProcess

class OptimizationProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizationProcess
        fields = ['id', 'input_data', 'result_data', 'status', 'created_at', 'credit_cost']
        read_only_fields = ['id', 'result_data', 'status', 'created_at']
