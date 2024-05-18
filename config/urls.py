from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Freelancer API",
        default_version="v1",
        description="Freelancer API",
        terms_of_services="freelancer",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('job/', include("job.urls")),
    path('payment/', include("payment.urls")),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    #JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  

    # swagger

    path('swagger/', schema_view.with_ui(
        "swagger", cache_timeout=0), name="swagger-swagger-ui"),
    path('redoc/', schema_view.with_ui(
        "redoc", cache_timeout = 0), name="schema-redoc"),
]
