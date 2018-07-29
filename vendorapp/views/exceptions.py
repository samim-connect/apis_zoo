from rest_framework.exceptions import APIException


class NoDataFound(APIException):
    status_code = 400
    default_detail = 'No Data Found'


class SomethingWentWrong(APIException):
    status_code = 400
    default_detail = 'Failed to create model.'

# class SubCategoryNotFound(APIException):
# 	status_code = 400
# 	default_detail = 'No Sub'
