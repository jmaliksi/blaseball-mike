import abc
import functools
import re


class _LazyLoadDecorator:

    def __init__(self, function, original_name, cache_name=None, default_value=None, use_default=True,
                 key_replace_name=None):
        """
        Lazy Loading Class Decorator

        This generates both a getter and setter for and attribute named after the attached function to allow for
        custom processing of the data without requiring a different name for the field. When the attribute is set,
        the value is instead saved in an attribute defined by `original_name`. This value can then be used
        in the attached function to return a custom value without needing to lose the original.

        This also includes some optional features:
        * The computation can be cached to a separate attribute, defined by `cache_name`. This will then be used
          if the value is requested multiple times rather than calling the function again. By default it will not cache.
        * A default value can be returned if the variable has never been set, defined by `default_value`. If you
          instead want this to call the attached function anyway, set `use_default` to False.
        * A lookup dictionary (`key_replace_name`) can be generated upon the setter being called, which will map the
          attribute name to the location of the original value. This is useful for cases where you want to map back to
          the original value programmatically.
        """
        functools.update_wrapper(self, function)
        self.func = function
        self.name = function.__name__
        self.original_name = original_name
        self.cache_name = cache_name
        self.default_value = default_value
        self.use_default = use_default
        self.key_replace_name = key_replace_name

    def __get__(self, obj, objtype=None):
        if self.use_default and not getattr(obj, self.original_name, None):
            return self.default_value

        if self.cache_name:
            cache = getattr(obj, self.cache_name, None)
            if cache:
                return cache

        value = self.func(obj)
        if self.cache_name:
            setattr(obj, self.cache_name, value)
        return value

    def __set__(self, obj, value):
        setattr(obj, self.original_name, value)

        if self.cache_name:
            setattr(obj, self.cache_name, None)

        if self.key_replace_name:
            key_lookup = getattr(obj, self.key_replace_name)
            key_lookup[self.name] = self.original_name
            setattr(obj, self.key_replace_name, key_lookup)


class Base(abc.ABC):
    """
    Base class for all blaseball-mike models. Provides common functionality for
    deserializing blaseball API responses.

    To accommodate the ever-changing nature of the blaseball API, blaseball_mike mainly infers
    properties from the returned JSON rather than explicitly mapping each property. This means
    that documentation of available fields with ultimately be incomplete. The easiest way
    to find available properties outside of looking at the spec is to look at the `fields`
    property to see what JSON keys have been deserialized.
    """

    _camel_to_snake_re = re.compile(r'(?<!^)(?=[A-Z])')

    def __init__(self, data, strict=False):
        self.fields = []
        self.key_transform_lookup = {}
        for key, value in data.items():
            self.fields.append(key)
            try:
                setattr(self, Base._from_api_conversion(key), value)
            except AttributeError:
                if strict:
                    raise

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.json() == other.json()
        return NotImplemented

    def __repr__(self):
        try:
            return f"<{self.__class__.__name__}: {self.id}>"
        except AttributeError:
            return super().__repr__()

    @staticmethod
    def _camel_to_snake(name):
        # Blaseball API uses camelCase for fields, convert to the more Pythonistic snake_case
        return Base._camel_to_snake_re.sub('_', name).lower()

    @staticmethod
    def _remove_leading_underscores(name):
        # Some fields historically have underscores before them (_id)
        return name.strip('_')

    @staticmethod
    def _from_api_conversion(name):
        return Base._remove_leading_underscores(Base._camel_to_snake(name))

    @staticmethod
    def lazy_load(original_name, cache_name=None, default_value=None, use_default=True,
                  key_replace_name="key_transform_lookup"):
        # Python requires Class Decorators with arguments to be wrapped by a function
        def lazy_wrapper(function):
            return _LazyLoadDecorator(function, original_name, cache_name, default_value, use_default, key_replace_name)
        return lazy_wrapper

    def _custom_key_transform(self, name):
        if name in self.key_transform_lookup:
            return self.key_transform_lookup[name]
        return name

    def json(self):
        """Returns dictionary of fields used to generate the original object"""
        data = {
            f: getattr(self, self._custom_key_transform(self._from_api_conversion(f))) for f in self.fields
        }
        if "timestamp" in data and not isinstance(data["timestamp"], str):
            data["timestamp"] = data["timestamp"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return data
