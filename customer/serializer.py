from rest_framework import serializers
from.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'name', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'phone_number']
