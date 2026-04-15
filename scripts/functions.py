"""
Utility functions for PySpark-based data processing.

Provides helpers for data inspection (missing values, shape),
outlier removal (IQR rule), and column standardisation.

Dependencies: PySpark, math (stdlib)
"""

from math import sqrt, log

from pyspark.sql.functions import col, mean, stddev, sum


def get_missing_value_counts(df):
    """Sum NULL values per column and display as a table. Returns the result DataFrame."""
    sum_columns = [
        sum(col(c).isNull().cast("int")).alias(c + "_count")
        for c in df.columns
    ]
    missing_values = df.select(sum_columns)
    missing_values.show()
    return missing_values


def get_dataset_shape(df):
    """Print and return the (row_count, column_count) shape of a DataFrame."""
    num_rows = df.count()
    num_columns = len(df.columns)
    print(f"Dataset shape: {num_rows} rows, {num_columns} columns")
    return num_rows, num_columns


def apply_iqr_rule(df, column):
    """Filter outliers from `column` using a domain-aware IQR rule for large samples (N > 100).

    The threshold is widened by sqrt(log(N)) - 0.5 times the IQR, which is more
    permissive than the standard 1.5*IQR multiplier and avoids over-filtering in
    very large rideshare datasets where genuine high-value trips exist.
    """
    quantiles = df.approxQuantile(column, [0.25, 0.75], 0.01)
    Q1, Q3 = quantiles
    IQR = Q3 - Q1
    N = df.count()

    # Domain-aware multiplier: loosens bounds as N grows
    threshold = (sqrt(log(N)) - 0.5) * IQR

    lower_bound = max(Q1 - threshold, 0)  # earnings/distance can't be negative
    upper_bound = Q3 + threshold

    return df.filter((col(column) >= lower_bound) & (col(column) <= upper_bound))


def standardise_column(df, column_name):
    """Z-score standardise `column_name` and add it as `{column_name}_standardised`."""
    mean_val = df.select(mean(col(column_name))).first()[0]
    sd_val = df.select(stddev(col(column_name))).first()[0]
    return df.withColumn(
        f"{column_name}_standardised",
        (col(column_name) - mean_val) / sd_val,
    )
