from rest_framework import serializers
from .models import AnnotatedImage

class PredictionRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    image_name = serializers.CharField(required=True, allow_blank=True, default="")

    model_name = serializers.CharField(required=True)
    annotate = serializers.BooleanField(required=True, default=True)
    
class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotatedImage
        field = '__all__'