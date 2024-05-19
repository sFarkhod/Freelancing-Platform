from django.urls import path
from .views import add_job, get_job, JobListApiView, add_skill, SkillsListApiView, \
    CreateProposalApiView, get_my_proposals, delete_proposal, \
    update_proposal, patch_proposal_for_client_for_close_proposal, \
    create_offer, ContractListApiView, MyOfferListApiViewForClient, MyOfferListApiViewForFreelancer, \
    close_offer, accept_offer, sign_contract, detail_proposal_for_client, close_contract, offer_update, \
    MyContractListApiViewForClient, MyContractListApiViewForFreelancer, MyContractListApiViewForFreelancerInArchive, \
    MyContractListApiViewForClientInArchive, MyOfferListApiViewForFreelancerInArchive, MyOfferListApiViewForClientInArchive


urlpatterns = [
    path('add_job/', add_job, ),
    path('get_jobs/', JobListApiView.as_view(), ),
    path('get_job/<int:pk>/', get_job, ),
    path('add_skills/', add_skill, ),
    path('get_skills/', SkillsListApiView.as_view(), ),
    path('create_proposal/', CreateProposalApiView.as_view(), ),
    path('proposal_list/', get_my_proposals, ),
    path('proposal_for_client/<int:pk>/', detail_proposal_for_client, ),
    path('delete_proposal/<int:pk>/', delete_proposal, ),
    path('update_proposal/<int:pk>/', update_proposal, ),
    # path('patch_proposal_for_client/<int:pk>/', detail_proposal_for_client, ),
    path('patch_proposal_for_close/<int:pk>/', patch_proposal_for_client_for_close_proposal, ),
    path('create_offer/', create_offer, ),
    path('contract_list/', ContractListApiView.as_view(), ),
    path('my_offer_for_client/', MyOfferListApiViewForClient.as_view(), ),
    path('my_offer_for_freelancer/', MyOfferListApiViewForFreelancer.as_view(), ),
    path('close_offer/<int:pk>/', close_offer, ),
    path('accept_offer/<int:pk>/', accept_offer, ),
    path('sign_contract/<int:pk>/', sign_contract, ),
    path('close_contract/<int:pk>/', close_contract, ),
    path('offer_update/<int:pk>/', offer_update, ),
    path('contract_list_for_client/', MyContractListApiViewForClient.as_view(), ),
    path('contract_list_for_freelancer/', MyContractListApiViewForFreelancer.as_view(), ),
    # for archive in contract
    path('contract_list_for_freelancer_for_archive/', MyContractListApiViewForFreelancerInArchive.as_view(), ),
    path('contract_list_for_client_for_archive/', MyContractListApiViewForClientInArchive.as_view(), ),
    # for archive in offer
    path('offer_list_for_freelancer_for_archive/', MyOfferListApiViewForFreelancerInArchive.as_view(), ),
    path('offer_list_for_client_for_archive/', MyOfferListApiViewForClientInArchive.as_view(), ),










]
