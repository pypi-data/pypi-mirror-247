from inspect import _empty
from typing import Any

from fast_depends.library import CustomField

from faststream.types import AnyDict
from faststream.utils.context.main import context


class Context(CustomField):
    """A class to represent a context.

    Attributes:
        param_name : name of the parameter

    Methods:
        __init__ : constructor method
        use : method to use the context
    """

    param_name: str

    def __init__(
        self,
        real_name: str = "",
        *,
        cast: bool = False,
        default: Any = _empty,
        prefix: str = "",
    ) -> None:
        """Initialize the object.

        Args:
            real_name: The real name of the object.
            cast: Whether to cast the object.
            default: The default value of the object.

        Raises:
            TypeError: If the default value is not provided.
        """
        self.name = real_name
        self.default = default
        self.prefix = prefix
        super().__init__(
            cast=cast,
            required=(default is _empty),
        )

    def use(self, /, **kwargs: Any) -> AnyDict:
        """Use the given keyword arguments.

        Args:
            **kwargs: Keyword arguments to be used

        Returns:
            A dictionary containing the updated keyword arguments

        Raises:
            KeyError: If the parameter name is not found in the keyword arguments
            AttributeError: If the parameter name is not a valid attribute
        """
        name = f"{self.prefix}{self.name or self.param_name}"

        try:
            kwargs[self.param_name] = context.resolve(name)
        except (KeyError, AttributeError):
            if self.required is False:
                kwargs[self.param_name] = self.default

        return kwargs
