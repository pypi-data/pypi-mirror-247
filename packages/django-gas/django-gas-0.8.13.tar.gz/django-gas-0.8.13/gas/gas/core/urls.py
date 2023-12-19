from django.contrib.auth.views import logout_then_login
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.GASLoginView.as_view(), name='login'),
    path('logout/', logout_then_login, {'login_url': 'gas:login'}, name='logout'),
    path('change-password/', views.GASPasswordChangeView.as_view(), name='change_password'),
    path('reset-password-confirm/<uidb64>/<token>/', views.GASPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-confirm/done/', views.GASPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset-password/done/', views.GASPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/', views.GASPasswordResetView.as_view(), name='reset_password'),
    path('', views.Index.as_view(), name='index'),
]
