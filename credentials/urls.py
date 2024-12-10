from django.urls import path
from credentials import views


urlpatterns = [
    path('credentials/', views.CredentialList.as_view()),
]
