from rest_framework import serializers
from .models import User
from .models import Event , Comment
class RegistrationForm(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])  # Хешування пароля
        user.save()
        return user

class ProfileUpdateForm(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'description', 'location_short']




class EventSerializer(serializers.ModelSerializer):
    posted_by_profile_picture = serializers.ImageField(source='posted_by.profile_picture', read_only=True)
    posted_by_first_name = serializers.CharField(source='posted_by.first_name', read_only=True)
    posted_by_last_name = serializers.CharField(source='posted_by.last_name', read_only=True)
    class Meta:
        model = Event
        fields = '__all__'  # Включаємо всі поля моделі
        read_only_fields = ['posted_by', 'is_approved']

    def validate(self, data):
        """Кастомна валідація події"""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Дата завершення не може бути раніше дати початку.")
        if data['people_needed'] < 1:
            raise serializers.ValidationError("Поле 'people_needed' повинно бути більше 0.")
        return data



class CommentSerializer(serializers.ModelSerializer):
    
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    author_profile_picture = serializers.ImageField(source='author.profile_picture', read_only=True)
    

    class Meta:
        model = Comment
        fields = ["id", "author_first_name",  "author_profile_picture", "author_last_name",  "text", "created_at"]