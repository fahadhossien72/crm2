from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('products/', views.products, name='products'),    
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('create_order/<str:pk>', views.create_Order, name='create_order'),
    path('update_order/<str:pk>/', views.update_Order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_Order, name='delete_order'),

    path('login/', views.loginPage, name='loginPage'),
    path('setting/', views.settingPage, name='settingPage'),
    path('user/', views.userPage, name='userPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
    path('register/', views.registerPage, name='registerPage'),

    path('password_reset', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
        name='password_reset'),
    path('password_reset_done', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), 
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), 
        name='password_reset_confirm'),
    path('password_reset_complete', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), 
        name='password_reset_complete')
]
