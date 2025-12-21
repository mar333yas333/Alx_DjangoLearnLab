from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, ProfileView, UserViewSet, FollowUserView, UnfollowUserView

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),    # << checker يريد user_id
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'), # << checker يريد user_id
]
urlpatterns += router.urls
