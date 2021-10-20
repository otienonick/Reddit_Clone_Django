from django.urls import path
from django.urls.conf import include
from .views import PostList,VoteCreate
from . import views
urlpatterns = [
    #posts
        path('posts',PostList.as_view(),name = 'api-overview'),
        path('posts/<int:pk>/vote',VoteCreate.as_view(),name = 'create-vote'),
        path('api-auth/',include('rest_framework.urls')),

    #Authentication
    path('signup',views.signup),
    path('login',views.login),
    path('logout',views.logout),

]