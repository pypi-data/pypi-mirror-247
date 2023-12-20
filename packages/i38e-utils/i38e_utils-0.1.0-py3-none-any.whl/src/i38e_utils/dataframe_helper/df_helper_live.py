#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#  Developed by: Luis Valverde, 2023
#  IBIS is a registered trademark
import datetime
import logging
import os
from copy import deepcopy

import dask.dataframe as dd
from django.db.models import Model
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from .config import *
from .io import read_frame
from .sql_model_builder import SqlModelBuilder
from ..date_utils import get_current_month, get_week_range, get_current_year, get_today_timerange, \
    get_current_quarter, get_yesterday, get_last_week
from ..file_utils import ensure_file_extension
from ..log_utils import Logger

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')


class DfHelperLive:
    # named class parameters. These should be called from the constructor of the extended class
    live: bool = False
    debug: bool = False
    use_exclude: bool = False
    connection_name: str = None
    table: str = None
    model: Model = None
    legacy_filters: bool = False
    field_map: Dict = {}
    live_config: Dict = {}
    default_config: Dict = {}
    n_records: int = 0
    dt_field: str = None
    use_dask: bool = False
    verbose: bool = False

    use_parquet: bool = False
    save_parquet: bool = False
    load_parquet: bool = False
    parquet_filename: str = None
    parquet_storage_path: str = None
    parquet_full_path: str = None
    parquet_max_age_minutes: int = 0
    parquet_is_recent: bool = False
    dataframe_params: Dict[str, Union[tuple, str, bool, None]] = {}
    dataframe_options: Dict[str, Union[bool, str, None]] = {}

    fixed_filters: Dict[str, Union[str, bool, int, float]] = {}
    filters: Dict[str, Union[str, Dict, bool, int, float]] = {}

    def __init__(self, **kwargs) -> None:
        """
        Initialize an instance of DfHelperLive. It sets up parameters, logging, and parse parameters if they exist.

                :param kwargs: Key-value pairs to configure the instance.
        """
        # we need to read the parameters from the extended class
        # the live parameter is read but may be overwritten by the default_config
        kwargs = {**deepcopy(default_kwargs), **kwargs}
        self.debug = kwargs.pop('debug', False)
        logger.logger.setLevel(logging.INFO) if not self.debug else logger.logger.setLevel(logging.DEBUG)
        self.live = kwargs.pop('live', False)  # Read/set parquet options
        parquet_options = {
            'use_parquet': kwargs.pop('use_parquet', False),
            'save_parquet': kwargs.pop('save_parquet', False),
            'load_parquet': kwargs.pop('load_parquet', False),
            'parquet_filename': kwargs.pop('parquet_filename', self.__class__.__name__.lower()),
            'parquet_storage_path': kwargs.pop('parquet_storage_path', "/"),
            'parquet_max_age_minutes': kwargs.pop('parquet_max_age_minutes', 0),
        }
        self.handle_parquet_options(**parquet_options)

        if not self.default_config and self.live_config:
            # force the live parameter to true if not specified and default_config is empty
            self.live = True
        if not self.live:
            kwargs = {**kwargs, **deepcopy(self.default_config)}
        else:
            kwargs = {**kwargs, **deepcopy(self.live_config)}
        kwargs['live'] = self.live
        self.handle_df_params(**kwargs)

    def handle_df_params(self, **kwargs) -> None:
        self.live = kwargs.pop('live', self.live)
        self.connection_name = kwargs.pop('connection_name', None)
        self.table = kwargs.pop('table', None)
        self.model = kwargs.pop('model', None)
        self.field_map = kwargs.pop('field_map', {})
        self.use_exclude = kwargs.pop('use_exclude', False)
        self.legacy_filters = kwargs.pop('legacy_filters', False)
        self.n_records = kwargs.pop('n_records', 0)
        # this is a datetime field named parameter to use period filters
        self.dt_field = kwargs.pop('dt_field', None)
        self.use_dask = kwargs.pop('use_dask', False)
        params = kwargs.pop('params', None)
        if params:
            self._parse_params(params)
        if self.connection_name is None:
            if self.debug:
                logger.critical('Connection name must be specified')
            raise ValueError('Connection name must be specified')
        if self.table is None:
            if self.debug:
                logger.critical('Table name must be specified')
            raise ValueError('Table name must be specified')
        if self.model is None:
            self.model = SqlModelBuilder(connection_name=self.connection_name, table=self.table).build_model()
        if self.model is None:
            if self.debug:
                logger.critical('Model must be specified')
            raise ValueError('Model must be specified')

    def handle_parquet_options(self, **parquet_options) -> None:
        self.use_parquet = parquet_options.pop('use_parquet', False)
        self.parquet_storage_path = parquet_options.pop('parquet_storage_path', "/")
        self.parquet_filename = parquet_options.pop('parquet_filename', None)
        self.parquet_max_age_minutes = parquet_options.pop('parquet_max_age_minutes', 0)
        self.parquet_is_recent = False
        self.load_parquet = False
        self.save_parquet = False
        self.parquet_full_path = ''
        if self.use_parquet:
            if not os.path.exists(self.parquet_storage_path):
                logger.info(f"Path {self.parquet_storage_path} does not exist. Parquet loading and saving disabled.")
                self.save_parquet = False
                self.load_parquet = False
                return

            self.parquet_full_path = ensure_file_extension(self.parquet_storage_path + self.parquet_filename,
                                                           'parquet')
            self.parquet_is_recent = self.is_file_recent()
            self.load_parquet = self.parquet_is_recent and os.path.exists(self.parquet_full_path)

            # if parquet_max_age_minutes <= 0, always generate the parquet file.
            # if self.parquet_max_age_minutes <= 0:
            #    self.save_parquet = True
            # else:
            self.save_parquet = not self.parquet_is_recent or not self.load_parquet
            if self.debug:
                logger.info(f"Parquet file {self.parquet_full_path} is recent: {self.parquet_is_recent}")
                logger.info(f"Parquet file {self.parquet_full_path} will be loaded: {self.load_parquet}")
                logger.info(f"Parquet file {self.parquet_full_path} will be saved: {self.save_parquet}")

    def _parse_params(self, params: Dict[str, Union[str, bool, Dict, None]]) -> None:
        """
                Parse the given parameters, splitting them into dataframe parameters, dataframe options, and filters.
                :param params: A dictionary of parameters to parse.
        """
        df_params, df_options, filters = {}, {}, {}
        params = params.copy()
        if params is None:
            return
        for key, value in params.items():
            if key in dataframe_params:
                df_params.update({key: value})
            elif key in dataframe_options:
                df_options.update({key: value})
            else:
                filters.update({key: value})

        if not self.fixed_filters:
            self.fixed_filters = filters
        self.filters = {**self.fixed_filters, **filters}
        if self.debug:
            logger.info(f'Fixed filters: {self.fixed_filters}')
            logger.info(f'Filters: {self.filters}')
        self.dataframe_params = {**self.dataframe_params, **df_params}
        self.dataframe_options = {**self.dataframe_options, **df_options}
        if self.legacy_filters:
            if self.debug:
                logger.info(f'Converting legacy filters...')
            self._convert_legacy_filters()

    def load(self, **options: Dict[str, Union[str, bool, Dict, None]]) -> pd.DataFrame:
        """
        Main method to load data from the database. It calls the __load method internally.

        :param options: Additional options to configure loading.
        :return: A DataFrame loaded with data from the database.
        """
        if self.debug:
            logger.info(f'Loading data... with options: {options}')
        return self._load(**options)

    def _load(self, **options: Dict[str, Union[str, bool, Dict, None]]) -> pd.DataFrame:
        """
        Private method to load data from the database. It parses the options, applies filters, and loads the data.

        :param options: Additional options to configure loading.
        :return: A DataFrame loaded with data from the database.
        """
        if options is not None:
            self._parse_params(options)
        if self.load_parquet:
            return self.load_from_parquet()
        else:
            return self._load_filtered_qs()

    def is_file_recent(self) -> bool:
        """Check if the file at self.parquet_full_path is less than self.parquet_max_age_minutes old.

            If self.parquet_max_age_minutes is less than or equal to 0, the function will return True
            regardless of the file's age. If the file does not exist, the function will return False.
            This would force a new query to be executed and a parquet file to be generated.

            Returns:
                bool: True if the file is recent, False otherwise.
            """
        if not os.path.exists(self.parquet_full_path):
            return False

        if self.parquet_max_age_minutes <= 0:
            """ If 0 it means, just use the existing file"""
            return True
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.parquet_full_path))
        if datetime.datetime.now() - file_time > datetime.timedelta(minutes=self.parquet_max_age_minutes):
            logger.info(f"File {self.parquet_full_path} is older than {self.parquet_max_age_minutes} minutes")
            return False
        else:
            logger.info(f"File {self.parquet_full_path} is newer than {self.parquet_max_age_minutes} minutes")
            return True

    def load_from_parquet(self) -> pd.DataFrame:
        if self.debug:
            logger.info(f'Loading from parquet file...{self.parquet_full_path}')
        try:
            if self.use_dask:
                return dd.read_parquet(self.parquet_full_path)
            return pd.read_parquet(self.parquet_full_path)
        except FileNotFoundError:
            if self.debug:
                logger.info(f'Parquet file {self.parquet_full_path} does not exist')
            if self.use_dask:
                return dd.from_pandas(pd.DataFrame(), npartitions=1)
            return pd.DataFrame()

    def save_to_parquet(self, df: pd.DataFrame, engine: str = 'auto') -> None:
        """IMPORTANT: This routine must be explicitly called to save the
        dataframe to a parquet file This is because sometimes the first generated df is not what we want to save but
        saving after cleaning data and after other merge operations
        """
        if self.debug:
            logger.info(f'Saving to parquet file...{self.parquet_full_path}')
        if not df.empty:
            try:
                df.to_parquet(self.parquet_full_path, engine=engine)
            except Exception as e:
                logger.error(f'Error while saving DataFrame to parquet: {e}')
        else:
            logger.warning(f'Attempted to save an empty DataFrame to {self.parquet_full_path}')

    def _load_filtered_qs(self) -> pd.DataFrame:
        """
        Load data from the database based on the filters provided. If no filters are given, it loads only the first
        n_records.
            n_records: Number of records to load if no filters are provided.
            :return: A DataFrame loaded with data from the database.
        """
        if self.model is None:
            if self.debug:
                logger.critical('Model must be specified')
            raise ValueError('Model must be specified')
        df = self._build_and_load()
        if df is not None:
            df = self._process_loaded_data(df)
        return df

    def _process_loaded_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._convert_columns(df)
        if self.field_map:
            if self.debug:
                logger.info(f'Renaming columns...{[col for col in self.field_map.keys()]}')
            set_to_keep1 = set(self.field_map.keys())
            set_to_keep2 = set(self.dataframe_params.get('column_names', []))
            columns_to_keep = list(set_to_keep1.union(set_to_keep2))
            cols_to_drop = [col for col in df.columns if col not in columns_to_keep]
            df.drop(columns=cols_to_drop, inplace=True)
            df.rename(columns=self.field_map, inplace=True)
        return df

    def _build_and_load(self) -> pd.DataFrame:
        query = self.model.objects.using(self.connection_name)
        if self.debug:
            logger.debug(query.query)
            logger.debug(self.filters)
        if not self.filters:
            # IMPORTANT: if no filters are provided show only the first n_records
            # this is to prevent loading the entire table by mistake
            n_records = 100
            if self.debug:
                logger.info(f'No filters provided, showing first %s records, {n_records}')
            queryset = query.all()[:n_records]
        else:
            q_objects = self.build_q_objects(self.filters, self.use_exclude)
            queryset = query.filter(q_objects)[:self.n_records] if self.n_records > 0 else query.filter(q_objects)
        if queryset is not None:
            if self.debug:
                logger.debug(queryset.query)

            df = read_frame(queryset, **self.dataframe_params)
            # df = self.batched_read_frame(qs, 100, **self.dataframe_params)
            if self.debug:
                logger.debug(df.head())
            return df
        else:
            return pd.DataFrame()

    @staticmethod
    def build_q_objects(filters: dict, use_exclude: bool):
        q_objects = Q()
        for key, value in filters.items():
            if not use_exclude:
                q_objects.add(Q(**{key: value}), Q.AND)
            else:
                q_objects.add(~Q(**{key: value}), Q.AND)
        return q_objects

    def batched_read_frame(self, qs, batch_size, **kwargs):
        total = qs.count()
        dfs = []
        for start in range(0, total, batch_size):

            end = min(start + batch_size, total)
            if self.debug:
                logger.info(f"Reading batch {start} to {end}")
            batch = qs[start:end]
            df = read_frame(batch, **kwargs)
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True)

    def _convert_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
                Convert the data types of columns in the DataFrame based on the field type in the Django model.

                :param df: DataFrame whose columns' data types are to be converted.
                :return: DataFrame with converted column data types.
        """
        if self.debug:
            logger.info(f'Converting columns:{[col for col in df.columns]}')
        model_fields = self.model._meta.get_fields()
        for field in model_fields:
            field_name = field.name
            field_type = type(field).__name__
            if field_name in df.columns:
                if self.debug:
                    logger.debug(f"Found column {field_name} of type {field_type}")
                if field_type in list(conversion_map.keys()):
                    try:
                        df[field_name] = conversion_map[field_type](df[field_name])
                        if self.debug:
                            logger.info(f"Converted column {field_name} of type {field_type}")
                    except Exception as e:
                        if self.debug:
                            logger.info(f"Error converting column {field_name} of type {field_type}")
                            logger.error(e)
                else:
                    if self.debug:
                        logger.error(f"Field type {field_type} not found in conversion_map")
            else:
                if self.debug:
                    logger.error(f"Column {field_name} not found in df.columns")
        return df

    def _convert_legacy_filters(self) -> None:
        """
            Convert filter names from English to Spanish (or vice versa) for compatibility with legacy databases.
        """
        """
        legacy database filters are in Spanish.  All new dbs and filters are in English
        in order to keep filters standard, we need to convert the English filters to Spanish
        when querying legacy databases
        """
        if not self.live or not self.legacy_filters or not self.field_map or not self.filters:
            return

        # create a reverse map of the field_map
        reverse_map = {v: k for k, v in self.field_map.items()}

        new_filters = {}
        for filter_field, value in self.filters.items():
            # split the filter_field if LOOKUP_SEP exists
            parts = filter_field.split(LOOKUP_SEP, 1)

            # replace each part with its legacy equivalent if it exists
            new_parts = [reverse_map.get(part, part) for part in parts]

            # join the parts back together and add to the new filters
            new_filter_field = LOOKUP_SEP.join(new_parts)
            new_filters[new_filter_field] = value

        # replace the old filters with the new ones
        if self.debug:
            logger.info(f'Converting legacy filters...{self.filters} to {new_filters}')
        self.filters = new_filters

    def load_period(self, **kwargs):
        dt_field = kwargs.pop('dt_field', None)
        if dt_field is None:
            dt_field = self.dt_field
        if dt_field is None:
            raise ValueError('dt_field must be provided')
        kwargs[f"{dt_field}__gte"] = kwargs.pop('start', None)
        kwargs[f"{dt_field}__lte"] = kwargs.pop('end', None)
        return self._load(**kwargs)

    def load_timeframe(self, timeframe_func, **kwargs):
        dt_field = kwargs.pop('dt_field', None)
        if dt_field is None:
            dt_field = self.dt_field
        if dt_field is None:
            raise ValueError('dt_field must be provided')
        result = self._eval_period(**timeframe_func())
        kwargs[f"{dt_field}__gte"] = result.pop('start', None)
        kwargs[f"{dt_field}__lte"] = result.pop('end', None)
        return self._load(**kwargs)

    @staticmethod
    def _eval_period(**kwargs):
        return {
            'start': kwargs.get('start', None),
            'end': kwargs.get('end', None),
        }

    """Support functions for loading data based on timeframes."""

    def load_today(self, **kwargs):
        return self.load_timeframe(get_today_timerange, **kwargs)

    def load_current_month(self, **kwargs):
        return self.load_timeframe(get_current_month, **kwargs)

    def load_current_week(self, **kwargs):
        return self.load_timeframe(get_week_range, **kwargs)

    def load_current_year(self, **kwargs):
        return self.load_timeframe(get_current_year, **kwargs)

    def load_yesterday(self, **kwargs):
        return self.load_timeframe(get_yesterday, **kwargs)

    def load_last_week(self, **kwargs):
        return self.load_timeframe(get_last_week, **kwargs)

    def load_current_quarter(self, **kwargs):
        return self.load_timeframe(get_current_quarter, **kwargs)

    def load_year(self, year):
        return self.load_period(start=f'{year}-01-01', end=f'{year}-12-31')

    def get_period_function(self, func_name):
        if func_name is None:
            return None
        period = func_name.lower()
        if period == 'today':
            return self.load_today
        elif period == 'yesterday':
            return self.load_yesterday
        elif period == 'current_week':
            return self.load_current_week
        elif period == 'current_month':
            return self.load_current_month
        elif period == 'current_year':
            return self.load_current_year
        elif period == 'last_week':
            return self.load_last_week
        elif period == 'current_quarter':
            return self.load_current_quarter
        else:
            return None
