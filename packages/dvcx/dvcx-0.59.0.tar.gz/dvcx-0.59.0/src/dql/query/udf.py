import typing
from collections.abc import Mapping
from dataclasses import dataclass
from functools import WRAPPER_ASSIGNMENTS
from inspect import isclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)

from dql.dataset import DatasetRow

from .batch import Batch, BatchingStrategy, DatasetRowsBatch, NoBatching, Partition
from .schema import (
    UDFParameter,
    UDFParamSpec,
    normalize_param,
)

if TYPE_CHECKING:
    from dql.catalog import Catalog

    from .batch import BatchingResult

ColumnType = Any


# Specification for the output of a UDF
UDFOutputSpec = typing.Mapping[str, ColumnType]

# Result type when calling the UDF wrapper around the actual
# Python function / class implementing it.
UDFResult = Union[List[Dict[str, Any]], List[List[Dict[str, Any]]]]


@dataclass
class UDFProperties:
    """Container for basic UDF properties."""

    params: List[UDFParameter]
    output: UDFOutputSpec
    batch: int = 1

    def get_batching(self, group_by: Optional[bool] = False) -> BatchingStrategy:
        if group_by:
            return Partition()
        if self.batch == 1:
            return NoBatching()
        if self.batch > 1:
            return Batch(self.batch)
        raise ValueError(f"invalid batch size {self.batch}")

    def signal_names(self) -> Iterable[str]:
        return self.output.keys()

    def parameter_parser(self) -> Callable:
        """Generate a parameter list from a dataset row."""

        def plist(catalog: "Catalog", row: "DatasetRow", **kwargs) -> list:
            return [p.get_value(catalog, row, **kwargs) for p in self.params]

        return plist


def udf(
    params: Sequence[UDFParamSpec],
    output: UDFOutputSpec,
    *,
    method: Optional[str] = None,  # only used for class-based UDFs
    batch: int = 1,
):
    """
    Decorate a function or a class to be used as a UDF.

    The decorator expects both the outputs and inputs of the UDF to be specified.
    The outputs are defined as a collection of tuples containing the signal name
    and type.
    Parameters are defined as a list of column objects (e.g. C.name).
    Optionally, UDFs can be run on batches of rows to improve performance, this
    is determined by the 'batch' parameter. When operating on batches of inputs,
    the UDF function will be called with a single argument - a list
    of tuples containing inputs (e.g. ((input1_a, input1_b), (input2_a, input2b))).
    """
    if isinstance(params, str):
        params = (params,)
    if not isinstance(output, Mapping):
        raise TypeError(f"'output' must be a mapping, got {type(output).__name__}")

    properties = UDFProperties([normalize_param(p) for p in params], output, batch)

    def decorator(udf_base: Union[Callable, Type]):
        if isclass(udf_base):
            return UDFClassWrapper(udf_base, properties, method=method)
        elif callable(udf_base):
            return UDFWrapper(udf_base, properties)

    return decorator


class UDFBase:
    """A base class for implementing stateful UDFs."""

    def __init__(
        self,
        func: Callable,
        properties: UDFProperties,
    ):
        self.func = func
        self.properties = properties
        self.signal_names = properties.signal_names()
        self.parameter_parser = properties.parameter_parser()
        self.output = properties.output

    def __call__(
        self,
        catalog: "Catalog",
        param: "BatchingResult",
        output_rows: bool = False,
        cache: bool = False,
    ) -> Optional[UDFResult]:
        if isinstance(param, DatasetRowsBatch):
            udf_inputs = [
                self.parameter_parser(catalog, row, cache=cache) for row in param.rows
            ]
            udf_outputs = self.func(udf_inputs)
            return self._process_results(param.rows, udf_outputs, output_rows)
        elif isinstance(param, DatasetRow):
            udf_inputs = self.parameter_parser(catalog, param, cache=cache)
            udf_outputs = self.func(*udf_inputs)
            return self._process_results([param], [udf_outputs], output_rows)
        else:
            raise ValueError(f"unexpected UDF parameter {param}")

    def _process_results(
        self,
        rows: Sequence["DatasetRow"],
        results: Sequence[Sequence[Any]],
        output_rows=False,
    ) -> UDFResult:
        """Create a list of dictionaries representing UDF results."""
        r = []

        # outputting rows
        if output_rows:
            for _, gen_rows in zip(rows, results):
                # gen_rows is a generator of rows, where each row is a tuple
                # of column values
                gen_rows_adapted = []  # adapted to the format for inserting into DB
                for row in gen_rows:
                    adapted_row = dict(zip(self.signal_names, row))
                    gen_rows_adapted.append(adapted_row)
                r.append(gen_rows_adapted)

            return r

        # outputting signals
        row_ids = [row.id for row in rows]
        for row_id, result in zip(row_ids, results):
            if result is None:
                continue  # type: ignore[unreachable]
            signals = dict(zip(self.signal_names, result))
            r.append(dict(id=row_id, **signals))  # type: ignore [arg-type]

        return r


class UDFClassWrapper:
    """
    A wrapper for class-based (stateful) UDFs.
    """

    def __init__(
        self,
        udf_class: Type,
        properties: UDFProperties,
        method: Optional[str] = None,
    ):
        self.udf_class = udf_class
        self.udf_method = method
        self.properties = properties
        self.output = properties.output

    def __call__(self, *args, **kwargs):
        return UDFFactory(
            self.udf_class,
            args,
            kwargs,
            self.properties,
            self.udf_method,
        )


class UDFWrapper(UDFBase):
    """A wrapper class for function UDFs to be used in custom signal generation."""

    def __init__(
        self,
        func: Callable,
        properties: UDFProperties,
    ):
        super().__init__(func, properties)
        # This emulates the behavior of functools.wraps for a class decorator
        for attr in WRAPPER_ASSIGNMENTS:
            if hasattr(func, attr):
                setattr(self, attr, getattr(func, attr))

    # This emulates the behavior of functools.wraps for a class decorator
    def __repr__(self):
        return repr(self.func)


class UDFFactory:
    """
    A wrapper for late instantiation of UDF classes, primarily for use in parallelized
    execution.
    """

    def __init__(
        self,
        udf_class: Type,
        args,
        kwargs,
        properties: UDFProperties,
        method: Optional[str] = None,
    ):
        self.udf_class = udf_class
        self.udf_method = method
        self.args = args
        self.kwargs = kwargs
        self.properties = properties
        self.output = properties.output

    def __call__(self):
        udf_func = self.udf_class(*self.args, **self.kwargs)
        if self.udf_method:
            udf_func = getattr(udf_func, self.udf_method)

        return UDFWrapper(udf_func, self.properties)


# UDFs can be callables or classes that instantiate into callables
UDFType = Union[UDFBase, UDFFactory, UDFClassWrapper]
