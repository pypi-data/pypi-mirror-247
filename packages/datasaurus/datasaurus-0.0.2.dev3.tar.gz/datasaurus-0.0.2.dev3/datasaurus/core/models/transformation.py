import pathlib
from abc import ABC, abstractmethod

import polars
from polars import DataFrame

from datasaurus.core import classproperty
from datasaurus.core.models import Model, columns, MissingMetaError
from datasaurus.core.models.base import ModelMeta, PreparedMeta, lazy_func
from datasaurus.core.models.columns import Columns, Column, IntegerColumn
from datasaurus.core.storage import LocalStorage, FileFormat


class TransformationMetaOptions:
    def __init__(self, *, meta, model):
        self.debug = getattr(meta, 'debug', False)
        self.debug_path = getattr(meta, 'debug_path', pathlib.Path(__file__).parent)
        self.debug_format = getattr(meta, 'debug_format', FileFormat.PARQUET)

        new_columns = [
            column for column in
            model.__dict__.values() if isinstance(column, Column)
        ]

        self.columns = Columns(new_columns)


class TransformationMeta(PreparedMeta):
    df: DataFrame
    def get_transformation_validated(cls):
        result = cls.transform(cls)
        is_compatible = cls._meta.columns.is_compatible_with_polars_df(result)

        if not is_compatible:
            raise ValueError(
                f'{cls} is not compatible with the defined schema.'
                f' Transformation schema: {cls.columns.get_schema()}, result schema {result.schema}'
            )

        if cls._meta.debug:
            LocalStorage(cls._meta.debug_path).write_file(
                result,
                file_name=f'debug/{cls.__name__}',
                format=cls._meta.debug_format
            )

        return result

    def _prepare(cls):
        meta = getattr(cls, 'Meta', None)
        if not meta:
            raise MissingMetaError(f'{cls} does not have Meta class')

        all_models = {k: v for k, v in meta.__dict__.items() if k.endswith('_model')}

        setattr(cls, 'df', lazy_func(cls.get_transformation_validated))
        # if 'initial_model' not in all_models.keys():
        #     raise ValueError(f" {cls} does not have 'initial_model' defined in the Meta.")

        opts = TransformationMetaOptions(meta=meta, model=cls)
        setattr(cls, '_meta', opts)

        # for model_name, model in all_models.items():
        #     setattr(cls, model_name, model)


class Transformation(metaclass=TransformationMeta):
    def _prepare(cls):
        print('what')
        return

    @classproperty
    def columns(self):
        return self._meta.columns

    @abstractmethod
    def transform(self, initial_model) -> 'polars.DataFrame':
        ...


class TestTransformation(Transformation):
    a = IntegerColumn()
    b = IntegerColumn()

    def transform(self, initial_model) -> DataFrame:
        return initial_model(
            {
                'a': [1, 2, 3],
                'b': [1, 2, 3],
            }
        )

    class Meta:
        initial_model = 1
        debug = True
        debug_format = FileFormat.CSV
#
print(TestTransformation.df)
print(TestTransformation)