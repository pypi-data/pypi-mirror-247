import dataclasses


@dataclasses.dataclass(frozen=True)
class PostgresQueryExecutionParameters:
    attempt_efficient_postgres_execution: bool = False
    """
    Overrides QueryExecutionParameters.attempt_efficient_parameters if True
    """

    polars_read_csv: bool = True
    """
    When `attempt_postgres_efficient_execution` is True, this flag decides whether to use polars'
    read_csv or pyarrow's read_csv.
    """

    skip_postgres_datetime_zone_cast: bool = False
    """
    When `attempt_postgres_efficient_execution` is True, this flag decides whether to skip casting of
    timezones to get around timestamp vs timestamptz schema issues
    """

    csv_read_then_cast: bool = False
    """
    When `attempt_postgres_efficient_execution` is True, another flag that may help
    to accommodate unzoned timestamps in postgres.
    """


@dataclasses.dataclass(frozen=True)
class QueryExecutionParameters:
    attempt_efficient_execution: bool = True
    """
    This will be overriden at query time if the source is a postgres source and
    PostgresQueryExecutionParameters.attempt_efficient_postgres_execution is True in the invoker
    """

    postgres: PostgresQueryExecutionParameters = dataclasses.field(default_factory=PostgresQueryExecutionParameters)
