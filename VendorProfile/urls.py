from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
	RegisterUserView, LoginUserView,
	VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView, PurchaseOrderListCreateAPIView,
	PurchaseOrderRetrieveUpdateDestroyAPIView, PurchaseOrderAcknowledge, HistoricalPerformanceView
)

urlpatterns = [
	path('login/', LoginUserView.as_view(), name='login-view'),
	path('register/', RegisterUserView.as_view(), name='register-view'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
	path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
	path('api/vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-modify-destroy'),

	path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase_orders-list-create'),
	path('api/purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase_orders-modify-destroy'),

	path('api/vendors/<int:vendor_id>/performance/', HistoricalPerformanceView.as_view(), name='performance-view'),
	path('api/purchase_orders/<int:po_id>/acknowledge/', PurchaseOrderAcknowledge.as_view(), name='purchase_orders-acknowledge'),
]
