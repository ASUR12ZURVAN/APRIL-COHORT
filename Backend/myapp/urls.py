from django.urls import path
from .views import chatgroq_response

urlpatterns = [
    path("groq-response/", chatgroq_response, name="chatgroq_response"),
]
