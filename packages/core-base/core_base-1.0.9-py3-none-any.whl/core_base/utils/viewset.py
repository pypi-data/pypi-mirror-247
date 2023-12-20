# -*- coding: utf-8 -*-

import uuid

from django.db import transaction
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from core_base.utils.filters import DataLevelPermissionsFilter
from core_base.utils.import_export_mixin import ExportSerializerMixin, ImportSerializerMixin
from core_base.utils.json_response import SuccessResponse, ErrorResponse, DetailResponse
from core_base.utils.permission import CustomPermission
from django_restql.mixins import QueryArgumentsMixin


class CustomModelViewSet(ModelViewSet, ImportSerializerMixin, ExportSerializerMixin, QueryArgumentsMixin):
    """
    自定义的ModelViewSet:
    统一标准的返回格式;新增,查询,修改可使用不同序列化器
    (1)ORM性能优化, 尽可能使用values_queryset形式
    (2)xxx_serializer_class 某个方法下使用的序列化器(xxx=create|update|list|retrieve|destroy)
    (3)filter_fields = '__all__' 默认支持全部model中的字段查询(除json字段外)
    (4)import_field_dict={} 导入时的字段字典 {model值: model的label}
    (5)export_field_label = [] 导出时的字段
    """
    values_queryset = None
    ordering_fields = '__all__'
    create_serializer_class = None
    update_serializer_class = None
    filter_fields = '__all__'
    search_fields = ()
    extra_filter_backends = [DataLevelPermissionsFilter]
    permission_classes = [CustomPermission]
    import_field_dict = {}
    export_field_label = {}

    def filter_queryset(self, queryset):
        for backend in set(set(self.filter_backends) | set(self.extra_filter_backends or [])):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        if getattr(self, 'values_queryset', None):
            return self.values_queryset
        return super().get_queryset()

    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    # 通过many=True直接改造原有的API，使其可以批量创建
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            with transaction.atomic():
                return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DetailResponse(data=serializer.data, msg="获取成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return DetailResponse(data=serializer.data, msg="更新成功")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return DetailResponse(data=[], msg="删除成功")

    # 数据移交-仅支持单层移交
    @action(methods=['post'], detail=False)
    def transfer(self, request, *args, **kwargs):
        nid = request.data.get("nid", 0)
        uid = request.data.get("uid", 0)
        if nid is None or nid == 0 or uid is None or uid == 0:
            return ErrorResponse(msg="用户不存在,请检查参数")
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        new_user = UserModel.objects.filter(id=uid).first()
        if new_user is None:
            return ErrorResponse(msg="用户不存在,请检查参数")
        instance = self.queryset.filter(id=nid, creator=request.user.id).first()
        if instance is None:
            return ErrorResponse(msg="数据不存在,请检查参数")
        instance.creator = new_user.id
        instance.modifier = new_user.id
        instance.save()
        serializer = self.get_serializer(instance)
        return DetailResponse(data=serializer.data, msg="获取成功")

    # 多选删除
    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        request_data = request.data
        keys = request_data.get('keys', None)
        if keys is None:
            return ErrorResponse(msg="参数不合法,请稍后再试")
        self.get_queryset().filter(id__in=keys).delete()
        return SuccessResponse(data=[], msg="删除成功")
