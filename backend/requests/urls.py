from django.urls import path
from .views import submit_request

urlpatterns = [
    path('submit-request/<str:request_type>/', submit_request, name='submit_request'),
]
