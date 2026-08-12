from functools import cache
from typing import Any

from pydantic import BaseModel, TypeAdapter


@cache
def _get_adapter(model_cls: type[BaseModel]) -> TypeAdapter:
    return TypeAdapter(model_cls)


def models_to_json(items: Any, *, indent: int | None = None) -> str:
    """
    Convert a Pydantic model instance, or a list of instances, to a JSON string.
    Infers the model type automatically -- no need to know the class upfront.

    Args:
        items: A single BaseModel instance, or a list of BaseModel instances
               (must all be the same type, or share a common base).
        indent: Optional indentation for pretty-printing.

    Returns:
        JSON string.

    Raises:
        TypeError: if items is not a BaseModel or a non-empty list of BaseModels,
                    or if the list contains mixed model types.
    """
    if isinstance(items, list):
        if not items:
            return "[]"

        first_type = type(items[0])
        for item in items:
            if not isinstance(item, BaseModel):
                raise TypeError(f"Expected BaseModel instances, got {type(item)}")
            if type(item) is not first_type:
                raise TypeError(
                    f"Mixed model types in list: {first_type.__name__} and {type(item).__name__}"
                )

        adapter = _get_adapter(list[first_type])
        return adapter.dump_json(items, indent=indent).decode()

    if isinstance(items, BaseModel):
        adapter = _get_adapter(type(items))
        return adapter.dump_json(items, indent=indent).decode()

    raise TypeError(f"Expected BaseModel or list of BaseModel, got {type(items)}")