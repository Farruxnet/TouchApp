from django.contrib import admin
from django.urls import path, include
# 123
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('app.urls')),
]
