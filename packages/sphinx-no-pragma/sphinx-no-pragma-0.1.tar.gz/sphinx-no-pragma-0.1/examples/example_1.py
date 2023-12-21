from typing import Any, Optional


def my_func(arg1: Optional[Any] = None) -> int:
    # This is a very long line that should normally fail, but we want it to
    # be present as is.
    my_very_very_very_long_variable_name_just_to_show_a_very_long_line_of_x_characters = (  # noqa
        1
    )
    print(
        my_very_very_very_long_variable_name_just_to_show_a_very_long_line_of_x_characters
    )  # noqa
    a = (
        arg1
        or my_very_very_very_long_variable_name_just_to_show_a_very_long_line_of_x_characters  # noqa
    )
    print(a)

    return "0"  # type: ignore


class ThirdPartyLibrary:
    @staticmethod
    def get_dynamic_object() -> Any:
        # Returns an object whose type is not known at compile time
        return "a string"  # In reality, this could be any type


# Usage of the third-party library
obj = ThirdPartyLibrary.get_dynamic_object()

# Attempt to use the object as a string, even though its type is 'Any'
length = len(obj)  # type: ignore

# Deliberately long line to violate PEP 8 line length rule, suppressed with # noqa
print(
    f"The length of the object, a dynamically typed one, is just {length}"
)  # noqa
