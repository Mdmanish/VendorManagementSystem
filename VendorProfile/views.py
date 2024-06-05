from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, RegisterUserSerializer, LoginUserSerializer
from datetime import datetime
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserView(APIView):
    """
    API endpoint for user registration.
    """

    def post(self, request):
        """
        Method for registering a new user.
        """
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    """
    API endpoint for user login.
    """

    def post(self, request):
        """
        Method for user login.
        """
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({'access': str(refresh.access_token), 'refresh_token': str(refresh)})
            else:
                return Response({'errors': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class VendorListCreateAPIView(APIView):
    """
    API endpoint for listing and creating vendors.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Method for retrieving all vendors.
        """
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Method for creating a new vendor.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorRetrieveUpdateDestroyAPIView(APIView):
    """
    API endpoint for retrieving, updating, and deleting a vendor.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        """
        Method for retrieving a specific vendor.
        """
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_id):
        """
        Method for updating a vendor.
        """
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        """
        Method for deleting a vendor.
        """
        vendor = get_object_or_404(Vendor, id=vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderListCreateAPIView(APIView):
    """
    API endpoint for listing and creating purchase orders.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Method for retrieving all purchase orders or filtering by vendor.
        """
        vendor_id = request.query_params.get('vendor_id', None)
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Method for creating a new purchase order.
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderRetrieveUpdateDestroyAPIView(APIView):
    """
    API endpoint for retrieving, updating, and deleting a purchase order.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, po_id):
        """
        Method for retrieving a specific purchase order.
        """
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, po_id):
        """
        Method for updating a purchase order.
        """
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        """
        Method for deleting a purchase order.
        """
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoricalPerformanceView(APIView):
    """
    API endpoint for retrieving historical performance of a vendor.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, vendor_id):
        """
        Method for retrieving historical performance of a vendor.
        """
        performance = HistoricalPerformance.objects.filter(vendor=vendor_id)
        serializer = HistoricalPerformanceSerializer(performance, many=True)
        return Response(serializer.data)


class PurchaseOrderAcknowledge(APIView):
    """
    API endpoint for acknowledging a purchase order.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, po_id):
        """
        Method for acknowledging a purchase order.
        """
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        return Response({'message': 'Purchase order acknowledged successfully'}, status=status.HTTP_200_OK)
