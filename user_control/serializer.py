from .models import User
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('iduser', 'username', "password", "email",'phone', 'addres')
        fields = '__all__'