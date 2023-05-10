from django.urls import path

from apps.accounts import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.user_logout, name="logout"),
    
    # for registration
    path("register/done/", views.RegisterDoneView.as_view(), name="register_done"),
    path("register/", views.UserRegisterView.as_view(), name="register"),

    # url for user activation 
    path("register/confirm/<str:uidb64>/<str:token>/", views.activate_account, name="account_activate")
]