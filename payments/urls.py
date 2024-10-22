from django.urls import path
from .views import ZaloPayCreateOrderView, ZaloPayCallbackView, ZaloPayQueryTransactionView

urlpatterns = [
    path('api/payments/zalopay_create_order/', ZaloPayCreateOrderView.as_view(), name='create_order'),
    path('api/payments/callback/', ZaloPayCallbackView.as_view(), name='zalo_pay_callback'),
    path('api/payments/query-transaction/<str:app_trans_id>/', ZaloPayQueryTransactionView.as_view(),
         name='query_transaction'),
]
