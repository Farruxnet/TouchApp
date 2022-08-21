from django.contrib import admin
from django.urls import path, include
# 1
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('app.urls')),
]
