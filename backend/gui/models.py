from django.db import models
import uuid
from datetime import datetime
from pathlib import Path

def annotated_image_upload_path(instance, filename):
    # Save files to MEDIA_ROOT/annotated/<uuid>.jpg
    
    filename = Path(filename)
    ext = filename.suffix
    new_filename = f"{uuid.uuid4().hex}{ext}"
    return Path('annotated') / new_filename

# Create your models here.
class AnnotatedImage(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=annotated_image_upload_path,
                              height_field='image_height',
                              width_field='image_width')
    
    image_height =  models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    class_color_map = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.name or f"AnnotatedImage {self.id}"
    
class PredictionModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    annotated_image = models.OneToOneField(AnnotatedImage,
                                           on_delete=models.CASCADE,
                                           null=True)
    
    class_counts = models.JSONField(blank=False, null=False)
    
    def __str__(self):
        if self.annotated_image:
            string = f"Prediction on {self.annotated_image}"
        else:
            string = f"Prediction at {self.timestamp}"
        return string