from rest_framework import serializers
from diet_app.models import User,UserProfile,FoodLog

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only = True)

    class Meta:

        model = User

        fields = ["id","username","password","email","phone","profile"]

        extra_kwargs = {
                        "password": {"write_only": True}
                       }
        
    def get_profile(self, obj):
        try:
            return UserProfileSerializer(obj.profile).data
        except UserProfile.DoesNotExist:
            return None

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):

    
    class Meta:

        model = UserProfile

        fields = "__all__"

        read_only_fields = ["id","owner","bmr"]


class FoodLogSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    class Meta:

        model = FoodLog

        fields = '__all__'

        read_only_fields = ['id','owner','created_at']
