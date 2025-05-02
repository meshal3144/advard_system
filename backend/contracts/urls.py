from django.urls import path
from . import views
app_name = 'contracts'



urlpatterns = [
    path('', views.contracts_list_view, name='contracts_list'),
    path('<int:contract_id>/', views.contract_detail_view, name='contract_detail'),
    path('<int:contract_id>/renew/', views.renew_contract, name='renew_contract'),
        # ✅ نضيف مسار جديد لإضافة عقد جديد
    path('add/', views.create_contract, name='add_contract'),

    

]




