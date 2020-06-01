from rest_framework import serializers
from model_results.models import Results

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ['provider_id', 'measure_id', 'performance_class']