from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    # ✅ عرض كل العقود
   path('', views.contracts_list, name='contracts_list'),

   # ✅ عرض العقود المؤرشفة
    path('archived/', views.archived_contracts, name='archived_contracts'),

    # ✅ تفاصيل عقد محدد
    path('<int:contract_id>/', views.contract_detail_view, name='contract_detail'),

    # ✅ تجديد العقد
    path('<int:contract_id>/renew/', views.renew_contract, name='renew_contract'),

    # ✅ حذف العقد
    path('<int:contract_id>/delete/', views.delete_contract_view, name='delete_contract'),

    # ✅ إضافة عقد جديد
    path('add/', views.create_contract, name='add_contract'),

    # ✅ تعديل عقد موجود
    # path('<int:contract_id>/edit/', views.update_contract_view, name='update_contract'),

    # ✅ قائمة العقود النشطة فقط (اختياري)
    # path('active/', views.active_contracts_view, name='active_contracts'),
]

