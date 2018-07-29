from rest_framework import serializers
from decimal import Decimal
from django.db.models import Q


# App level import
from multivendor import settings
from ..models import (
    Category,
    SubCategory,
    Product,
    UserProfile,
    Cart,
    Location
)


class CategorySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    # sub_categories = serializers.SerializerMethodField('get_sub_categories')
    sub_categories = serializers.SerializerMethodField(read_only=True)

    def get_sub_categories(self, data):

        if data.id:
            category_instance = Category.objects.get(id=data.id)
            sub_category_list = category_instance.parent_category.all()
            serialized_sub_categories = SubCategorySerializer(
                sub_category_list, many=True)
            return serialized_sub_categories.data
        return []

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class SubCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    parent_category = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        sub_category_instance = Category.objects.get(id=validated_data.get(
            'parent_category'))
        validated_data.pop('parent_category')
        return SubCategory.objects.create(
            parent_category=sub_category_instance, **validated_data)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_type = serializers.CharField(required=False)
    username = serializers.CharField(
        error_messages={'required': 'Enter an username. '})
    email = serializers.EmailField(
        error_messages={'invalid': 'Please enter a valid email address.',
                        'required': 'Please enter an email id'})
    seller_identity = serializers.UUIDField(read_only=True)
    password1 = serializers.CharField(
        write_only=True, error_messages={'required': 'Enter a password! '})
    password2 = serializers.CharField(
        write_only=True, error_messages={'required': 'Re-enter password field is empty! '})
    phone_number = serializers.CharField(required=False)

    def validate(self, data):
        if not data['user_type'].lower() in ['customer', 'seller', 'admin']:
            raise serializers.ValidationError('Invalid user type.')
        elif data['password1'] != data['password2']:
            raise serializers.ValidationError('Password did not match.')
        elif len(data['password1']) < 8:
            raise serializers.ValidationError(
                'Password length must be greater than 8 alphabet.')
        if UserProfile.objects.filter(
                Q(username=data['username']) | Q(email=data['email'])).exists():
            raise serializers.ValidationError('Username/Email already exists.')
        if data['user_type'] in ['seller']:
            if not data.get('phone_number'):
                raise serializers.ValidationError(
                    'Please enter your phone number.')
        return data

    def create(self, validated_data):
        try:
            if validated_data.get('user_type') == 'Customer':
                cart = Cart.objects.create()
            else:
                cart = None

            validated_data.pop('password2')
            password = validated_data.pop('password1')
            user = UserProfile.objects.create_user(cart=cart, **validated_data)
            user.set_password(password)
            user.save()
        except Exception as e:
            return e


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField(
        error_messages={'invalid': 'In stock should be a number '})
    in_stock = serializers.IntegerField(
        error_messages={'invalid': 'In stock should be a number '})
    category = serializers.IntegerField(write_only=True, default=0)
    image_url = serializers.CharField(read_only=True)

    def create(self, validated_data, user):
        category = validated_data.pop('category')
        if category:
            category = SubCategory.objects.filter(id=category)
            if category:
                validated_data['category'] = category[0]

        validated_data['seller'] = user
        product_instance = Product.objects.create(**validated_data)
        product_instance.location = user.location
        product_instance.save()
        return product_instance

    def update(self, validated_data):
        try:
            product_instance = Product.objects.get(id=validated_data.get('id'))
            for k, val in validated_data:
                setattr(product_instance, k, val)
            return product_instance

        except Product.DoesNotExist:
            return {}

        # if seller:
        #     self.update_item_location(seller[0], category[0], product_instance)

    # @staticmethod
    # def update_item_location(seller, category, product_instance):

    #     import pdb; pdb.set_trace()
    #     # category_key = 'product_' + str(category.id)
    #     # product_id = product_instance.id
    #     # seller_location = settings.redis_db.geopos('person', seller.id)[0]
    #     # if seller_location:
    #     #     lon = seller_location[0]
    #     #     lat = seller_location[0]
    #     # settings.redis_db.geoadd(category_key, lat, lon, product_id)


class ReviewSerialiser(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(required=False)
    description = serializers.CharField()
    item = serializers.IntegerField(write_only=True)
    user = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        user = UserProfile.objects.get(id=user)
        product = Product.objects.get(id=item)
        validated_data.pop('item')
        validated_data.pop('user')
        return Review.objects.create(user=user, item=product, **validated_data)


class ImageSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('image',)
