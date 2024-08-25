def get_missing_value_counts(df):

    from pyspark.sql.functions import col, sum

    """Takes in a dataset, sums the missing 
    values counts for each column and displays it as a table """

    # Initialise an empty list to hold the sum columns
    sum_columns = []

    # Iterate over each column, summing their counts of NULL values
    for c in df.columns:
        sum_expression = sum(col(c).isNull().cast("int")).alias(c + '_count')
        sum_columns.append(sum_expression)

    # Selection and display
    missing_values = df.select(sum_columns)
    missing_values.show()

    return

def get_dataset_shape(df):
    
    """Takes in a dataset, counts and prints out its shape"""

    # Number of rows
    # Number of rows
    num_rows = df.count()

    # Number of columns
    num_columns = len(df.columns)

    print(f"Dataset shape is: {num_rows} rows, {num_columns} columns")

    return


from math import sqrt, log
from pyspark.sql.functions import col

def apply_iqr_rule(df, column, N):

    """Takes in a dataset, specific column and dataset size
    returns the dataset after filtering that column using the IQR rule for N>100"""

    # Find quantiles of the column
    quantiles = df.approxQuantile(column, [0.25, 0.75], 0.01)
    Q1, Q3 = quantiles
    IQR = Q3 - Q1

    # Define IQR rule
    threshold = (sqrt(log(N)) - 0.5) * IQR

    # Define bounds using the IQR rule
    lower_bound = Q1 - threshold
    upper_bound = Q3 + threshold

    # Extra check to ensure lower bound is never less than 0 (negative)
    lower_bound = max(Q1 - threshold, 0)

    # Return filtered dataset
    return df.filter((col(column) >= lower_bound) & (col(column) <= upper_bound))

# Standardize a single column
def standardise_column(df, column_name):

    """Takes in a dataset and a column name, calculate mean and sd, and then uses these calculations to
    return the dataset with the specified column standardised"""

    from pyspark.sql.functions import mean, stddev, col

    mean_val = df.select(mean(col(column_name))).first()[0]
    sd_val = df.select(stddev(col(column_name))).first()[0]

    return df.withColumn(f"{column_name}_standardised", (col(column_name) - mean_val) / sd_val)







