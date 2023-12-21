from functools import partial, reduce
from itertools import chain
import inspect
from typing import Any, Callable, Optional


class InvalidCombinationError(Exception):
    pass


class NotPointFreeError(Exception):
    pass


class PointFreeFunction:

    def __init__(self,
                 f_function: Optional[Callable] = None,
                 f_name: Optional[str] = None,
                 f_multi: Optional[bool]= None,
                 list_of_names: Optional[list[str]] = None,
                 map_functions: Optional[dict[str, Callable]] = None,
                 map_multis: Optional[dict[str, bool]] = None
                 ):
        """

        Input for single function
        :param f_function: The function itself
        :param f_name: The name the function is going to use (must be unique)
        :param f_multi:The fact that a function receives a single parameter or a list of parameters

        Input for multiple functions
        :param list_of_names: Same as "f_name", but for a list of functions
        :param map_functions: A map of multiple entries of "f_name" and "f_function"
        :param map_multis: A map of multiple entries of "f_name" and "f_multi"

        """

        if (f_function is None and map_functions is None) or (f_function is not None and map_functions is not None):
            raise InvalidCombinationError(
                "Pointfree should be used for either one or more functions, but not both at once"
            )

        if f_function is not None:
            if f_name is None or f_multi is None:
                raise InvalidCombinationError(
                    "Single information is not complete, name and multivariable status required"
                )
            self.names = [f_name]
            self.f_map = {f_name: f_function}
            self.multi_map = {f_name: f_multi}

        if map_functions is not None:
            if list_of_names is None or map_multis is None:
                raise InvalidCombinationError(
                    "Multiple entries information is not complete, lists of names and multivariables status required"
                )
            self.names = list_of_names
            self.f_map = map_functions
            self.multi_map = map_multis

        self.reduction = None

    def evaluate(self, value: Any, name: str) -> Any:
        function = self.f_map[name]
        if self.multi_map[name]:
            if not isinstance(value, list):
                return function([value])
            elif len(value) == 0 or not isinstance(value[0], list):
                return function(value)
            else:
                return [function(v) for v in value]
        else:
            if isinstance(value, list):
                return [function(v) for v in value]
            else:
                return function(value)

    def pointfree_composition(self, _next: "PointFreeFunction") -> "PointFreeFunction":
        return PointFreeFunction(
            list_of_names=self.names + _next.names,
            map_functions={k: v for k, v in chain.from_iterable([self.f_map.items(), _next.f_map.items()])},
            map_multis={k: v for k, v in chain.from_iterable([self.multi_map.items(), _next.multi_map.items()])}
        )

    def __call__(self, *args, **kwargs):
        if not self.reduction:
            self.reduction = partial(reduce, self.evaluate, self.names)
        if len(args) != 1 or len(kwargs) > 0:
            raise NotPointFreeError(
                "More than one value was provided. Maybe you forgot to use `request_redefinitions=True`?"
            )
        return self.reduction(*args, **kwargs)

    def __add__(self, other: "PointFreeFunction") -> "PointFreeFunction":
        return self.pointfree_composition(other)

    def __lshift__(self, other: Any) -> Any:
        return self.__call__(other)


def get_specs(func):
    arg_spec = inspect.getfullargspec(func)
    spec_args = arg_spec.args if arg_spec.args is not None else []
    spec_defaults = arg_spec.defaults if arg_spec.defaults is not None else {}
    spec_kwargs = arg_spec.kwonlyargs if arg_spec.kwonlyargs is not None else []
    return spec_args, spec_defaults, spec_kwargs


def _pointfree(*args, uses_multiple_values=False, **kwargs):
    def __inner(func):
        """

        """
        _name = func.__name__
        spec_args, spec_defaults, spec_kwargs = get_specs(func)

        if len(spec_args) == 0:
            raise NotImplementedError(
                "No implementation for function with only only-keywords args"
            )

        if len(spec_defaults) < len(spec_args) - 1:
            dynamic_args = [*args, *kwargs.keys()]
            if spec_args[0] in dynamic_args:
                raise NotPointFreeError(
                    "Can not define point argument as a keyword"
                )
            defaultless_args = spec_args[0:-len(spec_defaults)] if len(spec_defaults) != 0 else spec_args
            no_default_or_keyword = [ar for ar in defaultless_args if ar not in dynamic_args]
            if len(no_default_or_keyword) > 1:
                raise NotImplementedError(
                    "No implementation for function which requires multiple positional arguments"
                )
        _wrapped_function = func if len(args) == 0 and len(kwargs) == 0 else partial(func, *args, **kwargs)
        return PointFreeFunction(f_name=_name, f_function=_wrapped_function, f_multi=uses_multiple_values)

    return __inner


def _pointfree_with_vars(*args, use_multiple_values=False, **kwargs):
    """
    Create a constructor for a pointfree function that takes arguments, making it possible to
    create functions that use arguments to do things.

    For example, a multiple_by_value(x) where x is a variable.
    """

    if len(args) > 0 or len(kwargs) > 0:
        raise NotImplementedError("No implementation for partial vars definition")

    def inner(func):

        def __inner_partial(*inner_args, **inner_kwargs):
            return _pointfree(*inner_args, uses_multiple_values=use_multiple_values, **inner_kwargs)(func)

        return __inner_partial

    return inner


def pointfree(*args, uses_multiple_values=False, request_redefinitions=False, **kwargs):
    def inner(func):
        if len(args) == 0 and len(kwargs) == 0:
            spec_args, spec_defaults, spec_kwargs = get_specs(func)
            if request_redefinitions or (len(spec_defaults) < len(spec_args) - 1):
                return _pointfree_with_vars(*args, use_multiple_values=uses_multiple_values, **kwargs)(func)
        return _pointfree(*args, uses_multiple_values=uses_multiple_values, **kwargs)(func)

    return inner
