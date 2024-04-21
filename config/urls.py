from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # allauth
    path('accounts/', include('allauth.urls')),
    path('user/', include("user.urls")),
    path('job/', include("job.urls")),
    path('payment/', include("payment.urls"))

]
