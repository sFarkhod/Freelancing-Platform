from django.urls import path
from .views import add_job, get_job, JobListApiView, add_skill, SkillsListApiView, \
    CreateProposalApiView, get_my_proposals, ProposalDetailApiView, delete_proposal, \
    update_proposal, patch_proposal_for_client, patch_proposal_for_client_for_close_proposal


urlpatterns = [
    path('add_job/', add_job, ),
    path('get_jobs/', JobListApiView.as_view(), ),
    path('get_job/<int:pk>/', get_job, ),
    path('add_skills/', add_skill, ),
    path('get_skills/', SkillsListApiView.as_view(), ),
    path('create_proposal/', CreateProposalApiView.as_view(), ),
    path('proposal_list/', get_my_proposals, ),
    path('proposal/<int:pk>/', ProposalDetailApiView.as_view(), ),
    path('delete_proposal/<int:pk>/', delete_proposal, ),
    path('update_proposal/<int:pk>/', update_proposal, ),
    path('patch_proposal_for_client/<int:pk>/', patch_proposal_for_client, ),
    path('patch_proposal_for_close/<int:pk>/', patch_proposal_for_client_for_close_proposal, ),




]
