
from reviews.models import Category, Company, Product, ProductSize, ProductSite, Comment, Image
from rest_framework import serializers

from  rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User
from django.utils.timezone import now
from versatileimagefield.serializers import VersatileImageFieldSerializer


# serializing the Models and its relationship using the "FlexFieldModelSerializer" instead of the "serializer.ModelSerializer"

# class CompanySerializer(serializers.ModelSerializer):
class CompanySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Company
        fields =["pk", "name", "url"]


# class CategorySerializer(serializers.ModelSerializer):
class CategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "name"]
        expandable_fields = {
            "products":("ProductSerializer", {"many":True})
        }


# class ProductSizeSerilizer(serializers.ModelSerializer):
class ProductSizeSerilizer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["pk", "name"]

# class ProductSerializer(serializers.ModelSerializer):
class ProductSerializer(FlexFieldsModelSerializer):
    # category = CategorySerializer(many = True)

    class Meta:
        model = Product
        fields = ["pk", "name", "content", "created", "updated" ]
        expandable_fields = {
            "category" : (CategorySerializer, {"many":True}),
            "sites": ("api.serializer.ProductSiteSerializer", {"many":True}),
            "comments": ("api.serializer.CommentSerializer", {"many":True}),
            "image": ("api.serializer.ImageSerializer", {"many":True})
        }
# class ProductSiteSerializer(serializers.ModelSerializer):
class ProductSiteSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ProductSite
        fields = ["pk", "name", "price", "url", "created", "updated" ]
        expandable_fields = {
            "products": ProductSerializer,
            "productsize": ProductSizeSerilizer,
            "company": CompanySerializer
        }


# class CommentSerializer(serializers.ModelSerializer):
class CommentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Comment
        fields = ["pk", "title", "content", "created", "updated", "user" ]
        expandable_fields = {
            "product": ProductSerializer,
            "user": "api.serializer.UserSerializer"
        }


# class UserSerializer(serializers.ModelSerializer):
class UserSerializer(FlexFieldsModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [ "id", "username" ]
    
    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days


# class ImageSerializer(serializers.ModelSerializer)
class  ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes= 'product_headshot'
    )
    class Meta:
        model = Image
        fields = ["pk", "name", "image"]

