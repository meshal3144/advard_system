
from django.urls import path
from . import views



urlpatterns = [
    path('set-password/<uidb64>/<token>/', views.set_password_view, name='set_password'),
    path('profile/', views.profile_view, name='profile'),  # مسار صفحة البروفايل
    path('mark-welcome-shown/', views.mark_welcome_shown, name='mark_welcome_shown'),
    path('clients/', views.clients_view, name='clients'),  # ← هذا هو الرابط
    path('clients/<int:user_id>/', views.client_detail_view, name='client_detail'),
    path('clients/<int:user_id>/activate/', views.activate_user_view, name='activate_user'),
    path('clients/<int:user_id>/deactivate/', views.deactivate_user_view, name='deactivate_user'),
    path('clients/<int:user_id>/send-link/', views.send_set_password_link_view, name='send_set_password_link'),
    path('clients/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),  # ✅ جديد
]


