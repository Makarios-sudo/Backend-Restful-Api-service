
from dataclasses import fields
from pkg_resources import require
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# imports for registeration of user
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator



# adiing claims to the payload for login in user
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["password"] = user.password
        token["id"]= user.id
        return token
    

# register user serializer
class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators = [validate_password])
    password2 = serializers.CharField( write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "first_name", "last_name")
        extra_kwargs = { 
            "first_name":{"required": True},
            "last_name":{"required": True}
        }

    #checking if the passwords are the same
    def validate(self,attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password Fields did not match."})
        return attrs
    # saving the data into the database
    def create(self, validated_data):
        user = User.objects.create( 
            username = validated_data["username"],
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"]        
        )

        user.set_password(validated_data["password"])
        user.save()
        return user

    #another way of saving register users
    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            ## At this point, user is a User object that has already been
            ## saved to the database. You can continue to change its 
            ## attributes if you want to change other fields.
        
    #     user.first_name = validated_data['first_name']
    #     user.last_name  = validated_data['last_name']
    #     user.save()
    #     return user
        
        
# Changing of user password 
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only  = True, required = True, validators=[validate_password])
    password2 = serializers.CharField( write_only = True, required = True)
    old_password = serializers.CharField( write_only  = True, required = True)

    class Meta:
        model = User
        fields = ("password", "password2", "old_password")

    # validate the new password
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({ "password": "Password fields didn't match."})
        return attrs
    
    # validating the password
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({ "old_password": "old password is not correct"})
        return value
    
    # updating user data
    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({ "authorize":"You do not have permission for this"})
        instance.set_password(validated_data["password"])
        instance.save()


        return instance

# for updating user profile
class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        extra_kwargs = { 
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

    # validating the email
    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({  "email": "This Email is already in use"})
        return value

     # validate user
    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({ "username": "This Username is already in use"})
        return value
    
    # updating 
    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize":"You do not have permission for this user"})

        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]

        instance.save()
        return instance

