from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.contrib.auth.models import User

class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor
		fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = PurchaseOrder
		fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = HistoricalPerformance
		fields = '__all__'

class RegisterUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		extra_kwargs = {'password': {'write_only': True}}

class LoginUserSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()
