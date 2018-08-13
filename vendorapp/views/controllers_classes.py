from rest_framework.authtoken.models import Token
from multivendor import settings
import pickle
import json


from decimal import Decimal
from ..models import (
    Category,
    SubCategory,
    Product,
    UserProfile,
    Location,
    Review,
    Carosal
)
from ..serializers.serialize import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    UserSerializer,
    CategorySerializer
)
from .exceptions import (
    NoDataFound,
    SomethingWentWrong
)

ERROR_LOGIN = 'Username/Password is invalid'


class CategoryClass:

    def __init__(self, request):
        self.method = request.method
        self.query = request.query_params
        self.request = request

    def get(self):

        try:
            if not self.query.get('id'):
                categories = Category.objects.all()
                result = CategorySerializer(categories, many=True)
            else:
                if self.query.get('id'):
                    category_id = self.query.get('id')
                    categories = Category.objects.get(id=category_id)
                    result = CategorySerializer(categories)
        except:
            raise NoDataFound

        return result.data

    def post(self):
        res = CategorySerializer(data=self.request.data)
        if res.is_valid():
            res.create(res.validated_data)
            return {'details': 'New category succesfully created.'}
        else:
            raise NoDataFound(res.errors)


class SubCategoryClass:

    def __init__(self, request):
        self.method = request.method
        self.query = request.query_params
        self.request = request

    def get(self):
        try:

            if self.query.get('id'):
                result = list()
                sub_category_id = self.query.get('id')
                sub_category_instance = SubCategory.objects.get(
                    id=sub_category_id)
                product_category = SubCategorySerializer(sub_category_instance)
                category_details = {}
                category_details['product_category'] = product_category.data
                category_details['products'] = list()
                try:
                    product_list = sub_category_instance.product_category.all()
                    product_list = ProductSerializer(product_list, many=True)
                    category_details['products'] = product_list.data

                except:
                    print('No product found for this category')
                result.append(category_details)
                return result

            else:
                sub_categories = SubCategory.objects.all()[:15]
                result = SubCategorySerializer(sub_categories, many=True)
                return result.data

        except:
            raise NoDataFound

    def post(self):
        res = SubCategorySerializer(data=self.request.data)
        if res.is_valid():
            res.create(res.validated_data)
            return {'details': 'New Sub-category succesfully created.'}
        else:
            raise SomethingWentWrong(res.errors)


class ProductClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def get(self):
        # import pdb; pdb.set_trace()
        # Needed to be extended later
        try:
            if self.query.get('id'):
                id = self.query.get('id')
                product_instance = Product.objects.get(id=id)
                product_detail = ProductSerializer(product_instance)
                return product_detail.data
            else:

                if self.query.get('city'):
                    city_name = self.query.get('city')
                    product_list = Product.objects.filter(
                        location__city__contains=city_name)[:15]
                    product_list = ProductSerializer(product_list, many=True)
                    return product_list.data
                else:
                    product_list = Product.objects.all()[:15]
                    product_list = ProductSerializer(product_list, many=True)
                    return product_list.data
        except:
            raise NoDataFound

    def post(self):
        res = ProductSerializer(data=self.request.data)
        if res.is_valid():
            res.create(res.validated_data)
            return {'details': 'New product succesfully created.'}
        else:
            raise SomethingWentWrong(res.errors)


class VendorProductAPIClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params
        self.user = request.user

    def get(self):
        if not self.query.get('item_id', ''):
            product_list = Product.objects.filter(seller=self.user)
            if product_list:
                res = ProductSerializer(product_list, many=True)
                return res.data
            return []

        elif self.query.get('action', '') in ['delete'] and self.query.get(
                'item_id'):
            try:
                item_id = self.query.get('item_id')
                product_instance = Product.objects.get(id=item_id)
                product_instance.delete()
            except:
                raise SomethingWentWrong(
                    'Could not delete item.'
                    'Make sure the item id exists in the database.')
        return []

    def post(self):
        if self.query.get('item_id'):
            res = ProductSerializer(data=self.request.data)
            if res.is_valid():
                if res.update(res.validated_data):
                    return {'detail': 'Product updated'}
                else:
                    raise SomethingWentWrong('Failed to update product.')

        else:
            res = ProductSerializer(data=self.request.data)
            if res.is_valid():
                product_instance = res.create(
                    res.validated_data, self.request.user)
                return {'item_id': product_instance.id}
            else:
                errors = json.dumps(res.errors)
                raise SomethingWentWrong(errors)


class UserProfileClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def get(self):
        try:
            if self.request.user.is_authenticated():
                user_profile_instance = self.request.user
                user_profile_details = UserSerializer(user_profile_instance)
                if user_profile_details.data.get('user_type') in ['Customer']:
                    user_profile_details.data.pop('seller_identity')
                return user_profile_details.data
            else:
                NoDataFound('No user found.')

        except:
            raise NoDataFound('No user found.')

    def post(self):
        res = UserSerializer(data=self.request.data)
        if res.is_valid():
            res.create(res.validated_data)
            if res.validated_data.get('user_type') in ['customer']:
                return {'details': 'User is created successfully.'}
            return {'details': 'Your partner account is created!'}
        else:
            # a = eval(res.errors)
            errors = json.dumps(res.errors)
            raise SomethingWentWrong(errors)


class LocationClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def post(self):
        location_info = self.get_location_dict()
        user = self.request.data.get('username')
        if location_info and user:
            location_instance = Location.objects.create(**location_info)
            if UserProfile.objects.filter(username=user):
                user_instance = UserProfile.objects.get(username=user)
                user_instance.location = location_instance
                user_instance.save()
            return {'details': 'Location is successfully updated.'}

        else:
            raise SomethingWentWrong('Failed to update location')

    def get_location_dict(self):
        result = {}
        location_json = self.request.data
        latitute = location_json.get('lat')
        longitute = location_json.get('long')

        if latitute and longitute:
            result['latitute'] = Decimal(float(latitute))
            result['longitute'] = Decimal(float(longitute))

        if location_json.get('city'):
            result['city'] = location_json.get('city')
        if location_json.get('state'):
            result['state'] = location_json.get('state')
        if location_json.get('country'):
            result['country'] = location_json.get('country')

        return result

    # def post(self):

    #     username = self.user.username
    #     try:
    #         data = self.request.body
    #         data = json.loads(data.decode('utf-8'))
    #         latitute = float(data.get('latitute'))
    #         longitute = float(data.get('longitute'))

    #         if latitute and longitute:
    #             if latitute < 86 and (longitute > -180 and latitute < 180):
    #                 status = settings.redis_db.geoadd(
    #                     'person', longitute, latitute, username)
    #         return {'details': 'Location updated.'}

    #     except:
    #         return SomethingWentWrong('Failed to update your location.')


class CartAPIClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def get(self):
        user = self.request.user
        cart = user.cart
        cart_products = cart.item_list.all()
        if cart_products and user.user_type.lower() in ['customer']:
            cart_products = ProductSerializer(cart_products, many=True)
            return cart_products.data
        else:
            raise SomethingWentWrong('Not a valid customer')
        return []

    def post(self):
        user = self.request.user
        cart = user.cart
        if self.query.get('item_id') and self.query.get(
                'action', '').lower() in ['update']:
            product_id = self.query.get('item_id')
            try:
                product_instance = Product.objects.get(id=product_id)
                cart.item_list.add(product_instance)
                return {'details': 'Cart updated'}

            except:
                raise SomethingWentWrong('Cart not updated.')

        elif self.query.get('item_id') and self.query.get(
                'action', '').lower() in ['delete']:
            product_id = self.query.get('item_id')
            try:
                product_instance = Product.objects.get(id=product_id)
                cart.item_list.remove(product_instance)
                return {'details': 'Removed item from the cart.'}
            except:
                raise SomethingWentWrong('Failed to remove item from the cart')

        return {'details': 'action not defined'}


class ReviewAPIClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def post(self):
        if self.query.get('product_id'):
            res = ReviewSerialiser(data=self.request.data)
            if res.is_valid():
                res.create(res.validated_data)
                return {'details': 'Review posted successfully'}

        raise SomethingWentWrong('Review is not updated. Please try again.')


class LoginViewAPIClass:

    def __init__(self, request):
        self.request = request

    def post(self):

        data = self.request.data
        if data:
            email = data.get('email')
            password = data.get('password')
            if email and password:
                user = self.get_user_instance()
                try:
                    if user.check_password(password):
                        user_instance = UserProfile.objects.filter(
                            email=email)[0]
                        token_instance = Token.objects.get_or_create(
                            user=user_instance)
                        res = {}
                        res['Authorization'] = 'Token ' + token_instance[0].key
                        return res
                    else:
                        raise SomethingWentWrong(ERROR_LOGIN)
                except:
                    raise SomethingWentWrong(ERROR_LOGIN)

        raise SomethingWentWrong(ERROR_LOGIN)

    def get_user_instance(self):

        data = self.request.data
        if data.get('email'):
            user = UserProfile.objects.filter(email=data.get('email'))
            if user:
                return user[0]
        return None


class LocationSelectionAPIClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def get(self):

        db = settings.redis_db
        location_query = self.query.get('location')
        result = {}
        if location_query:
            location_list = db.get('location')
            location_list = pickle.loads(location_list)
            result = self.get_matched_location(
                location_list, location_query)

        return {'locations': result}

    @staticmethod
    def get_matched_location(location_list, location_query):

        res = list()
        for location in location_list:
            if location_query.lower() in location:
                res.append(location)

        return res


class CarosalAPIClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def get(self):
        try:
            images = Carosal.objects.all()
            result = list()
            for image in images:
                result.append(
                    {'image_url': image.image.url, 'image_link': image.link})

            return result
        except:
            return []
