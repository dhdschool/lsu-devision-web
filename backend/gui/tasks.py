from django.conf import settings
from .models import AnnotatedImage, PredictionModel
from celery import shared_task
from .src.predictions import StardistWrapper
import os
from pathlib import Path
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import transaction

@shared_task
def process_image_task(image_bytes, model_name: str, annotate: bool=True, image_name: str=""):
    models_dir = settings.BASE_DIR / 'gui' / 'stardist-models'
    valid_models = os.listdir(models_dir)
    
    if model_name not in valid_models:
        raise ValueError(f'The model selected ({model_name}) is not present in the models folder. Valid models include {valid_models}')
    
    model = StardistWrapper(model_name)
    
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    class_counts, output_img = model.predict(img, annotate=annotate)
    
    with transaction.atomic():
        class_counts = {int(k):int(v) for k, v in class_counts.items()}
        if output_img is not None:
            color_map = model.color_dct
            buffer = BytesIO()
            output_img.save(buffer, format='JPEG')
            buffer.seek(0)
            
            filename_stem = Path(image_name).stem
            
            color_map = {int(k):v for k, v in color_map.items()}
            
            annotated = AnnotatedImage.objects.create(name=f"{filename_stem}",
                                                        class_color_map=color_map)
            annotated.image.save('result.jpg', ContentFile(buffer.read()), save=False)
            annotated.save()
            
        else:
            annotated=None
            
        predicted = PredictionModel.objects.create(annotated_image=annotated,
                                                class_counts=class_counts)
        predicted.save()
    return predicted.id