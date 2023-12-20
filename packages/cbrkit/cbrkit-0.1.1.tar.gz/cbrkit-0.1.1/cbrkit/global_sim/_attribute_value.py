from collections import defaultdict
from collections.abc import Callable, Iterator, Mapping
from typing import Any

import pandas as pd

from cbrkit.sim import sim2map
from cbrkit.typing import (
    AggregatorFunc,
    AnySimFunc,
    Casebase,
    KeyType,
    SimMap,
    SimMapFunc,
    SimVal,
    ValueType,
)

from ._aggregate import aggregator

__all__ = ["attribute_value", "AttributeValueData"]

AttributeValueData = Mapping[Any, Any] | pd.Series


def _key_getter(obj: AttributeValueData) -> Iterator[str]:
    if isinstance(obj, Mapping):
        yield from obj.keys()
    elif isinstance(obj, pd.Series):
        yield from obj.index
    else:
        raise NotImplementedError()


def _value_getter(obj: AttributeValueData, key: Any) -> Any:
    if isinstance(obj, Mapping):
        return obj[key]
    elif isinstance(obj, pd.Series):
        return obj[key]
    else:
        return getattr(obj, key)


_aggregator = aggregator()


def attribute_value(
    attributes: Mapping[str, AnySimFunc[KeyType, Any]] | None = None,
    types: Mapping[type[Any], AnySimFunc[KeyType, Any]] | None = None,
    types_fallback: AnySimFunc[KeyType, Any] | None = None,
    aggregator: AggregatorFunc[str] = _aggregator,
    value_getter: Callable[[Any, str], Any] = _value_getter,
    key_getter: Callable[[Any], Iterator[str]] = _key_getter,
) -> SimMapFunc[Any, AttributeValueData]:
    attributes_map: Mapping[str, AnySimFunc[KeyType, Any]] = (
        {} if attributes is None else attributes
    )
    types_map: Mapping[type[Any], AnySimFunc[KeyType, Any]] = (
        {} if types is None else types
    )

    def wrapped_func(
        x_map: Casebase[KeyType, ValueType], y: ValueType
    ) -> SimMap[KeyType]:
        local_sims: defaultdict[KeyType, dict[str, SimVal]] = defaultdict(dict)

        attribute_names = (
            set(attributes_map)
            if len(attributes_map) > 0
            and len(types_map) == 0
            and types_fallback is None
            else set(attributes_map).union(key_getter(y))
        )

        for attr_name in attribute_names:
            x_attributes = {
                key: value_getter(value, attr_name) for key, value in x_map.items()
            }
            y_attribute = value_getter(y, attr_name)
            attr_type = type(y_attribute)

            sim_func = (
                attributes_map[attr_name]
                if attr_name in attributes_map
                else types_map.get(attr_type, types_fallback)
            )

            assert (
                sim_func is not None
            ), f"no similarity function for {attr_name} with type {attr_type}"

            sim_func = sim2map(sim_func)
            sim_func_result = sim_func(x_attributes, y_attribute)

            for key, sim in sim_func_result.items():
                local_sims[key][attr_name] = sim

        return {key: aggregator(sims) for key, sims in local_sims.items()}

    return wrapped_func
