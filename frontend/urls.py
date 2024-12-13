from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, HomePageView, ticket_booking_page
from . import views

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='frontend/signin.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('routes/', views.route_list_frontend, name='route_list'),
    path('ticket/<int:route_id>/', ticket_booking_page, name='ticket_booking'),
    ]