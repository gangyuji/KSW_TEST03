from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='sign_up_view'), # /users/signup/
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/<int:user_id>/', views.ProfileView.as_view(), name="profile_view"), # /users/profile/<int:user_id>/
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'), # /users/follow/<int:user_id>/
]
