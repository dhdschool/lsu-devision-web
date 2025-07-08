from django.urls import path
from .views import SubmitPredictionView, PredictionResultView

urlpatterns = [
    path('predict/', SubmitPredictionView.as_view(), name='submit-prediction'),
    path('predict/status/<uuid:task_id>/', PredictionResultView.as_view(), name='prediction-status'),
]