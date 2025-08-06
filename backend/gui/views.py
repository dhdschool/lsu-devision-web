from celery.result import AsyncResult
from .models import PredictionModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .serializers import PredictionRequestSerializer, PredictionModelSerializer
from .tasks import process_image_task
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import os

class SubmitPredictionView(APIView):
    def post(self, request):
        serializer = PredictionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        self.validate_model_name(data['model_name'])
        
        image_bytes = data['image'].read()

        task = process_image_task.delay(
            image_bytes=image_bytes,
            model_name=data['model_name'],
            annotate=data['annotate'],
            image_name=data['image_name']
        )

        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)

    def validate_model_name(self, value):
        models_dir = settings.BASE_DIR / 'gui' / 'stardist-models'
        valid_models = os.listdir(models_dir)        
        if value not in valid_models:
            raise serializers.ValidationError(f"Invalid model: {value}")
        return value
    
class PredictionResultView(APIView):
    def get(self, request, task_id):
        task_id = str(task_id)
        result = AsyncResult(task_id)

        if not result.ready():
            return Response({'status': 'processing'}, status=status.HTTP_202_ACCEPTED)

        if result.failed():
            return Response({'status': 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        prediction_id = result.result
        try:
            pred = PredictionModel.objects.get(id=prediction_id)
        except PredictionModel.DoesNotExist:
            return Response({'error': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)

        data = PredictionModelSerializer(pred).data
        return Response({
            'status': 'completed',
            'result': data
        }, status = status.HTTP_200_OK)
        return Response(data, status=status.HTTP_200_OK)

@require_http_methods(["GET","POST"])
def export_settings(request):
    import json
    try:
        data = json.loads(request.body.decode('utf-8'))
        theme = data.get('theme')
        save_model = data.get('save_model')
        save_folder = data.get('save_folder')
        # Save to Profile or handle as needed
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)