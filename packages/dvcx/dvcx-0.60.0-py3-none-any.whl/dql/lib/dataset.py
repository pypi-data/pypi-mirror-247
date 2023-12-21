import inspect
from typing import Callable, Optional, Sequence, Union

from sqlalchemy.sql.elements import ColumnElement

from dql.lib.udf import Aggregator, BatchMapper, Generator, Mapper, UDFBase
from dql.query.dataset import DatasetQuery, GroupByType


class Dataset(DatasetQuery):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(
        self,
        udf: Union[Callable, UDFBase],
        processes: Union[bool, int] = False,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        params=None,
        output=None,
    ):
        self._validate_args("generate()", processes, workers, min_task_size)

        udf_obj = self._udf_to_obj(udf, Generator, "generate()", params, output)
        return DatasetQuery.generate(
            self, udf_obj.to_udf_wrapper(), processes, workers, min_task_size
        )

    def map(
        self,
        udf: Union[Callable, UDFBase],
        processes: Union[bool, int] = False,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        params=None,
        output=None,
    ):
        self._validate_args("map()", processes, workers, min_task_size)

        udf_obj = self._udf_to_obj(udf, Mapper, "map()", params, output)
        return self.add_signals(
            udf_obj.to_udf_wrapper(), processes, workers, min_task_size
        )

    def batch_map(
        self,
        udf: Union[Callable, UDFBase],
        processes: Union[bool, int] = False,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        params=None,
        output=None,
        batch=1000,
    ):
        self._validate_args("map()", processes, workers, min_task_size)

        udf_obj = self._udf_to_obj(
            udf, BatchMapper, "batch_map()", params, output, batch
        )
        return self.add_signals(
            udf_obj.to_udf_wrapper(), processes, workers, min_task_size
        )

    def aggregate(
        self,
        udf: Union[Callable, UDFBase],
        group_by: Optional[GroupByType] = None,
        processes: Union[bool, int] = False,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        params=None,
        output=None,
    ):
        self._validate_args("aggregate()", processes, workers, min_task_size, group_by)

        udf_obj = self._udf_to_obj(udf, Aggregator, "aggregate()", params, output)
        return self.add_signals(
            udf_obj.to_udf_wrapper(), processes, workers, min_task_size, group_by
        )

    def _udf_to_obj(
        self,
        udf,
        target_class,
        name,
        params=None,
        output=None,
        batch=1,
    ):
        if isinstance(udf, UDFBase):
            if not isinstance(udf, target_class):
                cls_name = target_class.__name__
                raise TypeError(
                    f"{name}: expected an instance derived from {cls_name}"
                    f", but received {udf.name}"
                )
            if params:
                raise ValueError(
                    f"params for BaseUDF class {udf.name} cannot be overwritten"
                )
            if output:
                raise ValueError(
                    f"output for BaseUDF class {udf.name} cannot be overwritten"
                )
            return udf

        if inspect.isfunction(udf):
            return target_class.create_from_func(udf, params, output, batch)

        if isinstance(udf, type):
            raise TypeError(
                f"{name} error: The class '{udf}' needs to be instantiated"
                f" as an object before you can use it as UDF"
            )

        if not callable(udf):
            raise TypeError(f"{name} error: instance {udf} must be callable for UDF")

        return target_class.create_from_func(udf, params, output, batch)

    def _validate_args(
        self, name, processes, workers, min_task_size=None, group_by=None
    ):
        msg = None
        if not isinstance(processes, bool) and not isinstance(processes, int):
            msg = (
                f"'processes' argument must be int or bool"
                f", {processes.__class__.__name__} was given"
            )
        elif not isinstance(workers, bool) and not isinstance(workers, int):
            msg = (
                f"'workers' argument must be int or bool"
                f", {workers.__class__.__name__} was given"
            )
        elif min_task_size is not None and not isinstance(min_task_size, int):
            msg = (
                f"'min_task_size' argument must be int or None"
                f", {min_task_size.__class__.__name__} was given"
            )
        elif (
            group_by is not None
            and not isinstance(group_by, ColumnElement)
            and not isinstance(group_by, Sequence)
        ):
            msg = (
                f"'group_by' argument must be GroupByType or None"
                f", {group_by.__class__.__name__} was given"
            )

        if msg:
            raise TypeError(f"Dataset {name} error: {msg}")
