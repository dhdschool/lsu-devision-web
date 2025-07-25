from rest_framework import serializers
from .models import PredictionModel, AnnotatedImage, SettingsProfile

class PredictionRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    image_name = serializers.CharField(allow_blank=True, default="")

    model_name = serializers.CharField(required=True)
    annotate = serializers.BooleanField(default=True)
    
class AnnotatedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotatedImage
        fields = ['id', 'name', 'image', 'image_height', 'image_width', 'class_color_map']

class PredictionModelSerializer(serializers.ModelSerializer):
    annotated_image = AnnotatedImageSerializer(read_only=True)
    
    class Meta:
        model = PredictionModel
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsProfile
        fields = ['theme', 'autoExport', 'folderPath', 'model']

        