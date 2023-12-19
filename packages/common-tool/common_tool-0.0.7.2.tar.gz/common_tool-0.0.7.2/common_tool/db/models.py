#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/3/28 4:07 PM
# @Author  : donghao
import datetime
import pickle

from django.db import models

from common_tool.db.extra_info_mixin import ExtraInfoMixin
from common_tool.enum import EnumBase, EnumItem

NOT_EXIST_ID = 0


class CommonExtraFields(EnumBase):
    COMMENT = EnumItem('comment', '备注')


class QueryManagerMixin(object):
    """
    django query manager mixin, 提供通用的查询函数

    使用方法：

    class MyModel(models.Model, QueryManagerMixin):
        pass

    ...

    def get_my_model_by_field_db_safe(field_value):
        return MyModel.get_by_field_safe(field=field_value)

    """

    @classmethod
    def get_by_id_safe(cls, instance_id):
        """
        按主键获取数据, 如果不存在返回None
        """
        instance_id = int(instance_id) if instance_id else None
        if not instance_id or instance_id <= NOT_EXIST_ID:
            return None
        return cls.get_by_field_safe(id=instance_id)

    @classmethod
    def get_by_field_safe(cls, *args, **kwargs):
        """
        按某个字段获取数据, 不存在返回None
        """
        try:
            return cls.objects.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_or_create(cls, *args, **kwargs):
        """
        按某个字段获取数据, 不存在返回None
        """
        return cls.objects.get_or_create(*args, **kwargs)


class BaseModel(models.Model, QueryManagerMixin):
    """
    created_time：创建时间
    last_modified：最后更新时间
    """

    class Meta(object):
        abstract = True
        managed = False

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    last_modified = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class ModelWithExtraInfo(models.Model, QueryManagerMixin, ExtraInfoMixin):
    """
    抽象model，提供一json格式的字典的extra_info域。
    """

    class Meta(object):
        abstract = True

    extra_info = models.TextField(blank=True, default="", null=True, help_text="json字典形式的额外信息")

    @staticmethod
    def simple_property(property_name, default, omit_none_value=False):
        pickled_default = pickle.dumps(default)  # 避免 [], {} 等可变类型被修改

        def get_property(self):
            return self.get_extra_info_with_key(property_name, pickle.loads(pickled_default))

        def set_property(self, value):
            if value is None and omit_none_value:
                self.delete_extra_info_with_key(property_name)
            else:
                self.set_extra_info_with_key(property_name, value)

        def del_property(self):
            self.delete_extra_info_with_key(property_name)

        return property(get_property, set_property, del_property)
