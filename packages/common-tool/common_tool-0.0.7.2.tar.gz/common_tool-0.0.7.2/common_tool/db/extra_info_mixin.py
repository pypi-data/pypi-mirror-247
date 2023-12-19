"""
提供 ExtraInfoMixin 基类
"""
import json


# copied from django-compressor
class cached_property(object):
    """Property descriptor that caches the return value
    of the get function.

    *Examples*

    .. code-block:: python

         @cached_property
         def connection(self):
              return Connection()

         @connection.setter  # Prepares stored value
         def connection(self, value):
              if value is None:
                    raise TypeError("Connection must be a connection")
              return value

         @connection.deleter
         def connection(self, value):
              # Additional action to do at del(self.attr)
              if value is not None:
                    print("Connection %r deleted" % (value, ))
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.__get = fget
        self.__set = fset
        self.__del = fdel
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.__name__]
        except KeyError:
            value = obj.__dict__[self.__name__] = self.__get(obj)
            return value

    def __set__(self, obj, value):
        if obj is None:
            return self
        if self.__set is not None:
            ret_val = self.__set(obj, value)
            if ret_val is not None:
                # 写setter时，通常不会写return。如果是None，认为是没写。
                # 好像写了obj.pro = val (val不是None)后，希望接下来 obj.pro 获取到的值是None的情况也没有
                value = ret_val
        obj.__dict__[self.__name__] = value

    def __delete__(self, obj):
        if obj is None:
            return self
        try:
            value = obj.__dict__.pop(self.__name__)
        except KeyError:
            pass
        else:
            if self.__del is not None:
                self.__del(obj, value)

    def setter(self, fset):
        return self.__class__(self.__get, fset, self.__del)

    def deleter(self, fdel):
        return self.__class__(self.__get, self.__set, fdel)


class ExtraInfoMixin(object):
    EXTRA_SORT_KEYS = False
    EXTRA_ENSURE_ASCII = False

    @cached_property
    def _cached_extra_info_dict(self):
        """
        :rtype: dict
        """
        return json.loads(self.extra_info) if self.extra_info else {}

    @_cached_extra_info_dict.setter
    def _cached_extra_info_dict(self, extra_info_dict):
        self.extra_info = json.dumps(extra_info_dict, ensure_ascii=self.EXTRA_ENSURE_ASCII,
                                     sort_keys=self.EXTRA_SORT_KEYS)

    def get_extra_info_dict(self):
        """
        将extra_info json形式的字符串转换成一dict
        :return: dict
        """
        return self._cached_extra_info_dict

    def set_extra_info_dict(self, extra_info_dict):
        """
        设置extra_info的值。
        注意: 不会主动保存到数据库，如需更新到数据库，需额外调用save方法
        """
        self._cached_extra_info_dict = extra_info_dict

    def get_extra_info_with_key(self, key, default=None):
        """
        从extra_info中获取指定key的值，如果该key不存在返回default
        """
        return self._cached_extra_info_dict.get(key, default)

    def set_extra_info_with_key(self, key, value):
        """
        将extra_info中的指定key的值设为value(没有，添加)
        """
        extra_info_dict = self.get_extra_info_dict()
        extra_info_dict[key] = value
        self.set_extra_info_dict(extra_info_dict)

    def delete_extra_info_with_key(self, key):
        """
        删除某个key
        RET: 是否有修改
        """
        extra_info_dict = self.get_extra_info_dict()
        if key in extra_info_dict:
            extra_info_dict.pop(key)
            self.set_extra_info_dict(extra_info_dict)
            return True
        return False

    def update_extra_info_dict(self, update_dict):
        """
        将update_dict字典更新到extra_info
        """
        extra_info_dict = self.get_extra_info_dict()
        extra_info_dict.update(update_dict)
        self.set_extra_info_dict(extra_info_dict)
