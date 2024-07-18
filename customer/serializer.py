from rest_framework import serializers
from.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user','unique_id', 'first_name', 'last_name', 'address1', 'address2', 'zip_code', 'city', 'state', 'country', 'phone_number']
