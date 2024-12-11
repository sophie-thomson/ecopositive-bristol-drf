from django.urls import path
from endorsements import views

urlpatterns = [
    path('endorsements/', views.EndorsementList.as_view()),
    path('endorsements/<int:pk>/', views.EndorsementDetail.as_view())
]
