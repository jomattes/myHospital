from rest_framework import serializers
from model_results.models import Results

# class ResultSerializer(serializers.Serializer):
#     provider_id = serializers.CharField(max_length=100, allow_blank=True)
#     measure_id = serializers.CharField(max_length=100, allow_blank=True)
#     performance_class = serializers.CharField(max_length=100, allow_blank=True)

#     def create(self, validated_data):
#         """
#         Create and return a new 'Result' instance, given the validated data.
#         """
#         return Results.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing 'Result' instance, given the validated data.
#         """

#         instance.provider_id = validated_data.get('provider_id', instance.provider_id)
#         instance.measure_id = validated_data.get('measure_id', instance.measure_id)
#         instance.performance_class = validated_data.get('performance_class', instance.performance_class)

#         instance.save()
#         return instance

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ['provider_id', 'measure_id', 'performance_class']