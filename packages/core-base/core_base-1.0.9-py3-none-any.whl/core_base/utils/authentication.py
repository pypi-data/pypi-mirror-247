from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import get_user_model
from core_base import settings as config
from jwt import decode as jwt_decode

User = get_user_model()

from django.http import QueryDict
from rest_framework.request import Request


def get_parameter_dic(request, *args, **kwargs):
    if isinstance(request, Request) == False:
        return {}

    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()
    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        return query_params
    else:
        return result_data


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if type(request.data) == dict:
            request.data.update(request.query_params.dict())
        token = ""
        dataDict = get_parameter_dic(request)
        ACCESS_TOKEN = request.META.get('HTTP_ACCESSTOKEN', None)
        if 'access_token' in dataDict:
            token = dataDict['access_token']
        if ACCESS_TOKEN is not None:
            token = ACCESS_TOKEN
        if token == "":
            raise exceptions.AuthenticationFailed(detail={'code': 400, 'msg': '缺少access_token'})
        try:
            decoded_data = jwt_decode(token, config.SECRET_KEY, algorithms=["HS256"])
            userid = decoded_data["user_id"]
            currentUser = User.objects.get(id=int(userid))
            return (currentUser, token)
        except Exception as ex:
            raise exceptions.AuthenticationFailed(detail={'code': 401, 'msg': 'access_token已过期'})

    def authenticate_header(self, request):
        pass
