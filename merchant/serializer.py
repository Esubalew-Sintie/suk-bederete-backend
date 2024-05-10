from rest_framework.serializers import ModelSerializer
from .models import Merchant
from account.serializer import AccountSerializer
from account.models import Account

class MerchantSerializer(ModelSerializer):
    user = AccountSerializer()

    class Meta:
        model = Merchant
        fields = ('user','unique_id', 'bank_account_number', 'has_physical_store', 'physical_shop_name', 'physical_shop_address', 'physical_shop_city', 'physical_shop_phone_number', 'online_shop_type')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = Account.objects.create_user(**user_data)
        merchant = Merchant.objects.create(user=user, **validated_data)
        return merchant