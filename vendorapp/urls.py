from django.conf.urls import url, include
from .views import home, pipelines
from .views.controllers import (
    CategoryAPI,
    SubCategoryAPI,
    ProductAPI,
    UserProfileAPI,
    LocationAPI,
    CartAPI,
    ReviewAPI,
    # SocialAuth,
    LoginViewAPI,
    LocationSelectionAPI,
    SearchAPI,
    CarosalAPI,
    VendorProductAPI,
    ProductImageAPI,
)


urlpatterns = [
    url(r'^$', home.home, name='homepage'),
    url(r'^categories/', CategoryAPI.as_view(), name='category_api'),
    url(r'^sub-categories/', SubCategoryAPI.as_view(), name='sub_category_api'),
    url(r'^product/', ProductAPI.as_view(), name='product_api'),
    url(r'^user-profile/', UserProfileAPI.as_view(), name='user_profile_api'),
    # url(r'^social-auth/', SocialAuth.as_view(), name='social_auth_api'),
    url(r'^login/', LoginViewAPI.as_view(), name='login_api'),
    url(r'^location/', LocationAPI.as_view(), name='user_profile_api'),
    url(r'^cart/', CartAPI.as_view(), name='cart_api'),
    url(r'^review/', ReviewAPI.as_view(), name='review_api'),
    # url('', include('social_django.urls', namespace='social')),
    url(r'^carosal/', CarosalAPI.as_view(), name='carosal_api'),
    url(r'^product-image-upload/', ProductImageAPI.as_view(), name='product_image_api'),
    # url(r'^location-setter/', LocationSelectionAPI.as_view(), name='location_setter_api'),
    url(r'^vendor-products/', VendorProductAPI.as_view(), name='vendor_product_api'),
    url(r'^search-api/', SearchAPI.as_view(), name='search_api'),
    url(r'^search/', include('haystack.urls'))
]
