from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
import json
import base64

# App level import
from .controllers_classes import (
    CategoryClass,
    SubCategoryClass,
    ProductClass,
    UserProfileClass,
    LocationClass,
    ReviewAPIClass,
    CartAPIClass,
    LoginViewAPIClass,
    LocationSelectionAPIClass,
    CarosalAPIClass,
    VendorProductAPIClass
)
from .search_api import SearchAPIClass
from .permission_classes import (
    ProfilePermission,
    ProductOwnerPermission,
    CustomerPermission
)
from ..models import (
    Product
)
from ..serializers.serialize import (
    ImageSerilizer
)
from .exceptions import (
    SomethingWentWrong
)
from ..serializers.serialize import (
    ImageSerilizer
)
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File

from multivendor.settings import (
    MEDIA_ROOT,
    MEDIA_URL
)


class CategoryAPI(APIView):

    def get(self, request, format=None):
        res = CategoryClass(request).get()
        return Response(res)

    def post(self, request, format=None):
        res = CategoryClass(request).post()
        return Response(res)


class SubCategoryAPI(APIView):

    def get(self, request, format=None):
        res = SubCategoryClass(request).get()
        return Response(res)

    def post(self, request, format=None):
        pass
        res = SubCategoryClass(request).post()
        return Response(res)


class ProductAPI(APIView):

    def get(self, request, format=None):
        res = ProductClass(request).get()
        return Response(res)

    def post(self, request, format=None):
        res = ProductClass(request).post()
        return Response(res)


class UserProfileAPI(APIView):

    permission_classes = (ProfilePermission,)

    def get(self, request, format=None):
        res = UserProfileClass(request).get()
        return Response(res)

    def post(self, request, format=None):
        res = UserProfileClass(request).post()
        return Response(res)


class VendorProductAPI(APIView):

    permission_classes = (ProductOwnerPermission,)

    def get(self, request, format=None):
        res = VendorProductAPIClass(request).get()
        return Response(res)

    def post(self, request, format=None):
        res = VendorProductAPIClass(request).post()
        return Response(res)


class ProductImageAPI(APIView):

    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, format=None):
        import pdb; pdb.set_trace()
        file_obj = request.FILES.get('image')
        filename = 'media/' + str(uuid.uuid4()) + '.png'
        path = default_storage.save(filename, ContentFile(file_obj.read()))
        item_id = request.query_params.get('item_id')
        try:
            product_instance = Product.objects.get(id=item_id)
            product_instance.image_url = path
            product_instance.save()
            # image_path = IMAGE_URL + path (image resizer should be added later)
        except:
            return {'detail': 'No data found'}
        # do some stuff with uploaded file
        return Response(status=200)


class LocationAPI(APIView):

    def post(self, request, format=None):
        res = LocationClass(request).post()
        return Response(res)


class CartAPI(APIView):

    permission_classes = (CustomerPermission,)

    def get(self, request, format=None):
        res = CartAPIClass(request).get()
        return Response(res)

    def post(self, request, format=None):
        res = CartAPIClass(request).post()
        return Response(res)


class ReviewAPI(APIView):

    def post(self, request, format=None):
        res = ReviewAPIClass(request).post()
        return Response(res)


# class SocialAuth(APIView):

#     def get(self, request, format=None):
#         response = request.user.social_auth.values()
#         auth_info = {}
#         Authorization_val = response[0].get(
#             'extra_data', {}).get('token_type', '')
#         Authorization_val += ' ' + response[0].get(
#             'extra_data', {}).get('access_token', '')
#         auth_info['Authorization'] = Authorization_val
#         return Response(auth_info)

class LoginViewAPI(APIView):

    def post(self, request, format=None):
        res = LoginViewAPIClass(request).post()
        return Response(res)


class LocationSelectionAPI(APIView):

    def get(self, request, format=None):
        res = LocationSelectionAPIClass(request).get()
        return Response(res)


class SearchAPI(APIView):

    def get(self, request, format=None):
        res = SearchAPIClass(request).get()
        return Response(res)


class CarosalAPI(APIView):

    def get(self, request, format=None):
        res = CarosalAPIClass(request).get()
        return Response(res)
