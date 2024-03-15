from django.contrib import admin
from django.urls import path
from newsagencyAPI.views import loginView, logoutView, StoriesView

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/login', loginView, name='login'),
    path('api/logout', logoutView, name='logout'),
    path('api/stories', StoriesView.as_view(), name='get_stories'),
    path('api/stories/<int:storyID>', StoriesView.as_view(), name='delete_stories')
]
