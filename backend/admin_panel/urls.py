from django.urls import path
from . import views
from django.conf.urls.i18n import set_language
from django.urls import path, include


urlpatterns = [
    path('set-language/', set_language, name='set_language'),
    path('submit/<str:request_type>/', views.submit_request, name='submit_request'),
    path('thank-you/', views.thank_you, name='success_page'),
    path('dashboard/', views.reports_page, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('service-requests/', views.service_requests_view, name='service_requests'),
    path('service-requests/<int:request_id>/', views.view_request_detail, name='view_request_detail'),
    path('accounts/', include('accounts.urls')),
    path('clients/<int:user_id>/', views.client_detail_view, name='client_detail'),
    



]

