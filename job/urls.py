from django.urls import path
from .views import add_job, get_job, JobListApiView, add_skill, SkillsListApiView


urlpatterns = [
    path('add_job/', add_job, ),
    path('get_jobs/', JobListApiView.as_view(), ),
    path('get_job/<int:pk>/', get_job, ),
    path('add_skills/', add_skill, ),
    path('get_skills/', SkillsListApiView.as_view(), ),



]

