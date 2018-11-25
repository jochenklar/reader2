from django.urls import include, path
from django.contrib import admin

from reader.views import index, login, logout


urlpatterns = [
    path('', index),
    path('login/', login),
    path('logout/', logout),
    path('api/', include('feeds.urls')),

    path('admin/', admin.site.urls),
]
