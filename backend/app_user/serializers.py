from rest_framework import serializers

from .models import User, Characters


class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        password = request.data.get('password')

        if len(password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters.")
        
        password_split = [*password]
        if ord(password_split[0]) not in range(65, 90):
            raise serializers.ValidationError("The first letter of the password must be capitalized.")
        check_have_number = False
        for i in password_split:
            if ord(i) in range(48, 57):
                check_have_number = True
                break
        if not check_have_number:
            raise serializers.ValidationError("Password must contain number.")
        validated_data['password'] = password

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    

class CharactersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Characters
        fields = "__all__"

    def create(self, validated_data):
        
        return super().create(validated_data)
