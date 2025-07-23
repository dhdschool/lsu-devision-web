from django.urls import path
from .views import SubmitPredictionView, PredictionResultView, export_settings

urlpatterns = [
    path('predict/', SubmitPredictionView.as_view(), name='submit-prediction'),
    path('predict/status/<uuid:task_id>/', PredictionResultView.as_view(), name='prediction-status'),
    path('settings/export', export_settings, name='export_settings'),
]