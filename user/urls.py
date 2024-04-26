from django.urls import path
from user.views import (CreateUserView, VerifyAPIView, GetNewVerification, FreelancerListAPIView, ClientListAPIView,ClientUdateAPIView, 
                        FreelancerDetailAPIView, ClientDetailAPIView, LoginView, LoginRefreshView, LogoutView,FreelancerUdateAPIView,
                        ForgotPasswordView, ResetPasswordView, FeedbackAPIView, GithubLoginAPIView, GithubCallbackAPIView, GoogleLoginAPIView, GoogleCallbackAPIView)


urlpatterns = [
    path('github/callback', GithubCallbackAPIView.as_view()),
    path('github-login', GithubLoginAPIView.as_view()),
    path('google/callback', GoogleCallbackAPIView.as_view()),
    path('google-login', GoogleLoginAPIView.as_view()),
    path('feedback', FeedbackAPIView.as_view()),
    path('clients', ClientListAPIView.as_view()),
    path('clients/<str:id>', ClientDetailAPIView.as_view()),
    path('clients/<str:id>/update', ClientUdateAPIView.as_view()),
    path('freelancers', FreelancerListAPIView.as_view()),
    path('freelancers/<str:id>', FreelancerDetailAPIView.as_view()),
    path('freelancers/<str:id>/update', FreelancerUdateAPIView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('login/refresh', LoginRefreshView.as_view()),
    path('signup', CreateUserView.as_view()),
    path('verify', VerifyAPIView.as_view()),
    path('new-verify', GetNewVerification.as_view()),
    path('forgot-password', ForgotPasswordView.as_view()),
    path('reset-password', ResetPasswordView.as_view()),
]