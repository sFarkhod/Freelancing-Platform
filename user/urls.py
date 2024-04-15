from django.urls import path
from user.views import (CreateUserView, VerifyAPIView, GetNewVerification, FreelancerListAPIView, ClientListAPIView,
                        FreelancerDetailAPIView, ClientDetailAPIView, LoginView, LoginRefreshView, LogoutView,
                        ForgotPasswordView, ResetPasswordView, FeedbackAPIView)


urlpatterns = [
    path('feedback', FeedbackAPIView.as_view()),
    path('clients', ClientListAPIView.as_view()),
    path('clients/<str:id>', ClientDetailAPIView.as_view()),
    path('freelancers', FreelancerListAPIView.as_view()),
    path('freelancers/<str:id>', FreelancerDetailAPIView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('login/refresh', LoginRefreshView.as_view()),
    path('signup', CreateUserView.as_view()),
    path('verify', VerifyAPIView.as_view()),
    path('new-verify', GetNewVerification.as_view()),
    path('forgot-password', ForgotPasswordView.as_view()),
    path('reset-password', ResetPasswordView.as_view()),
]