from django.contrib import admin
from django.urls import path
from newsagencyAPI.views import loginView, logoutView, StoriesView

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'),
    path('stories', StoriesView.as_view(), name='stories'),
]
