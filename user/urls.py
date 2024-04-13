from django.urls import path
from user.views import ClientAPIView, FreelancerAPIView


urlpatterns = [
    path('clients', ClientAPIView.as_view()),
    path('freelancers', FreelancerAPIView.as_view()),
]