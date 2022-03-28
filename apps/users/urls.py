from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('sign-up/', views.UserRegisterView.as_view(), name='sign_up'),
    path('sign-in/', views.TokenObtainPairPatchedView.as_view(), name='sign_in'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('logout-all/', views.UserLogoutAllView.as_view(), name='logout_all'),
    path('me/', views.CurrentUserView.as_view(), name='me'),
    path('change-password/', views.ChangePasswordView.as_view(), name='me'),

    # Forget password
    path('forget-password-send-email/', views.ForgetPasswordView.as_view(), name='forget_password_send_email'),
    path('forget-password-verification/<uuid:uuid>/', views.ForgetPasswordView.as_view(),
         name='forget_password_verification'),
    path('forget-password-set-new/', views.SetForgetPasswordView.as_view(), name='forget_password_set_new'),
]
